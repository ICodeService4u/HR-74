# T2 v2 - PTO Liability at 08/31/2026

**Status: built 09/22/2026 as a full rescope of T2, on the owner's decision of the same day, and
narrowed again by review round 1 the same day.** T2 measured the determination well and priced
it badly: 55 rows and 105 points, of which 14 were the page and its form and 29 were BambooHR
records at 1 point each, so a response that got every rule wrong still collected them. The
remedy taken here is the rescope rather than a reweighting: **the lines that drew those rows
are out of the request**, and what is left is the determination. Review round 1 then found the
per-employee table itself over the platform's 25-criterion limit, 52 rows of three values, and
the measurement-date sentence an ask no row read. Both are out, and the request asks for five
department lines in the table's place, Sales and Marketing joined because Marketing alone is a
figure the load already carries right. 13 rows and 79 points, of which 1 point is not a
determination. The battery reads **793 of 793 verdicts correct across 61 snapshots**, and the ten
Gemini trajectories already measured in this world score 1.3% and 1.3% against this rubric,
where T2's own read 23.9% and 38.1%. The first v2 trajectory, G1 of 09/23/2026, reads 1.3%: the
load's own figures line for line, $111,100.39 on 1,751.71 hours, the page row alone, 106 steps on the
platform's count. Four Gemini runs and three GPT Sol 5.6 are owed.

| Event | Date | Result |
|---|---|---|
| Built | 09/22/2026 | the memo narrowed to three asks, the golden recomputed from the world, 27 rows at 143 points, seven registered paths, predictions dated |
| Review round 1 | 09/22/2026 | two findings, both accepted: the per-employee table and the measurement-date sentence out of the memo, five department lines in, 13 rows at 79 points, every figure recomputed from the world |
| Verifier code and battery | 09/22/2026 | 13 row files generated from the rows onto `build/verifier_engine.py`, 231 to 234 lines each; **793 of 793 verdicts correct** across 61 snapshots |
| Re-scored, T2's run sets | 09/22/2026 | the ten archived trajectories read under this rubric: the 09/20/2026 five at a mean of 1.3%, the 09/21/2026 five at 1.3%, none over 1.3%. Their pages carry no line, so `--as-lines` sums each run's own rows onto the five lines: 1.3% and 1.3%, none having applied the cap |
| Negative controls | 09/22/2026 | see the table below, from `build/negative_controls.py` |
| First v2 trajectory | 09/23/2026 | G1, gemini-3.8-flash, task version 34, task data id `snap_31202a8918284a76a7c53582bfc550ec`, all 13 verifiers on the export; $111,100.39 on 1,751.71 hours, the page row alone, 1.3%, 106 steps; the memo opened at step 19, its cap quoted at step 22, the capped total computed at step 89 and set aside for the report. Archived under `qc/findings/run_set_09-23-2026/`, recorded in `06_failure_analysis.md` |

## The ask, in one paragraph

The Finance Manager asks the People Operations Analyst for the PTO liability at 08/31/2026 for
the August close: one wiki page stating the total dollar liability and the total PTO hours, and
the PTO hours and the PTO liability for each of five lines, Customer Success, Engineering,
Finance and Corporate, Product, and Sales and Marketing. The memo names the July detail it
replaces and no rule. The cutover memo of 06/20/2026 caps carryover at 40.0 hours, accrues
biweekly at the tier over 26 by adjusted service date, and values at the rate on file over 2,080.
The HRIS report is uncapped at the loaded tiers, nine service dates were loaded as 07/01/2026,
a rehire bridges, an anniversary falls inside the window, two signed pay changes were dropped by
the load, a step fell due, and a part-time schedule changed. 1,522.17 hours and $92,739.54. The July
close booked $90,862.13 and the load's own figures come to 1,751.71 hours and $111,100.39.

## What the rubric prices

Every row but one is a determination. Every line figure is one the load carries wrong, so a
response that copies the HRIS time off report earns none of them, and each figure's weight is
the dollars it moves:

| Rows | Weight | What they read |
|---|---|---|
| 1 | 1 | the page published under the title, the only row that is not a determination |
| 1 | 10 | the stated total dollar liability, $92,739.54, the gate |
| 1 | 8 | the stated total PTO hours, 1,522.17 |
| 6 | 7 | Engineering hours, Engineering dollars, Finance and Corporate hours, Finance and Corporate dollars, Sales and Marketing hours, Sales and Marketing dollars |
| 2 | 6 | Customer Success hours, Customer Success dollars |
| 2 | 3 | Product hours, Product dollars |

10 line figures, $36,991.13 of movement in all. Nothing grades the absence of content: a response that
also prints every employee, or Sales and Marketing apart beside the joined line, scores exactly
what the golden scores.

