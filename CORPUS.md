# Research corpus

Deep background for the agent-first guide in this repository. Start at `START_HERE.md` for the current state of the field; come here for depth, mechanisms, history and the bibliography.

Literature review of Parkinson's disease research, compiled 2026-10-06. Status of the field as of October 2026, with the historical arc included.

## Start here

- `reports/Parkinsons disease research review.md` — the synthesized review (33,654 words; fetch in thirds, the open-questions section and bibliography are at the end). Twelve sections, an open-questions section, and a consolidated bibliography of ~330 entries organized by topic. Read the opening paragraph for the one-paragraph verdict.

## Research notes

Each file is 5,000 to 10,000 words with no section index; grep for a keyword rather than reading whole files. Ambroxol, GBA1 trial evidence and LRRK2 pipeline are in 06; test performance and staging in 03; gene variant classes and penetrance in 02; DBS and focused ultrasound in 04; body-first vs brain-first in 01.

`research_notes/Parkinsons disease research review/` holds the ten source files the report was built from. Each is organized by key question with a Takeaway, Cited Findings, Inferences, and Gaps block, and each carries inline citations with URLs. They are more detailed than the report and are the place to go for a specific number or paper.

| File | Words | Covers |
|---|---|---|
| 01_pathophysiology_and_mechanisms.md | 5,192 | How dopaminergic neurons die, alpha-synuclein causality debate, prion-like spread, body-first vs brain-first, mitochondria, lysosomes, inflammation, gut microbiome |
| 02_genetics_epidemiology_risk_factors.md | 7,873 | Monogenic and risk genes (LRRK2, GBA1 variants N370S/L444P/E326K, PRKN, PINK1, SNCA, RAB32), penetrance, GWAS and GP2, prevalence, pesticides, TCE, air pollution, prodromal markers, major cohorts |
| 03_diagnosis_biomarkers_staging.md | 6,184 | Clinical criteria and misdiagnosis rates, seed amplification assays (CSF, skin, blood), NSD-ISS vs SynNeurGe staging and the Espay critique, DaTscan, fluid and digital biomarkers, prodromal criteria, RBD conversion rates |
| 04_motor_treatment_drugs_devices_surgery.md | 9,531 | Levodopa and LEAP, adjunct drugs, subcutaneous infusions, deep brain stimulation (targets, cognition, adaptive DBS), focused ultrasound approvals, gait and falls, tavapadon |
| 05_nonmotor_symptoms_and_management.md | 8,880 | Cognition and dementia, psychosis drug ratings, mood and impulse control, autonomic and orthostatic hypotension, sleep, pain, assessment scales |
| 06_disease_modifying_therapy_pipeline.md | 7,895 | Every disease-modifying trial and result: prasinezumab, cinpanemab, LRRK2 (LUMA, BEACON, BIIB094), GBA1 (venglustat, ambroxol trials incl. ASPro-PD, GREAT, AMBITIOUS; BIA 28-6156), GLP-1, c-Abl, repurposed drugs, platform trials, 2026 pipeline census |
| 07_cell_gene_therapy_and_emerging_tech.md | 9,292 | Fetal grafts to stem cell trials (bemdaneprocel, exPDite-2), Japan's 2026 conditional approval, AAV gene therapies (GDNF, GBA1, AAV-GAD), spinal stimulation, digital and AI detection |
| 08_exercise_lifestyle_care_models_outcomes.md | 5,602 | SPARX and Park-in-Shape exercise protocols, tai chi, rehabilitation, diet and supplements, care models, telemedicine, palliative care, quality of life, economics |
| 09_basal_ganglia_circuits_iron_gut_origin.md | 7,739 | Rate model and revisions, beta oscillations, iron and ferroptosis and why chelation failed, vagotomy and appendectomy and IBD evidence, SNCA dosage, HLA |
| 10_history_and_research_infrastructure.md | 8,981 | 1817 to 2026 timeline, funders and consortia (MJFF, PPMI data access, ASAP, GP2, Parkinson's Foundation, AMP-PD), cohorts and biobanks, publication counts |

## How to read the caveats

Researchers exhausted the web search budget partway through. Later work fell back to the PubMed and ClinicalTrials.gov APIs, which verify that a citation exists but do not return abstracts. As a result:

- Every citation is real and resolvable.
- Figures that could not be read from a source are flagged inline as unverified rather than filled in from memory. Files 09 and 10 carry this flag most heavily.
- Conflicts between sources (for example, two dates for the tavapadon approval) are documented rather than resolved.
- The report's "Open questions and known gaps" section lists what the corpus does not cover.

Two readouts that would most change the picture were unpublished at compile time: NOPARK (nicotinamide riboside, 410 participants) and SPARX3 (exercise intensity, 370 participants).
