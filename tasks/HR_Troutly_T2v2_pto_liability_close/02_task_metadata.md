# T2 v2 - task metadata, weighting and the registered record

Built 09/22/2026 from T2's measured record. Same world, same determination, a narrower ask and
a rubric priced by what a wrong figure costs the output. T2's own package stays where it is and
keeps its history; nothing here restates it. Review round 1, the same day, narrowed the ask
again, from a row per current employee to five department lines, and is recorded below.

## Identity

| Field | Value |
|---|---|
| **Task name** | PTO Liability at 08/31/2026 |
| **1.1) Prompt** | the one line below, blockquoted verbatim |
| **1.3) Steps** | `08_section_1_3_step_plan.md` |
| **1.4) Additional task files** | `00_task_input_pto_liability_request.pdf` on the **Filesystem** target, md5 `81963ec80cd2bee9fa1cb561c9df1eb7`, 2429 bytes. It uploads as `pto_liability_request.pdf` |
| **1.5) Expected Output Files** | Nothing. The deliverable is one published page |
| **Grading target** | None. Every row is App DB Programatic on the Wiki.js `pages` table |
| **Apps** | Wiki.js (written), BambooHR (read), Greenhouse (untouched and ungraded) |
| **Deliverable** | one page, `PTO Liability - 08/31/2026` |
| **World snapshot** | `snap_c6f6a0879f3d47a19048ee80d7529157` |
| **Task data id** | `snap_31202a8918284a76a7c53582bfc550ec`, v2's own, read off its first export on 09/23/2026 |
| **Rubric import** | `05_rubric_import.xlsx`, md5 `9521e24e215ffd0a071bb0d1c7d7418b`, **13 rows and 79 points**, 12 primary, one sheet named Rubric in the HR 79 T1 column order |
| **Golden output** | `04_golden_output_PTO_Liability.md`, md5 `4568b979097e4411479f9960b0e10fae` |
| **Verifier code** | 13 row files under `qc/verifiers/`, each the row's spec stamped onto `build/verifier_engine.py`. `qc/verifier_harness.py` reads every row against every snapshot with the answer known |

## 1.1) The prompt, verbatim

> Complete the request (using the HRIS time off report and the rest of the Troutly files) about the August 2026 close by publishing the Wiki.js page PTO Liability - 08/31/2026.

## What changed from T2, and why

Grader feedback on another world, carried here by the owner on 09/22/2026: a criterion whose
failure materially changes the output weighs more than 2. Weight 2 suits an extraction and
weight 1 a formatting line. T2's rubric was full of rows under that bar - 14 points of page
form and 29 BambooHR rows at 1 - and a response that got the determination wrong earned them
all. The remedy taken is the full rescope, not a reweighting: the lines that drew those rows
are out of the request, so the rubric has nothing to price low.

| T2 asked for | v2 | The rows it used to draw |
|---|---|---|
| a short summary above one table | gone | the layout row |
| the employee count in the summary | gone | the summary row |
| name, department and annual PTO tier columns | gone | three column rows |
| a dollar liability column | gone | the precision row on dollars |
| Dates MM/DD/YYYY | gone | the date row |
| hours to two decimals, rates to four, dollars to the cent | gone | three precision rows |
| the total is the sum of the rows | gone | the reconciliation row |
| an employee ID on every row | gone | the ID row |
| the BambooHR instruction | gone | 29 BambooHR rows at 1 |
| a row per current employee with ID, balance and rate | gone in review round 1 | 24 cell rows, and 156 values no 25-criterion rubric covers |
| Use 08/31/2026 as the measurement date | gone in review round 1 | no row, an ask the title already carries that the review found unread |
| the page and the two totals | kept | rows 1 to 3 |
| hours and dollars for five department lines, Sales and Marketing joined | added in review round 1 | rows 4 to 13 |

## Review round 1, 09/22/2026

The first review read the 27-row file and raised two findings, both accepted.

1. **Prompt scope against rubric coverage.** The request asked for a row per current employee
   with three values, 52 by 3, 156 requirements before the title and the totals, and the
   platform's feasibility limit is 25 criteria. The 27-row rubric was itself over it. The
   per-employee table is out of the request and five department lines are in: each line's PTO
   hours and PTO liability, 13 criteria in all.
2. **Prompt-rubric alignment.** The measurement-date sentence and the per-employee table were
   explicit asks no row read. The table is gone with finding 1, and the sentence is gone
   because the page title and the subject already carry the date and every graded figure is a
   figure at that date.

**Why Sales and Marketing are one line.** Marketing alone is a line the load already carries
right, so a response that copied the HRIS report would have earned both its figures. Joined to
Sales, which the load carries wrong until TRT-0018's tier change is timed inside the fourth
period, the line is wrong on every path from P0 to P4. The memo names the five lines and asks for no
per-employee figure, and `build/build_task_input.py` bars the table and the date sentence from
returning, one control each.

