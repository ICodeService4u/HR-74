# T1 - Approved Hiring and Staffed Role Views

**Status: retired 09/19/2026 on its first run set.** Five Gemini 3.8 Flash runs meant 96.5% against
a registered 38% and a retirement line of 60%; nine of nine runs reconciled the population. The
record, the run set and the two verifier fixes the set bought are kept as the measurement, and
`06_failure_analysis.md` says why the lever did not hold. The first HR 74 task package, in the
HR 79 T1 shape: one builder generates the two golden pages, the 35-row rubric, the import, the
show-your-work and the 35 verifier files from the world's bytes; a battery of 39 snapshots proves
the verifiers grade before any of them is imported; negative controls plant a defect in every
guard and confirm the red. `02_task_metadata.md` carries the record, `06_failure_analysis.md`
the predictions with their date, `qc/README.md` the harness result.

| Event | Date | Result |
|---|---|---|
| Built | 09/19/2026 | 35 verifiers, 113 points, 1 gate, EA 64.6%; one 1.4 input on the Filesystem target; two golden pages |
| Verifier battery | 09/19/2026 | **1295 of 1295 verdicts correct** across 37 scenarios and 35 rows at the build, two false-pass defects found and closed on the way; **1365 of 1365 across 39** after the run set's two false-zero fixes |
| Negative controls | 09/19/2026 | see the table below, from `build/negative_controls.py` |
| Prompt round 1 | 09/19/2026 | two major findings, archived to `qc/findings/` and answered in `qc/README.md` |
| Run set | 09/19/2026 | five Gemini 3.8 Flash, three GPT Sol 5.6 and one Opus 4.8: Gemini mean **96.5%**, GPT 89.1%, Opus 85.8%; scored by `qc/score_run_set.py` against the registered paths in `06_failure_analysis.md` |
| Retired | 09/19/2026 | on the decision rule registered before the runs: over 60% and the population has healed |
| Task round 1 | not run | the package retired at the prompt half |

## The ask, in one paragraph

The recruiting lead asks the People Operations Analyst for two Wiki.js pages for the 09/10/2026
operating review: every open requisition with its Board approval and hiring status, and every
current employee by department and role with the open requisition that carries the same title.
He carries 57 people, 8 open requisitions and 8 roles at $868,000.00 from his own wiki pages. The
world says 52 people, 5 Board-approved roles at $612,000.00, three requisitions the Board did not
authorize with a signed offer on one of them, three ended employees BambooHR still calls Active,
four contractors it calls employees, and two working hires it never loaded. The prompt is one
sentence; the memo carries the tables, the vocabulary and the fence.

## What the run has to get wrong to fail

**The population.** BambooHR says 57 and the requester says 57. The truth is a comparison the
request names in one sentence and nothing prompts: the August org chart and the master roster
carry 52, the crosswalk names the five reconciling items, the archive dates the three endings.
This is the gate and 44 of the 113 points.

**The Board reading of REQ-2026-036.** The ATS export says Backfill and the Board authorised a
backfill. Page 2 of the plan says the backfill is CSM I and the requisition is CSM II, and the
plan requires a line-for-line trace. Nine points.

The registered modal failing path takes both wrong and everything else right, and scores 37 of
113, 32.7%. The registered Gemini mean is 38%, and the decision rule is in the record.

## What ships

| File | Purpose |
|---|---|
| `00_task_input_operating_review_request.pdf` | The request memo, the one 1.4 input, Filesystem target, md5 in `02_task_metadata.md` |
| `01_prompt.md` | The prompt verbatim, its shape reasoning, the cell families, the Spec table, the withheld list |
| `02_task_metadata.md` | Identity, graded values and sources, the two pages, required files and the selection block, fences, rival readings, reviewer decision rules, the asks table, the rubric, the plan, the time estimate, the predictions, the platform state, the open items |
| `03_show_your_work.xlsx` | Sources, Verifiers, Row assembly |
| `04_golden_output_Approved_Hiring_View.md`, `04_golden_output_Staffed_Role_View.md` | The two pages as they should be published, generated from the same facts as the rubric |
| `05_rubric_import.xlsx` | The file that registers, once the snapshot ids are read off an export |
| `06_failure_analysis.md` | The seven registered paths, the mean, the decision rule, what to read in a trajectory |
| `08_section_1_3_step_plan.md` | The fourteen checkpoints and the dependency chain |
| `09_rubric_import.md` | The import's mappings, the verifier form fields, the Additional Notes block, the harness record |
| `build/build_package_artifacts.py` | The single source of truth: facts, pages, rubric, checks, outputs, verifier generation |
| `build/build_task_input.py`, `build/task_input_source.md` | The memo's source and its guarded renderer |
| `build/verifier_engine.py` | The shared verifier body every row file is stamped from |
| `build/negative_controls.py` | Every guard made to fail once |
| `build/rubric_preview.csv` | The package's own record of the rubric |
| `qc/README.md`, `qc/findings/` | The task AutoQC register and the verbatim archive |
| `qc/ctx.py`, `qc/run_battery.py` | The verifier skill's stand-in `ctx` and battery runner, carried from HR 79 |
| `qc/scenarios.py`, `qc/verifier_harness.py` | The 39-snapshot battery and the runner over all rows |
| `qc/score_run_set.py` | Scores an archived run set under `qc/findings/` against the verifier files, which is where the numbers in `06_failure_analysis.md` come from |
| `qc/verifiers/` | The 35 generated row files, each a standalone `check(ctx)` |

