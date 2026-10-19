# Enroll

verified: 2026-10-19. Navigation, not medical advice. This page explains how joining a study works, what to have ready, and how to make first contact. Which study, and whether to join one at all, is a decision for the person with their clinician.

## Contribute today, before any trial

Three things take almost anyone with a diagnosis, cost nothing, block nothing, and feed the research that every trial depends on. An agent should offer these first and separately from drug trials.

| Program | Who | How | What you get back |
|---|---|---|---|
| **PD GENEration** | Any confirmed PD diagnosis, 18+, in the US, Canada, Puerto Rico, Dominican Republic (at home) or Chile, Mexico, Israel (in person) | Online consent, blood kit by mail, counseling call. genetics@parkinson.org | Seven-gene result with counseling; the status several trials require |
| **PPMI online (myPPMI)** | Anyone 18+ in the US, with or without PD | Sign up at michaeljfox.org/ppmi, questionnaires at home | Nothing clinical; data to the field's reference cohort |
| **Fox Insight** | People with PD and family members, any country | foxinsight.michaeljfox.org, questionnaires every 90 days | Same |
| **PPMI in clinic** | Recently diagnosed and not yet on medication, people with REM sleep behavior disorder, known genetic carriers; 50 sites in 12 countries, listed with cities in `data/program_sites.yaml` | US and Canada: mysmelltest.org/site, PPMI's five-minute online intake (two questions, then a mailed smell test and routing to the nearest site), or 877-525-PPMI; elsewhere, coordinator contacts in `data/programs.yaml` | Free synuclein assay, DaTscan and MRI; coordinators who know local trials |
| **PD Frontline** (UK) | Formal diagnosis, UK resident, age 18 to 90 | Saliva and blood kits by post via Parkinson's UK; allow 7 to 9 months for results | LRRK2 and GBA1 status; recontact for UK trials including ASPro-PD |

Joining these does not exclude you from any drug trial later. The in-clinic PPMI arm for untreated people is a window that closes once medication starts.

## How enrollment in a drug trial works

1. **Contact.** You, or someone acting for you with your consent, reach the sponsor's inquiry line or the trial team. Per-trial routes are in `data/trials.yaml` under `contact`, with every published registry contact in `data/contacts.yaml`. Many sponsors route all inquiries centrally and connect you to the nearest site; Roche asks for its inquiry form, Biohaven and BlueRock give one line for all sites. UK NHS trials are usually entered by referral from your neurologist or Parkinson's nurse, so ask them first and email the trial team in parallel.
2. **Pre-screening call.** A coordinator asks the key criteria: age, when diagnosed, medications, implanted devices, prior surgery, other trials. Ten to twenty minutes. The checklist below is what they ask.
3. **Records.** The site asks for your most recent neurologist letter and medication list to confirm the diagnosis.
4. **Informed consent visit.** The study is explained in full: visits, procedures, placebo odds, risks, what happens to your data. You sign a consent form. Signing permits screening; it is not enrollment, and you can withdraw at any point.
5. **Screening.** Exam on and off medication, rating scales, blood work, often MRI, sometimes lumbar puncture or genetic testing. **This is where most people who do not get in are turned away**, usually on something the registry never listed. The matcher in this repo uses key criteria only; a match means "worth a call," not "accepted."
6. **Randomization.** You are assigned to an arm, and the visit schedule begins.

Timing from first contact to randomization is typically a few weeks to two or three months, mostly waiting for a screening slot and results.

## Gather before you call

Structured version in `data/checklist.yaml`, aligned with the profile file `scripts/match.py` reads. Split by who can supply it, because several items need a clinic visit and a person should not be sent chasing scores alone.

**Ask your neurologist for:**
- Hoehn and Yahr stage **off** medication and on medication. Most people know only the on-medication stage. PARAISO uses off; ASPro-PD uses on.
- Whether you have dyskinesia or wearing-off (MDS-UPDRS Part IV). PARAISO requires none; the surgical trials require fluctuations.
- A cognitive screen score (MoCA) if one exists.
- Your clinical motor subtype.
- The most recent clinic letter and a medication list, for the site.
- For UK trials: a referral, or at least a note that you are suitable to be contacted.

**You can gather yourself:**
- Diagnosis date and who made it; first symptom date (BHV-8000 counts from onset).
- Medications, doses, and how long the regimen has been stable.
- Genetic test status and result, if any. If none and a trial needs it, the routes and how long each takes are in `get-typed.md`: about 2 months free in the Americas, 7 to 9 months free in the UK, 2 to 4 weeks for a paid clinical panel.
- Implanted devices, with the model and MRI conditions from your cardiologist in writing.
- Prior brain surgery; other trials in the last 12 months; major conditions; recent cancer or infections.
- Weight and height; smoking.
- Hours per day OFF, from a diary, if you have fluctuations.
- Which cities you can reach, how often, and whether you need travel reimbursed.

## What each recruiting trial will ask first

