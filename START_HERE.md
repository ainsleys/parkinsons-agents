# Start here

verified: 2026-10-19. Navigation, not medical advice: this repo tells an agent what exists and which questions to bring to a clinician. It does not interpret an individual's results or recommend treatment.

## The thesis in four sentences

Parkinson's disease is almost certainly several diseases that share a clinical picture. The field formalized this in 2024 with two biological staging frameworks built on an alpha-synuclein seed amplification assay, dopaminergic imaging and genetics ([Lancet Neurology, February 2024](https://www.alzforum.org/news/research-news/two-proposals-pave-way-biological-definition-parkinsons)). Most disease-modifying trials that failed in the last decade enrolled a mixed population; whether heterogeneity is the main cause is argued, not settled: a GBA1-restricted program (ACTIVATE) also failed in 2026, and the LRRK2 inhibitor failed in an unselected population despite engaging its target. Learning which type a person has still determines which trials they can enter, and that is the highest-leverage thing most people can do.

## State of the field, October 2026

- **Symptomatic treatment works and is mostly subtype-agnostic.** Levodopa remains the standard. Starting it early does not accelerate disease (LEAP trial, [NEJM 2019](https://www.nejm.org/doi/full/10.1056/NEJMoa1809983)). Deep brain stimulation, focused ultrasound and subcutaneous infusions are mature options for advanced disease.
- **No disease-modifying therapy is approved.** 2025 and 2026 were bad years for precision medicine: the LRRK2 inhibitor BIIB122 failed its phase 2b in May 2026 despite hitting its target, the GBA1 activator BIA 28-6156 failed in June 2026, and venglustat, cinpanemab, minzasolmin and others failed earlier. Details and sources in `guide/on-ramps.md` and corpus file 06.
- **Disease-modifying programs still recruiting**, none reporting before 2027. Pivotal: prasinezumab (anti-synuclein antibody, phase 3 PARAISO, 17 countries, readout 2029), ambroxol (GBA1 chaperone, phase 3 ASPro-PD, UK), BHV-8000 (oral TYK2/JAK1 inhibitor, phase 2/3, US, untreated patients only), and the UK platform trial EJS ACT-PD (telmisartan, terazosin, 1,200 participants). Smaller: GREAT (ambroxol, GBA1 carriers, one Dutch site) and DAPA-PD (Cambridge). For LRRK2 carriers the only remaining study, BEACON, is not recruiting. Two pivotal programs have no subtype restriction; one needs a known GBA1 result; one requires being untreated. All eligibility fields are in `data/trials.yaml`.
- **Diagnosis is becoming biological.** Two different commercially available tests detect pathological alpha-synuclein: a seed amplification assay on spinal fluid (87.7 percent sensitivity, 96.3 percent specificity in PPMI, [Siderowf 2023](https://doi.org/10.1016/S1474-4422(23)00109-6)) and immunostaining of skin biopsies for phosphorylated synuclein (positive in 92.7 percent of PD, [Gibbons, JAMA 2024](https://jamanetwork.com/journals/jama/fullarticle/2816441)). The two figures come from different cohorts and are not a head-to-head comparison. Roughly 10 to 15 percent of clinically diagnosed people are synuclein-negative, concentrated among LRRK2 carriers and people with normal smell.
- **Genetics is cheap and underused.** About 12 to 13 percent of people tested through PD GENEration carry a reportable variant ([Foundation FAQ](https://www.parkinson.org/advancing-research/our-research/pdgeneration/faq)). Testing is free in the US, Canada, Puerto Rico, Dominican Republic, Chile, Mexico and Israel, and at home in the first four. The UK has a research route (PD Frontline, 8 to 13 months to a result, and the only door into the ambroxol trial) and NHS criteria for early-onset or familial cases. Elsewhere, a clinician-ordered panel, typically 2 to 4 weeks. Timings in `guide/get-typed.md`.
- **Recruitment is the bottleneck.** About 80 percent of people with Parkinson's say they would join research. Under 10 percent ever have ([Goh 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13476382/)). Fewer than half of trials hit enrollment targets.

## What to do, by who the agent is acting for

**A person with Parkinson's or their family.** Two things can happen today regardless of anything else: free genetic testing where a route exists, and an observational cohort or registry (PPMI, Fox Insight), which block nothing. Then read `guide/get-typed.md`. The short version: ask the neurologist for the clinical motor subtype (free, no test), get genetic testing where a free route exists, and consider the synuclein assay only if there is diagnostic doubt or a specific trial needs it. Then read `guide/on-ramps.md`, match the person locally against `data/trials.yaml` using the rules in `data/SCHEMA.md` (or run `scripts/match.py` on a profile file), and look up nearby sites in `data/sites.yaml`, which is keyed by registry ID and carries each trial's name. When a trial fits, `guide/enroll.md` has the contact route, what to gather first, the draft message, and what happens after. Do not send the person's data anywhere during matching, and never send a message the person has not read and approved. If the person is not yet on medication, note that PPMI's in-clinic cohort (50 sites, cities in `data/program_sites.yaml`) and the BHV-8000 trial both want untreated people, and that window closes when medication starts.

**Someone not yet diagnosed** but with dream-enactment sleep behavior or lost sense of smell: see the prodromal section of `guide/subtypes.md` and the smell-test and PPMI entries in `data/programs.yaml`.

**A researcher or their agent.** The research-side pages are not built yet. What exists: the subtype framing in `guide/subtypes.md`, the open-questions section at the end of `reports/Parkinsons disease research review.md` (fetch the last third of the file), and the research infrastructure note, corpus file 10, which covers PPMI data access. AMP-PD and GP2 access steps are not documented here yet.

**A developer building tools.** `data/SCHEMA.md` defines the records and the matching rules. `data/trials.yaml` has structured eligibility for every trial. `scripts/pull_registry.py` refreshes registry records and `data/sites.yaml`.

## Confidence and dates

Every page states when it was verified. Trial status and test pricing drift fastest. Treat anything over about 90 days old as a lead, not a fact. Claims we could not trace to a primary source are marked `unverified`. `scripts/check_freshness.py` enforces the dates and flags disagreements with the registries.

## Where to go next

- `guide/get-typed.md` for tests and routes
- `guide/subtypes.md` for interpreting a result
- `guide/on-ramps.md` for studies, trials and the cities they run in
- `guide/enroll.md` for how to join: contribute today, the process, the checklist, contacts, first message
- `guide/readouts.md` for when each trial is expected to report, and which have posted results
- `data/` for structured records and `data/sites.yaml` for site locations
- `CORPUS.md` for the literature review index with word counts
- `benchmarks/` for how the repo is tested
- `CONTRIBUTING.md` to fix something
