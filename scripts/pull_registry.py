#!/usr/bin/env python3
"""Pull trial registry records for every registry ID in data/trials.yaml.

Sources:
  ClinicalTrials.gov v2 API   for NCT IDs    -> data/registry/NCTxxxxxxxx.json
  ISRCTN registry API (XML)   for ISRCTN IDs -> data/registry/ISRCTNxxxxxxxx.xml

Also writes data/sites.yaml: for each trial, the site list (facility, city, state,
country, site status) and a per-country count, taken from the registry record.

Change feed: before overwriting a record, the script diffs the old and new copies and
records every material difference (status, dates, eligibility, contacts, enrollment,
sites added/removed/status) in data/changes.yaml (newest first), data/changes.xml (Atom)
and a dated section at the top of CHANGELOG.md. scripts/match.py reads the feed to tell a
person about changes near them. Deterministic; no LLM involved.

Usage: python3 scripts/pull_registry.py [--quiet]
"""
import json, re, sys, html, hashlib, urllib.request, pathlib, datetime, collections

ROOT = pathlib.Path(__file__).resolve().parent.parent
TRIALS = ROOT / "data" / "trials.yaml"
OUT = ROOT / "data" / "registry"
SITES = ROOT / "data" / "sites.yaml"
CONTACTS = ROOT / "data" / "contacts.yaml"
PROGRAM_SITES = ROOT / "data" / "program_sites.yaml"
READOUTS_YAML = ROOT / "data" / "readouts.yaml"
READOUTS_MD = ROOT / "guide" / "readouts.md"
CHANGES = ROOT / "data" / "changes.yaml"
CHANGES_FEED = ROOT / "data" / "changes.xml"
CHANGELOG = ROOT / "CHANGELOG.md"
REPO_URL = "https://github.com/ainsleys/parkinsons-agents"
PPMI_SITES_JSON = "https://www.ppmi-info.org/sites/default/files/tables-data/clinical-sites-tables.json"
US_STATES = {"AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY","DC"}
EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
PHONE_RE = re.compile(r"^[+()0-9][0-9()+\-.\s]{5,30}(\s*\(.{0,40}\))?$")

def clean_contact(c):
    """Keep only fields that look like what they claim to be. Anything else goes to
    registry_note so an agent never pastes free text from a registry into a message."""
    name, role, phone, email = (c.get("name") or "").strip(), (c.get("role") or "").strip(), (c.get("phone") or "").strip(), (c.get("email") or "").strip()
    out, notes = {}, []
    if name and len(name) <= 60 and "http" not in name.lower() and "@" not in name and not re.search(r"\d{4,}", name):
        out["name"] = name
    elif name:
        notes.append(name)
    if role: out["role"] = role.replace("_", " ").lower()
    if phone and PHONE_RE.match(phone): out["phone"] = phone
    elif phone: notes.append(phone)
    if email and EMAIL_RE.match(email): out["email"] = email.lower()
    elif email: notes.append(email)
    if notes: out["registry_note"] = " | ".join(notes)[:300]
    return out
CTG = "https://clinicaltrials.gov/api/v2/studies/{}"
ISRCTN = "https://www.isrctn.com/api/query/format/default?q={}"
UA = {"User-Agent": "parkinsons-agents/0.1 (github.com/ainsleys/parkinsons-agents)"}

def place(l):
    return ", ".join(str(x) for x in (l.get("facility"), l.get("city"), l.get("state"), l.get("country")) if x)

def site_key(l):
    return (l.get("facility") or "", l.get("city") or "", l.get("state") or "", l.get("country") or "")

def site_fields(l):
    return {"city": l.get("city"), "state": l.get("state"), "country": l.get("country"), "facility": l.get("facility"), "site_status": l.get("status")}