| Trial | First questions | Route |
|---|---|---|
| PARAISO | Age 50 to 85; 3 to 36 months since diagnosis; on levodopa alone; any dyskinesia or wearing-off; off-medication stage; weight; MRI OK | Roche inquiry form or 888-662-6728; study BN44715 |
| ASPro-PD (UK) | Age 35 to 75; within 7 years; on stable treatment 3 months; **GBA1 result in hand** (PD Frontline takes 7 to 9 months; ask the team about testing at screening, or a paid panel takes about a month); not a LRRK2 G2019S carrier; MoCA; prior DBS; ambroxol or GLP-1 in past year | cctu.aspro-pd@ucl.ac.uk, 020 3108 4908, or referral |
| EJS ACT-PD (UK) | Diagnosed at 30 or older; on levodopa or agonist 2 months; MoCA; not a known PRKN, PINK1 or PARK7 carrier; other trials in 6 months; blood pressure (terazosin arm) | mrcctu.ejsactpd@ucl.ac.uk, or referral to a listed NHS site |
| BHV-8000 (US) | Age 40 to 80; onset within 2 years; **not on any PD medication**; smoker; infections | clinicaltrials@biohavenpharma.com, 203-404-0410 |
| exPDite-2 | Age 45 to 75; 4 to under 12 years since diagnosis; hours OFF per day; levodopa response; falls; prior surgery; immunosuppression concerns | clinicaltrials@bluerocktx.com, 1-877-380-3967 |
| GREAT (NL) | GBA1 variant; under 10 years; MRI compatible; DBS | o.siemeling@umcg.nl |
| DAPA-PD (UK, Cambridge) | Age 50 to 80; under 5 years; stage 2 or below; no known PD gene variant; recent CRP; immune drugs | cuh.dapa-pd.trial@nhs.net, +44 1223 767069 |

## Making first contact

An agent may draft the message. The person reviews it and sends it from their own account, or the agent sends only after the person has read that exact message and said yes to sending it. Do not contact more than two or three trials at once; sites talk to each other and a person can only screen for one at a time. If the person has already contacted a trial through another channel, say so in the message.

Include the facts that decide a pre-screen, because a message without them just produces a call that repeats them. Leave out the full history, genetic results (unless the trial requires status before screening) and anything not asked for. Nothing in a first message should be copied from a registry's free-text fields.

**Email template, drug trial**

> Subject: Inquiry about [trial name] ([registry ID]), prospective participant in [city]
>
> Hello,
>
> I am asking about eligibility for [trial name]. I was diagnosed with Parkinson's disease in [month year] by a [neurologist / movement disorder specialist] and [am not yet taking Parkinson's medication / have been on a stable dose of levodopa since month year]. I am [age], live in [city], and could attend [nearest listed site]. [I have / have not] had genetic testing[; result: GBA1 status known / not known, if the trial requires it]. [I have no implanted devices / I have a pacemaker, model X, labelled MRI-conditional.]
>
> Could you tell me whether I appear to meet the key criteria and, if so, arrange a pre-screening call? My neurologist is aware and can provide records. I consent to being contacted at this address or by phone at [number].
>
> Thank you,
> [name]

**Phone script, drug trial.** "I'm calling about [trial], study [ID]. I was diagnosed in [year], I'm [age], I'm [on / not on] medication, and I'm in [city]. Could I do a pre-screening call?" Then answer from the checklist. If speaking is hard, say so and ask for the questions by email; sites do this routinely. A carer can make the call with the person's permission; say that at the start.

**Observational studies** need none of this. PD GENEration, myPPMI and Fox Insight are online consent forms. For PPMI in clinic, email the nearest site that you are recently diagnosed and untreated, or a known carrier, and ask to be screened.

## After you send

- Expect a reply within one to two weeks from sponsor lines, longer from academic teams. If nothing after two weeks, phone.
- "Not eligible" at pre-screen is common and usually about a window (time since diagnosis, medication) rather than about you. Ask what would change it and whether another study at the site fits.
- Once you contact a site, it holds your health information under its own privacy rules and the consent you sign. Ask what is kept if you do not enroll.
- You can withdraw at any stage, including after randomization, without giving a reason.
- Tell your neurologist which trials you have contacted. Enrollment in one usually blocks others for its duration, and some trials require a stable medication plan the neurologist controls.

## Country notes

- **US:** self-referral is normal; sponsor lines route to sites.
- **UK:** trials recruit through NHS clinics. Ask your neurologist or Parkinson's nurse for a referral, and email the trial team in parallel. Parkinson's UK's Take Part hub lists studies. Genetic status for ASPro-PD comes from PD Frontline or the trial team.
- **Netherlands:** GREAT is a single academic site; email the coordinator directly.
- **Elsewhere:** PARAISO runs in 17 countries and routes through Roche's form; exPDite-2 has Canadian and Australian sites via the BlueRock line. For anything else the repo has no route yet.
