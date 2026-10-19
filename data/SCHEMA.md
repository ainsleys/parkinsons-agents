# Data schema

Every record in `data/*.yaml` carries `verified` (ISO date the facts were last checked against a source) and `sources` (URLs). An agent should treat a record older than about 90 days as a lead, not a fact.

## tests.yaml

| Field | Type | Meaning |
|---|---|---|
| id | string | Stable slug |
| name | string | Common name, product name in parentheses if any |
| axis | enum | `motor_phenotype`, `genetic`, `synuclein`, `neurodegeneration`, `origin_site`, `prodromal` |
| result_type | string | What the result looks like (binary, categorical, panel) |
| route | string | How a person gets it |
| ordered_by | enum | `self`, `clinician`, `study` |
| invasiveness | enum | `none`, `sample`, `blood`, `biopsy`, `lumbar_puncture`, `imaging` |
| geography | list | Countries or regions where available |
| cost | string | Free text; include currency and date context |
| coverage | string | Insurance or health-system coverage notes |
| availability | enum | `clinical`, `research_only`, `consumer` |
| unlocks | list | What a result changes today |
| caveats | list | Known limits |
| verified | date | |
| sources | list of URLs | |

## programs.yaml

| Field | Type | Meaning |
|---|---|---|
| id, name | string | |
| sponsor | string | |
| type | enum | `genetic_testing`, `observational_cohort`, `online_registry`, `matching_service` |
| eligibility | list | Plain-language criteria |
| geography | list | |
| burden | string | Visits, procedures, time |
| gives_participant | list | What the person receives (results, imaging, counseling) |
| excludes_from_other_studies | bool | |
| registry_id | string | NCT number if any |
| status | string | |
| url | string | |
| verified, sources | | |

## trials.yaml

| Field | Type | Meaning |
|---|---|---|
| id, name, registry_id | string | |
| sponsor, phase | string | |
| intervention | string | |
| target_axis | string | Which subtype axis or population it is restricted to |
| status | enum | `recruiting`, `active_not_recruiting`, `completed`, `failed`, `planned` |
| geography | list | |
| sites | integer or null | |
| eligibility | object | Structured where known: `age_min`, `age_max`, `disease_duration_min_months`, `disease_duration_max_months`, `hoehn_yahr`, `medication_state`, `genetic_requirement`, `other` (list) |
| burden | object | `route`, `frequency`, `blinded_duration_weeks`, `open_label_extension` (bool), `placebo_probability`, `mri_required` (bool or `likely`/`unknown`) |
| primary_completion | date or string | |
| background | string | One or two sentences on the evidence behind it |
| verified, sources | | |

Unknown values are written as `null` or `unknown`, never omitted silently and never guessed.
