# Changelog

Newest first. Agents can poll this file to see what changed.

## 2026-10-19 (later)

- Added `scripts/pull_registry.py`: pulls every NCT ID in `data/trials.yaml` from the ClinicalTrials.gov v2 API into `data/registry/` (raw JSON, one file per trial) and prints a reviewable summary. Deterministic, no LLM.
- Populated structured eligibility for all trials in `data/trials.yaml` from the registry: ages, disease duration, stage, medication state, genetic requirement, key exclusions, enrollment target, primary completion, registry last-updated date.
- Corrections found by the pull: LUMA is NCT05348785 (the record previously cited, NCT05418673, is LIGHTHOUSE, a terminated phase 3 in LRRK2 carriers). PARAISO lists 192 sites, not 231. BHV-8000 requires participants to be **untreated** and non-smokers, ages 40 to 80, onset within 2 years. ASPro-PD is ages 35 to 75, within 7 years of diagnosis, and excludes LRRK2 G2019S carriers. GREAT enrolls GBA1 carriers only; its ClinicalTrials.gov record is stale and the EU registry shows it recruiting since September 2024.
- `guide/on-ramps.md` updated to match.

## 2026-10-19

- Initial public release.
- `START_HERE.md`, `llms.txt`, `guide/get-typed.md`, `guide/subtypes.md`, `guide/on-ramps.md`.
- `data/tests.yaml`, `data/programs.yaml`, `data/trials.yaml`, `data/SCHEMA.md`.
- Imported the 2026-10-06 literature review corpus (`CORPUS.md`, `reports/`, `research_notes/`).
- Verified against sources on 2026-10-19: PD GENEration eligibility and geography, SYNTap cost and billing status, Syn-One status, 23andMe variant coverage, NHS genetic testing criteria, PD Frontline, PPMI online and smell-test eligibility, PARAISO eligibility and status, ASPro-PD status, LUMA failure (May 2026), PROPEL status, BEACON status.