def diff_nct(old, new):
    """Material differences between two ClinicalTrials.gov records: list of dicts with kind, detail, and site fields."""
    if not old:
        return []
    out = []
    op, np_ = old.get("protocolSection", {}), new.get("protocolSection", {})
    os_, ns = op.get("statusModule", {}), np_.get("statusModule", {})
    if os_.get("overallStatus") != ns.get("overallStatus"):
        out.append({"kind": "status_change", "detail": f"overall status {os_.get('overallStatus')} -> {ns.get('overallStatus')}"})
    if os_.get("whyStopped") != ns.get("whyStopped") and ns.get("whyStopped"):
        out.append({"kind": "status_change", "detail": f"registry reason for stopping: {ns.get('whyStopped')}"})
    for k, label in (("primaryCompletionDateStruct", "primary completion"), ("completionDateStruct", "study completion")):
        a, b = os_.get(k, {}), ns.get(k, {})
        if (a.get("date"), a.get("type")) != (b.get("date"), b.get("type")):
            out.append({"kind": "date_change", "detail": f"{label} {a.get('date')} ({a.get('type')}) -> {b.get('date')} ({b.get('type')})"})
    oe, ne = op.get("eligibilityModule", {}), np_.get("eligibilityModule", {})
    if oe != ne:
        fields = [k for k in sorted(set(oe) | set(ne)) if oe.get(k) != ne.get(k)]
        out.append({"kind": "eligibility_change", "detail": "eligibility fields changed: " + ", ".join(fields) + "; re-verify the eligibility block in data/trials.yaml"})
    od = op.get("designModule", {}).get("enrollmentInfo", {}); nd = np_.get("designModule", {}).get("enrollmentInfo", {})
    if od != nd:
        out.append({"kind": "enrollment_change", "detail": f"enrollment {od.get('count')} ({od.get('type')}) -> {nd.get('count')} ({nd.get('type')})"})
    oc, nc = op.get("contactsLocationsModule", {}), np_.get("contactsLocationsModule", {})
    if oc.get("centralContacts") != nc.get("centralContacts"):
        out.append({"kind": "contact_change", "detail": "central contacts changed; re-verify the contact block in data/trials.yaml"})
    ol = {site_key(l): l for l in oc.get("locations", [])}
    nl = {site_key(l): l for l in nc.get("locations", [])}
    for k in sorted(set(nl) - set(ol)):
        out.append({"kind": "site_added", "detail": f"new site {place(nl[k])} ({nl[k].get('status') or 'status not listed'})", **site_fields(nl[k])})
    for k in sorted(set(ol) - set(nl)):
        out.append({"kind": "site_removed", "detail": f"site removed {place(ol[k])}", **site_fields(ol[k])})
    for k in sorted(set(ol) & set(nl)):
        if ol[k].get("status") != nl[k].get("status"):
            out.append({"kind": "site_status_change", "detail": f"{place(nl[k])} {ol[k].get('status')} -> {nl[k].get('status')}", **site_fields(nl[k])})
    if bool(old.get("hasResults") or "resultsSection" in old) != bool(new.get("hasResults") or "resultsSection" in new):
        out.append({"kind": "results_posted", "detail": "results section now posted on the registry"})
    return out

def parse_isrctn_centres(raw):
    """ISRCTN centres are free-text blocks: facility, address lines, city, blank, country, postcode, optional OID."""
    centres = xml_tag(raw, "trialCentres") or ""
    parsed = []
    for block in re.split(r"\n\s*\n\s*\n", centres):
        lines = [l.strip() for l in block.split("\n")]
        lines = [l for l in lines if not re.match(r"^[A-Z0-9]+@[\d.]+$", l)]
        if not any(lines):
            continue
        try:
            i = lines.index("")
            city, country = lines[i-1], lines[i+1] if i+1 < len(lines) else None
        except ValueError:
            city, country = None, None
        facility = next((l for l in lines if l), None)
        if country in ("England", "Scotland", "Wales", "Northern Ireland"):
            country = "United Kingdom"
        parsed.append({"facility": facility, "city": city, "country": country})
    return parsed

