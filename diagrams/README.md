# Diagrams

Visuals an agent can show the person it is helping, or adapt for them. Everything here is Mermaid source. Mermaid renders natively on GitHub, in most chat clients and notebooks, and can be converted to SVG or PNG with the Mermaid CLI (`mmdc -i file.mmd -o file.svg`) for anywhere it does not. Each file begins with a comment stating its source data and verified date; keep that comment in anything you derive.

Navigation, not medical advice. These diagrams show routes and populations, not recommendations for an individual.

## Ready to render

| File | What it shows | Use when |
|---|---|---|
| `pathway.mmd` | Flowchart from diagnosis to enrolled: subtype, genetic test route by country, the untreated window, and which trial tier a person's situation points to | The person asks "where do I start" or "what are my options" |
| `recruitment-gap.mmd` | Sankey of 1,000 people with Parkinson's: willing to join research vs ever enrolled | Explaining why participation matters, or in a pitch to funders |
| `gene-test-outcomes.mmd` | Sankey of 1,000 people taking the seven-gene panel: who gets a reportable result and in which gene | The person is deciding whether to get tested |
| `synuclein-test-paths.mmd` | Flowchart of the two synuclein tests and what a positive or negative means | The person is deciding about, or has received, a synuclein test |

## Generated per person

`scripts/match.py profile.yaml` reads a profile the agent writes locally, applies the matching rules in `data/SCHEMA.md` to every trial in `data/trials.yaml`, and prints:

- a verdict table: qualifies, unclear (with the missing field named), or does not qualify (with the first failing criterion);
- a Mermaid Sankey showing where each trial drops out, so the person sees why 14 trials became one or two;
- the nearest sites by country from `data/sites.yaml`.

The profile never leaves the machine. Example profile and output are in `example-profile.yaml` and `example-match.mmd`.

## Specs for diagrams not yet built

If you build one of these, keep the data source and verified date in the file.

- **Trial funnel for one trial.** Screened, eligible, consented, randomized, completed. We do not yet hold these numbers for any trial; the registry gives only enrollment targets. A per-trial funnel needs sponsor data or a publication.
- **Time windows.** A horizontal timeline from diagnosis with each trial's eligibility window as a bar (PARAISO 3 to 36 months, BHV-8000 0 to 24 months from onset, ASPro-PD 0 to 84 months, surgical trials 48 to 120 or 143 months). Mermaid `gantt` can approximate it; a proper version is an SVG.
- **Site map.** `data/sites.yaml` has city and country for every site but no coordinates. A map needs a geocoding pass; keep it offline so no person's location is sent anywhere.

## Rules for derived diagrams

1. State the source file and its `verified` date in a comment at the top.
2. Numbers in a diagram must come from a record in `data/` or a cited line in a guide page. Do not estimate to fill a box.
3. If the person's own data is in the diagram, it stays local. Do not upload a rendered personal diagram to a third-party renderer.
4. Prefer a flowchart for routes and a Sankey for populations. A Sankey of one person's path is a flowchart.
