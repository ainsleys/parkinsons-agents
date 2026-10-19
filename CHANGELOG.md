# Changelog

Newest first. Agents can poll this file to see what changed.

## 2026-10-19 (benchmark and fixes)

- Added `benchmarks/`: 20 fixed personas, the prompt template, and the baseline from 35 fresh-agent runs (Fable, Opus, Sonnet, Haiku). Baseline Fable mean 3.45 of 5.
- Fixed START_HERE.md errors found by the benchmark: skin biopsy is immunostaining, not a seed amplification assay; pivotal program count; "every program restricted by subtype" removed; pointer to open questions corrected; developer line updated; headline numbers now cited.
- Added `data/sites.yaml`: every trial site with city, state, country and status, from the registries. On-ramps page now names cities per trial.
- Normalized eligibility in `data/trials.yaml` (stage with on/off state, duration with reference point, medication state enum, structured genetic requirement, motor complications, smoking, cognition) and added matching rules to `data/SCHEMA.md`.
- Added six trials to `data/trials.yaml`: EJS ACT-PD (ISRCTN17799294), DAPA-PD (ISRCTN16806940), exPDite-2, REGENERATE-PD, AMBITIOUS, Agyany ambroxol, plus TAME-PD (withdrawn). Every trial on the on-ramps page now has a data record.
- `data/programs.yaml`: added cost, genes, countries, at_home and how_to_join fields.
- `data/tests.yaml`: added turnaround and negative_means; primary citation for the CSF assay figures; payer-policy source for the CPT code; fixed the 23andMe link; PD GENEration yield stated as 12 to 13 percent with both sources.
- Guide pages: disclaimer on every page; new sections on choosing between the skin and spinal fluid tests and on what a negative means; plain-language GBA1 definition; timing windows for untreated people; a section stating what the repo does not cover outside the US, UK and Netherlands.
- `scripts/pull_registry.py` now also reads ISRCTN records and writes `data/sites.yaml`. New `scripts/check_freshness.py` and a nightly GitHub Actions workflow.
- llms.txt and CORPUS.md now list every file with word counts.

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