def diff_isrctn(old_raw, new_raw):
    if not old_raw:
        return []
    out = []
    for tag, label in (("recruitmentStart", "recruitment start"), ("recruitmentEnd", "recruitment end"), ("overallEndDate", "overall end date"), ("targetEnrolment", "target enrolment")):
        a, b = (xml_tag(old_raw, tag) or "")[:10], (xml_tag(new_raw, tag) or "")[:10]
        if a != b:
            out.append({"kind": "date_change" if "Date" in tag or "recruitment" in tag else "enrollment_change", "detail": f"{label} {a or 'none'} -> {b or 'none'}"})
    if (xml_tag(old_raw, "inclusion") or "") != (xml_tag(new_raw, "inclusion") or "") or (xml_tag(old_raw, "exclusion") or "") != (xml_tag(new_raw, "exclusion") or ""):
        out.append({"kind": "eligibility_change", "detail": "inclusion or exclusion text changed; re-verify the eligibility block in data/trials.yaml"})
    ol = {site_key(l): l for l in parse_isrctn_centres(old_raw)}
    nl = {site_key(l): l for l in parse_isrctn_centres(new_raw)}
    for k in sorted(set(nl) - set(ol)):
        out.append({"kind": "site_added", "detail": f"new centre {place(nl[k])}", **site_fields(nl[k])})
    for k in sorted(set(ol) - set(nl)):
        out.append({"kind": "site_removed", "detail": f"centre removed {place(ol[k])}", **site_fields(ol[k])})
    return out

def record_changes(entries, today):
    """Prepend entries to data/changes.yaml, rebuild data/changes.xml, and add a dated section to CHANGELOG.md.
    Each entry: registry_id, trial, kind, detail, registry_last_updated, optional city/state/country/facility/site_status."""
    if not entries:
        return
    header = ["# Registry change feed, newest first. Written by scripts/pull_registry.py when a trial's registry record",
              "# changes materially: status, dates, eligibility, contacts, enrollment, sites added or removed, site status,",
              "# results posted. Agents: poll this file or data/changes.xml; scripts/match.py reports entries near a person.",
              "# A human still re-verifies the trial in data/trials.yaml before its `verified` date moves. Do not edit by hand.", ""]
    existing = CHANGES.read_text() if CHANGES.exists() else ""
    body = existing[existing.index("- "):] if "- " in existing else ""
    lines = []
    for e in entries:
        lines.append(f"- date_observed: {today}")
        for k in ("registry_id", "trial", "kind", "detail", "registry_last_updated", "city", "state", "country", "facility", "site_status"):
            if k in e and e[k] is not None:
                lines.append(f"  {k}: {yaml_str(e[k])}")
        lines.append(f"  registry_url: {yaml_str(e['registry_url'])}")
    CHANGES.write_text("\n".join(header + lines) + "\n" + body)
    # CHANGELOG section
    cl = CHANGELOG.read_text()
    head = f"## {today} (registry changes, automated)\n\n"
    bullets = "".join(f"- **{e['trial'] or e['registry_id']}** ({e['registry_id']}): {e['detail']}. Registry updated {e.get('registry_last_updated') or 'date not given'}; needs re-verification in `data/trials.yaml`.\n" for e in entries)
    if head in cl:
        cl = cl.replace(head, head + bullets, 1)
    else:
        anchor = "Newest first. Agents can poll this file to see what changed.\n\n"
        cl = cl.replace(anchor, anchor + head + bullets + "\n", 1) if anchor in cl else head + bullets + "\n" + cl
    CHANGELOG.write_text(cl)
    write_feed()

