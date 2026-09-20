# T2 - PTO Liability Schedule and BambooHR PTO Records

**Status: built 09/20/2026 at the prompt half, no run yet.** The second HR 74 ask, built on the
measured record of T1 and T1 v2: thirteen Gemini trajectories healed a population reconciliation
with and without pointers, so the next ask had to be a determination the tier gets wrong, not a
lookup. This one is the PTO liability at 08/31/2026, a rule application over 52 people where
every record the run opens prints a finished wrong number. By the decision of 09/20/2026 the
prompt half ships first, the five Gemini trajectories decide, and the rubric half is built only
if they fail.

| Event | Date | Result |
|---|---|---|
| Built | 09/20/2026 | the memo, the prompt, 31 selections, 22 world files, the golden schedule recomputed from the world, a 21-row plan at 92 points, seven registered paths, predictions dated |
| Negative controls | 09/20/2026 | see the table below, from `build/negative_controls.py` |
| Run set | owed | five Gemini 3.8 Flash and three GPT Sol 5.6, scored against the registered paths |
| Prompt round 1 | owed | archived verbatim to `qc/findings/` when it lands |
| Rubric half | conditional | built from `build/rubric_plan.csv` only under 40% |

## The ask, in one paragraph

The Finance Manager asks the People Operations Analyst for the PTO liability at 08/31/2026 for
the August close: one wiki page with a row per current employee, the tier, the balance, the
hourly rate and the dollar liability, a summary with the count and the totals, and BambooHR
brought to the schedule. The memo names the July detail it replaces and no rule. The cutover
memo of 06/20/2026 caps carryover at 40.0 hours, accrues biweekly at the tier over 26 by adjusted
service date, and values at the rate on file over 2,080; the HRIS report is uncapped at the
loaded tiers, nine service dates were loaded as 07/01/2026, a rehire bridges, an anniversary
falls inside the window, two signed pay changes were dropped by the load, a step fell due, and a
part-time schedule changed. 1,522.17 hours and $92,739.54; the July close booked $90,862.13.

## What ships

| File | Purpose |
|---|---|
| `00_task_input_pto_liability_request.pdf` | The 1.4 input, Filesystem target, uploads as `pto_liability_request.pdf` |
| `01_prompt.md` | The prompt verbatim, the shape reasoning, why this ask, the cell families, the Spec table, the withheld list |
| `02_task_metadata.md` | Identity, the weights and the registered paths, graded values, the selection block, fences, rival readings, reviewer decision rules, the asks table, the rubric plan, the checkpoints, the time estimate, the predictions, the platform state, the open items |
| `06_failure_analysis.md` | The predictions, dated, with the honest note and the decision rule |
| `08_section_1_3_step_plan.md` | The checkpoint table, held until the bar is measured |
| `build/build_task_input.py`, `build/task_input_source.md` | The memo source and its renderer with the leak guards |
| `build/build_package_artifacts.py` | The one builder: the schedule from the world's bytes, the paths, the plan, the guards |
| `build/schedule_preview.csv`, `build/rubric_plan.csv` | The golden schedule and the plan, regenerated on every build |
| `build/negative_controls.py` | Every guard made to fail once |
| `qc/README.md`, `qc/findings/` | The AutoQC register and the verbatim archive |

Not shipped at the prompt half: the golden page, the show-your-work, the rubric import, the
verifier engine and row files, the battery and the run-set archiver. Each is generated from the
builder and the plan if the first run set fails.

## Running the checks

From the package root:

```
python3 build/build_task_input.py
python3 build/build_package_artifacts.py --docs
python3 build/negative_controls.py
python3 ../check_selection_blocks.py
```

## Negative controls

| Control | Result |
|---|---|
| memo: the cap leaked | RED |
| memo: the accrual period leaked | RED |
| memo: a tier value leaked | RED |
| memo: a policy document named | RED |
| memo: the service-date basis leaked | RED |
| memo: the rehire rule leaked | RED |
| memo: the part-time rule leaked | RED |
| memo: a signed change leaked | RED |
| memo: one of the eight names | RED |
| memo: the total leaked | RED |
| memo: a record called wrong | RED |
| memo: a word for checking | RED |
| memo: the shape of the answer | RED |
| memo: the definition of a current employee dropped | RED |
| memo: the seat | RED |
| memo: an unlicensed date | RED |
| names: the upload name the record publishes | RED |
| world: the cap | RED |
| world: the posted periods | RED |
| world: the rehire bridging rule | RED |
| world: the step | RED |
| world: the tier boundaries | RED |
| world: a signed rate dropped | RED |
| world: the part-time schedule | RED |
| world: a phrase the cutover memo must carry | RED |
| world: the population | RED |
| plan: weight band | RED |
| plan: the gate demoted off the total | RED |
| plan: a row not opening on States | RED |
| plan: the free base over a tenth | RED |
| plan: the golden not scoring every point | RED |
| plan: P0 scoring over a fifth | RED |
| docs: the prompt blockquote | RED |
| docs: a stale figure in the record | RED |
| docs: a stale path score in the predictions | RED |
| docs: a planned row missing from the record | RED |
| docs: a selection dropped from the block | RED |
| docs: a file missing from the README | RED |
| docs: a non-ASCII character in a package document | RED |
| selection: a wildcard in the block | RED |

**40 of 40 controls went red**, 09/20/2026, and the closing rebuild left the tree clean.
