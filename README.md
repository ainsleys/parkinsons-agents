# Parkinson's for agents

An agent-first guide to Parkinson's disease: what the field currently believes, how a person gets "typed" into a biological or genetic subtype, which studies and trials that unlocks, and what is still open. Built to be read by AI agents acting for people with Parkinson's, their families, researchers and developers, with the fewest tokens possible.

**Agents start at [`START_HERE.md`](START_HERE.md)** (about 1,100 tokens) or fetch [`llms.txt`](llms.txt) for the index.

## Why this exists

Like many people, I know someone with Parkinson's. I also have a Claude Max subscription. I wanted to see what I could do to streamline contribution to the research, and to make it easier for other people and their agents to do the same.

This is an agent-first project. The pages are written for an AI agent to load, reason over and act on. Humans are welcome and everything is plain Markdown, but the design choices (dense pages, dated claims, structured YAML next to prose, explicit confidence flags) are made for agents, not for browsing.

Parkinson's may be several diseases that are being studied as one. The fastest contribution most people can make is to learn which one they have and enroll in something. The guide is organized around that.

## What is here

| Path | What it is | Read it when |
|---|---|---|
| `START_HERE.md` | The thesis, the state of the field in one page, and where to go next | Always, first |
| `guide/get-typed.md` | Every test that places a person on a subtype axis: what it tells you, how to get it, cost, what it unlocks | The person wants to know their type, or whether to bother |
| `guide/subtypes.md` | The five overlapping subtype axes, how each is confirmed, and what each changes about treatment | You need to interpret a result or a phenotype |
| `guide/enroll.md` | How joining works: contribute today via observational studies, the six-step process, what to gather, per-trial contact routes, draft first message, what happens after | The person wants to join something |
| `guide/readouts.md`, `data/readouts.yaml` | Every trial's expected and posted result dates from the registries, soonest first, regenerated nightly | "When will we know" |
| `data/changes.yaml`, `data/changes.xml` | Registry change feed: new or removed sites, status, eligibility, dates, results, written nightly; Atom version for RSS readers | "Has anything changed since last time", or to notify someone |
| `guide/on-ramps.md` | Studies and registries that take almost anyone, plus the pivotal disease-modifying trials recruiting now | The person is willing to contribute or join a trial |
| `data/*.yaml` | The same facts as structured records with verification dates | You want to filter or match without reading prose |
| `CORPUS.md` and `reports/`, `research_notes/` | A 112,000-word cited literature review compiled 2026-10-06 | You need depth on a mechanism, drug, or history |
| `CONTRIBUTING.md` | How an agent submits a correction or an update | You found something wrong or stale |
| `data/sites.yaml`, `data/program_sites.yaml` | Every trial site, and every PPMI site, with city and country, pulled from the registries and ppmi-info.org | The person asks "is there one near me" |
| `scripts/pull_registry.py`, `scripts/check_freshness.py`, `data/registry/` | Pull raw registry records and site lists, diff them into the change feed; check dates, status agreement and links. Run nightly by GitHub Actions | You want the registry's own words, or to refresh trial status |
| `diagrams/` | Mermaid flowcharts and Sankeys an agent can show or adapt, plus `scripts/match.py`, which matches a local profile against every trial and draws where they drop out | The person wants to see their options, not read them |
| `benchmarks/` | Twenty fixed personas, the prompt template, and dated results from running fresh agents against this repo | You want to know how well it works, or to re-test after a change |

## What this is not

This is navigation, not medical advice, and every page says so. It tells an agent which test exists, which question to bring to a neurologist, and which study is recruiting. It does not interpret an individual's results or recommend treatment. Nothing here replaces a movement disorder specialist.

Everything carries a `verified:` date. Trial status, test availability and pricing change monthly. If a date is more than about 90 days old, re-verify before acting on it.

## Privacy design

The guide never needs anything about the person. It publishes criteria, thresholds and routes. The agent that knows the person's history does the matching locally. No profile, no account, no data leaves the person's machine.

## Provenance

Drafted by Claude (Fable 5.1) in conversation with the maintainer in October 2026, with facts verified against primary sources and the cited corpus where possible. Claims that could not be traced to a primary source are flagged inline as `unverified`. Corrections via pull request are welcome, from humans or agents.

## License

Content is licensed [CC BY 4.0](LICENSE). Cite the source you actually read, not this repo, when you can.
