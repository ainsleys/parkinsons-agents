# Benchmarks

A usability benchmark for this repository: can a fresh agent, pointed only at the public repo, help a realistic person? Each run is one persona, one model, one task. The agent reports what it fetched, how many repo tokens it read, whether it needed the open web, what was missing or wrong, and a 1 to 5 effectiveness score.

## How to run

1. Take the prompt template and a persona from `personas.md`.
2. Launch a fresh agent (no prior context) with WebFetch and WebSearch available. Model is a variable; record it.
3. Collect the report in the fixed format. Add a row to a dated TSV in `results/` with: persona, model, score, approximate repo tokens read, external searches needed, key gaps.
4. Run the same 20 personas each time so results compare. Add new personas only alongside the fixed set.

Scoring is the agent's own 1 to 5 judgment, so it is noisy. The useful signals are the mean across the fixed set, the token cost, how many external searches were needed, and the specific defects reported.

## Results

| Date | Runs | Fable mean | Opus mean | Sonnet mean | Haiku mean | Fable median tokens | Notes |
|---|---|---|---|---|---|---|---|
| 2026-10-19 | 35 | 3.45 (n=20) | 3.83 (n=6) | 3.67 (n=6) | 3.67 (n=3) | ~20,000 | Baseline. Scores identical across models on shared tasks. Lowest: India (2), Brazil, Israel, Australia (3). |

Per-run detail: `results/2026-10-19-baseline.tsv`.

## Baseline findings, ranked by impact

1. Factual errors in START_HERE.md (skin biopsy mislabeled as a seed amplification assay; "three pivotal programs"; "every program restricted by subtype"; bad pointer to open questions; stale developer line).
2. No site locations, so no "near me" answer was possible.
3. Matching semantics undefined: stage on vs off medication, "stable" treatment, onset vs diagnosis, free-text fields.
4. Geography bias: routes exist only for US, UK, Netherlands.
5. Staleness logic doesn't fire: old registry records stamped verified today.
6. Prose and data disagree: trials on the on-ramps page missing from trials.yaml; no cost field in programs.yaml.
7. Missing pages for whole personas: care partners, advanced disease, undiagnosed, pre-surgery, researchers.
8. Citation hygiene: uncited start-page numbers, internal citations, one dead link.
9. Navigation: llms.txt doesn't list all files; no word counts.
10. Disclaimer only in two files (all models honored it anyway).

What held: every model produced a correct, hedged plan for the core path; all four models declined to choose a test when asked to; nine cited claims checked against primary sources all held (one rounding difference).
