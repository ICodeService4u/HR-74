# T2 v2 - PTO Liability at 08/31/2026

**Status: built 09/22/2026 as a full rescope of T2, on the owner's decision of the same day.**
T2 measured the determination well and priced it badly: 55 rows and 105 points, of which 14
were the page and its form and 29 were BambooHR records at 1 point each, so a response that got
every rule wrong still collected them. Grader feedback carried from another world says a
criterion whose failure materially changes the output weighs more than 2, and that 2 is an
extraction's weight and 1 a formatting line's. The remedy taken here is the rescope rather than
a reweighting, because a reweighting would have left the same low-weight rows in place with
bigger numbers on them: **the lines that drew those rows are out of the request**, and what is
left is the determination. 27 rows and 143 points, of which 1 point is not a determination. The
battery reads **837 of 837 verdicts correct across 31 snapshots**, and the ten Gemini
trajectories already measured in this world score 8.3%% and 14.7%% against this rubric, where
T2's own read 23.9%% and 38.1%%. A v2 run set is owed.

| Event | Date | Result |
|---|---|---|
| Built | 09/22/2026 | the memo narrowed to three asks, the golden recomputed from the world, 27 rows at 143 points, seven registered paths, predictions dated |
| Verifier code and battery | 09/22/2026 | 27 row files generated from the rows onto `build/verifier_engine.py`, 320 lines each against T2's 762; **837 of 837 verdicts correct** across 31 snapshots |
| Re-scored, T2's run sets | 09/22/2026 | the ten archived trajectories read under this rubric: the 09/20/2026 five at a mean of 8.3%, the 09/21/2026 five at 14.7%, none over 30.8%, every one of them failing the gate and the cap |
| Negative controls | 09/22/2026 | see the table below, from `build/negative_controls.py` |

## The ask, in one paragraph

The Finance Manager asks the People Operations Analyst for the PTO liability at 08/31/2026 for
the August close: one wiki page stating the total dollar liability and the total PTO hours, with
a row per current employee carrying the employee ID, the balance in hours and the hourly rate.
The memo names the July detail it replaces and no rule. The cutover memo of 06/20/2026 caps
carryover at 40.0 hours, accrues biweekly at the tier over 26 by adjusted service date, and
values at the rate on file over 2,080; the HRIS report is uncapped at the loaded tiers, nine
service dates were loaded as 07/01/2026, a rehire bridges, an anniversary falls inside the
window, two signed pay changes were dropped by the load, a step fell due, and a part-time
schedule changed. 1,522.17 hours and $92,739.54; the July close booked $90,862.13 and the load's own
figures come to 1,751.71 hours and $111,100.39.

## What the rubric prices

Every row but one is a determination. A cell is graded only where the figure the world gives at
08/31/2026 is not the figure the load carries, so a response that copies the HRIS time off
report earns none of them, and each cell's weight is the dollars it moves:

| Rows | Weight | What they read |
|---|---|---|
| 1 | 1 | the page published under the title, the only row that is not a determination |
| 1 | 10 | the stated total dollar liability, $92,739.54, the gate |
| 1 | 8 | the stated total PTO hours, 1,522.17 |
| 4 | 7 | one cell each, moving $2,000.00 or more |
| 6 | 6 | one cell each, moving $800.00 or more |
| 7 | 5 | one cell each, moving $250.00 or more |
| 4 | 4 | one cell each, moving $80.00 or more |
| 3 | 3 | one cell each, moving $0.00 or more |

24 cells over 22 employees, $23,539.62 of movement in all. Nothing grades the absence of content: a
response that prints all 52 current employees scores exactly what one that prints only the 22
the load has wrong scores.

| Path | What the run does | Total it prints | Score |
|---|---|---|---|
| P0 | the July close method rolled forward: the HRIS report's rows and balances, the loaded tiers and rates, contractors and ended records inside, the two unloaded hires outside | $119,758.03 | 1 of 143, 0.7% |
| P1 | the HRIS report with the population fixed: 52 rows, balances uncapped, the loaded tiers and rates | $111,455.78 | 19 of 143, 13.3% |
| P2 | P1 with the 40.0-hour cap applied at 06/30/2026 | $90,983.94 | 76 of 143, 53.1% |
| P3 | P2 with tiers from the archive's service dates, the rehire unbridged, the tier change not timed, the rates as loaded | $92,804.10 | 100 of 143, 69.9% |
| P4 | P3 with the two signed pay changes applied | $92,934.50 | 107 of 143, 74.8% |
| P5 | P4 with the rehire bridged and the tier change timed; the step and the part-time schedule still missed | $92,789.47 | 119 of 143, 83.2% |
| P6 | the heal | $92,739.54 | 143 of 143, 100.0% |

## What ships

