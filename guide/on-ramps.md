# On-ramps

verified: 2026-10-19. Trial status drifts monthly; confirm on ClinicalTrials.gov or with the site coordinator before acting. Structured versions of these records are in `data/programs.yaml` and `data/trials.yaml`.

## The gap this page exists to close

About 80 percent of people with Parkinson's say they are at least somewhat likely to join research. Under 10 percent ever have. Fewer than half of trials hit recruitment targets. The barriers people report are awareness, travel and cost, invasive procedures, mistrust and misconceptions, and age cutoffs. Convenience and non-invasiveness are rated as deciding factors, so each entry below states burden explicitly. Sources: [Goh et al. 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13476382/), [scoping review 2025](https://www.researchgate.net/publication/388008928_Improving_recruitment_and_retention_of_people_with_Parkinson's_disease_to_clinical_studies_A_scoping_review).

## Tier 1: takes almost anyone, no downside, do first

**PD GENEration** (Parkinson's Foundation; NCT04057794). Free seven-gene test with counseling. Confirmed diagnosis, 18 or older. At-home blood kit in the US, Canada, Puerto Rico, Dominican Republic; sites also in Chile, Mexico, Israel. Burden: one sample, one counseling call. Does not exclude you from anything. Over 30,000 enrolled. Details in `get-typed.md`.

**PPMI** (Michael J. Fox Foundation; renamed Parkinson's Precision Medicine Initiative in 2026). The field's reference cohort, about 50 sites in 12 countries, over 5,000 in-clinic and over 50,000 online participants. Two ways in:
- *Online (myPPMI / PPMI Online, NCT05065060).* Anyone 18 or older in the US, with or without Parkinson's. Questionnaires at home. Recruiting through 2041.
- *In clinic.* Enrolling people recently diagnosed and not yet on medication, people with REM sleep behavior disorder, known genetic carriers, and controls; Ashkenazi Jewish participants specifically sought. Burden: visits every 6 to 12 months with lumbar puncture, DaTscan, MRI and blood. In return the participant gets the synuclein assay and imaging at no cost, and site coordinators know which drug trials are opening locally. Observational, no placebo, does not block later trials. MRI requirement matters for anyone with an implanted device.
- *Smell test.* Free kit by mail in the US and Canada; over 40 without a diagnosis or over 30 and diagnosed within 7 years.
Sources: [MJFF PPMI](https://michaeljfox.org/ppmi), [PPMI Online registry](https://clinicaltrials.gov/study/NCT05065060), corpus file 10.

**Fox Insight** (Michael J. Fox Foundation). Online longitudinal study, about 56,000 participants, people with Parkinson's and family members. Questionnaires every 90 days plus topic surveys. De-identified data shared with researchers. Relationship to myPPMI not confirmed; both were live in October 2026. Source: [foxinsight.michaeljfox.org](https://foxinsight.michaeljfox.org/).

**PD Frontline** (UK). Saliva kit by post; finds LRRK2 and GBA1 carriers for recontact. Prioritising ages 35 to 75 diagnosed within 7 years.

**Fox Trial Finder** (Michael J. Fox Foundation). Matching service. Historically, volunteer locations and site locations overlapped poorly, so an agent should search ClinicalTrials.gov directly as well.

## Tier 2: pivotal disease-modifying trials recruiting now

These are the only randomized, placebo-controlled programs powered for disease modification in idiopathic PD as of October 2026. None reports before 2027. Eligibility fields below are for local matching; `data/trials.yaml` has the structured version.

**PARAISO, prasinezumab** (Roche; NCT07174310; phase 3). Anti-alpha-synuclein antibody, IV infusion every 4 weeks, at least 104 weeks blinded then open-label drug for all. About 900 participants, 192 sites in 17 countries per the registry, started November 2025, primary completion June 2029. Eligibility: age 50 to 85; idiopathic PD by MDS criteria; Hoehn and Yahr 1 or 2 off medication; MDS-UPDRS Part IV score 0, meaning no motor complications yet; on stable symptomatic monotherapy (site listings say levodopa); weight 40 to 110 kg; BMI 18 to 34. Site listings add a disease duration of 3 months to 3 years. Half receive placebo for two years. MRI very likely required. Background: phase 2b PADOVA missed its primary endpoint (hazard ratio 0.84, p 0.066) with a prespecified levodopa subgroup at 0.79; this is effectively the first adequately powered test of the extracellular-synuclein hypothesis. Source: [registry](https://clinicaltrials.gov/study/NCT07174310), corpus file 06.

**ASPro-PD, ambroxol** (UCL; NCT05778617; phase 3; UK only). Oral GBA1 chaperone, 1,260 mg per day versus placebo for 104 weeks then 26 weeks open-label. 330 participants, 15 UK sites. Eligibility: age 35 to 75; PD diagnosed within 7 years; Hoehn and Yahr 1 to 2.5 on medication; on stable dopaminergic treatment for at least 3 months; GBA1 status known before screening, with carriers and non-carriers both enrolled; LRRK2 G2019S carriers excluded. Also excludes prior deep brain stimulation, ambroxol or a GLP-1 agonist in the past 12 months, MoCA below 20, and recent anticholinergics. Primary completion February 2029. Burden: daily pills, clinic visits, optional lumbar puncture sub-study. Source: [protocol](https://pubmed.ncbi.nlm.nih.gov/41708985/), [Cure Parkinson's](https://cureparkinsons.org.uk/2025/04/the-aspro-pd-trial-is-now-underway/).

**GREAT, high-dose ambroxol** (Groningen; NCT05830396, EU CT 2024-514976-41-00; phase 2/3; Netherlands, one site). 1,800 mg per day for 60 weeks; 80 planned. GBA1 carriers only, age 18 and over, disease duration under 10 years, MRI required. The EU registry says recruiting since September 2024; the ClinicalTrials.gov record has not been updated since 2023.

**BHV-8000** (Biohaven; NCT06976268; phase 2/3; US). Oral TYK2/JAK1 inhibitor, 48 weeks blinded then 48 open-label, 550 planned, 24 US sites, primary completion August 2027. Eligibility: age 40 to 80; probable PD by MDS criteria with onset within 2 years; **not on any PD medication**; non-smoker, including e-cigarettes. The untreated requirement means this trial competes with starting levodopa, which is a decision for the person and their neurologist. Immune suppression risk and infection screening. Source: [registry](https://clinicaltrials.gov/study/NCT06976268).

**EJS ACT-PD** (UK platform; telmisartan, terazosin, ursodeoxycholic acid versus shared placebo over 3 years; 43 UK sites). PD within a few years of diagnosis. Terazosin lowers blood pressure, relevant for anyone with orthostatic symptoms. Source: corpus file 06.

## Tier 3: subtype-restricted or later-stage, check status before pursuing

- **BEACON** (Denali; NCT06602193): BIIB122 in LRRK2 carriers only, ages 30 to 80 (no upper limit for homozygous carriers), 20 sites in 4 countries. Active, not recruiting. Data first half of 2027.
- **PROPEL** (Lilly/Prevail; NCT04127578): PR001 gene therapy in GBA1 PD, ages 35 to 80, Hoehn and Yahr 3 to 4, single intracisternal injection with immunosuppression. Active, not recruiting. Primary completion August 2031.
- **REGENERATE-PD** (NCT06285643): AAV2-GDNF gene therapy, sham-controlled neurosurgery, moderate PD, ages 45 to 75.
- **exPDite-2** (NCT06944522): bemdaneprocel stem cell transplant, phase 3, moderate PD with motor fluctuations, 12 months immunosuppression.
- **DAPA-PD** (dapansutrile, NLRP3 inhibitor, phase 2, started March 2026) and **TAME-PD** (terazosin, phase 1/2, University of Iowa, NCT07288450): small early-phase options.

## Recently closed or failed, so an agent does not chase them

LUMA (BIIB122, NCT05348785, failed May 2026; its companion phase 3 in LRRK2 carriers, LIGHTHOUSE, was terminated in 2023). ACTIVATE (BIA 28-6156, GBA1 activator, failed June 2026). MOVES-PD (venglustat, failed). SPARK (cinpanemab, failed). ORCHESTRA (minzasolmin, failed December 2024). Exenatide-PD3 (failed February 2025; expression of concern June 2026). SPARX3 (exercise intensity, enrollment closed, results pending). NOPARK (nicotinamide riboside, results pending).

## Questions an agent should have the person ask each coordinator

1. Is MRI required, and does the site scan MRI-conditional implanted devices?
2. Must the person be untreated, on stable medication, or either?
3. Does enrollment here exclude other trials, and for how long?
4. What is the placebo probability and for how long?
5. Is travel reimbursed, and can any visits be remote?
6. Is there an open-label extension where everyone receives the drug?
