# Research corpus

Deep background for the agent-first guide in this repository. Start at `START_HERE.md` for the current state of the field; come here for depth, mechanisms, history and the bibliography.

Literature review of Parkinson's disease research, compiled 2026-10-06. Status of the field as of October 2026, with the historical arc included.

## Start here

- `reports/Parkinsons disease research review.md` — the synthesized review (~33,500 words). Twelve sections, an open-questions section, and a consolidated bibliography of ~330 entries organized by topic. Read the opening paragraph for the one-paragraph verdict.

## Research notes

`research_notes/Parkinsons disease research review/` holds the ten source files the report was built from. Each is organized by key question with a Takeaway, Cited Findings, Inferences, and Gaps block, and each carries inline citations with URLs. They are more detailed than the report and are the place to go for a specific number or paper.

| File | Covers |
|---|---|
| 01_pathophysiology_and_mechanisms.md | How dopaminergic neurons die, alpha-synuclein causality debate, prion-like spread, body-first vs brain-first, mitochondria, lysosomes, inflammation, gut microbiome |
| 02_genetics_epidemiology_risk_factors.md | Monogenic and risk genes, GWAS and GP2, prevalence and 2050 projections, pesticides, TCE, air pollution, protective factors, prodromal markers, major cohorts |
| 03_diagnosis_biomarkers_staging.md | Clinical criteria and misdiagnosis rates, seed amplification assays, NSD-ISS vs SynNeurGe biological staging and the controversy, imaging, fluid and digital biomarkers, prodromal criteria |
| 04_motor_treatment_drugs_devices_surgery.md | Levodopa and LEAP, adjunct drugs, subcutaneous infusions, deep brain stimulation including adaptive DBS, focused ultrasound, guidelines, gait and falls, tavapadon and pipeline |
| 05_nonmotor_symptoms_and_management.md | Cognition and dementia, psychosis, mood and impulse control, autonomic, sleep, pain, assessment scales, evidence-based treatment ratings |
| 06_disease_modifying_therapy_pipeline.md | Every major neuroprotection trial and its result, GLP-1 agonists, alpha-synuclein antibodies, LRRK2 and GBA1 programs, repurposed drugs, platform trials, 2026 pipeline census |
| 07_cell_gene_therapy_and_emerging_tech.md | Fetal grafts to stem cell trials, Japan's 2026 conditional approval, AAV gene therapies, spinal stimulation, digital and AI detection, timelines |
| 08_exercise_lifestyle_care_models_outcomes.md | SPARX and Park-in-Shape protocols, tai chi, rehabilitation, diet and supplements, care models, palliative care, quality of life, prevention policy, economics |
| 09_basal_ganglia_circuits_iron_gut_origin.md | Rate model and its revisions, beta oscillations as a DBS control signal, iron and ferroptosis and why chelation failed, vagotomy and appendectomy and IBD evidence, SNCA dosage, HLA |
| 10_history_and_research_infrastructure.md | 1817 to 2026 timeline, dopamine discovery, funders and consortia (MJFF, PPMI, ASAP, GP2, Parkinson's Foundation), cohorts and biobanks, journals, publication counts, strategic debates |

## How to read the caveats

Researchers exhausted the web search budget partway through. Later work fell back to the PubMed and ClinicalTrials.gov APIs, which verify that a citation exists but do not return abstracts. As a result:

- Every citation is real and resolvable.
- Figures that could not be read from a source are flagged inline as unverified rather than filled in from memory. Files 09 and 10 carry this flag most heavily.
- Conflicts between sources (for example, two dates for the tavapadon approval) are documented rather than resolved.
- The report's "Open questions and known gaps" section lists what the corpus does not cover.

Two readouts that would most change the picture were unpublished at compile time: NOPARK (nicotinamide riboside, 410 participants) and SPARX3 (exercise intensity, 370 participants).