## Running it

From the package root:

```
python3 build/build_task_input.py          # renders the memo under the leak guards
python3 build/build_package_artifacts.py   # world checks, pages, rubric, import, verifiers
python3 build/build_package_artifacts.py --docs    # also holds 01, 02, README and qc to the build
python3 build/build_package_artifacts.py --table   # prints the rubric as a markdown table
python3 qc/verifier_harness.py             # every verifier against every scenario
python3 build/negative_controls.py         # every guard made to fail once
```

`--docs` is what catches a document drifting from the artifact it describes, and it is the one to
run before any commit that touches the package. From the repo root, `python3
world/checks/world_manifest.py` and `python3 tasks/check_selection_blocks.py` hold the world and
the selection block.

## The negative controls

The table is `build/negative_controls.py`'s own output on 09/19/2026. Every control plants one
defect, runs the guard, and reverts; a control that comes back green is a guard the package does
not have.

| Control | Result |
|---|---|
| memo: the current employee count | RED |
| memo: the Board's role count | RED |
| memo: the backfill level | RED |
| memo: a record called stale | RED |
| memo: the word contractor | RED |
| memo: one of the five names | RED |
| memo: the workbook called superseded | RED |
| memo: a word for checking | RED |
| memo: the shape of the answer | RED |
| memo: the premise dropped | RED |
| memo: a Board reading asserted | RED |
| memo: the seat | RED |
| memo: an unlicensed date | RED |
| names: the upload name the record publishes | RED |
| world: the population | RED |
| world: a stale record read as current | RED |
| world: the Board reading of 036 | RED |
| world: the backfill line moved to CSM II | RED |
| world: Okonkwo's start date | RED |
| world: the department counts | RED |
| golden: a contractor on the staffed page | RED |
| golden: an ISO date | RED |
| rubric: weight band | RED |
| rubric: the gate demoted off weight 10 | RED |
| rubric: atomicity | RED |
| rubric: a row not opening on States | RED |
| register: punctuation | RED |
| register: a spelled month | RED |
| register: grading vocabulary | RED |
| register: self-reference | RED |
| register: two rows carrying one explanation verbatim | RED |
| asks: a row hung on the request's scope fence | RED |
| asks: a form the request sets left ungraded | RED |
| asks: the request reworded out from under a row | RED |
| asks: a row with no clause to hang on | RED |
| tools: a catalogue with no wiki page writer | RED |
| tools: a catalogue that is a stub | RED |
| import: the guide's spelling of the App DB type | RED |
| import: a form row losing its Style / formatting tag | RED |
| import: a grading target on an App DB row | RED |
| import: a reference artifact as a bare path | RED |
| import: a world reference dropped | RED |
| verifier: a substring match on the status cell | RED |
| verifier: the key matched as a substring | RED |
| verifier: a key with an identifier beside it rejected | RED |
| verifier: the source-date hint demanding a word the memo does not use | RED |
| verifier: page history read as pages | RED |
| verifier: the published flag assumed | RED |
| verifier: a count that tallies substrings | RED |
| verifier: absence passing without the item named | RED |
| verifier: a duplicate page passing on its better copy | RED |
| battery: a scenario expecting the wrong verdict | RED |
| docs: the prompt blockquote | RED |
| docs: a stale explanation in the record's rubric table | RED |
| docs: a non-ASCII character in a package document | RED |

**55 of 55 controls went red**, the last run on 09/19/2026 after the run set's three additions.

## What the run set closed, and what is still not here

- The run set, the step counts, the snapshot ids and the tool catalogue are all measured now:
  `06_failure_analysis.md`, `qc/findings/run_set_09-19-2026/runs.json`, the builder's `SNAP` and
  `TASK_SNAP`, and `tasks/APP_TOOL_SURFACE.md`. `02_task_metadata.md` records how each closed.
- A platform grading run on this rubric: none happened, so the pages table's shape in a grading
  snapshot is still read off the harness and not off a `details` string.
- A Model Final Output row: nothing the judge can open exists, because the deliverable is two
  wiki pages.
- A lock-set note: this is the first package in the world. The fences in `02_task_metadata.md`
  name the surfaces a later package is likely to grade, so the second package can take them.