| File | Purpose |
|---|---|
| `00_task_input_pto_liability_request.pdf` | The 1.4 input, Filesystem target, uploads as `pto_liability_request.pdf` |
| `01_prompt.md` | The prompt verbatim, the shape reasoning, why this ask, the Spec table, the withheld list |
| `02_task_metadata.md` | Identity, what changed from T2, the weighting, the registered paths, the graded cells, the rubric, the selection block, the reviewer rules, the predictions and the open items |
| `03_show_your_work.xlsx` | The show-your-work, generated by the builder |
| `04_golden_output_PTO_Liability.md` | The golden page, generated from the schedule in the request's shape |
| `05_rubric_import.xlsx` / `09_rubric_import.md` | The file that registers, and its mappings |
| `06_failure_analysis.md` | The predictions, dated, with the decision rule |
| `07_paste_guide.md` | The paste, row by row, written by `qc/write_paste_guide.py` from the plan's rows |
| `08_section_1_3_step_plan.md` | The checkpoint table |
| `build/build_task_input.py`, `build/task_input_source.md` | The memo source and its renderer, with the leak guards and the bars on every line v2 removed |
| `build/build_package_artifacts.py` | The one builder: the schedule from the world's bytes, the graded cells, the plan, the import, the golden page, the row files, the guards |
| `build/verifier_engine.py` | The engine every row file stamps its spec into, five check kinds and no more |
| `build/schedule_preview.csv`, `build/rubric_plan.csv` | The golden schedule, and the plan with the import's columns beside its own |
| `build/negative_controls.py` | Every guard made to fail once |
| `build/write_metadata.py`, `build/write_readme.py` | `02_task_metadata.md` and this file, written from the build so every figure in them is the build's own |
| `qc/README.md`, `qc/findings/` | The AutoQC register and the verbatim archive, including T2's two run sets, carried here to be re-scored |
| `qc/ctx.py`, `qc/run_battery.py` | The verifier skill's stand-in `ctx` and battery runner |
| `qc/scenarios.py`, `qc/verifier_harness.py` | The 31-snapshot battery and the runner over all rows |
| `qc/verifiers/` | The 27 generated row files |
| `qc/write_paste_guide.py` | Writes `07_paste_guide.md` from the rows |
| `qc/archive_run_set.py`, `qc/score_run_set.py` | The archiver and the scorer, each with a `--self-check` |
| `qc/compare_platform_grade.py` | Reads a transcribed grading pane against the verifiers' own verdicts |

## Running the checks

From the package root. `build_task_input.py` needs `pikepdf`, `reportlab` and `python-docx`,
and the builder `openpyxl` and `pdfplumber`:

```
python3 build/build_task_input.py
python3 build/build_package_artifacts.py --docs
python3 build/build_package_artifacts.py --table
python3 qc/verifier_harness.py
python3 qc/write_paste_guide.py
python3 build/negative_controls.py
python3 ../check_selection_blocks.py
python3 qc/score_run_set.py --self-check
python3 qc/score_run_set.py --set run_set_09-21-2026 --details
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
| memo: a fence returning, the Greenhouse line | RED |
| memo: a fence returning, the scope line | RED |
| memo: a deadline returning | RED |
| memo: a retention line returning | RED |
| memo: the Form section returning | RED |
| memo: the BambooHR ask returning | RED |
| memo: the summary count returning | RED |
| memo: a dropped column returning | RED |
| memo: the one-table shape returning | RED |
| world: the cap | RED |
| world: the posted periods | RED |
| world: the rehire bridging rule | RED |
| world: the step | RED |
| world: the tier boundaries | RED |
| world: the part-time rule | RED |
| world: the valuation basis | RED |
| plan: the gate demoted off the total | RED |
| plan: a row not opening on States | RED |
| plan: the free base over a seventh | RED |
| plan: a cell priced outside its band | RED |
| plan: a cell the load already carries right | RED |
| plan: the golden not scoring every point | RED |
| rubric: a compliance row flagged primary | RED |
| register: punctuation | RED |
| register: a spelled month | RED |
| register: grading vocabulary | RED |
| register: no source named | RED |
| register: over 240 characters | RED |
| import: the sheet not named Rubric | RED |
| import: a column out of the HR 79 T1 order | RED |
| import: a criterion type outside the code-verifier dropdown | RED |
| import: the 1.4 upload dropped from every row | RED |
| verifier: the key matched as a substring | RED |
| verifier: a band around a stated cell | RED |
| verifier: the band around a stated total | RED |
| verifier: a total read off an employee row | RED |
| verifier: two pages under the title graded one by one | RED |
| verifier: the title read off any cell of a page row | RED |
|  | RED |
| verifier: a run's narration read instead of the database | RED |
| battery: an expectation planted wrong | RED |
| battery: a page that over-delivers expected to fail | RED |
| golden: a total the schedule did not give | RED |
| docs: a stale figure in the record | RED |
| docs: a planned row missing from the record | RED |
| docs: a file missing from the README | RED |
| docs: a non-ASCII character in a package document | RED |
| selection: a wildcard in the block | RED |

**64 of 64 controls went red**, 09/22/2026. A defect planted in the memo, the world constants,
the plan, the rubric, the register, the import, the engine, the battery or a document fails the
build or the harness, and the closing rebuild left the tree clean at the published md5s and the
battery at 918 of 918. Five of the controls are v2's own: each line the rescope took out of the
memo planted back, the Form section, the BambooHR ask, the summary count, a dropped column and
the one-table shape, and each one fails the memo build. Three more hold the rescope's own rule -
a cell priced outside its band, a cell the load already carries right, and a page that
over-delivers expected to fail - so a row that grades absence or a cell that is free cannot be
added without the controls going green.
