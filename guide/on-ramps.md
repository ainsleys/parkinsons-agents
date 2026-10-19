# On-ramps

verified: 2026-10-19. Navigation, not medical advice. Trial status drifts monthly; confirm on the registry or with the site coordinator before acting. Structured records with full eligibility fields are in `data/trials.yaml` (use the matching rules in `data/SCHEMA.md`), programs in `data/programs.yaml`, and per-site cities in `data/sites.yaml`.

## The gap this page exists to close

About 80 percent of people with Parkinson's say they are at least somewhat likely to join research. Under 10 percent ever have. Fewer than half of trials hit recruitment targets. The barriers people report are awareness, travel and cost, invasive procedures, mistrust and misconceptions, and age cutoffs. Convenience and non-invasiveness are rated as deciding factors, so each entry below states burden and location. Sources: [Goh et al. 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13476382/), [scoping review 2025](https://www.researchgate.net/publication/388008928_Improving_recruitment_and_retention_of_people_with_Parkinson's_disease_to_clinical_studies_A_scoping_review).

## Two timing windows worth knowing about

- **Not yet on medication.** PPMI's in-clinic cohort and the BHV-8000 trial both enroll untreated people. That window closes when medication starts. Starting levodopa is a clinical decision for the person and their neurologist; the point here is only that the two choices interact.
- **Time since diagnosis.** PARAISO takes people up to 3 years from diagnosis, BHV-8000 up to 2 years from symptom onset, ASPro-PD up to 7 years. The surgical trials start at 4 years.

## Tier 1: takes almost anyone, no downside, do first

