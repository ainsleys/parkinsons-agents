#!/usr/bin/env python3
"""Pull trial registry records for every registry ID in data/trials.yaml.

Sources:
  ClinicalTrials.gov v2 API   for NCT IDs    -> data/registry/NCTxxxxxxxx.json
  ISRCTN registry API (XML)   for ISRCTN IDs -> data/registry/ISRCTNxxxxxxxx.xml

Also writes data/sites.yaml: for each trial, the site list (facility, city, state,
country, site status) and a per-country count, taken from the registry record.
Deterministic; no LLM involved. Prints a compact summary for a reviewer.

Usage: python3 scripts/pull_registry.py [--quiet]
"""
import json, re, sys, html, urllib.request, pathlib, datetime, collections

ROOT = pathlib.Path(__file__).resolve().parent.parent
TRIALS = ROOT / "data" / "trials.yaml"
OUT = ROOT / "data" / "registry"
SITES = ROOT / "data" / "sites.yaml"
CTG = "https://clinicaltrials.gov/api/v2/studies/{}"
ISRCTN = "https://www.isrctn.com/api/query/format/default?q={}"
UA = {"User-Agent": "parkinsons-agents/0.1 (github.com/ainsleys/parkinsons-agents)"}

def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()

def xml_tag(s, t):
    m = re.search(rf"<{t}[^>]*>(.*?)</{t}>", s, re.S)
    return html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip() if m else None

def yaml_str(s):
    if s is None:
        return "null"
    s = str(s).replace('"', '\\"')
    return f'"{s}"'

def main():
    quiet = "--quiet" in sys.argv
    text = TRIALS.read_text()
    ncts = sorted(set(re.findall(r"\bNCT\d{8}\b", text)))
    isrctns = sorted(set(re.findall(r"\bISRCTN\d{8}\b", text)))
    OUT.mkdir(exist_ok=True)
    today = datetime.date.today().isoformat()
    changed, errors = [], []
    sites_out = [f"# Trial site locations pulled from registries on {today} by scripts/pull_registry.py.",
                 "# Do not edit by hand; re-run the script. Site status is the registry's per-site status where given.", ""]

    for nct in ncts:
        try:
            raw = fetch(CTG.format(nct))
        except Exception as e:
            errors.append(f"{nct}: {e}"); continue
        data = json.loads(raw)
        path = OUT / f"{nct}.json"
        new = json.dumps(data, indent=1, sort_keys=True)
        if not path.exists() or path.read_text() != new:
            changed.append(nct)
        path.write_text(new)
        p = data["protocolSection"]
        st = p.get("statusModule", {})
        el = p.get("eligibilityModule", {})
        de = p.get("designModule", {})
        locs = p.get("contactsLocationsModule", {}).get("locations", [])
        bycountry = collections.Counter(l.get("country", "unknown") for l in locs)
        sites_out.append(f"{nct}:")
        sites_out.append(f"  registry_status: {st.get('overallStatus')}")
        sites_out.append(f"  registry_last_updated: {st.get('lastUpdatePostDateStruct',{}).get('date')}")
        sites_out.append(f"  site_count: {len(locs)}")
        sites_out.append("  countries:")
        for c, n in sorted(bycountry.items(), key=lambda x: -x[1]):
            sites_out.append(f"    {yaml_str(c)}: {n}")
        sites_out.append("  sites:")
        for l in sorted(locs, key=lambda l: (l.get("country",""), l.get("state") or "", l.get("city",""))):
            sites_out.append(f"    - {{facility: {yaml_str(l.get('facility'))}, city: {yaml_str(l.get('city'))}, state: {yaml_str(l.get('state'))}, country: {yaml_str(l.get('country'))}, status: {yaml_str(l.get('status'))}}}")
        sites_out.append("")
        if quiet:
            continue
        print(f"\n=== {nct}  {p['identificationModule'].get('briefTitle','')[:90]}")
        print(f"status: {st.get('overallStatus')}  last update: {st.get('lastUpdatePostDateStruct',{}).get('date')}")
        print(f"start: {st.get('startDateStruct',{}).get('date')}  primary completion: {st.get('primaryCompletionDateStruct',{}).get('date')}")
        print(f"phases: {de.get('phases')}  enrollment: {de.get('enrollmentInfo',{}).get('count')}  sites: {len(locs)}  countries: {dict(bycountry)}")
        print(f"age: {el.get('minimumAge')} to {el.get('maximumAge')}")

    for isr in isrctns:
        try:
            raw = fetch(ISRCTN.format(isr)).decode("utf-8", "replace")
        except Exception as e:
            errors.append(f"{isr}: {e}"); continue
        path = OUT / f"{isr}.xml"
        if not path.exists() or path.read_text() != raw:
            changed.append(isr)
        path.write_text(raw)
        # ISRCTN exposes recruitment start/end dates rather than a status enum.
        rs, re_ = (xml_tag(raw, "recruitmentStart") or "")[:10], (xml_tag(raw, "recruitmentEnd") or "")[:10]
        if rs and re_ and rs <= today <= re_:
            status = "recruiting (derived from recruitment dates)"
        elif re_ and today > re_:
            status = "recruitment ended (derived from recruitment dates)"
        else:
            status = "unknown"
        edited = None  # the public XML does not carry a last-edited date
        centres = xml_tag(raw, "trialCentres")
        sites_out.append(f"{isr}:")
        sites_out.append(f"  registry_status: {yaml_str(status)}")
        sites_out.append(f"  registry_last_updated: null")
        sites_out.append(f"  recruitment_start: {yaml_str(rs or None)}")
        sites_out.append(f"  recruitment_end: {yaml_str(re_ or None)}")
        sites_out.append(f"  site_count: {len(re.findall(r'United Kingdom|England|Scotland|Wales|Northern Ireland', centres or ''))}")
        sites_out.append(f"  countries: {{{yaml_str(xml_tag(raw, 'countries') or 'unknown')}: null}}")
        sites_out.append(f"  sites_note: {yaml_str((centres or '')[:500])}")
        sites_out.append("")
        if not quiet:
            print(f"\n=== {isr}  {(xml_tag(raw,'title') or '')[:90]}")
            print(f"status: {status}  recruitment {rs} to {re_}")

    SITES.write_text("\n".join(sites_out))
    print(f"\npulled {len(ncts)} NCT and {len(isrctns)} ISRCTN records on {today}; changed: {changed or 'none'}; errors: {errors or 'none'}")
    if errors:
        sys.exit(1)

if __name__ == "__main__":
    main()
