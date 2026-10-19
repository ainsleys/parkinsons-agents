#!/usr/bin/env python3
"""Match one person's profile against every trial in data/trials.yaml, locally.

Implements the matching rules in data/SCHEMA.md: unknown never passes; stage is
state-dependent; duration has a reference point; untreated vs on-treatment is an
enum; genetics has three parts; geography is a country match, not a travel match.

Usage: python3 scripts/match.py profile.yaml [--mermaid]
Output: a verdict per trial with the deciding criterion, nearest sites by country,
and (with --mermaid) a Sankey showing where trials drop out. Nothing leaves the machine.
Needs pyyaml.
"""
import sys, pathlib, collections
import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent

def load(p): return yaml.safe_load(pathlib.Path(p).read_text())

def norm_state(v):
    if v is True: return "on"
    if v is False: return "off"
    return v

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
            if e.get("duration_min_months") is not None and dur < e["duration_min_months"]: return "no", f"{dur} months since {ref.replace('_',' ')} is under the {e['duration_min_months']}-month minimum"
            if e.get("duration_max_months") is not None and dur > e["duration_max_months"]: return "no", f"{dur} months since {ref.replace('_',' ')} is over the {e['duration_max_months']}-month maximum"
    # medication state
    ms = e.get("medication_state")
    pm = p.get("medication_state")
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
    # genetics
    g = e.get("genetic_requirement") or {}
    req = g.get("required_variant"); known = g.get("status_must_be_known"); excl = g.get("excluded_variants") or []
    variants = [v.upper() for v in (p.get("variants") or [])]
    for x in excl:
        if any(x.upper().split()[0] in v for v in variants): return "no", f"excludes {x} carriers"
    if req and req != "none":
        if not p.get("genetics_tested"): return "no", f"requires a {req} variant; not tested"
        if not any(req.upper() in v for v in variants): return "no", f"requires a {req} variant; none reported"
    elif known and not p.get("genetics_tested"): return "no", "genetic status must be known before screening; not tested yet"
    # smoking, cognition
    if e.get("smoking_allowed") is False:
        if p.get("smoker") is True: return "no", "excludes smokers"
        if p.get("smoker") is None: unclear.append("smoking status")
    if e.get("cognition") and p.get("moca") is None and "MoCA" in str(e.get("cognition")): unclear.append(f"cognition ({e['cognition']})")
    if unclear: return "unclear", "; ".join(unclear)
    return "qualifies", "meets every listed key criterion; screening applies more"

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args: print(__doc__); sys.exit(1)
    p = load(args[0]); trials = load(ROOT/"data"/"trials.yaml"); sites = load(ROOT/"data"/"sites.yaml")
    rows = [(t, *check(t, p)) for t in trials]
    order = {"qualifies": 0, "unclear": 1, "no": 2}
    rows.sort(key=lambda r: order[r[1]])
    print("Navigation, not medical advice. Registries list key criteria only; confirm with the site coordinator.\n")
    for t, v, why in rows:
        print(f"{v.upper():<10} {t['name']} ({t['registry_id']}): {why}")
        if v != "no" and p.get("country"):
            s = sites.get(t["registry_id"], {})
            cities = sorted({f"{x.get('city')}{', ' + x['state'] if x.get('state') else ''}" for x in s.get("sites", []) if x.get("country") == p["country"]})
            if cities: print(f"           sites in {p['country']}: {', '.join(cities[:12])}{' ...' if len(cities) > 12 else ''}")
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
            else: key = "Likely eligible"
            buckets[key] += 1
        for k, n in buckets.most_common():
            print(f"All trials in the data,{k},{n}")

if __name__ == "__main__":
    main()
