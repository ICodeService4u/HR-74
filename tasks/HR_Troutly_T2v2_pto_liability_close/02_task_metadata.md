# T2 v2 - task metadata, weighting and the registered record

Built 09/22/2026 from T2's measured record. Same world, same determination, a narrower ask and
a rubric priced by what a wrong cell costs the output. T2's own package stays where it is and
keeps its history; nothing here restates it.

## Identity

| Field | Value |
|---|---|
| **Task name** | PTO Liability at 08/31/2026 |
| **1.1) Prompt** | the one line below, blockquoted verbatim |
| **1.3) Steps** | `08_section_1_3_step_plan.md` |
| **1.4) Additional task files** | `00_task_input_pto_liability_request.pdf` on the **Filesystem** target, md5 `b1b8dbf887bfd55f632f4224633fdf14`, 2395 bytes. It uploads as `pto_liability_request.pdf` |
| **1.5) Expected Output Files** | Nothing. The deliverable is one published page |
| **Grading target** | None. Every row is App DB Programatic on the Wiki.js `pages` table |
| **Apps** | Wiki.js (written), BambooHR (read), Greenhouse (untouched and ungraded) |
| **Deliverable** | one page, `PTO Liability - 08/31/2026` |
| **World snapshot** | `snap_c6f6a0879f3d47a19048ee80d7529157` |
| **Task data id** | `snap_1e12795ed0df4d489a36382afdb63279`, the id measured on 09/21/2026. v2's own is read off its first export |
| **Rubric import** | `05_rubric_import.xlsx`, md5 `12b9c24b04a769ebbfa56ebfb032692d`, **27 rows and 143 points**, 26 primary, one sheet named Rubric in the HR 79 T1 column order |
| **Golden output** | `04_golden_output_PTO_Liability.md`, md5 `6ff98cc8274ed771391957dda38c3903` |
| **Verifier code** | 27 row files under `qc/verifiers/`, each the row's spec stamped onto `build/verifier_engine.py`. `qc/verifier_harness.py` reads every row against every snapshot with the answer known |

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
| an employee ID on every row | gone as a line, kept as the key each value row reads | the ID row |
| the BambooHR instruction | gone | 29 BambooHR rows at 1 |
| the page, the totals, a balance and a rate per employee | kept | every row v2 carries |

`build/build_task_input.py` bars each removed line from returning, one negative control each,
the way the fence, the deadline and the retention line are barred.

## The weighting, registered before any v2 run

**27 rows, 143 points.** One row is not a determination: row 1, the page published under the
title, at 1 point, 0.7% of the set. That is the whole of what a response earns for publishing
a page with the wrong numbers on it.

| Row | Weight | What it reads |
|---|---|---|
| 1 | 1 | the page exists under the title with its published flag set |
| 2 | 10 | the stated total dollar liability, $92,739.54, the gate |
| 3 | 8 | the stated total PTO hours, 1,522.17 |
| 4 to 27 | 3 to 7 | one cell each, the 19 balances and 5 hourly rates the load carries wrong |

**A cell's weight is the dollars it moves.** Each graded cell is priced by the liability
between the figure the world gives and the figure the load carries, $23,539.62 across the 24 cells:

| Band | Weight | Rows |
|---|---|---|
| moves $2,000.00 or more | 7 | 4 |
| moves $800.00 or more | 6 | 6 |
| moves $250.00 or more | 5 | 7 |
| moves $80.00 or more | 4 | 4 |
| moves less than $80.00 | 3 | 3 |

**Why the request still asks for a row per current employee.** The rubric reads 24 cells, so a
request that asked only for the rows the load has wrong would have matched it exactly. It would
also have told the response that the load is wrong, which is the determination this ask
measures, and a response told where to look is a response handed the answer. The request asks
for the whole schedule, in the three columns the totals are built from, and says nothing about
the report beyond naming it as a source. The rubric then reads the cells that separate a
response that applied the rules from one that copied the report.

**Nothing in the set grades the absence of content.** A response that prints all 52 current
employees passes exactly what a response that prints only the 22 the load has wrong passes.
An exclusion criterion would invalidate the golden, because a correct response over-delivers
anyway, and the battery proves both directions.