**PD GENEration** (Parkinson's Foundation; NCT04057794). Free seven-gene test with counseling. Confirmed diagnosis, 18 or older. At-home blood kit in the US, Canada, Puerto Rico, Dominican Republic; in-person sites also in Chile, Mexico, Israel. Burden: one sample, one counseling call. Does not exclude you from anything. Over 30,000 enrolled. Details in `get-typed.md`. Not available in Europe, Asia, Africa, Australia or South America outside Chile; those regions need a clinician-ordered panel or a local research study.

**PPMI** (Michael J. Fox Foundation; renamed Parkinson's Precision Medicine Initiative in 2026 per corpus file 10). The field's reference cohort, about 50 sites in 12 countries, over 5,000 in-clinic and over 50,000 online participants. Three ways in:
- *Online (myPPMI / PPMI Online, NCT05065060).* Anyone 18 or older in the US, with or without Parkinson's. Questionnaires at home. Recruiting through 2041.
- *In clinic.* Enrolling people recently diagnosed and not yet on medication, people with REM sleep behavior disorder, known genetic carriers, and controls; Ashkenazi Jewish participants specifically sought. Burden: visits every 6 to 12 months with lumbar puncture, DaTscan, MRI and blood. In return the participant gets the synuclein assay and imaging at no cost, and site coordinators know which drug trials are opening locally. Observational, no placebo, does not block later trials. MRI requirement matters for anyone with an implanted device. Site list at ppmi-info.org.
- *Smell test.* Free kit by mail in the US and Canada; over 40 without a diagnosis or over 30 and diagnosed within 7 years.
Sources: [MJFF PPMI](https://michaeljfox.org/ppmi), [PPMI Online registry](https://clinicaltrials.gov/study/NCT05065060), corpus file 10.

**Fox Insight** (Michael J. Fox Foundation). Online longitudinal study open from any country, about 56,000 participants, people with Parkinson's and family members. Questionnaires every 90 days plus topic surveys. De-identified data shared with researchers. Relationship to myPPMI not confirmed; both were live in October 2026. Source: [foxinsight.michaeljfox.org](https://foxinsight.michaeljfox.org/).

**PD Frontline** (UK). Saliva kit by post; finds LRRK2 and GBA1 carriers for recontact. Prioritising ages 35 to 75 diagnosed within 7 years. This is the practical UK route to a GBA1 result for someone who does not meet NHS clinical testing criteria (onset before 50, or a first-degree relative with onset before 50). Turnaround not published.

**Fox Trial Finder** (Michael J. Fox Foundation). Matching service, US-focused. Historically, volunteer locations and site locations overlapped poorly, so an agent should search ClinicalTrials.gov directly as well.

## Tier 2: disease-modifying trials recruiting now

Randomized, placebo-controlled programs in Parkinson's as of October 2026. None reports before 2027. Eligibility summaries below; `data/trials.yaml` has every field, `data/sites.yaml` has every site.

**PARAISO, prasinezumab** (Roche; NCT07174310; phase 3). Anti-alpha-synuclein antibody, IV infusion every 4 weeks, at least 104 weeks blinded then open-label drug for all. About 900 participants, 192 sites in 17 countries, started November 2025, primary completion June 2029. Eligibility: age 50 to 85; idiopathic PD by MDS criteria; Hoehn and Yahr 1 or 2 **off medication**; MDS-UPDRS Part IV score 0, meaning no motor complications yet; on stable symptomatic monotherapy (site listings say levodopa); weight 40 to 110 kg; BMI 18 to 34; no genetic requirement. Site listings add a disease duration of 3 months to 3 years. Half receive placebo for two years. MRI very likely required. **Where:** 53 US sites including Chicago, Cleveland, Boston, New York, Philadelphia, Los Angeles, San Francisco, Phoenix, Dallas, Atlanta, Miami, Nashville, Portland, Las Vegas, Albuquerque; 7 UK sites (London, Oxford, Newcastle, Dundee, Exeter, Plymouth); 8 in Brazil; 7 in Australia; 3 in Canada; 2 in Mexico; and sites in China, Germany, Italy, Spain, France, Poland, Portugal, South Korea, Taiwan, Austria, Denmark. Full list in `data/sites.yaml`. Background: phase 2b PADOVA missed its primary endpoint (hazard ratio 0.84, p 0.066) with a prespecified levodopa subgroup at 0.79; this is effectively the first adequately powered test of the extracellular-synuclein hypothesis. Source: [registry](https://clinicaltrials.gov/study/NCT07174310), corpus file 06.

**ASPro-PD, ambroxol** (UCL; NCT05778617; phase 3; UK only). Oral GBA1 chaperone, 1,260 mg per day versus placebo for 104 weeks then 26 weeks open-label. 330 participants. Eligibility: age 35 to 75; PD diagnosed within 7 years; Hoehn and Yahr 1 to 2.5 **on medication**; on stable dopaminergic treatment for at least 3 months; GBA1 status known before screening, with carriers and non-carriers both enrolled; LRRK2 G2019S carriers excluded; MoCA 20 or above. Also excludes prior deep brain stimulation, ambroxol or a GLP-1 agonist in the past 12 months, and recent anticholinergics. Primary completion February 2029. Burden: daily pills, clinic visits, optional lumbar puncture sub-study. **Where:** 15 UK sites: London, Birmingham, Bristol, Cambridge, Edinburgh, Newcastle, Oxford, Plymouth, Salford (Manchester area), Southampton, Wales. The registry record was last updated May 2025; Cure Parkinson's reported sites open in 2026. Sources: [registry](https://clinicaltrials.gov/study/NCT05778617), [protocol](https://pubmed.ncbi.nlm.nih.gov/41708985/), [Cure Parkinson's](https://cureparkinsons.org.uk/2025/04/the-aspro-pd-trial-is-now-underway/).

**EJS ACT-PD** (UCL; ISRCTN17799294; phase 3 platform; UK only). Telmisartan 40 mg or terazosin 5 mg daily versus shared placebo, on top of standard care, for up to 36 months; a ursodeoxycholic acid arm is planned for 2026. 1,200 participants, 43 sites, recruiting from September 2025 to June 2029. Eligibility: PD diagnosed at 30 or older with no upper age limit; on levodopa or a dopamine agonist for at least 2 months (MAO-B inhibitor alone does not count); MoCA 21 or above; excludes known PRKN, PINK1 or PARK7 carriers, prior or planned brain surgery or infusion therapy, another interventional trial within 6 months, significant depression. Terazosin lowers blood pressure, so arm-specific exclusions apply. Screening is in person; later visits can be remote, which lowers the travel burden considerably. **Where:** Newcastle, Sheffield, Salford, Birmingham, Cambridge, London (UCLH, Royal London, St George's), Oxford, Brighton, Bath, Plymouth, Dundee, Cardiff, Belfast, Liverpool and others; full list on the registry. Sources: [ISRCTN](https://www.isrctn.com/ISRCTN17799294), [Cure Parkinson's](https://cureparkinsons.org.uk/2025/10/ejs-act-pd-recruitment-announcement/).

**BHV-8000** (Biohaven; NCT06976268; phase 2/3; US). Oral TYK2/JAK1 inhibitor, 48 weeks blinded then 48 open-label, 550 planned, primary completion August 2027. Eligibility: age 40 to 80; probable PD by MDS criteria with onset within 2 years; **not on any PD medication**; non-smoker, including e-cigarettes. Immune suppression risk and infection screening. **Where:** 24 US sites: Albany, Atlantis and Boca Raton and Maitland (Florida), Aurora (Colorado), Bellevue and Seattle, Birmingham (Alabama), Boston and Foxborough, Chesterfield (Missouri), Chicago, Cleveland, Farmington Hills (Michigan), Farmington and New Haven (Connecticut), Henrico and Newport News (Virginia), Irvine and Los Angeles, Kansas City, New York, Portland (Oregon), Round Rock (Texas). Source: [registry](https://clinicaltrials.gov/study/NCT06976268).

**GREAT, high-dose ambroxol** (Groningen; NCT05830396, EU CT 2024-514976-41-00; phase 2/3; Netherlands, one site). 1,800 mg per day for 60 weeks; 80 planned. GBA1 carriers only, age 18 and over, disease duration under 10 years, MRI required. The EU registry says recruiting since September 2024; the ClinicalTrials.gov record has not been updated since 2023.

**DAPA-PD, dapansutrile** (Cambridge; ISRCTN16806940; phase 2; UK, one site). Oral NLRP3 inhibitor, 2 to 1 versus placebo for 26 weeks, then optional 26 weeks open-label. 36 participants, recruiting to February 2027. Eligibility: age 50 to 80; early PD, Hoehn and Yahr 2 or below, under 5 years duration; drug-naive or on stable dopaminergic therapy for 3 months; raised high-sensitivity CRP; no known PD gene variant; fluent English; about 10 in-person visits in Cambridge including PET. Source: [ISRCTN](https://www.isrctn.com/ISRCTN16806940).

## Tier 2b: advanced-disease trials, surgical

For people with motor fluctuations, typically 4 or more years from diagnosis. Both involve brain surgery with a sham-surgery control arm, immunosuppression or long follow-up, and MRI.

**exPDite-2, bemdaneprocel** (BlueRock/Bayer; NCT06944522; phase 3; recruiting). Stem-cell-derived dopamine neuron precursors implanted bilaterally, versus sham surgery, with about 12 months of immunosuppression and 5 years of follow-up. 102 planned. Eligibility: age 45 to 75; 4 to under 12 years since diagnosis; clear levodopa response; at least 2.5 hours of OFF time a day; excludes recurrent falls, prior DBS or brain surgery, prior infusion therapy, prior gene or cell therapy, active infection, malignancy within 5 years. **Where:** 43 sites. US: Houston, Chicago, Boston, New York, Los Angeles, Miami, Tampa, Jacksonville, Nashville, Durham, Richmond, Washington DC, Baltimore, Portland, Palo Alto, Orange, Scottsdale, Sun City, Aurora, Kansas City, Ann Arbor, Farmington Hills, Toledo, Louisville, Little Rock, Charleston, Providence, Buffalo, Burlington, Kirkland. Canada: Toronto, Montreal, Vancouver. Australia: Melbourne, Parkville, Clayton, Randwick, Southport, Woolloongabba (Brisbane). Full list in `data/sites.yaml`. Phase 1 in 12 people was open-label and showed no tumours and about one more hour of good ON time at 3 years; sham-controlled cell therapy has failed under blinding before. Source: [registry](https://clinicaltrials.gov/study/NCT06944522), corpus file 07.

**REGENERATE-PD, AAV2-GDNF** (AskBio; NCT06285643; phase 2; **active, not recruiting** as of October 2026). Gene therapy by MRI-guided neurosurgery versus control surgery. Age 45 to 75, 4 to 10 years from diagnosis, motor fluctuations, levodopa responsive. 46 sites in the US (including Columbus, Chicago, Houston, Boston, New York, Philadelphia, Miami, Phoenix, San Francisco), UK (Bristol, Cardiff), Germany and Poland. Primary completion August 2028. Listed so an agent does not chase it.

## Tier 3: subtype-restricted or closed, check status before pursuing

- **BEACON** (Denali; NCT06602193): BIIB122 in LRRK2 carriers only, ages 30 to 80 (no upper limit for homozygous carriers), 20 sites in the US, Spain, Germany and Israel. Active, not recruiting. Data first half of 2027.
- **PROPEL** (Lilly/Prevail; NCT04127578): PR001 gene therapy in GBA1 PD, ages 35 to 80, Hoehn and Yahr 3 to 4, single intracisternal injection with immunosuppression. Active, not recruiting. 15 sites in the US and Israel. Primary completion August 2031.
- **AMBITIOUS** (Milan; NCT05287503): ambroxol in GBA1 carriers with over 5 years of symptoms. Completed December 2024; results not yet located.
- **Agyany high-dose ambroxol** (Israel; NCT06193421): open-label, newly diagnosed GBA1 carriers. Registry status unknown since 2024.
- **TAME-PD** (Iowa; NCT07288450): terazosin. Withdrawn before enrolling.

## Recently closed or failed, so an agent does not chase them

LUMA (BIIB122, NCT05348785, failed May 2026; its companion phase 3 in LRRK2 carriers, LIGHTHOUSE, NCT05418673, was terminated in 2023). ACTIVATE (BIA 28-6156, GBA1 activator, failed June 2026). MOVES-PD (venglustat, failed). SPARK (cinpanemab, failed). ORCHESTRA (minzasolmin, failed December 2024). Exenatide-PD3 (failed February 2025; expression of concern June 2026). SPARX3 (exercise intensity, enrollment closed, results pending). NOPARK (nicotinamide riboside, results pending). Details and sources in corpus file 06.

## Outside the US, UK and Netherlands

Coverage here is thin and we know it. What the data does show: PARAISO has sites in Brazil (8, including São Paulo), Australia (7), Canada (3), Mexico (2), China, South Korea, Taiwan and ten European countries. exPDite-2 runs in Canada and Australia. BEACON and PROPEL have Israeli sites. Fox Insight is open online from anywhere. PD GENEration covers Chile, Mexico and Israel in person. For India and most of Asia, Africa and the rest of South America, the repo currently has nothing beyond these, and an agent should say so rather than guess. Contributions welcome via `CONTRIBUTING.md`.

## Questions an agent should have the person ask each coordinator

1. Is MRI required, and does the site scan MRI-conditional implanted devices?
2. Must the person be untreated, on stable medication, or either? For how long?
3. Is the Hoehn and Yahr stage assessed on or off medication?
4. Does enrollment here exclude other trials, and for how long?
5. What is the placebo (or sham) probability and for how long?
6. Is travel reimbursed, and can any visits be remote?
7. Is there an open-label extension where everyone receives the drug?
