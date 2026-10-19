#!/usr/bin/env python3
"""Pull ClinicalTrials.gov v2 records for every NCT ID in data/trials.yaml.

Writes one JSON file per trial to data/registry/ and prints a compact summary
of status, dates, enrollment and eligibility so a reviewer (human or agent)
can update data/trials.yaml. Deterministic; no LLM involved.

Usage: python3 scripts/pull_registry.py [--quiet]
"""
import json, re, sys, urllib.request, pathlib, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
TRIALS = ROOT / "data" / "trials.yaml"
OUT = ROOT / "data" / "registry"
API = "https://clinicaltrials.gov/api/v2/studies/{}"

def main():
    quiet = "--quiet" in sys.argv
    ids = sorted(set(re.findall(r"\bNCT\d{8}\b", TRIALS.read_text())))
    OUT.mkdir(exist_ok=True)
    today = datetime.date.today().isoformat()
    changed = []
    for nct in ids:
        req = urllib.request.Request(API.format(nct), headers={"User-Agent": "parkinsons-agents/0.1"})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.load(r)
        path = OUT / f"{nct}.json"
        new = json.dumps(data, indent=1, sort_keys=True)
        if not path.exists() or path.read_text() != new:
            changed.append(nct)
        path.write_text(new)
        if quiet:
            continue
        p = data["protocolSection"]
        st = p.get("statusModule", {})
        el = p.get("eligibilityModule", {})
        de = p.get("designModule", {})
        locs = p.get("contactsLocationsModule", {}).get("locations", [])
        countries = sorted({l.get("country", "?") for l in locs})
        print(f"\n=== {nct}  {p['identificationModule'].get('briefTitle','')[:90]}")
        print(f"status: {st.get('overallStatus')}  last update: {st.get('lastUpdatePostDateStruct',{}).get('date')}")
        print(f"start: {st.get('startDateStruct',{}).get('date')}  primary completion: {st.get('primaryCompletionDateStruct',{}).get('date')}")
        print(f"phases: {de.get('phases')}  enrollment: {de.get('enrollmentInfo',{}).get('count')}  sites: {len(locs)}  countries: {len(countries)}")
        print(f"age: {el.get('minimumAge')} to {el.get('maximumAge')}  sex: {el.get('sex')}  healthy volunteers: {el.get('healthyVolunteers')}")
        print("criteria:")
        print(el.get("eligibilityCriteria", "").strip())
    print(f"\npulled {len(ids)} records on {today}; changed: {changed or 'none'}")

if __name__ == "__main__":
    main()