`build/build_task_input.py` bars each removed line from returning, one negative control each,
the way the fence, the deadline and the retention line are barred.

## The weighting, registered before any v2 run

**13 rows, 79 points.** One row is not a determination: row 1, the page published under the
title, at 1 point, 1.3% of the set. That is the whole of what a response earns for publishing
a page with the wrong numbers on it.

| Row | Weight | What it reads |
|---|---|---|
| 1 | 1 | the page exists under the title with its published flag set |
| 2 | 10 | the stated total dollar liability, $92,739.54, the gate |
| 3 | 8 | the stated total PTO hours, 1,522.17 |
| 4 to 13 | 3 to 7 | each line's PTO hours and PTO liability, five lines, every figure one the load carries wrong |

**A line figure's weight is the dollars it moves.** A dollar figure is priced by the liability
between the line the world gives and the line the load carries, an hours figure by the hours
it is off by, each at its own employee's rate, $36,991.13 across the 10 figures:

| Band | Weight | Rows |
|---|---|---|
| moves $2,000.00 or more | 7 | 6 |
| moves $800.00 or more | 6 | 2 |
| moves $250.00 or more | 5 | 0 |
| moves $80.00 or more | 4 | 0 |
| moves less than $80.00 | 3 | 2 |

**Why the lines and not the exceptions.** A request that named the employees the load has
wrong would have told the response that the load is wrong, which is the determination this ask
measures. A department line is a figure a finance close asks for anyway, every current
employee sits on exactly one, and each line is off in the load for a different mix of rules,
so the lines score a response rule by rule without pointing at a record.

**Nothing in the set grades the absence of content.** A response that also prints all 52
current employees, or Sales and Marketing apart beside the joined line, passes exactly what the
golden passes. An exclusion criterion would invalidate the golden, because a correct response
over-delivers anyway, and the battery proves both directions.

## The registered paths

| Path | What the run does | Rows | Total it prints | Score |
|---|---|---|---|---|
| P0 | the July close method rolled forward: the HRIS report's rows and balances, the loaded tiers and rates, contractors and ended records inside, the two unloaded hires outside | 57 | $119,758.03 | 1 of 79, 1.3% |
| P1 | the HRIS report with the population fixed: 52 rows, balances uncapped, the loaded tiers and rates | 52 | $111,455.78 | 1 of 79, 1.3% |
| P2 | P1 with the 40.0-hour cap applied at 06/30/2026 | 52 | $90,983.94 | 15 of 79, 19.0% |
| P3 | P2 with tiers from the archive's service dates, the rehire unbridged, the tier change not timed, the rates as loaded | 52 | $92,804.10 | 22 of 79, 27.8% |
| P4 | P3 with the two signed pay changes applied | 52 | $92,934.50 | 29 of 79, 36.7% |
| P5 | P4 with the rehire bridged and the tier change timed; the step and the part-time schedule still missed | 52 | $92,789.47 | 49 of 79, 62.0% |
| P6 | the heal | 52 | $92,739.54 | 79 of 79, 100.0% |

## The graded lines, from the world's own bytes

| # | Line | Figure | The world gives | The load carries | Moves | Weight |
|---|---|---|---|---|---|---|
| 1 | Customer Success | hours | 297.79 hours | 322.95 hours | $1,515.08 | 6 |
| 2 | Customer Success | dollars | $12,627.20 | $14,023.72 | $1,396.52 | 6 |
| 3 | Engineering | hours | 558.31 hours | 694.66 hours | $11,435.89 | 7 |
| 4 | Engineering | dollars | $41,542.16 | $52,936.56 | $11,394.40 | 7 |
| 5 | Finance and Corporate | hours | 121.53 hours | 165.53 hours | $2,934.04 | 7 |
| 6 | Finance and Corporate | dollars | $8,187.68 | $11,121.71 | $2,934.03 | 7 |
| 7 | Product | hours | 170.50 hours | 161.54 hours | $27.33 | 3 |
| 8 | Product | dollars | $10,984.34 | $10,957.00 | $27.34 | 3 |
| 9 | Sales and Marketing | hours | 374.04 hours | 407.03 hours | $2,663.26 | 7 |
| 10 | Sales and Marketing | dollars | $19,398.16 | $22,061.40 | $2,663.24 | 7 |

## The rubric, row by row

