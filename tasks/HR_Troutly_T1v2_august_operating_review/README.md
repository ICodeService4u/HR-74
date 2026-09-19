# T1 v2 - Approved Hiring and Staffed Role Views

**Status: built 09/19/2026, at the prompt half, no v2 run yet.** The second version of the first
HR 74 package, built from T1's measured run set of the same day. T1 read nine of nine runs healing
the population and a Gemini mean of 96.5%, and its traces showed every run following the sources
the memo named. v2 strips the memo of every pointer, figure and reconciliation, defines the two
terms the prompt AutoQC round called pinned, and rescopes the rubric so the population carries
67% of the points and the fields a run prints on any path carry 8%. T1 stays in the
repository as the measurement.

| Event | Date | Result |
|---|---|---|
| Built | 09/19/2026 | 24 verifiers, 83 points, 1 gate, EA 75.9%; one 1.4 input on the Filesystem target; two golden pages |
| Verifier battery | 09/19/2026 | **864 of 864 verdicts correct** across 36 scenarios and 24 rows, the three registered failing paths among them |
| Negative controls | 09/19/2026 | see the table below, from `build/negative_controls.py` |
| Run set | owed | five Gemini 3.8 Flash and three GPT Sol 5.6, archived and scored by `qc/score_run_set.py` against the registered paths |
| Prompt round 1 | owed | archived verbatim to `qc/findings/` when it lands |

## The ask, in one paragraph

The recruiting lead asks the People Operations Analyst for two Wiki.js pages for the 09/10/2026
operating review: every requisition open in Greenhouse at 08/31/2026 with its Board approval and
hiring status, and every current employee by department and role with the open requisition that
carries the same title. The memo defines a current employee as anyone employed by Troutly on
08/31/2026 and defines the three status values. It names no record. BambooHR carries 57 active
rows and 52 people are employed; the recruiting lead's own wiki page says the Board approved
eight roles at $868,000.00 and the Board's plan says five at $612,000.00.

## What v2 changes from T1

| T1's memo carried | v2 |
|---|---|
| "read the 06/20/2026 Board-approved hiring plan and the Board minutes of that meeting, and no other record" | gone; the run finds what the Board approved among a wiki page, a workbook, a plan and minutes |
| "count people the way the People Metrics page describes" | "A current employee is anyone employed by Troutly on 08/31/2026" |
| "managers and reporting lines come from the August org chart" | gone |
| the lookups paragraph naming three wiki pages | gone |
| "a second table for recruiting records with no matching BambooHR employee record" | gone, with its four rows |
| "the reconciling items between that count and the BambooHR active record count" | gone, with the 57 row and the naming half of the absence rows |
| the requester's 57 people, 8 open requisitions and 8 roles at $868,000.00 | gone |
| the source date column | gone, with its two rows |
| "Hiring status reads Open, Offer accepted or Filled" | kept, with what each value means |

**T1's nine runs, graded by the v2 rubric.** They carried the memo's pointers, so they are not a
measurement of v2's lever; they show that the v2 verifiers pass correct work in the forms real
runs use. Gemini mean 97.3%, low 94.0%, high 100.0%; run by run in `06_failure_analysis.md`.

The rubric goes from 35 rows and 113 points to 24 rows and 83 points. The registered failing paths
score 27 of 83, 32.5% and 31 of 83, 37.3%; the free base is 7 of 83.

## What ships

| File | Purpose |
|---|---|
| `00_task_input_operating_review_request.pdf` | The 1.4 input, Filesystem target, uploads as `operating_review_request.pdf` |
| `01_prompt.md` | The prompt verbatim, what v2 changes and why, the cell families, the Spec table, the withheld list |
| `02_task_metadata.md` | Identity, the weights and the registered paths, graded values, the selection block, fences, rival readings, reviewer decision rules, the asks table, the rubric, the checkpoints, the time estimate, the predictions, the platform state, the open items |
| `03_show_your_work.xlsx` | Sources, Verifiers, Row assembly |
| `04_golden_output_Approved_Hiring_View.md`, `04_golden_output_Staffed_Role_View.md` | The deliverable |
| `05_rubric_import.xlsx` / `09_rubric_import.md` | The file that registers, and its mappings |
| `06_failure_analysis.md` | The predictions, dated, with the honest note |
| `08_section_1_3_step_plan.md` | The checkpoint table |
| `build/build_task_input.py`, `build/task_input_source.md` | The memo source and its renderer with the leak guards |
| `build/build_package_artifacts.py`, `build/rubric_preview.csv` | The one builder and its CSV form of the rubric |
| `build/verifier_engine.py` | The engine every verifier file stamps its spec into |
| `build/negative_controls.py` | Every guard made to fail once |
| `qc/README.md`, `qc/findings/` | The AutoQC register and the verbatim archive |
| `qc/ctx.py`, `qc/run_battery.py` | The verifier skill's stand-in `ctx` and battery runner |
| `qc/scenarios.py`, `qc/verifier_harness.py` | The 36-snapshot battery and the runner over all rows |
| `qc/score_run_set.py` | Scores an archived run set under `qc/findings/` against the verifier files |
| `qc/verifiers/` | The 24 generated row files |

## Running the checks

From the package root:

```
python3 build/build_task_input.py
python3 build/build_package_artifacts.py --docs
python3 qc/verifier_harness.py             # every verifier against every scenario
python3 build/negative_controls.py         # every guard made to fail once
```

## Negative controls

| Control | Result |
|---|---|
| memo: the current employee count | RED |
| memo: the Board's role count | RED |
| memo: the backfill level | RED |
| memo: a record called stale | RED |
| memo: the word contractor | RED |
| memo: one of the six names | RED |
| memo: a source record named | RED |
| memo: a lookup page named | RED |
| memo: the reconciliation named | RED |
| memo: the workbook called superseded | RED |
| memo: a word for checking | RED |
| memo: the shape of the answer | RED |
| memo: the definition of a current employee dropped | RED |
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
| golden: a recruiting table the request no longer asks for | RED |
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
| verifier: a key with a note beside it rejected | RED |
|  | RED |
| verifier: absence passing on a thin table | RED |
| verifier: page history read as pages | RED |
| verifier: the published flag assumed | RED |
| verifier: a count that tallies substrings | RED |
| verifier: a duplicate page passing on its better copy | RED |
| battery: a scenario expecting the wrong verdict | RED |
| docs: the prompt blockquote | RED |
| docs: a stale explanation in the record's rubric table | RED |
| docs: a non-ASCII character in a package document | RED |

**59 of 59 controls went red**, 09/19/2026, and the closing rebuild left the tree clean.