def write_feed():
    """Atom feed of the change file, so a person can subscribe in an RSS reader. Parsed with regexes to avoid a pyyaml dependency."""
    if not CHANGES.exists():
        return
    items = re.findall(r"^- date_observed: (\S+)\n((?:  .*\n)+)", CHANGES.read_text(), re.M)[:100]
    esc = lambda s: html.escape(str(s), quote=True)
    out = ['<?xml version="1.0" encoding="utf-8"?>', '<feed xmlns="http://www.w3.org/2005/Atom">',
           '<title>Parkinson\'s trial registry changes</title>', f'<link href="{REPO_URL}/blob/main/data/changes.yaml"/>',
           f'<id>{REPO_URL}/data/changes.xml</id>', f'<updated>{items[0][0] if items else "1970-01-01"}T06:30:00Z</updated>',
           '<author><name>registry-bot (scripts/pull_registry.py)</name></author>']
    for d, blk in items:
        f = dict(re.findall(r"^  (\w+): (.*)$", blk, re.M))
        unq = lambda v: v[1:-1].replace('\\"', '"') if v.startswith('"') and v.endswith('"') else v
        f = {k: unq(v) for k, v in f.items()}
        title = f"{f.get('trial') or f.get('registry_id')}: {f.get('kind', '').replace('_', ' ')}"
        out += ["<entry>", f"<title>{esc(title)}</title>", f"<link href=\"{esc(f.get('registry_url', ''))}\"/>",
                f"<id>{REPO_URL}/changes/{f.get('registry_id')}/{d}/{f.get('kind')}/{hashlib.sha1(f.get('detail', '').encode()).hexdigest()[:8]}</id>",
                f"<updated>{d}T06:30:00Z</updated>", f"<summary>{esc(f.get('detail', ''))} (registry record updated {esc(f.get('registry_last_updated') or 'date not given')}; navigation, not medical advice; a human re-verifies before the guide changes)</summary>", "</entry>"]
    out.append("</feed>")
    CHANGES_FEED.write_text("\n".join(out) + "\n")

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
    # trial names by registry id, from the records' own name/registry_id pairs
    names = {}
    for m in re.finditer(r"^- id: .*?\n  name: (.*?)\n  registry_id: (\S+)", text, re.S | re.M):
        names[m.group(2)] = m.group(1).strip()
    names.setdefault("NCT05418673", "LIGHTHOUSE (terminated phase 3 in LRRK2 carriers; see LUMA record)")
    isrctns = sorted(set(re.findall(r"\bISRCTN\d{8}\b", text)))
    OUT.mkdir(exist_ok=True)
    today = datetime.date.today().isoformat()
    changed, errors = [], []
    readouts = []
    change_entries = []
    contacts_out = [f"# Trial contact details pulled from registries on {today} by scripts/pull_registry.py.",
                    "# These are work contacts published by sponsors for recruitment inquiries. Fields are validated:",
                    "# emails must look like emails, phones like phones, names are short and free of URLs; anything else is",
                    "# kept in registry_note and must never be pasted into a message. Hand-reviewed routes live in",
                    "# trials.yaml under `contact`; prefer those. Do not edit this file by hand; re-run the script.", ""]
    sites_out = [f"# Trial site locations pulled from registries on {today} by scripts/pull_registry.py.",
                 "# Do not edit by hand; re-run the script. Site status is the registry's per-site status where given.", ""]

    for nct in ncts:
        try:
            raw = fetch(CTG.format(nct))
        except Exception as e:
            errors.append(f"{nct}: {e}"); continue
        data = json.loads(raw)
        # versionHolder is the registry's daily snapshot date; drop it so unchanged records do not churn nightly
        data.get("derivedSection", {}).get("miscInfoModule", {}).pop("versionHolder", None)
        path = OUT / f"{nct}.json"
        new = json.dumps(data, indent=1, sort_keys=True)
        old = json.loads(path.read_text()) if path.exists() else None
        if not path.exists() or path.read_text() != new:
            changed.append(nct)
        path.write_text(new)
        p = data["protocolSection"]
        st = p.get("statusModule", {})
        for d in diff_nct(old, data):
            change_entries.append({"registry_id": nct, "trial": names.get(nct), "registry_last_updated": st.get("lastUpdatePostDateStruct", {}).get("date"),
                                   "registry_url": f"https://clinicaltrials.gov/study/{nct}", **d})
        el = p.get("eligibilityModule", {})
        de = p.get("designModule", {})
        locs = p.get("contactsLocationsModule", {}).get("locations", [])
        bycountry = collections.Counter(l.get("country", "unknown") for l in locs)
        sites_out.append(f"{nct}:")
        sites_out.append(f"  name: {yaml_str(names.get(nct))}")
        sites_out.append(f"  registry_id: {yaml_str(nct)}")
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
        # readouts
        has_results = bool(data.get("hasResults")) or "resultsSection" in data
        readouts.append({
            "registry_id": nct, "name": names.get(nct), "registry_status": st.get("overallStatus"),
            "why_stopped": st.get("whyStopped"),
            "primary_completion": st.get("primaryCompletionDateStruct", {}).get("date"),
            "primary_completion_type": st.get("primaryCompletionDateStruct", {}).get("type"),
            "study_completion": st.get("completionDateStruct", {}).get("date"),
            "results_posted": has_results,
            "results_first_posted": st.get("resultsFirstPostDateStruct", {}).get("date"),
            "registry_last_updated": st.get("lastUpdatePostDateStruct", {}).get("date"),
            "registry_url": f"https://clinicaltrials.gov/study/{nct}",
        })
        # contacts
        cc = [clean_contact(c) for c in p.get("contactsLocationsModule", {}).get("centralContacts", [])]
        contacts_out.append(f"{nct}:")
        contacts_out.append(f"  name: {yaml_str(names.get(nct))}")
        contacts_out.append(f"  registry_url: \"https://clinicaltrials.gov/study/{nct}\"")
        contacts_out.append(f"  registry_status: {st.get('overallStatus')}")
        contacts_out.append(f"  registry_last_updated: {st.get('lastUpdatePostDateStruct',{}).get('date')}")
        contacts_out.append("  central_contacts:")
        for c in cc:
            contacts_out.append("    - {" + ", ".join(f"{k}: {yaml_str(v)}" for k, v in c.items()) + "}")
        if not cc: contacts_out.append("    []")
        site_cs = [l for l in locs if l.get("contacts")]
        contacts_out.append(f"  sites_with_contacts: {len(site_cs)} of {len(locs)}")
        contacts_out.append("  site_contacts:")
        for l in sorted(site_cs, key=lambda l: (l.get("country",""), l.get("state") or "", l.get("city",""))):
            cs = [clean_contact(c) for c in l.get("contacts", [])]
            cs = [c for c in cs if c.get("phone") or c.get("email") or c.get("name")]
            if not cs: continue
            contacts_out.append(f"    - facility: {yaml_str(l.get('facility'))}")
            contacts_out.append(f"      city: {yaml_str(l.get('city'))}")
            contacts_out.append(f"      state: {yaml_str(l.get('state'))}")
            contacts_out.append(f"      country: {yaml_str(l.get('country'))}")
            contacts_out.append(f"      site_status: {yaml_str(l.get('status'))}")
            contacts_out.append("      contacts:")
            for c in cs:
                contacts_out.append("        - {" + ", ".join(f"{k}: {yaml_str(v)}" for k, v in c.items()) + "}")
        if not site_cs: contacts_out.append("    []")
        contacts_out.append("")
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
        old_raw = path.read_text() if path.exists() else None
        if not path.exists() or path.read_text() != raw:
            changed.append(isr)
        path.write_text(raw)
        for d in diff_isrctn(old_raw, raw):
            change_entries.append({"registry_id": isr, "trial": names.get(isr), "registry_last_updated": None,
                                   "registry_url": f"https://www.isrctn.com/{isr}", **d})
        # ISRCTN exposes recruitment start/end dates rather than a status enum.
        rs, re_ = (xml_tag(raw, "recruitmentStart") or "")[:10], (xml_tag(raw, "recruitmentEnd") or "")[:10]
        if rs and re_ and rs <= today <= re_:
            status = "recruiting (derived from recruitment dates)"
        elif re_ and today > re_:
            status = "recruitment ended (derived from recruitment dates)"
        else:
            status = "unknown"
        edited = None  # the public XML does not carry a last-edited date
        parsed = parse_isrctn_centres(raw)
        bycountry = collections.Counter(p["country"] or "unknown" for p in parsed)
        sites_out.append(f"{isr}:")
        sites_out.append(f"  name: {yaml_str(names.get(isr))}")
        sites_out.append(f"  registry_id: {yaml_str(isr)}")
        sites_out.append(f"  registry_status: {yaml_str(status)}")
        sites_out.append(f"  registry_last_updated: null")
        sites_out.append(f"  recruitment_start: {yaml_str(rs or None)}")
        sites_out.append(f"  recruitment_end: {yaml_str(re_ or None)}")
        sites_out.append(f"  site_count: {len(parsed)}")
        sites_out.append("  countries:")
        for c, n in sorted(bycountry.items(), key=lambda x: -x[1]):
            sites_out.append(f"    {yaml_str(c)}: {n}")
        sites_out.append("  sites:")
        for l in sorted(parsed, key=lambda l: (l["country"] or "", l["city"] or "")):
            sites_out.append(f"    - {{facility: {yaml_str(l['facility'])}, city: {yaml_str(l['city'])}, state: null, country: {yaml_str(l['country'])}, status: null}}")
        sites_out.append("")
        # ISRCTN contacts: <contact> blocks with contactType Public / Scientific / Principal investigator
        contacts_out.append(f"{isr}:")
        contacts_out.append(f"  name: {yaml_str(names.get(isr))}")
        contacts_out.append(f"  registry_url: \"https://www.isrctn.com/{isr}\"")
        contacts_out.append(f"  registry_status: {yaml_str(status)}")
        contacts_out.append("  registry_last_updated: null")
        contacts_out.append("  central_contacts:")
        n_c = 0
        for cm in re.finditer(r"<contact\b[^>]*>(.*?)</contact>", raw, re.S):
            cb = cm.group(1)
            types = ", ".join(t.lower() for t in re.findall(r"<contactType>(.*?)</contactType>", cb))
            nm = " ".join(x for x in (xml_tag(cb, "title"), xml_tag(cb, "forename"), xml_tag(cb, "surname")) if x)
            c = clean_contact({"name": re.sub(r"\s+", " ", nm), "role": types, "phone": (xml_tag(cb, "telephone") or "").replace("-", "").strip() or "", "email": xml_tag(cb, "email") or ""})
            if c.get("email") or c.get("phone"):
                contacts_out.append("    - {" + ", ".join(f"{k}: {yaml_str(v)}" for k, v in c.items()) + "}"); n_c += 1
        if not n_c: contacts_out.append("    []")
        contacts_out.append("  sites_with_contacts: 0")
        contacts_out.append("  site_contacts: []")
        contacts_out.append("")
        readouts.append({
            "registry_id": isr, "name": names.get(isr), "registry_status": status, "why_stopped": None,
            "primary_completion": (xml_tag(raw, "overallEndDate") or "")[:10] or None, "primary_completion_type": "overall end date (ISRCTN)",
            "study_completion": (xml_tag(raw, "overallEndDate") or "")[:10] or None,
            "results_posted": bool(re.search(r"<(?:results|publicationList|outputs)>\s*<", raw) and re.search(r"<output\b", raw) and "Results" in (xml_tag(raw, "outputs") or "")),
            "results_first_posted": None, "registry_last_updated": None,
            "registry_url": f"https://www.isrctn.com/{isr}",
        })
        if not quiet:
            print(f"\n=== {isr}  {(xml_tag(raw,'title') or '')[:90]}")
            print(f"status: {status}  recruitment {rs} to {re_}")

    SITES.write_text("\n".join(sites_out))
    CONTACTS.write_text("\n".join(contacts_out))
    record_changes(change_entries, today)

    # Readouts: expected result dates and posted-results flags, all from the registries.
    def sort_key(r):
        d = r.get("primary_completion") or "9999"
        return (0 if r["results_posted"] else 1, d)
    rows = sorted(readouts, key=lambda r: (r.get("primary_completion") or "9999-99"))
    ry = [f"# Expected and posted results for every trial in data/trials.yaml, from the registries, pulled on {today}.",
          "# Generated by scripts/pull_registry.py; do not edit by hand. primary_completion_type ACTUAL means the date has passed;",
          "# ESTIMATED means the sponsor's projection. results_posted is the registry's own flag; sponsors usually announce",
          "# topline results by press release months before posting to the registry, so a false here does not mean no result exists.", ""]
    md = ["# Readouts", "", f"Generated by `scripts/pull_registry.py` from the registries on {today}. Do not edit by hand.", "",
          "Expected result dates for every trial in the data, soonest first. `ACTUAL` means the registry records the completion as having happened; `ESTIMATED` is the sponsor's projection and slips often. The results flag is the registry's own; sponsors usually announce topline results by press release months earlier, so check the trial's `background` line in `data/trials.yaml` and the changelog for anything reported but not yet posted.", "",
          "| Trial | Registry status | Primary completion | Type | Results posted | Note |", "|---|---|---|---|---|---|"]
    for r in rows:
        ry.append(f"- registry_id: {yaml_str(r['registry_id'])}")
        for k in ("name", "registry_status", "why_stopped", "primary_completion", "primary_completion_type", "study_completion", "results_posted", "results_first_posted", "registry_last_updated", "registry_url"):
            v = r.get(k)
            ry.append(f"  {k}: {str(v).lower() if isinstance(v, bool) else yaml_str(v)}")
        pc = r.get("primary_completion") or ""
        overdue = bool(pc) and pc[:7] < today[:7] and not r["results_posted"] and r.get("registry_status") not in ("RECRUITING", "ACTIVE_NOT_RECRUITING", "WITHDRAWN")
        note = ("results posted" if r["results_posted"]
                else "registry status unknown; past estimated completion" if (overdue and r.get("registry_status") == "UNKNOWN")
                else "completed, results not yet posted on the registry" if overdue
                else r.get("why_stopped") or "")
        md.append(f"| {r.get('name') or r['registry_id']} ([{r['registry_id']}]({r['registry_url']})) | {r.get('registry_status') or 'unknown'} | {pc or 'unknown'} | {r.get('primary_completion_type') or ''} | {'yes' if r['results_posted'] else 'no'} | {note} |")
    md += ["", "## How to use this", "", "- A completed trial with no posted results is normal for the first year; after that, look for a publication or press release and add it to the trial's `background` with a source.",
           "- The nightly job regenerates this page. A status flip or a results flag turning on shows up as a diff in the commit history.",
           "- Dates here are registry dates. Topline announcements (for example LUMA, May 2026) precede registry posting; those are recorded in `data/trials.yaml` under `background` with their sources.", ""]
    READOUTS_YAML.write_text("\n".join(ry) + "\n")
    READOUTS_MD.write_text("\n".join(md))

    # PPMI in-clinic sites: the public table on ppmi-info.org is fed by a JSON file.
    try:
        rows = json.loads(fetch(PPMI_SITES_JSON))
        strip = lambda v: html.unescape(re.sub(r"<[^>]+>", " ", str(v or ""))).strip()
        out = [f"# Observational program sites pulled on {today} by scripts/pull_registry.py.",
               f"# PPMI in-clinic sites from {PPMI_SITES_JSON} (the table on ppmi-info.org/about-ppmi/ppmi-clinical-sites).",
               "# Coordinator contacts for international sites are hand-maintained in data/programs.yaml (ppmi_clinic). Do not edit this file by hand.", "",
               "ppmi_clinic:", "  name: \"PPMI in-clinic cohort\"", f"  site_count: {len(rows)}", "  sites:"]
        for r in sorted(rows, key=lambda r: strip(r.get("location"))):
            loc = re.sub(r"\s+", " ", strip(r.get("location")))
            city, _, rest = loc.partition(",")
            rest = rest.strip()
            if rest in US_STATES:
                state, country = rest, "United States"
            elif rest in ("England", "United Kingdom"):
                state, country = None, "United Kingdom"
            else:
                state, country = None, rest or None
            out.append(f"    - {{facility: {yaml_str(re.sub(r'\\s+', ' ', strip(r.get('organization'))))}, city: {yaml_str(city.strip())}, state: {yaml_str(state)}, country: {yaml_str(country)}, principal_investigator: {yaml_str(re.sub(r'\\s+', ' ', strip(r.get('pi'))))}}}")
        PROGRAM_SITES.write_text("\n".join(out) + "\n")
    except Exception as e:
        errors.append(f"PPMI sites: {e}")
    print(f"\npulled {len(ncts)} NCT and {len(isrctns)} ISRCTN records on {today}; changed: {changed or 'none'}; errors: {errors or 'none'}")
    for e in change_entries:
        print(f"CHANGE {e['registry_id']} {e['kind']}: {e['detail']}")
    if errors:
        sys.exit(1)

if __name__ == "__main__":
    main()