| # | Wt | Type | Primary | Criterion | Explanation |
|---|---|---|---|---|---|
| 1 | 1 | Objective Compliance | No | States that a Wiki.js page titled PTO Liability - 08/31/2026 is published. | One page under that title is what the request asks for in Wiki.js, so it exists with its published flag set. |
| 2 | 10 | Expert Assessment | Yes | States, on the PTO liability page, a total dollar liability of $92,739.54. | The cutover memo caps carryover at 40.0 hours, accrues four posted periods at the tier over 26 and values each balance at the rate on file over 2,080. The 52 balances sum to $92,739.54, or $92,772.88 rounding each posting. |
| 3 | 8 | Expert Assessment | Yes | States, on the PTO liability page, total PTO hours of 1,522.17. | The 52 current employees hold 1,522.17 hours at 08/31/2026 once the cutover memo's cap runs and four posted periods accrue by adjusted service date. The HRIS report's columns add to 1,751.71. |
| 4 | 6 | Expert Assessment | Yes | States, on the PTO liability page, PTO hours of 297.79 for Customer Success. | In Customer Success the cutover memo caps TRT-0021 at 40.0 hours, the archive puts TRT-0083 at the 120-hour tier, handbook 2.2 prorates TRT-0141 and TRT-0153 accrues from the start. The line holds 297.79 hours, the HRIS report 322.95. |
| 5 | 6 | Expert Assessment | Yes | States, on the PTO liability page, a PTO liability of $12,627.20 for Customer Success. | Handbook 3.2 and 5.4 put TRT-0088 at $118,000.00 and TRT-0096 at $61,000.00, and the roster puts TRT-0153 at $92,000.00. On those rates and the capped balances Customer Success carries $12,627.20 against the load's $14,023.72. |
| 6 | 7 | Expert Assessment | Yes | States, on the PTO liability page, PTO hours of 558.31 for Engineering. | Five Engineering balances sit over the cutover memo's 40.0-hour cap, TRT-0005 at 92.50 in the archive, and the archive puts TRT-0051 at the 120-hour tier. Engineering holds 558.31 hours against the HRIS report's 694.66. |
| 7 | 7 | Expert Assessment | Yes | States, on the PTO liability page, a PTO liability of $41,542.16 for Engineering. | The signed amendment sets TRT-0117 at $148,200.00 from 05/16/2026 over the loaded $138,000.00. With the capped balances Engineering carries $41,542.16 of liability against the load's $52,936.56. |
| 8 | 7 | Expert Assessment | Yes | States, on the PTO liability page, PTO hours of 121.53 for Finance and Corporate. | Finance and Corporate has one balance over the cap, TRT-0009 at 84.00 in the archive, which the cutover memo holds to 40.0 hours. The line holds 121.53 hours against the HRIS report's 165.53. |
| 9 | 7 | Expert Assessment | Yes | States, on the PTO liability page, a PTO liability of $8,187.68 for Finance and Corporate. | Capping TRT-0009 under the cutover memo takes Finance and Corporate to $8,187.68 at the rates on the roster. The load values the same five employees at $11,121.71. |
| 10 | 3 | Expert Assessment | Yes | States, on the PTO liability page, PTO hours of 170.50 for Product. | Product nets close to the load because the cutover memo caps TRT-0040 while handbook 7.6 bridges TRT-0071 and the archive puts TRT-0079 at the 120-hour tier. It holds 170.50 hours against the HRIS report's 161.54. |
| 11 | 3 | Expert Assessment | Yes | States, on the PTO liability page, a PTO liability of $10,984.34 for Product. | At the rates on the roster the Product line carries $10,984.34, the cap on TRT-0040 offset by the bridged TRT-0071 and the retiered TRT-0079 under the cutover memo. The load carries $10,957.00. |
| 12 | 7 | Expert Assessment | Yes | States, on the PTO liability page, PTO hours of 374.04 for Sales and Marketing. | The request joins Sales and Marketing. The cutover memo caps TRT-0018, TRT-0029 and TRT-0043, times TRT-0018's tier change and accrues TRT-0155 from the start, 374.04 hours against the HRIS report's 407.03. |
| 13 | 7 | Expert Assessment | Yes | States, on the PTO liability page, a PTO liability of $19,398.16 for Sales and Marketing. | Valued at the roster's rates, TRT-0155 at $56,300.00, the joined Sales and Marketing line carries $19,398.16 under the cutover memo. The load's figures for the same 13 employees come to $22,061.40. |

## Required world files

The world files and app tables this package reads, in picker form, one per line. The block is
authoritative for which tables are selected.

