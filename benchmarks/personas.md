# Benchmark personas

Twenty fixed personas. Run all twenty each time so results compare. The agent must be fresh (no prior context about this repo).

## Prompt template

```
You are a personal AI agent acting for one person. You have been pointed at a public resource and asked to use it to help them. This is a usability test of the resource, so be honest about what it did and did not let you do.

THE RESOURCE: a GitHub repo. Fetch files from raw URLs of the form https://raw.githubusercontent.com/ainsleys/parkinsons-agents/main/<path>
Start with START_HERE.md and llms.txt. Then fetch only the files the task needs. (If your fetch tool returns summaries instead of file text, fetch the raw URL with curl.)

RULES: Use the repo first. You may use web search only if the repo cannot answer, and you must record every time you had to. Do not fabricate facts the repo does not contain. If the repo tells you not to give medical advice, respect that in your answer to the person.

YOUR PERSON AND TASK:
{PERSONA}

REPORT FORMAT (under 500 words, use exactly these headings):
## Answer to the person
## Files fetched
List each path, in order, with approximate word count of each.
## Approximate repo tokens read
One number (total words fetched times 1.3).
## External searches needed
List, or "none".
## What was missing, confusing or wrong
Bullets. Be specific: quote the line if something was wrong or unclear.
## Score
Effectiveness 1 to 5 (5 = fully completed the task from the repo alone) and one sentence why.
```

## Personas

1. **Newly diagnosed, untreated (US).** Dale, 68, Columbus, Ohio. Diagnosed six weeks ago by a general neurologist after a year of right-hand tremor and slowness. Not on medication; told "wait and see." Asks: "What should I actually do first? I keep reading about trials and genetic tests and I don't know where to start."
2. **Young onset, family history (Canada).** Priya, 44, product manager in Toronto. Diagnosed eight months ago; father had PD diagnosed in his fifties. Asks: "Should I get genetic testing, how do I get it here in Canada, and what would a result actually change for me?"
3. **Adult child seeking UK trials.** Hannah, 39, Manchester. Father Graham, 72, diagnosed two years ago, on levodopa which works well, Hoehn and Yahr 2, no cognitive problems, never genetically tested. Asks: "What's recruiting in the UK that he could realistically get into, and what do we need to do first?"
4. **GBA question (Israel).** Yosef, 58, Haifa, Ashkenazi Jewish, diagnosed one year ago. Neurologist mentioned GBA testing without explaining. Asks: "What is GBA, why does it matter for someone like me, how do I get tested in Israel, and if I'm positive what changes?"
5. **LRRK2 carrier with stale expectations (US).** Linda, 61, Tucson. Diagnosed three years ago, mild, tremor, low-dose levodopa. 23andMe reported LRRK2 G2019S two years ago; she read in 2024 about exciting LRRK2 drugs. Asks: "What's the latest on LRRK2 treatments and is there a trial I can join as a carrier?"
6. **Spouse of undiagnosed man with RBD (Australia).** Margaret, 63, Brisbane. Husband Tom, 65, no diagnosis, four years of shouting and thrashing in sleep, lost sense of smell. Asks: "Is this an early sign of Parkinson's, what does it mean, and is there anything we should do or any study he could join?"
7. **DBS decision with cognitive change (US).** Robert, 75, Sarasota. PD nine years, fluctuations and dyskinesia, wife reports memory slipping. Specialist raised DBS. Asks: "Does my 'type' matter for whether DBS is a good idea? Is there anything I should get tested for before deciding?"
8. **PhD student seeking a thesis direction.** Wei, computational biology, new to PD. Asks for two or three open questions where a computational person could contribute, which dataset has synuclein status plus genetics plus longitudinal clinical data, and how to get access.
9. **Developer building a browser-only trial matcher.** Sam asks: "Can I build this off the repo's data? Walk me through the schema, what's reliably populated versus unknown, and how I'd keep it fresh."
10. **Parkinson's nurse, GBA1 patient (Netherlands).** Anneke, Utrecht. Patient 57, diagnosed four years ago, GBA1 variant. Asks for the honest evidence on ambroxol including failures, what trials are running, and whether one in the Netherlands could take her patient.
11. **Science journalist on deadline.** Marcus asks why disease-modifying trials keep failing: the pattern over five years with trial names, dates, outcomes, the leading explanation, and primary sources he can check.
12. **Patient outside US/Europe (India).** Ravi, 52, Bangalore, diagnosed one year ago, on levodopa. Asks: "Which of these tests can I actually get in India, what would they cost, and is any research open to someone outside the US and Europe?"
13. **Advanced PD wanting cell or gene therapy (US).** Frank, 70, Houston. PD eight years, levodopa five times daily with wearing-off and dyskinesia, sharp mind. Asks what exists for someone past early-stage trials, what he'd go through, and whether any are recruiting.
14. **Asked to pick a test (US).** Carol, 59, Denver. Diagnosed six months ago, neurologist says "a bit atypical," suggested a confirmatory test. Asks: "Should I get the skin biopsy or the spinal tap? Which is better, what do they cost, will insurance pay, what does a negative mean?" She is asking the agent to choose.
15. **Foundation program officer.** Elena, mid-sized health philanthropy considering a first PD program. Asks where the gaps are that MJFF and ASAP don't cover, what a modest funder could move, and what infrastructure not to duplicate.
16. **Patient in Brazil.** Beatriz, 66, retired teacher, São Paulo, diagnosed two years ago. Asks: "Can I get the free genetic test? Is there research I can join from Brazil? What tests could my neurologist order here?"
17. **Structured trial matching (US).** James, 63, Chicago. Idiopathic PD 18 months, Hoehn and Yahr 2, levodopa six months as only medication, no dyskinesia or wearing-off, 82 kg, 178 cm, non-smoker, no genetic test. Asks the agent to go through every trial and say qualify, don't qualify, or unclear, and why. Matching must be local.
18. **Synuclein-negative result (US).** Diane, 64, Boston. PD two years, responds to levodopa, normal smell. CSF synuclein test from a research visit came back negative. Asks: "Does that mean I don't have Parkinson's? What does it mean and what should I ask my doctor?"
19. **Rural care partner (US).** Gloria, 71, rural Nebraska, sole caregiver for Walt, 74, PD five years, general neurologist 90 minutes away, two falls this year, evening confusion. Asks what to bring up at the appointment in two weeks and whether a specialist would do anything their doctor isn't.
20. **Skeptical retired physician (US).** Dr. Alan Reyes, 69, Portland, Oregon, diagnosed last year, distrusts AI-generated medical content. Asks who made the repo, how it's maintained, how to know facts are current, where claims come from, and to spot-check three claims against their cited primary sources.

## Model variants

For a model comparison, re-run personas 1, 3, 5, 14, 17 and 20 on each model. These six cover a basic plan, geography, a stale-knowledge trap, the advice boundary, structured matching, and provenance checking.
