#!/usr/bin/env python3
"""Match one person's profile against every trial in data/trials.yaml, locally.

Implements the matching rules in data/SCHEMA.md: unknown never passes; stage is
state-dependent; duration has a reference point; untreated vs on-treatment is an
enum; genetics has three parts; geography is a country match, not a travel match.

Usage: python3 scripts/match.py profile.yaml [--mermaid] [--draft] [--since YYYY-MM-DD]
Output: a verdict per trial with the deciding criterion, nearest sites by country,
registry changes from data/changes.yaml in the last 30 days (or since --since) that
touch this person's options (a new site in their city or state, a status flip),
(with --mermaid) a Sankey showing where trials drop out, and (with --draft) the
contact route plus a first-contact email DRAFT for each trial still in play.
Run it weekly and the changes block is a private notification: the repo never
knows who is asking.
Drafts are for the person to review and send; this script never sends anything.
Nothing leaves the machine.
Needs pyyaml.
"""
import sys, pathlib, collections, datetime
try:
    import yaml
except ImportError:
    sys.exit("This script needs PyYAML: python3 -m pip install --user pyyaml")

ROOT = pathlib.Path(__file__).resolve().parent.parent

def load(p): return yaml.safe_load(pathlib.Path(p).read_text())

def norm_state(v):
    if v is True: return "on"
    if v is False: return "off"
    return v

# Registry city names that people know by a different name
CITY_ALIASES = {"salford": "manchester", "eccles": "manchester", "plymouth,devon": "plymouth", "woolloongabba": "brisbane",
                "southport": "gold coast", "parkville": "melbourne", "clayton": "melbourne", "randwick": "sydney",
                "atlantis": "west palm beach", "maitland": "orlando", "englewood": "denver", "aurora": "denver",
                "round rock": "austin", "farmington hills": "detroit", "kirkland": "seattle", "bellevue": "seattle",
                "la jolla": "san diego", "stanford": "palo alto", "scottsdale": "phoenix", "sun city": "phoenix"}

def same_city(site, p):
    c = (site.get("city") or "").strip().lower(); pc = (p.get("city") or "").strip().lower()
    if not c or not pc: return False
    return c == pc or CITY_ALIASES.get(c) == pc or CITY_ALIASES.get(pc) == c

def nearby(sites_for_trial, p):
    """Sites in the person's city (or a known alias) first, then the rest of their state/region."""
    allc = [x for x in sites_for_trial.get("sites", []) if x.get("country") == p.get("country")]
    city = [x for x in allc if same_city(x, p)]
    state = [x for x in allc if p.get("state") and x.get("state") == p["state"] and x not in city]
    return city, state, allc