```
HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx
HR/Policies/Employee_Handbook_v3.pdf
HR/Policies/PTO_Policy_2025.docx
HR/Data/HRIS_Time_Off_Report_2026-08-31.xlsx
HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx
HR/Data/2026-08-31_Master_Employee_Roster.xlsx
HR/Data/2026-08-28_Employee_ID_Crosswalk.xlsx
HR/Data/Migration/HRIS_Import_Load_2026-07-01.csv
HR/Data/Migration/2026-06-24_Field_Mapping_Workbook.xlsx
HR/Data/Migration/2026-07-22_Migration_Closeout_Memo.docx
HR/Payroll/2026-06-25_Payroll_Procedures_Memo.docx
HR/Payroll/HRIS_Payroll_History_2026-07-01_to_2026-08-31.xlsx
Finance/Close/2026-07_Close_Package.xlsx
HR/Comp/Promotions/2026-06-10_Promotion_Approval_TRT-0088.docx
HR/Comp/Amendments/2026-05-12_Comp_Amendment_TRT-0117.pdf
HR/People/Offer_Letters/2024-04-08_Rehire_Offer_TRT-0071.pdf
HR/People/Offer_Letters/Historical_Offer_Letters_2020-2026.pdf
HR/Benefits/2026-08-10_Schedule_Change_TRT-0141.pdf
Recruiting/Offers/2026-07-02_Offer_TRT-0153_SIGNED.pdf
Wiki/Paid_Time_Off.md
Wiki/Compensation_Authority.md
Wiki/Onboarding_Data_Standards.md
bamboohr/Employee.csv
bamboohr/TimeOffBalance.csv
bamboohr/TimeOffPolicy.csv
bamboohr/TimeOffRequest.csv
bamboohr/EmployeePolicy.csv
bamboohr/TimeOffType.csv
wiki_js/Page.csv
```

## Fences

There is no fence. The memo carries no out-of-scope block, no deadline and no retention line,
and `build/build_task_input.py` bars each from returning. HR 79 T1 closed the same argument in
its round 9 and T2 closed it in rounds 3 and 4: a clause that fences work out of scope asks for
nothing, so a row on it is a point every response earns.

## Reviewer decision rules

1. A stated total is read as stated. The page is asked to state both totals, so a sum a reader
   would have to do themselves is not a stated total.
2. A line is read where the page names it: a table row one of whose cells is the line's name, or
   a prose line that opens on it. Sales alone is not Sales and Marketing, and a figure inside an
   employee row is that employee's, never a line's or a total.
3. A line a reader would have to add up from the employees is not a stated line.
4. The two totals and the ten line figures are graded to half a dollar and a twentieth of an
   hour. The request carries no Form section, so a response that rounds what it states has
   still stated it, and no registered path comes within either band.
5. Extra rows, extra columns and extra tables cost nothing. Only what the criterion names is read.
6. The page is the one row of the `pages` table whose title matches. Two rows under the title
   fail every page row, because the request asks for one page.

## Predictions, dated 09/22/2026, before any v2 run

1. A response that copies the HRIS time off report scores 1 of 79, the page row alone.
2. The gate fails on any response that misses the cap, which is every trajectory measured in
   this world so far, ten of ten.
3. Finance and Corporate is the line this tier gets right most often, because the cap is its
   only rule. Product is the line it gets right least, because the cap and the bridge pull it
   in opposite directions and net to $27.34.
4. A Gemini set will land under 25%. The ten trajectories already measured against the earlier
   ask read 1.3% and 1.3% under this rubric as printed, and 1.3% and 1.3% with each run's own rows
   summed onto the lines. None of them applied the cap, and the cap moves every line.
5. If a set lands over 60%, the lever is measured insufficient in this world for this tier and
   the package retires. The rubric is not rescoped around whatever failed.

## Open items

1. **A v2 run set.** One of the five Gemini 3.8 Flash trajectories the decision rule reads has
   run: G1 of 09/23/2026, archived under `qc/findings/run_set_09-23-2026/` and scored from its
   bytes at 1.3%, the load's own figures line for line, $111,100.39, the page row and nothing else,
   106 steps on the platform's count. The record is in `06_failure_analysis.md`. Four Gemini
   runs and three GPT Sol 5.6 are owed, and the rule fires on five.
2. **v2's task data id.** Measured 09/23/2026 off G1's export:
   `snap_31202a8918284a76a7c53582bfc550ec`, minted by the memo's 1.4 upload. `TASK_SNAP` carries it and the
   import's task-source reference points at it.
3. **The wiki in the graded dump.** Measured 09/23/2026: row 1 with both wiki services ticked
   was handed 57 BambooHR and Greenhouse tables and no Wiki.js table, which is why every wiki
   row failed on 09/21/2026. The rows now read the page off the run's own Wiki.js calls when the
   dump has no pages table. Measured the same day: a graded ctx carries `trajectory`, 96
   messages in the export's shape, and row 1 passed on a create and a get_page of page 11.
   Row 2 then read the page's total off the same calls and failed it, as it should. The record is
   `qc/findings/platform_grading_09-23-2026.md`.
4. **The import does not populate Tags, Reference Artifacts or Grading Target.** Measured on T2
   and unchanged. They are entered by hand from `build/rubric_plan.csv`.