## The registered paths

| Path | What the run does | Rows | Total it prints | Score |
|---|---|---|---|---|
| P0 | the July close method rolled forward: the HRIS report's rows and balances, the loaded tiers and rates, contractors and ended records inside, the two unloaded hires outside | 57 | $119,758.03 | 1 of 143, 0.7% |
| P1 | the HRIS report with the population fixed: 52 rows, balances uncapped, the loaded tiers and rates | 52 | $111,455.78 | 19 of 143, 13.3% |
| P2 | P1 with the 40.0-hour cap applied at 06/30/2026 | 52 | $90,983.94 | 76 of 143, 53.1% |
| P3 | P2 with tiers from the archive's service dates, the rehire unbridged, the tier change not timed, the rates as loaded | 52 | $92,804.10 | 100 of 143, 69.9% |
| P4 | P3 with the two signed pay changes applied | 52 | $92,934.50 | 107 of 143, 74.8% |
| P5 | P4 with the rehire bridged and the tier change timed; the step and the part-time schedule still missed | 52 | $92,789.47 | 119 of 143, 83.2% |
| P6 | the heal | 52 | $92,739.54 | 143 of 143, 100.0% |

## The graded cells, from the world's own bytes

| # | Employee | Cell | The world gives | The load carries | Moves | Weight |
|---|---|---|---|---|---|---|
| 1 | Mikelle Hosana, TRT-0005 | balance | 64.62 hours | 117.12 hours | $4,732.82 | 7 |
| 2 | Krystale Jumawan, TRT-0009 | balance | 64.62 hours | 108.62 hours | $2,934.04 | 7 |
| 3 | Jessica Ko, TRT-0012 | balance | 18.46 hours | 49.96 hours | $2,671.44 | 7 |
| 4 | Marisela Thornbury, TRT-0018 | balance | 60.00 hours | 87.87 hours | $2,322.05 | 7 |
| 5 | Edith Bustamante, TRT-0021 | balance | 42.46 hours | 76.46 hours | $1,982.79 | 6 |
| 6 | Rohan Iyer, TRT-0014 | balance | 58.46 hours | 84.46 hours | $1,958.75 | 6 |
| 7 | Maeve Oyinlola, TRT-0023 | balance | 58.46 hours | 78.96 hours | $1,526.66 | 6 |
| 8 | Zephyr Adebayo, TRT-0031 | balance | 26.46 hours | 38.46 hours | $930.00 | 6 |
| 9 | Emeka Thorsen, TRT-0029 | balance | 50.46 hours | 67.46 hours | $828.75 | 6 |
| 10 | Ilse Van der Kolk, TRT-0040 | balance | 58.46 hours | 67.96 hours | $805.67 | 6 |
| 11 | Samuel Burkenham, TRT-0071 | balance | 51.87 hours | 39.56 hours | $479.38 | 5 |
| 12 | Priyamvada Raghunath, TRT-0051 | balance | 6.71 hours | 0.56 hours | $383.78 | 5 |
| 13 | Wren Takahashi-Bell, TRT-0079 | balance | 24.96 hours | 18.81 hours | $353.63 | 5 |
| 14 | Callum Oyelaran, TRT-0058 | balance | 40.96 hours | 34.81 hours | $280.15 | 5 |
| 15 | Desmond Achterberg, TRT-0083 | balance | 18.71 hours | 12.56 hours | $275.27 | 5 |
| 16 | Simone Okonkwo, TRT-0153 | balance | 6.15 hours | 0.00 hours | $272.02 | 5 |
| 17 | Simone Okonkwo, TRT-0153 | rate | $44.2308 | no record | $272.02 | 5 |
| 18 | Oren Kastellanos, TRT-0043 | balance | 34.46 hours | 31.81 hours | $124.03 | 4 |
| 19 | Yolanda Featherstone, TRT-0088 | rate | $56.7308 | $50.0000 | $88.91 | 4 |
| 20 | Rafael Ibarra, TRT-0155 | balance | 3.08 hours | 0.00 hours | $83.37 | 4 |
| 21 | Rafael Ibarra, TRT-0155 | rate | $27.0673 | no record | $83.37 | 4 |
| 22 | Beatriz Quintanilla, TRT-0141 | balance | 29.60 hours | 33.06 hours | $79.58 | 3 |
| 23 | Belaviv Luk, TRT-0117 | rate | $71.2500 | $66.3462 | $41.49 | 3 |
| 24 | Delphine Marchetti, TRT-0096 | rate | $29.3269 | $27.8846 | $29.65 | 3 |

