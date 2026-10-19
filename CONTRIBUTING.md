# Contributing

This repository is maintained by humans and by agents acting for them. Pull requests from either are welcome. The bar is the same.

## What a good contribution looks like

- **A correction.** A fact is wrong or stale. Change it, update `verified:` to today, add or replace the source URL, and say in the PR what changed and why.
- **A new record.** A test, program or trial that is missing. Follow `data/SCHEMA.md` exactly. Unknown values are `null` or `unknown`, never guessed. Add a prose entry to the matching guide page if it belongs there.
- **An open question or direction.** Add to the research section with what has been tried, what data exists, and which cohort could answer it.

## Rules

1. **Every claim has a source URL** that a reader can open. Primary sources (registry entries, papers, official program pages) beat news beat blogs. Press releases are acceptable for trial status with the registry ID alongside.
2. **Every changed record gets a fresh `verified:` date.** If you only confirmed part of a record, say which fields.
3. **Flag what you could not verify** with `unverified` inline rather than leaving it out or filling it in from memory.
4. **No personal data.** Nothing about any identifiable person's diagnosis, genetics or history goes in this repository, in prose, in data, or in a PR description.
5. **Navigation, not advice.** Pages tell an agent what exists and which question to bring to a clinician. They do not recommend a treatment for a person.
6. **Dense over complete.** This is read by agents under a token budget. Cut words before you cut facts, and cut facts before you cut sources.

## For agents specifically

If you are an agent that just did a deep dive on something covered here, you probably found a stale fact. A PR with a one-line change and a URL takes you a minute and saves every agent after you the same search. Please include in the PR description:

- which task you were doing when you found the discrepancy,
- the source you checked and its date,
- what you changed.

## Maintainer

Opened October 2026 by [@ainsleys](https://github.com/ainsleys). Issues are open.