def check(trial, p):
    """Return (verdict, reason). verdict in {qualifies, unclear, no}."""
    e = trial.get("eligibility") or {}
    unclear = []
    if trial.get("status") not in ("recruiting",):
        return "no", f"status is {trial.get('status')}"
    if p.get("country") and trial.get("countries") and p["country"] not in trial["countries"]:
        return "no", f"no sites in {p['country']} (runs in {', '.join(trial['countries'][:4])}{'...' if len(trial['countries'])>4 else ''})"
    # age
    if p.get("age") is None: unclear.append("age")
    else:
        if e.get("age_min") is not None and p["age"] < e["age_min"]: return "no", f"age {p['age']} below minimum {e['age_min']}"
        if e.get("age_max") is not None and p["age"] > e["age_max"]: return "no", f"age {p['age']} above maximum {e['age_max']}"
    # duration
    ref = e.get("duration_reference")
    dur = p.get("months_since_diagnosis") if ref == "diagnosis" else p.get("months_since_onset") if ref == "symptom_onset" else None
    if e.get("duration_min_months") is not None or e.get("duration_max_months") is not None:
        if ref not in ("diagnosis", "symptom_onset"): unclear.append("duration reference point unknown for this trial")
        elif dur is None: unclear.append(f"months since {ref.replace('_',' ')} not given")
        else:
            if e.get("duration_min_months") is not None and dur < e["duration_min_months"]:
                wait = e["duration_min_months"] - dur
                return "no", f"{dur} months since {ref.replace('_',' ')} is under the {e['duration_min_months']}-month minimum; becomes time-eligible in about {wait} month{'s' if wait != 1 else ''}{' if on stable medication by then' if e.get('medication_state') == 'on_stable_treatment' else ''}"
            if e.get("duration_max_months") is not None and dur > e["duration_max_months"]: return "no", f"{dur} months since {ref.replace('_',' ')} is over the {e['duration_max_months']}-month maximum"
    # medication state
    ms = e.get("medication_state")
    pm = {"on_stable_treatment": "on_treatment"}.get(p.get("medication_state"), p.get("medication_state"))
    if ms == "untreated":
        if pm == "on_treatment": return "no", "requires people not on Parkinson's medication"
        if pm is None: unclear.append("medication state")
    elif ms == "on_stable_treatment":
        if pm == "untreated": return "no", "requires being on stable Parkinson's medication"
        if pm is None: unclear.append("medication state")
        elif e.get("medication_min_months") and (p.get("medication_months") is None or p["medication_months"] < e["medication_min_months"]):
            if p.get("medication_months") is None: unclear.append(f"months on medication (needs {e['medication_min_months']})")
            else: return "no", f"needs {e['medication_min_months']} months on stable medication, has {p['medication_months']}"
    elif ms in (None, "unknown"): unclear.append("trial's medication requirement unknown")
    # stage
    tstate = norm_state(e.get("hoehn_yahr_state"))
    if e.get("hoehn_yahr_min") is not None or e.get("hoehn_yahr_max") is not None:
        if p.get("hoehn_yahr") is None: unclear.append("Hoehn and Yahr stage")
        else:
            pstate = norm_state(p.get("hoehn_yahr_state"))
            hy = p["hoehn_yahr"]
            if e.get("hoehn_yahr_max") is not None and hy > e["hoehn_yahr_max"] and (tstate == pstate or tstate == "unknown"):
                return "no", f"stage {hy} above maximum {e['hoehn_yahr_max']}"
            if e.get("hoehn_yahr_min") is not None and hy < e["hoehn_yahr_min"] and (tstate == pstate or tstate == "unknown"):
                return "no", f"stage {hy} below minimum {e['hoehn_yahr_min']}"
            if tstate in ("on", "off") and pstate != tstate:
                unclear.append(f"stage must be assessed {tstate} medication; yours was assessed {pstate or 'in an unknown state'}")
    # motor complications
    if e.get("motor_complications_allowed") is False and p.get("motor_complications") is True: return "no", "requires no motor complications (dyskinesia or wearing-off)"
    if e.get("motor_complications_required") is True and p.get("motor_complications") is False: return "no", "requires motor fluctuations or OFF time"
    if e.get("motor_complications_allowed") is False and p.get("motor_complications") is None: unclear.append("motor complications (MDS-UPDRS Part IV)")
    # body size
    if e.get("weight_kg_min") is not None or e.get("bmi_min") is not None:
        w, h = p.get("weight_kg"), p.get("height_cm")
        if w is None: unclear.append("weight")
        else:
            if e.get("weight_kg_min") is not None and w < e["weight_kg_min"]: return "no", f"weight {w} kg below {e['weight_kg_min']}"
            if e.get("weight_kg_max") is not None and w > e["weight_kg_max"]: return "no", f"weight {w} kg above {e['weight_kg_max']}"
            if e.get("bmi_min") is not None:
                if h is None: unclear.append("height (for BMI)")
                else:
                    bmi = w / ((h/100)**2)
                    if bmi < e["bmi_min"] or bmi > e.get("bmi_max", 99): return "no", f"BMI {bmi:.1f} outside {e['bmi_min']} to {e.get('bmi_max')}"
    # genetics
    g = e.get("genetic_requirement") or {}
    req = g.get("required_variant"); known = g.get("status_must_be_known"); excl = g.get("excluded_variants") or []
    variants = [v.upper() for v in (p.get("variants") or [])]
    for x in excl:
        if any(x.upper().split()[0] in v for v in variants): return "no", f"excludes {x} carriers"
    if req and req != "none":
        if not p.get("genetics_tested"): return "no", f"requires a {req} variant; not tested. Only worth pursuing after a genetic result"
        if not any(req.upper() in v for v in variants): return "no", f"requires a {req} variant; none reported"
    elif known and not p.get("genetics_tested"): return "no", "genetic status must be known before screening; not tested yet. Becomes possible once tested (routes and turnaround in guide/get-typed.md)"
    # smoking, cognition
    if e.get("smoking_allowed") is False:
        if p.get("smoker") is True: return "no", "excludes smokers"
        if p.get("smoker") is None: unclear.append("smoking status")
    if e.get("cognition") and p.get("moca") is None and "MoCA" in str(e.get("cognition")): unclear.append(f"cognition ({e['cognition']})")
    if unclear: return "unclear", "; ".join(unclear)
    extra = [o for o in (e.get("other") or []) if not o.lower().startswith("excludes")][:3]
    return "likely", "meets every structured key criterion; still to confirm at pre-screen: " + ("; ".join(extra) if extra else "protocol criteria the registry does not list")

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args: print(__doc__); sys.exit(1)
    p = load(args[0]); trials = load(ROOT/"data"/"trials.yaml"); sites = load(ROOT/"data"/"sites.yaml")
    rows = [(t, *check(t, p)) for t in trials]
    order = {"likely": 0, "unclear": 1, "no": 2}
    rows.sort(key=lambda r: order[r[1]])
    print("Navigation, not medical advice. Registries list key criteria only; confirm with the site coordinator.\n")
    for t, v, why in rows:
        print(f"{v.upper():<10} {t['name']} ({t['registry_id']}): {why}")
        if v != "no" and p.get("country"):
            s = sites.get(t["registry_id"], {})
            city, state_, allc = nearby(s, p)
            fmt = lambda xs: sorted({f"{x.get('facility')} ({x.get('city')}{', ' + x['state'] if x.get('state') else ''}; {x.get('status') or 'status not listed'})" for x in xs})
            if city: print(f"           sites in or near your city: {'; '.join(fmt(city))}")
            if state_: print(f"           other sites in your state: {'; '.join(fmt(state_))}")
            cities = sorted({f"{str(x.get('city')).split(',')[0]}{', ' + x['state'] if x.get('state') else ''}" for x in allc})
            if cities: print(f"           all sites in {p['country']} ({len(cities)}): {', '.join(cities)}")
    # Registry changes that touch this person: read from the generated feed, filtered locally.
    since_arg = next((sys.argv[i+1] for i, a in enumerate(sys.argv) if a == "--since" and i+1 < len(sys.argv)), None)
    since = since_arg or (datetime.date.today() - datetime.timedelta(days=30)).isoformat()
    changes = (load(ROOT/"data"/"changes.yaml") or []) if (ROOT/"data"/"changes.yaml").exists() else []
    verdict = {t["registry_id"]: v for t, v, _ in rows}
    hits = []
    for c in changes:
        if str(c.get("date_observed")) < since: continue
        v = verdict.get(c.get("registry_id"))
        here = c.get("country") == p.get("country") if c.get("country") else False
        tag = ""
        if c.get("kind") in ("site_added", "site_status_change", "site_removed") and here:
            if same_city(c, p): tag = " [in or near your city]"
            elif p.get("state") and c.get("state") == p["state"]: tag = " [in your state]"
        if v != "no" or tag or (c.get("kind") == "site_added" and here):
            hits.append(f"  {c.get('date_observed')}  {c.get('trial') or c.get('registry_id')}: {c.get('detail')}{tag}")
    print(f"\nRegistry changes since {since} touching these options (from data/changes.yaml; a human re-verifies before the guide changes):")
    print("\n".join(hits) if hits else "  none")
    if "--draft" in sys.argv:
        checklist = load(ROOT/"data"/"checklist.yaml")
        print("\n=== Contact routes and DRAFT first messages (not sent; the person reviews and sends) ===")
        print("Contact at most two or three trials. Screening failure is common; a match here means 'worth a call'.")
        print("Joining one interventional trial normally excludes the others for its duration (6 to 12 month lookbacks are typical).")
        if p.get("medication_state") == "untreated":
            print("You are untreated: ask each untreated-only study whether starting medication after enrollment is permitted. The registries do not say.")
        for t, v, why in rows:
            if v == "no": continue
            c = t.get("contact") or {}
            print(f"\n--- {t['name']} ({t['registry_id']}) ---")
            print("Route:", c.get("preferred_route", "see registry page"))
            for k in ("inquiry_form", "portal", "email", "phone", "reference", "registry_url"):
                if c.get(k): print(f"  {k}: {c[k]}")
            if c.get("notes"): print("  notes:", c["notes"])
            missing = [m for m in why.split("; ")] if v == "unclear" else []
            if missing: print("Before contacting, resolve:", "; ".join(missing))
            dx = p.get("months_since_diagnosis")
            medname = p.get("medication_name") or "Parkinson's medication"
            pm2 = {"on_stable_treatment": "on_treatment"}.get(p.get("medication_state"), p.get("medication_state"))
            alone = " alone" if p.get("monotherapy") is True else ""
            mc = p.get("motor_complications")
            e_ = t.get("eligibility") or {}
            if mc is False: mc_line = ", with no dyskinesia or wearing-off"
            elif mc is True:
                off = p.get("off_hours_per_day")
                mc_line = f", with wearing-off{' and dyskinesia' if p.get('dyskinesia') else ''}{f' and about {off} hours OFF per day' if off is not None else ''}"
            else: mc_line = ""
            falls_line = (" I have had no falls in the past year." if p.get("recurrent_falls") is False else "") if e_.get("motor_complications_required") else ""
            med = {"untreated": "am not yet taking Parkinson's medication", "on_treatment": f"have been on a stable dose of {medname}{alone} for {p.get('medication_months') or '[n]'} months{mc_line}"}.get(pm2, "[medication status]")
            def since(months):
                if months is None: return "[n] months ago"
                return f"{months} months ago" if months < 24 else f"about {months//12} years ago"
            city = p.get("city") or "[city]"
            city_s, state_s, _ = nearby(sites.get(t["registry_id"], {}), p)
            cand = city_s or state_s
            named = [x for x in cand if x.get("facility") and not str(x.get("facility")).lower().startswith("site")]
            nearest = named[0]["facility"] if named else ("the " + (cand[0].get("city") or "") + " site" if cand else "[nearest listed site]")
            devices = p.get("implanted_devices")
            # Only state a fact the profile actually contains; null becomes a bracket for the person to fill.
            if devices is None or str(devices).strip() == "":
                dev_line = " [Implanted devices: none / pacemaker model X, MRI-conditional.]"
            elif str(devices).strip().lower() in ("none", "no", "false"):
                dev_line = " I have no implanted devices."
            else:
                dev_line = f" I have an implanted device: {devices}."
            who = p.get("diagnosed_by") or "[neurologist / movement disorder specialist]"
            pname = p.get("name") or "[name]"
            gen = ("have had genetic testing" if p.get("genetics_tested") else "have not had genetic testing")
            e = t.get("eligibility") or {}
            g = e.get("genetic_requirement") or {}
            gen_line = f" I {gen}." if (g.get("status_must_be_known") or (g.get("required_variant") and g.get("required_variant") != "none")) else ""
            us = (p.get("country") == "United States")
            route_text = str(c.get("preferred_route", "")).lower()
            if not us and c.get("portal") and "outside the us" in route_text:
                print(f"\nYou are outside the US: use the sponsor's patient portal ({c['portal']}), find the study by its reference and use its contact or callback form. The inquiry form and US phone line are for US residents; the email address is a fallback.")
            elif c.get("inquiry_form") and "form" in route_text:
                print(f"\nThe sponsor prefers its form ({c['inquiry_form']}). Paste the text below into it; the email address is a fallback.")
            print("\nDRAFT (not sent; the person reviews, fills the bracketed items, and sends):")
            print(f"Subject: Inquiry about {t['name']} ({t['registry_id']}{', ' + c['reference'] if c.get('reference') else ''}), prospective participant in {city}")
            print(f"\nHello,\n\nI am asking about eligibility for {t['name']}. I was diagnosed with Parkinson's disease {since(dx)} by a {who} and {med}. I am {p.get('age', '[age]')}, live in {city}, and could attend {nearest}.{gen_line}{dev_line}{falls_line}")
            print("\nCould you tell me whether I appear to meet the key criteria and, if so, arrange a pre-screening call? [Confirm before sending: My neurologist is aware and can provide records.] I consent to being contacted at this address or by phone at [number].\n\nThank you,\n" + pname)
    if "--mermaid" in sys.argv:
        print("\n%% Where the trials drop out for this profile. Generated by scripts/match.py from data/trials.yaml; verified dates inside that file.")
        print("sankey-beta\n")
        buckets = collections.Counter()
        for t, v, why in rows:
            if v == "no":
                key = ("Closed or not recruiting" if "status is" in why else "Not in your country" if "no sites" in why
                       else "Genetic test needed" if "genetic" in why or "variant" in why else "Medication state" if "medication" in why
                       else "Stage or complications" if "stage" in why or "motor" in why else "Age or time since diagnosis")
            elif v == "unclear": key = "Unclear: ask your neurologist"
            else: key = "Likely eligible on listed criteria"
            buckets[key] += 1
        for k, n in buckets.most_common():
            print(f"All trials in the data,{k},{n}")

if __name__ == "__main__":
    main()
