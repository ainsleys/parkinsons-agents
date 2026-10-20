#!/usr/bin/env python3
"""Consistency and staleness checks for the data files. Exit 1 on any failure.

Checks:
  - every record has verified and sources
  - verified date is within MAX_VERIFIED_DAYS
  - trials.yaml status agrees with the registry record in data/registry/
  - registry_last_updated in trials.yaml matches the registry record
  - registry record itself not updated for over STALE_REGISTRY_DAYS gets a warning
  - every NCT/ISRCTN mentioned in guide/on-ramps.md has a record in trials.yaml
  - relative links in markdown files resolve

Usage: python3 scripts/check_freshness.py   (needs pyyaml)
"""
import sys, re, json, pathlib, datetime
import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
TODAY = datetime.date.today()
MAX_VERIFIED_DAYS = 90
STALE_REGISTRY_DAYS = 365
CTG_STATUS = {
    "RECRUITING": "recruiting", "ACTIVE_NOT_RECRUITING": "active_not_recruiting",
    "COMPLETED": "completed", "TERMINATED": "failed", "WITHDRAWN": "withdrawn",
    "NOT_YET_RECRUITING": "planned", "UNKNOWN": "unknown", "ENROLLING_BY_INVITATION": "active_not_recruiting",
    "SUSPENDED": "unknown",
}
fails, warns = [], []

def d(s):
    if s is None: return None
    s = str(s)
    for fmt in ("%Y-%m-%d", "%Y-%m"):
        try: return datetime.datetime.strptime(s[:len(fmt)+2 if fmt=="%Y-%m-%d" else 7], fmt).date()
        except ValueError: pass
    return None

for f in ["tests.yaml", "programs.yaml", "trials.yaml"]:
    recs = yaml.safe_load((ROOT/"data"/f).read_text())
    for r in recs:
        rid = r.get("id", "?")
        if not r.get("sources"): fails.append(f"{f}:{rid} has no sources")
        v = d(r.get("verified"))
        if not v: fails.append(f"{f}:{rid} has no parsable verified date")
        elif (TODAY - v).days > MAX_VERIFIED_DAYS: fails.append(f"{f}:{rid} verified {v}, over {MAX_VERIFIED_DAYS} days old")

trials = yaml.safe_load((ROOT/"data"/"trials.yaml").read_text())
for t in trials:
    rid = t.get("registry_id")
    if not rid: continue
    if rid.startswith("NCT"):
        p = ROOT/"data"/"registry"/f"{rid}.json"
        if not p.exists(): fails.append(f"trials:{t['id']} registry file missing for {rid}"); continue
        st = json.loads(p.read_text())["protocolSection"]["statusModule"]
        reg_status = CTG_STATUS.get(st.get("overallStatus"), "unknown")
        reg_updated = st.get("lastUpdatePostDateStruct", {}).get("date")
        if t.get("status") not in (reg_status, "failed") and not (t.get("status") == "failed" and reg_status == "completed"):
            if t.get("status_note") and "registry" in str(t.get("status_note")).lower():
                warns.append(f"trials:{t['id']} status '{t.get('status')}' differs from registry '{reg_status}' (explained in status_note)")
            else:
                fails.append(f"trials:{t['id']} status '{t.get('status')}' but registry says '{reg_status}'")
        if str(t.get("registry_last_updated")) != str(reg_updated):
            fails.append(f"trials:{t['id']} registry_last_updated {t.get('registry_last_updated')} but registry says {reg_updated}")
        ru = d(reg_updated)
        if ru and (TODAY - ru).days > STALE_REGISTRY_DAYS and t.get("status") in ("recruiting", "planned"):
            warns.append(f"trials:{t['id']} registry record not updated since {reg_updated} yet status is {t.get('status')}")
    elif rid.startswith("ISRCTN"):
        p = ROOT/"data"/"registry"/f"{rid}.xml"
        if not p.exists(): fails.append(f"trials:{t['id']} registry file missing for {rid}")

for t in trials:
    if t.get("status") == "recruiting" and not t.get("contact"):
        fails.append(f"trials:{t['id']} is recruiting but has no contact block")
if not (ROOT/"data"/"contacts.yaml").exists(): fails.append("data/contacts.yaml missing; run scripts/pull_registry.py")
# Hand-entered contact routes must be corroborated by the registry pull (second source) unless marked verified_by_page
contacts = yaml.safe_load((ROOT/"data"/"contacts.yaml").read_text()) or {}
for t in trials:
    c = t.get("contact") or {}
    if not c: continue
    reg = contacts.get(t.get("registry_id"), {})
    reg_emails = {x.get("email") for x in reg.get("central_contacts", []) if x.get("email")}
    for sc in reg.get("site_contacts", []):
        reg_emails |= {x.get("email") for x in sc.get("contacts", []) if x.get("email")}
    if c.get("email") and c["email"].lower() not in reg_emails:
        warns.append(f"trials:{t['id']} contact email {c['email']} not found in registry contacts; confirm against the registry page or mark the source")
    reg_phones = {re.sub(r"\D", "", x.get("phone") or "") for x in reg.get("central_contacts", [])}
    if c.get("phone") and re.sub(r"\D", "", c["phone"])[-7:] not in {ph[-7:] for ph in reg_phones if ph}:
        warns.append(f"trials:{t['id']} contact phone {c['phone']} not found in registry contacts; confirm")
# Readouts: completed over a year ago with no posted results
readouts = yaml.safe_load((ROOT/"data"/"readouts.yaml").read_text()) or []
for r in readouts:
    pc = d(r.get("primary_completion"))
    if pc and not r.get("results_posted") and (TODAY - pc).days > 365 and r.get("registry_status") in ("COMPLETED", "TERMINATED"):
        warns.append(f"readouts:{r['registry_id']} completed {pc} with no posted results; look for a publication and record it in trials.yaml background")
onramps = (ROOT/"guide"/"on-ramps.md").read_text()
programs = yaml.safe_load((ROOT/"data"/"programs.yaml").read_text())
ids_in_data = set(re.findall(r"\b(?:NCT\d{8}|ISRCTN\d{8})\b", (ROOT/"data"/"trials.yaml").read_text()))
ids_in_data |= {p.get("registry_id") for p in programs if p.get("registry_id")}
for m in sorted(set(re.findall(r"\b(?:NCT\d{8}|ISRCTN\d{8})\b", onramps))):
    if m not in ids_in_data:
        fails.append(f"on-ramps.md mentions {m} but trials.yaml has no record for it")

for md in list(ROOT.glob("*.md")) + list((ROOT/"guide").glob("*.md")) + [ROOT/"llms.txt"]:
    txt = md.read_text()
    for link in re.findall(r"\]\(([^)]+)\)", txt):
        if link.startswith(("http://", "https://", "#", "mailto:")): continue
        target = (md.parent / link.split("#")[0].replace("%20", " ")).resolve()
        if not target.exists(): fails.append(f"{md.relative_to(ROOT)} links to missing {link}")

for w in warns: print("WARN", w)
for f in fails: print("FAIL", f)
print(f"{len(fails)} failures, {len(warns)} warnings")
sys.exit(1 if fails else 0)