| Path | What the run does | Total it prints | Score |
|---|---|---|---|
| P0 | the July close method rolled forward: the HRIS report's rows and balances, the loaded tiers and rates, contractors and ended records inside, the two unloaded hires outside | $119,758.03 | 1 of 79, 1.3% |
| P1 | the HRIS report with the population fixed: 52 rows, balances uncapped, the loaded tiers and rates | $111,455.78 | 1 of 79, 1.3% |
| P2 | P1 with the 40.0-hour cap applied at 06/30/2026 | $90,983.94 | 15 of 79, 19.0% |
| P3 | P2 with tiers from the archive's service dates, the rehire unbridged, the tier change not timed, the rates as loaded | $92,804.10 | 22 of 79, 27.8% |
| P4 | P3 with the two signed pay changes applied | $92,934.50 | 29 of 79, 36.7% |
| P5 | P4 with the rehire bridged and the tier change timed; the step and the part-time schedule still missed | $92,789.47 | 49 of 79, 62.0% |
| P6 | the heal | $92,739.54 | 79 of 79, 100.0% |

## What ships

| File | Purpose |
|---|---|
| `00_task_input_pto_liability_request.pdf` | The 1.4 input, Filesystem target, uploads as `pto_liability_request.pdf` |
| `01_prompt.md` | The prompt verbatim, the shape reasoning, why this ask, the Spec table, the withheld list |
| `02_task_metadata.md` | Identity, what changed from T2, the weighting, the registered paths, the graded cells, the rubric, the selection block, the reviewer rules, the predictions and the open items |
| `03_show_your_work.xlsx` | The show-your-work, generated by the builder |
| `04_golden_output_PTO_Liability.md` | The golden page, generated from the schedule in the request's shape |
| `05_rubric_import.xlsx` / `09_rubric_import.md` | The file that registers, and its mappings |
| `06_failure_analysis.md` | The predictions, dated, with the decision rule, and the measured record of each v2 run under them |
| `07_paste_guide.md` | The paste, row by row, written by `qc/write_paste_guide.py` from the plan's rows |
| `08_section_1_3_step_plan.md` | The checkpoint table |
| `build/build_task_input.py`, `build/task_input_source.md` | The memo source and its renderer, with the leak guards and the bars on every line v2 removed |
| `build/build_package_artifacts.py` | The one builder: the schedule from the world's bytes, the five lines, the plan, the import, the golden page, the row files, the guards |
| `build/verifier_engine.py` | The engine every row file stamps its spec into |
| `build/schedule_preview.csv`, `build/rubric_plan.csv` | The golden schedule, and the plan with the import's columns beside its own |
| `build/negative_controls.py` | Every guard made to fail once |
| `build/write_metadata.py`, `build/write_readme.py`, `build/measured.py` | `02_task_metadata.md` and this file, written from the build, the battery and the re-scoring so every figure in them is measured on the write |
| `qc/README.md`, `qc/findings/` | The AutoQC register and the verbatim archive: v2's own run set, and T2's two, carried here to be re-scored |
| `qc/ctx.py`, `qc/run_battery.py` | The verifier skill's stand-in `ctx` and battery runner |
| `qc/scenarios.py`, `qc/verifier_harness.py` | The 61-snapshot battery and the runner over all rows |
| `qc/verifiers/` | The 13 generated row files |
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
python3 qc/score_run_set.py --set run_set_09-23-2026 --details
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
| memo: the per-employee table returning | RED |
| memo: the measurement-date line returning | RED |
| memo: a line dropped from the ask | RED |
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
| plan: a line the load already carries right, Marketing alone | RED |
| plan: the golden not scoring every point | RED |
| plan: over 25 criteria | RED |
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
| verifier: a line matched as a substring | RED |
| verifier: a line read off a prose word | RED |
| verifier: a figure read off an employee row | RED |
| verifier: a figure read in any unit (R3) | RED |
| verifier: a struck figure read as stated | RED |
| verifier: a band around a stated line | RED |
| verifier: the band around a stated total | RED |
| verifier: two pages under the title graded one by one | RED |
| verifier: the title read off any cell of a page row | RED |
| verifier: a page row reading a ctx primitive the measured surface does not carry | RED |
| verifier: a run's narration read instead of the database | RED |
| verifier: a write the app refused read as written | RED |
| verifier: the page's first state read instead of its last | RED |
| verifier: a page under any title read as this one | RED |
| verifier: an update to any page read as this one | RED |
| verifier: the run's record read where the dump holds the wiki | RED |
| verifier: two pages created under the title graded as one | RED |
| verifier: a row file over the 240-line cap | RED |
| verifier: an import the platform's AST gate bans | RED |
| battery: an expectation planted wrong | RED |
| battery: a page that over-delivers expected to fail | RED |
| golden: a total the schedule did not give | RED |
| docs: a stale figure in the record | RED |
| docs: a planned row missing from the record | RED |
| docs: a file missing from the README | RED |
| docs: a non-ASCII character in a package document | RED |
| selection: a wildcard in the block | RED |

**79 of 79 controls went red**, 09/23/2026. A defect planted in the memo, the world constants,
the plan, the rubric, the register, the import, the engine, the battery or a document fails the
build or the harness, and the closing rebuild left the tree clean at the published md5s and the
battery at 793 of 793. The memo controls include each line the rescope and review round 1 took
out, planted back, and each one fails the memo build. The plan controls hold the rescope's own
rule: a Marketing line on its own is a figure the load already carries right and fails the build,
and a page that over-delivers expected to fail fails the battery. The verifier controls hold the
line reader to a whole-cell name, a prose line that opens on the name and no employee row.