## The rubric, row by row

| # | Wt | Type | Primary | Criterion | Explanation |
|---|---|---|---|---|---|
| 1 | 1 | Objective Compliance | No | States that a Wiki.js page titled PTO Liability - 08/31/2026 is published. | One page under that title is what the request asks for in Wiki.js, so it exists with its published flag set. |
| 2 | 10 | Expert Assessment | Yes | States, on the PTO liability page, a total dollar liability of $92,739.54. | The cutover memo caps carryover at 40.0 hours, accrues four posted periods at the tier over 26 and values each balance at the rate on file over 2,080. The 52 rows sum to $92,739.54, or $92,772.88 rounding each posting. |
| 3 | 8 | Expert Assessment | Yes | States, on the PTO liability page, total PTO hours of 1,522.17. | The 52 current employees hold 1,522.17 hours at 08/31/2026 once the cutover memo's cap runs and four posted periods accrue by adjusted service date. The HRIS report's columns add to 1,751.71. |
| 4 | 7 | Expert Assessment | Yes | States, on the PTO liability page, a balance of 64.62 hours for Mikelle Hosana, TRT-0005. | Hosana carries 117.12 hours on the HRIS report and the archive holds 92.50 at 06/30/2026. The cutover memo caps carryover at 40.0 hours, and four periods at the 160-hour tier add 24.6152. |
| 5 | 7 | Expert Assessment | Yes | States, on the PTO liability page, a balance of 64.62 hours for Krystale Jumawan, TRT-0009. | Jumawan carries 108.62 hours on the HRIS report and the archive holds 84.00 at 06/30/2026. The cutover memo caps carryover at 40.0 hours, and four periods at the 160-hour tier add 24.6152. |
| 6 | 7 | Expert Assessment | Yes | States, on the PTO liability page, a balance of 18.46 hours for Jessica Ko, TRT-0012. | Ko carries 49.96 hours on the HRIS report and the archive holds 71.50 at 06/30/2026. The cutover memo caps carryover at 40.0 hours, and four periods at the 120-hour tier add 18.4616. |
| 7 | 7 | Expert Assessment | Yes | States, on the PTO liability page, a balance of 60.00 hours for Marisela Thornbury, TRT-0018. | The archive dates Thornbury's service from 08/09/2021 and her capped opening is 40.00 hours. She reaches five years on 08/09/2026 inside the fourth posted period, so the cutover memo accrues three periods of 4.6154 hours and one of 6.1538. |
| 8 | 6 | Expert Assessment | Yes | States, on the PTO liability page, a balance of 42.46 hours for Edith Bustamante, TRT-0021. | Bustamante carries 76.46 hours on the HRIS report and the archive holds 58.50 at 06/30/2026. The cutover memo caps carryover at 40.0 hours, and four periods at the 120-hour tier add 18.4616. |
| 9 | 6 | Expert Assessment | Yes | States, on the PTO liability page, a balance of 58.46 hours for Rohan Iyer, TRT-0014. | Iyer carries 84.46 hours on the HRIS report and the archive holds 66.00 at 06/30/2026. The cutover memo caps carryover at 40.0 hours, and four periods at the 120-hour tier add 18.4616. |
| 10 | 6 | Expert Assessment | Yes | States, on the PTO liability page, a balance of 58.46 hours for Maeve Oyinlola, TRT-0023. | Oyinlola carries 78.96 hours on the HRIS report and the archive holds 60.50 at 06/30/2026. The cutover memo caps carryover at 40.0 hours, and four periods at the 120-hour tier add 18.4616. |
| 11 | 6 | Expert Assessment | Yes | States, on the PTO liability page, a balance of 26.46 hours for Zephyr Adebayo, TRT-0031. | Adebayo carries 38.46 hours on the HRIS report and the archive holds 52.00 at 06/30/2026. The cutover memo caps carryover at 40.0 hours, and four periods at the 120-hour tier add 18.4616. |
| 12 | 6 | Expert Assessment | Yes | States, on the PTO liability page, a balance of 50.46 hours for Emeka Thorsen, TRT-0029. | Thorsen carries 67.46 hours on the HRIS report and the archive holds 57.00 at 06/30/2026. The cutover memo caps carryover at 40.0 hours, and four periods at the 120-hour tier add 18.4616. |
| 13 | 6 | Expert Assessment | Yes | States, on the PTO liability page, a balance of 58.46 hours for Ilse Van der Kolk, TRT-0040. | Kolk carries 67.96 hours on the HRIS report and the archive holds 49.50 at 06/30/2026. The cutover memo caps carryover at 40.0 hours, and four periods at the 120-hour tier add 18.4616. |
| 14 | 5 | Expert Assessment | Yes | States, on the PTO liability page, a balance of 51.87 hours for Samuel Burkenham, TRT-0071. | Burkenham's archive service bridges a 241-day break under the handbook's 7.6, five completed years at 08/31/2026. Four posted periods accrue at the 160-hour tier, so 51.87 hours stand against the HRIS report's 39.56. |
| 15 | 5 | Expert Assessment | Yes | States, on the PTO liability page, a balance of 6.71 hours for Priyamvada Raghunath, TRT-0051. | Raghunath reads the 80-hour tier in BambooHR and the archive dates the hire 05/03/2022, four completed years at 08/31/2026. The cutover memo accrues at the 120-hour tier, so 6.71 hours stand against the HRIS report's 0.56. |
| 16 | 5 | Expert Assessment | Yes | States, on the PTO liability page, a balance of 24.96 hours for Wren Takahashi-Bell, TRT-0079. | Takahashi-Bell reads the 80-hour tier in BambooHR and the archive dates the hire 02/06/2023, three completed years at 08/31/2026. The cutover memo accrues at the 120-hour tier, so 24.96 hours stand against the HRIS report's 18.81. |
| 17 | 5 | Expert Assessment | Yes | States, on the PTO liability page, a balance of 40.96 hours for Callum Oyelaran, TRT-0058. | Oyelaran reads the 80-hour tier in BambooHR and the archive dates the hire 09/12/2022, three completed years at 08/31/2026. The cutover memo accrues at the 120-hour tier, so 40.96 hours stand against the HRIS report's 34.81. |
| 18 | 5 | Expert Assessment | Yes | States, on the PTO liability page, a balance of 18.71 hours for Desmond Achterberg, TRT-0083. | Achterberg reads the 80-hour tier in BambooHR and the archive dates the hire 06/19/2023, three completed years at 08/31/2026. The cutover memo accrues at the 120-hour tier, so 18.71 hours stand against the HRIS report's 12.56. |
| 19 | 5 | Expert Assessment | Yes | States, on the PTO liability page, a balance of 6.15 hours for Simone Okonkwo, TRT-0153. | Okonkwo started 07/22/2026 on the roster and the crosswalk marks TRT-0153 Never Loaded. The cutover memo accrues each posted period at the 80-hour tier, 3.0769 hours a period since the start. |
| 20 | 5 | Expert Assessment | Yes | States, on the PTO liability page, an hourly rate of $44.2308 for Simone Okonkwo, TRT-0153. | Okonkwo's roster salary of $92,000.00 over 2,080 is $44.2308 an hour, and the crosswalk marks TRT-0153 Never Loaded with no BambooHR rate against it. |
| 21 | 4 | Expert Assessment | Yes | States, on the PTO liability page, a balance of 34.46 hours for Oren Kastellanos, TRT-0043. | Kastellanos carries 31.81 hours on the HRIS report and the archive holds 43.50 at 06/30/2026. The cutover memo caps carryover at 40.0 hours, and four periods at the 120-hour tier add 18.4616. |
| 22 | 4 | Expert Assessment | Yes | States, on the PTO liability page, an hourly rate of $56.7308 for Yolanda Featherstone, TRT-0088. | The signed promotion approval sets Featherstone's salary at $118,000.00 from 06/16/2026 and the handbook's 3.2 puts the signed document over the record. BambooHR carries $104,000.00. $118,000.00 over 2,080 is $56.7308. |
| 23 | 4 | Expert Assessment | Yes | States, on the PTO liability page, a balance of 3.08 hours for Rafael Ibarra, TRT-0155. | Ibarra started 08/03/2026 on the roster and the crosswalk marks TRT-0155 Never Loaded. The cutover memo accrues each posted period at the 80-hour tier, 3.0769 hours a period since the start. |
| 24 | 4 | Expert Assessment | Yes | States, on the PTO liability page, an hourly rate of $27.0673 for Rafael Ibarra, TRT-0155. | Ibarra's roster salary of $56,300.00 over 2,080 is $27.0673 an hour, and the crosswalk marks TRT-0155 Never Loaded with no BambooHR rate against it. |
| 25 | 3 | Expert Assessment | Yes | States, on the PTO liability page, a balance of 29.60 hours for Beatriz Quintanilla, TRT-0141. | The schedule change form moves Quintanilla from 25 to 32 hours a week on 08/10/2026 and the handbook's 2.2 accrues part-time hours pro-rata under 30. The HRIS report accrues her at a full week and shows 33.06 hours. |
| 26 | 3 | Expert Assessment | Yes | States, on the PTO liability page, an hourly rate of $71.2500 for Belaviv Luk, TRT-0117. | The signed amendment sets Luk's salary at $148,200.00 from 05/16/2026 and the archive recorded it. BambooHR carries the loaded $138,000.00, and $148,200.00 over 2,080 is $71.2500. |
| 27 | 3 | Expert Assessment | Yes | States, on the PTO liability page, an hourly rate of $29.3269 for Delphine Marchetti, TRT-0096. | Marchetti's offer letter carries the Support Specialist step on each anniversary and the handbook's 5.4 sets it at $3,000.00. Her anniversary fell 08/17/2026, so the rate on file is $61,000.00, $29.3269 an hour. |

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
2. A cell is read on the row keyed by the employee ID, on a whole-cell match, never a substring.
3. A balance is graded to half a hundredth of an hour and an hourly rate to half a cent. A
   response may print more decimals than that and is read at the precision it prints.
