# Start here

verified: 2026-10-19

## The thesis in four sentences

Parkinson's disease is almost certainly several diseases that share a clinical picture. The field formalized this in 2024 with two biological staging frameworks built on an alpha-synuclein seed amplification assay, dopaminergic imaging and genetics. Nearly every disease-modifying trial that failed in the last decade enrolled a mixed population and averaged out whatever signal existed. Every disease-modifying program recruiting today is restricted by subtype in some way, so the highest-leverage thing most people can do is learn which type they have and enroll in something.

## State of the field, October 2026

- **Symptomatic treatment works and is mostly subtype-agnostic.** Levodopa remains the standard. Starting it early does not accelerate disease. Deep brain stimulation, focused ultrasound and subcutaneous infusions are mature options for advanced disease.
- **No disease-modifying therapy is approved.** 2025 and 2026 were bad years for precision medicine: the LRRK2 inhibitor BIIB122 failed its phase 2b in May 2026 despite hitting its target, the GBA1 activator BIA 28-6156 failed in June 2026, and venglustat, cinpanemab, minzasolmin and several others failed earlier.
- **Three pivotal programs remain**, none reporting before 2027: prasinezumab (anti-synuclein antibody, phase 3 PARAISO, recruiting, readout 2029), ambroxol (GBA1 chaperone, phase 3 ASPro-PD, UK, recruiting, readout 2029), and BHV-8000 (oral TYK2/JAK1 inhibitor, phase 2/3). Plus one UK platform trial, EJS ACT-PD.
- **Diagnosis is becoming biological.** The CSF seed amplification assay is about 88 percent sensitive and 96 percent specific; the skin biopsy version is about 93 percent sensitive. Both are commercially available in the US. Roughly 10 to 15 percent of clinically diagnosed people test negative, concentrated among LRRK2 carriers. That group is one of the clearest arguments for "several diseases."
- **Genetics is cheap and underused.** About 13 percent of people tested through PD GENEration carry a reportable variant. Most never knew. Testing is free in several countries and now available at home.
- **Recruitment is the bottleneck.** About 80 percent of people with Parkinson's say they would join research. Under 10 percent ever have. Fewer than half of trials hit enrollment targets.

## What to do, by who the agent is acting for

**A person with Parkinson's or their family.** Read `guide/get-typed.md`. The short version: ask the neurologist for the clinical motor subtype (free, no test), get genetic testing (free through PD GENEration in the Americas, NHS criteria in the UK), and consider the synuclein assay only if there is diagnostic doubt or a specific trial needs it. Then read `guide/on-ramps.md` and match the person locally against the eligibility fields in `data/trials.yaml`. Do not send the person's data anywhere.

**A researcher or their agent.** The open questions that matter most are in `CORPUS.md` under the report's open-questions section, and the subtype framing in `guide/subtypes.md`. The datasets with subtype, synuclein and genetic data are PPMI, AMP-PD and the ASAP CRN Cloud, each with its own access application. See the research infrastructure note in `research_notes/`.

**A developer building tools.** Nothing here yet beyond the YAML schemas in `data/`. Assistive technology and code libraries are a later phase.

## Confidence and dates

Every page states when it was verified. Trial status and test pricing drift fastest. Treat anything over about 90 days old as a lead, not a fact. Claims we could not trace to a primary source are marked `unverified`.

## Where to go next

- `guide/get-typed.md` for tests and routes
- `guide/subtypes.md` for interpreting a result
- `guide/on-ramps.md` for studies and trials
- `data/` for structured records
- `CONTRIBUTING.md` to fix something