4. The two totals are graded to half a dollar and a twentieth of an hour. The request carries no
   Form section, so a response that rounds what it states has still stated it, and no registered
   path comes within either band.
5. Extra rows, extra columns and extra tables cost nothing. Only what the criterion names is read.
6. The page is the one row of the `pages` table whose title matches. Two rows under the title
   fail every page row, because the request asks for one page.

## Predictions, dated 09/22/2026, before any v2 run

1. A response that copies the HRIS time off report scores 1 of 143, the page row alone.
2. The gate fails on any response that misses the cap, which is every trajectory measured in
   this world so far, ten of ten.
3. The two unloaded hires are the cells this tier gets right: nine of the ten measured
   trajectories created them and computed both balances, so rows on them are earned, not free.
4. A Gemini set will land under 25%. The ten trajectories already measured against T2's wider
   ask read 8.3% and 14.7% under this rubric.
5. If a set lands over 60%, the lever is measured insufficient in this world for this tier and
   the package retires. The rubric is not rescoped around whatever failed.

## Open items

1. **A v2 run set.** Five Gemini 3.8 Flash trajectories against this memo, and three GPT Sol
   5.6 for the record. Nothing here has been run against v2's own ask yet.
2. **v2's task data id.** The memo is a new 1.4 upload, so it mints one. `TASK_SNAP` carries
   the id measured on 09/21/2026 until the first v2 export is read.
3. **The wiki target app.** T2's first platform grading, 09/21/2026, failed every wiki row on a
   page the app had returned. Two causes fit and one test run separates them; the record is in
   `../HR_Troutly_T2_pto_liability_close/qc/findings/platform_grading_09-21-2026.md`. v2's rows
   are grounded on the same service, so the answer carries straight over.
4. **The import does not populate Tags, Reference Artifacts or Grading Target.** Measured on T2
   and unchanged. They are entered by hand from `build/rubric_plan.csv`.
