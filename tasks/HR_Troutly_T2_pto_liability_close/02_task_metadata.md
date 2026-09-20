# Task metadata - PTO Liability Schedule and BambooHR PTO Records (T2)

## Identity

| Field | Value |
|---|---|
| **Package** | `HR_Troutly_T2_pto_liability_close`, the second HR 74 ask, built 09/20/2026 at the prompt half on the measured record of T1 and T1 v2: a determination the tier has to get wrong, not a lookup it heals |
| **Task name** | `PTO Liability Schedule and BambooHR PTO Records`. The house convention names a task from its output: one wiki page and the BambooHR rows brought to it |
| **World** | HR 74 - Troutly Analytics, Inc. (HR), `filesystem/` (69 files) and `apps_data/` (31 seed tables), the bytes of `HR 74.zip` held in place by `world/checks/world_manifest.py`. **No world byte moves** |
| **Anchor date** | 08/31/2026, the measurement date the request sets; the request dates itself 09/01/2026 |
| **Expected output** | **Make New App Data** and **Edit Existing App Data**: one page published in Wiki.js, and BambooHR policy and balance rows changed. The picker's field is a list |
| **1.5) Expected Output Files** | Nothing. The deliverable is app state and no file |
| **Grading target** | None. Every planned row is App DB Programatic, on the `wiki_js` `pages` table and the `bamboohr` `EmployeePolicy` and `TimeOffBalance` tables |
| **Apps** | BambooHR (read and written), Wiki.js (written), Greenhouse (read). Three apps |
| **Task input** | One file through **1.4) Additional task files on the Filesystem target**: `00_task_input_pto_liability_request.pdf`, 2,798 bytes, md5 `d9f3b3830c7b2f0bf5c3c1ef8395b11b`. It uploads as `pto_liability_request.pdf`. `build/task_input_source.md` records what it carries and what it withholds |
| **Golden output** | Not built at the prompt half. `build/schedule_preview.csv` is the schedule the golden page will be generated from, md5 recomputed on every build |
| **Show Your Work** | Not built at the prompt half |
| **Rubric import** | Not built at the prompt half. The task data id is the sentinel `SNAPSHOT_ID_NOT_YET_READ` until it is read off the first export; the world id is T1's, `snap_c6f6a0879f3d47a19048ee80d7529157` |
| **Rubric plan** | **21 planned rows, 87 points, 1 gate**, in `build/rubric_plan.csv` and below, the registered paths scored against it by `build/build_package_artifacts.py` on every build. Verifier code, the battery and the import are built only if the first run set fails, by the decision of 09/20/2026 |
| **Human time estimate** | 14 hours |
| **Spec 2A** | **Unmeasured, predicted.** The registered failing paths score 29 of 87, 33.3% and 42 of 87, 48.3%; the free base is 5 of 92, 5.4%; the registered Gemini mean is 45%, with the decision rule and the honest note in `06_failure_analysis.md`, dated before any run |

## The prompt

> Complete the request (using the HRIS time off report, the BambooHR records, and the rest of the Troutly files) about the August 2026 close by publishing the Wiki.js page PTO Liability - 08/31/2026 and updating the BambooHR PTO records to match it.

Asserted against the builder's `PROMPT`. `01_prompt.md` carries the shape reasoning.

## The determination, and the arithmetic behind the weights

Three families, and the share of the 87 points each carries:

| Family | Rows | Points | Share |
|---|---|---|---|
| **The determination.** The liability at 08/31/2026: the cap, the tiers from adjusted service dates with the rehire bridged and the anniversary timed, the signed rates and the step, the part-time schedule, the population, the posted periods and the usage, and the total they give | 5 to 18 | 70 | 80.5% |
| **BambooHR brought to the schedule.** The six policies, the 52 balances, the two rows created | 19 to 21 | 12 | 13.8% |
| **The page and its form.** Published, 52 rows keyed by ID, the form, the summary | 1 to 4 | 5 | 5.7% |

**The registered paths**, each the golden with rules dropped, recomputed by the builder:

| Path | What the run does | Rows | Total it prints | Score |
|---|---|---|---|---|
| P0 | the July close method rolled forward: the HRIS report's rows and balances, the loaded tiers and rates, contractors and ended records inside, the two unloaded hires outside | 57 | $119,758.03 | 8 of 87, 9.2% |
| P1 | the HRIS report with the population fixed: 52 rows, balances uncapped, the loaded tiers and rates | 52 | $111,455.78 | 24 of 87, 27.6% |
| P2 | P1 with the 40.0-hour cap applied at 06/30/2026 | 52 | $90,983.94 | 24 of 87, 27.6% |
| P3 | P2 with tiers from the archive's service dates, the rehire unbridged, the tier change not timed, the rates as loaded | 52 | $92,804.10 | 29 of 87, 33.3% |
| P4 | P3 with the two signed pay changes applied | 52 | $92,934.50 | 42 of 87, 48.3% |
| P5 | P4 with the rehire bridged and the tier change timed; the step and the part-time schedule still missed | 52 | $92,789.47 | 65 of 87, 74.7% |
| P6 | the heal | 52 | $92,739.54 | 87 of 87, 100.0% |

**Why the gate is the total.** Finance books one number. A schedule that misses any one rule
prints a wrong total, and the ask is the total; a run that applies the explicit rules and misses
the implicit ones scores its rows and not the gate. The gate accepts the total under either
rounding convention the cutover memo permits, sum-then-round ($92,739.54) and post-by-post
($92,772.88), because the memo says per-period accrual is carried to four decimals and posted
balances to two and does not say which the measurement reads.

**Why the free base is 5.7%.** T1 v2 measured the fields a run prints on any path at
8% and the population healed; here the population is a sub-step and carries 12 points inside the
determination family, not the free base.

**Considered and rejected.** A row on Grayson Oshimoto's 07/31/2026 payout: not owed under the
notice rule and paid anyway, but he is out of the liability either way and the row would grade
a payroll surface. A row per employee: 52 rows at 1 point would let the explicit rules carry the
score. A row on the July close's $90,862.13 being wrong: the memo asks for the August number and
names no reconciliation, by the T1 v2 lesson. A row on the reconciling items: the same.

## Graded values and their sources

| Value | Source |
|---|---|
| 1,522.17 hours and $92,739.54 across 52 current employees at 08/31/2026 ($92,772.88 post-by-post) | `build/schedule_preview.csv`, every input below |
| The rules: biweekly accrual at the tier over 26 posted on the pay date, the 40.0-hour cap at 06/30/2026, tiers by adjusted service date changing in the period containing the anniversary, the rate on file over 2,080, ended employees out | `HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx`; `HR/Policies/Employee_Handbook_v3.pdf` sections 1.3 and 7 |
| Four posted periods, pay dates 07/10, 07/24, 08/07 and 08/21/2026 | `HR/Payroll/2026-06-25_Payroll_Procedures_Memo.docx` |
| The 06/30/2026 balances, 11 of them over 40.0 and capped | `SplinterHR_Final_Archive_2026-07-28.xlsx` Balances; the HRIS report and the load carry them uncapped |
| The 52 current employees, the four contractors and three ended records out, the two unloaded hires in | `2026-08-31_Master_Employee_Roster.xlsx`; `2026-08-28_Employee_ID_Crosswalk.xlsx`; `apps_data/bamboohr/Employee.csv` |
| Adjusted service dates: the archive's original hire dates on nine records loaded as 07/01/2026; TRT-0071 bridged from 04/22/2024 across a 241-day break to 03/08/2021 | The archive Employees tab; the rehire offer; the historical offer letters; handbook 7.6 |
| Tiers: 18 at 80, 28 at 120, 6 at 160; six BambooHR policies wrong; TRT-0018 at 120 for three periods and 160 for the fourth | `apps_data/bamboohr/EmployeePolicy.csv` against the service dates |
| Rates: $118,000.00 for TRT-0088, $148,200.00 for TRT-0117, $61,000.00 for TRT-0096; every other rate as BambooHR carries it | The promotion approval; the amendment; Marchetti's offer letter and handbook 5.4; `apps_data/bamboohr/Employee.csv` |
| TRT-0141's accrual at 25 hours for three periods and 32 for the fourth | `2026-08-10_Schedule_Change_TRT-0141.pdf`; handbook 2.2 |
| 560 hours of approved time off in July, 24 requests | `apps_data/bamboohr/TimeOffRequest.csv` |

**Every graded value recomputes from the world's own bytes on every build** by `check_world()`,
which reads each rule off the document that states it and each amount off the document that
signs it.

## The page, for a reviewer

**PTO Liability - 08/31/2026.** A summary with 52 employees, 1,522.17 hours and $92,739.54; one
table of 52 rows, Employee ID, Name, Department, Annual PTO tier, PTO balance at 08/31/2026,
Hourly rate and Liability, ordered as the run likes. Then BambooHR: six policy assignments
changed, 52 balances set to the schedule, two balance rows created.

## Required world files

Twenty-two world files are cited by the plan. That is above the guide's general ceiling of ten,
and it is the ask: the rules sit in three documents, the records in six, the traps in the rest,
and each file below decides at least one planned row or carries a number a failing path prints.

| # | Path | What it supplies |
|---|---|---|
| 1 | `/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx` | The rules from 07/01/2026: biweekly accrual at the tier over 26 posted on the pay date, the 40.0-hour cap at 06/30/2026, tiers by adjusted service date with the change in the period containing the anniversary, valuation at the rate on file over 2,080, ended employees out |
| 2 | `/HR/Policies/Employee_Handbook_v3.pdf` | Section 7 incorporates the memo; 2.2 part-time accrual pro-rata under 30 hours; 7.6 service bridges under 365 days; 5.4 the $3,000.00 Support Specialist step; 3.2 and 1.3 the signed document over the record; 7.3 totals are the sum of the rounded rows |
| 3 | `/HR/Policies/PTO_Policy_2025.docx` | The superseded policy: monthly accrual on the 1st, unlimited carryover |
| 4 | `/HR/Data/HRIS_Time_Off_Report_2026-08-31.xlsx` | The tempting number: 57 rows, every balance uncapped at the loaded tier, four contractors and three ended employees on it, the two unloaded hires off it |
| 5 | `/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx` | The 06/30/2026 balances for 51 actives, the original hire and rehire dates, the salary history with the two signed changes and the 08/25/2023 termination behind the rehire |
| 6 | `/HR/Data/2026-08-31_Master_Employee_Roster.xlsx` | The 52 current employees with department, scheduled hours, FLSA status and the loaded 07/01/2026 dates on nine migrated records |
| 7 | `/HR/Data/2026-08-28_Employee_ID_Crosswalk.xlsx` | Terminated on the three ended records, Never Loaded on the two unloaded hires |
| 8 | `/HR/Data/Migration/HRIS_Import_Load_2026-07-01.csv` | The 56 records loaded on 07/01/2026 with their hire dates and uncapped balances |
| 9 | `/HR/Data/Migration/2026-06-24_Field_Mapping_Workbook.xlsx` | HireDate to 07/01/2026 and PTOBalance carried with no cap: the load's own specification |
| 10 | `/HR/Data/Migration/2026-07-22_Migration_Closeout_Memo.docx` | The claim that hire dates and salaries were spot-checked clean |
| 11 | `/HR/Payroll/2026-06-25_Payroll_Procedures_Memo.docx` | The biweekly calendar: pay dates 07/10, 07/24, 08/07 and 08/21/2026 posted by 08/31/2026, 09/04/2026 not |
| 12 | `/HR/Payroll/HRIS_Payroll_History_2026-07-01_to_2026-08-31.xlsx` | The rates payroll actually paid since cutover, the loaded ones, and the 07/31/2026 off-cycle |
| 13 | `/Finance/Close/2026-07_Close_Package.xlsx` | The requester's own method: the HRIS balance, tier and rate per row, three ended employees inside, $90,862.13 booked |
| 14 | `/HR/Comp/Promotions/2026-06-10_Promotion_Approval_TRT-0088.docx` | $118,000.00 from 06/16/2026, signed by the manager and the CEO |
| 15 | `/HR/Comp/Amendments/2026-05-12_Comp_Amendment_TRT-0117.pdf` | $148,200.00 from 05/16/2026, signed |
| 16 | `/HR/People/Offer_Letters/2024-04-08_Rehire_Offer_TRT-0071.pdf` | The 04/22/2024 rehire that, with the archive's 08/25/2023 termination, bridges under 365 days |
| 17 | `/HR/People/Offer_Letters/Historical_Offer_Letters_2020-2026.pdf` | The original offers of the nine migrated records with their true start dates, and Marchetti's letter carrying the anniversary step |
| 18 | `/HR/Benefits/2026-08-10_Schedule_Change_TRT-0141.pdf` | 25 hours to 32 hours effective 08/10/2026 |
| 19 | `/Recruiting/Offers/2026-07-02_Offer_TRT-0153_SIGNED.pdf` | Okonkwo's $92,000.00 and the start date that moved to 07/22/2026 |
| 20 | `/Wiki/Paid_Time_Off.md` | The page the Office Manager left: monthly accrual, unlimited carryover, last edited 01/2025 |
| 21 | `/Wiki/Compensation_Authority.md` | The signed document over the HRIS; the step increase's mechanics |
| 22 | `/Wiki/Onboarding_Data_Standards.md` | The adjusted service date defaulted to the hire date, the rehire bridging rule, and the claim that the loaded records need no validation |
| App | `bamboohr/Employee.csv`, `bamboohr/TimeOffBalance.csv`, `bamboohr/TimeOffPolicy.csv`, `bamboohr/TimeOffRequest.csv`, `bamboohr/EmployeePolicy.csv`, `bamboohr/TimeOffType.csv` | The 57 active rows and their loaded rates, the balances and policies the run corrects, the per-period rates, the 24 requests |
| App | `greenhouse/applications.csv`, `greenhouse/candidates.csv` | The two hires with no BambooHR row |
| App | `wiki_js/Page.csv` | The ten seeded pages, three of them the wrong rules, and the table the deliverable lands in |

**Every world file is selected on its plain filesystem path**, and the app tables are selected
as app tables, one selection per line, no `apps_data/` prefix, no wildcard. The twenty-two world
files:

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
```

and the nine app tables beside them:

```
bamboohr/Employee.csv
bamboohr/TimeOffBalance.csv
bamboohr/TimeOffPolicy.csv
bamboohr/TimeOffRequest.csv
bamboohr/EmployeePolicy.csv
bamboohr/TimeOffType.csv
greenhouse/applications.csv
greenhouse/candidates.csv
wiki_js/Page.csv
```

## Fences - what this package deliberately does not grade

- **Grayson Oshimoto's 07/31/2026 payout**, 88.0 hours at $38.75 paid on eleven days' notice
  against a rule that pays on fourteen: a payroll surface, and he is out of the liability.
- **The underpayment of TRT-0088 and TRT-0117 since 07/10/2026**, four checks each at the loaded
  rate: a payroll surface the memo fences with "payroll changes".
- **TRT-0021's 74.0 on the report against 58.5 on the archive**: moot under the cap.
- **Benefits eligibility from the schedule change**, and the September compensation cycle.
- **The three ended employees still drawing pay** and the contractors' PTO rows in BambooHR: not
  on the schedule, not asked.
- **Page paths, headings, column order, row order and the summary's wording.** No planned row
  reads any of them.
- **Every clause of the request that fences work out.** `check_asks()`, when built, bars a row
  from hanging on any.

## The rival readings, answered

**The HRIS report's balance as the balance.** It is the system of record's own number and it is
what the July close used. But the cutover memo caps carryover at 40.0 hours at 06/30/2026, the
field mapping workbook says the balances were loaded with no cap, and eleven rows on the report
exceed the cap.

**The July close's method as the method.** Prepared by the requester, tied to the balance sheet.
It applies the HRIS tier, the HRIS rate and the uncapped HRIS balance and carries three ended
employees. The memo asks for the August number and names the July detail as the thing replaced,
not the rule.

**Monthly accrual and unlimited carryover.** The wiki page and the 2025 policy say so. The
cutover memo replaces the 2025 policy from 07/01/2026, the handbook incorporates the memo and
says wiki pages do not set policy, and the page was last edited 01/2025 by the Office Manager who
left.

**The loaded service dates.** Nine migrated records read 07/01/2026 on the roster and in BambooHR.
The archive, the historical offer letters and the field mapping workbook say the load set
HireDate to the cutover date; the onboarding standards page says the adjusted service date
defaults to the hire date and bridges across a rehire under 365 days.

**The rehire at his rehire date.** TRT-0071 rehired 04/22/2024 after a termination on 08/25/2023,
241 days; the handbook's 7.6 bridges service under 365 days to the original hire date of
03/08/2021, so he is at five years and the 160-hour tier, not the 80 BambooHR gives him.

**TRT-0018 at 160 from cutover.** BambooHR assigned the 5-plus policy by hire date at load. She
reached five years on 08/09/2026; the memo puts the change in the period containing the
anniversary, so three periods accrue at 120 and one at 160.

**The recorded rates for TRT-0088 and TRT-0117.** BambooHR, the roster and every register carry
$104,000.00 and $138,000.00. The signed promotion and the signed amendment, effective 06/16/2026
and 05/16/2026, carry $118,000.00 and $148,200.00; SplinterHR recorded both; the load dropped
them. Handbook 3.2 and 1.3 and the Compensation Authority page put the signed document over the
record until the record is corrected.

**TRT-0096 at $58,000.00.** Her signed offer letter carries the Support Specialist step, effective
in the pay period containing her anniversary, 08/17/2026; handbook 5.4 sets it at $3,000.00 with
no separate approval. The rate on 08/31/2026 is $61,000.00 by the signed letter and the policy,
and the record has not been processed. The row carries 3 points for that reason.

**TRT-0141 at 32 hours.** The roster carries her current schedule. The schedule change form
moves her from 25 to 32 hours effective 08/10/2026; the handbook accrues part-time pro-rata to
scheduled hours under 30. Three periods at 25 hours and the fourth at 32, by the same rule the
memo applies to a tier change: the schedule in effect at the period's close.

**Five posted periods.** Handbook 7.1 says accrual is credited at the close of the pay period,
and the fifth period closed 08/30/2026. The memo says accrual posts on the pay date, 09/04/2026,
and the dated memo governs the section it replaces. BambooHR's own balances carry four.

**A prorated first period for a mid-period start.** The memo accrues per pay period and BambooHR
credits the period containing the start in full, as it did for TRT-0150 and TRT-0154. Okonkwo
accrues two periods from 07/22/2026 and Ibarra one from 08/03/2026.

## Reviewer decision rules, recorded in advance

Every planned row is read from the Wiki.js pages table or the BambooHR tables and nothing else.

1. **The existence row (1)** passes when a page carrying the exact title, dashes normalised, is
   published. A draft fails.
2. **The population row (2)** passes when the ID-keyed rows are the roster's 52 and no other.
3. **The form row (3)** reads two decimals on hours, four on rates, cents on dollars, and a total
   equal to the sum of the rows within one cent.
4. **The gate (5)** passes on $92,739.54 or $92,772.88 within one cent, in the summary or the total
   row.
5. **The hours rows (6, 9, 13, 17, 18)** pass on the golden value under either rounding
   convention, within 0.005 of an hour.
6. **The tier rows (7, 8, 16)** read the tier cell as 80, 120 or 160, a policy name accepted.
7. **The rate rows (10, 11, 12)** read the hourly rate cell to four decimals, within 0.00005.
8. **The absence rows (14, 15)** pass when the ID sits on no table that carries at least 40 keyed
   rows.
9. **The BambooHR rows (19, 20, 21)** read `EmployeePolicy` and `TimeOffBalance` in the grading
   snapshot: the policy name per employee; the balance within 0.005 of the schedule's under
   either convention; a row present for TRT-0153 and TRT-0155.

## Explicit asks and the row that grades each

Every clause below is a verbatim substring of the request memo, asserted when the rubric is built,
and the row counts foot to the plan.

| Clause of the request, verbatim | Kind | Rows |
|---|---|---|
| *One page published in Wiki.js, PTO Liability - 08/31/2026* | deliverable | 1 |
| *employee ID, name, department, annual PTO tier in hours, PTO balance in hours at 08/31/2026, hourly rate, and dollar liability* | deliverable | 12 |
| *A current employee is anyone employed by Troutly on 08/31/2026* | deliverable | 4 |
| *the number of employees on the schedule, the total hours, and the total dollar liability* | deliverable | 1 |
| *the PTO policy and the PTO balance in BambooHR are the ones the schedule shows* | deliverable | 3 |
| *Hours to two decimals. Hourly rates to four decimals. Dollars to the cent. The total is the sum of the rows.* | **form** | 1 |
| *Payroll changes, the September compensation cycle and benefits are no part of this request* | fence | none, by kind |
| *Change nothing in Greenhouse* | fence | none, by kind |

**Six asking clauses, 21 planned rows, two fences that carry none.** Rows 4 and 5 hang on the
summary clause; the gate is the summary's total.

## The rubric plan (generated by the builder; `check_docs()` holds this table to it)

| # | Family | Wt | Gate | Criterion |
|---|---|---|---|---|
| 1 | free | 1 | - | States that a Wiki.js page titled PTO Liability - 08/31/2026 is published. |
| 2 | free | 2 | - | States, on the PTO liability page, the 52 current employees at 08/31/2026 as the only employee rows. |
| 3 | free | 1 | - | States, on the PTO liability page, hours to two decimals, hourly rates to four decimals, dollars to the cent and a total equal to the sum of the rows. |
| 4 | free | 1 | - | States, on the PTO liability page, a summary with the employee count, the total hours and the total dollar liability. |
| 5 | determination | 10 | Critical value | States, on the PTO liability page, a total dollar liability of $92,739.54. |
| 6 | determination | 5 | - | States, on the PTO liability page, an opening balance of 40.00 hours for each of the 11 employees whose 06/30/2026 balance exceeded 40.0 hours. |
| 7 | determination | 5 | - | States, on the PTO liability page, the 120-hour tier for TRT-0043, TRT-0051, TRT-0058, TRT-0079 and TRT-0083. |
| 8 | determination | 7 | - | States, on the PTO liability page, the 160-hour tier for Samuel Burkenham, TRT-0071, with service bridged to 03/08/2021. |
| 9 | determination | 6 | - | States, on the PTO liability page, an accrual of 20.0000 hours for Marisela Thornbury, TRT-0018, three periods at the 120-hour tier and one at 160. |
| 10 | determination | 7 | - | States, on the PTO liability page, an hourly rate of $56.7308 for Yolanda Featherstone, TRT-0088. |
| 11 | determination | 6 | - | States, on the PTO liability page, an hourly rate of $71.2500 for Belaviv Luk, TRT-0117. |
| 12 | determination | 3 | - | States, on the PTO liability page, an hourly rate of $29.3269 for Delphine Marchetti, TRT-0096. |
| 13 | determination | 4 | - | States, on the PTO liability page, a balance of 29.60 hours for Beatriz Quintanilla, TRT-0141. |
| 14 | determination | 4 | - | States, on the PTO liability page, no contractor row, CTR-2001 to CTR-2004. |
| 15 | determination | 4 | - | States, on the PTO liability page, no row for TRT-0037, TRT-0049, TRT-0064 or TRT-0006. |
| 16 | determination | 4 | - | States, on the PTO liability page, Simone Okonkwo, TRT-0153, and Rafael Ibarra, TRT-0155, at the 80-hour tier with accruals since their start dates. |
| 17 | determination | 3 | - | States, on the PTO liability page, a balance of 62.62 hours for Sora Jackson, TRT-0002, four posted periods at the 160-hour tier. |
| 18 | determination | 2 | - | States, on the PTO liability page, a balance of 22.87 hours for Michael Labeson, TRT-0001, with 40.00 hours of approved time off deducted. |
| 19 | bamboohr | 5 | - | States, in BambooHR, the PTO policy the schedule's tier gives for each of the 6 employees whose loaded policy differed. |
| 20 | bamboohr | 5 | - | States, in BambooHR, a PTO balance equal to the schedule's 08/31/2026 balance for every employee on the schedule. |
| 21 | bamboohr | 2 | - | States, in BambooHR, a PTO balance row for TRT-0153 and TRT-0155. |

Explanations, verifier specs, the golden page, the import and the battery are built from these
rows only if the first run set fails.

## Plan and model checkpoints - prompt-stage section 1.3

`08_section_1_3_step_plan.md` carries the fourteen-checkpoint table and the dependency chain.

## Human time estimate - 14 hours

| Stage | Hours | Result |
|---|---|---|
| 1. The request | 0.5 | The page, the columns, the definition, the summary, the BambooHR ask, the form, the fence |
| 2. The rules | 2.0 | The cutover memo against the 2025 policy, the wiki page and the handbook; the cap, the period, the tiers, the rate, the part-time and rehire rules, the step |
| 3. The population | 1.5 | 52 current employees against BambooHR's 57 |
| 4. The opening balances | 1.5 | The archive's 06/30/2026 balances against the report's, the cap applied to eleven |
| 5. The service dates and tiers | 3.0 | Nine loaded dates against the archive and the offer letters, the rehire bridged, the anniversary inside the window, the tier per period for 52 |
| 6. The rates | 1.5 | The two signed changes and the step against BambooHR and the registers |
| 7. The arithmetic | 2.0 | 52 rows at four decimals, two decimals and cents; the total |
| 8. The page and BambooHR | 2.0 | The page written and published; six policies and 52 balances set, two rows created; read back |

## Predictions, registered in advance (09/20/2026, before any run)

`06_failure_analysis.md` carries the registered paths, the registered Gemini mean of 45%, the
decision rule and the honest note. Under 40% on five Gemini runs the rubric half is built and the
package ships; 40% to 60% the package is held with the traces for the pod lead's call, never
rescoped around what failed; over 60% the lever is measured insufficient for this tier in this
world and the package retires.

## Platform state

Measured off the five Gemini exports of 09/20/2026: the task runs on the platform as `PTO Liability Request`, task version
17 at G1 and G3 and 18 at G2, G4 and G5, the builder's PROMPT verbatim, the 1.4 upload under task data id
`snap_45e68b376f2547dca61408b65d8ba774`, and it carries T1's twenty synth verifiers, which target
Approved Hiring View - August 2026 and Staffed Role View - August 2026. What each field has to hold:

| Field | Value |
|---|---|
| 1.1 Task name | `PTO Liability Schedule and BambooHR PTO Records`; the platform holds `PTO Liability Request` |
| 1.3 Step plan | The Checkpoints table in `08_section_1_3_step_plan.md`, held until the difficulty bar is measured, as v2's was |
| 1.4 Additional task files | `pto_liability_request.pdf`, 2,798 bytes, md5 `d9f3b3830c7b2f0bf5c3c1ef8395b11b`, target **Filesystem**. Confirm the upload by digest |
| 1.5 Expected Output Files | Nothing |
| Expected output type | Make New App Data and Edit Existing App Data |
| Files and data tables | 31 selected: the twenty-two world files and nine app tables above |
| Rubric | None of the plan's rows. The task carries T1's twenty synth verifiers, which target two pages this task never writes, so a platform grading of a T2 run is against those rows and says nothing. The import is built only if the set fails |
| Task-data snapshot | `snap_45e68b376f2547dca61408b65d8ba774`, read off G1 on 09/20/2026 and carried by the builder. The world snapshot is `snap_c6f6a0879f3d47a19048ee80d7529157` |

## Open items

1. **The task data id**: read off G1 on 09/20/2026, `snap_45e68b376f2547dca61408b65d8ba774`, carried
   by the builder. Closed.
2. **The first run set.** The five Gemini 3.8 Flash landed 09/20/2026: G1, G3 and G4 P1 row for
   row at 27.6%, G2 and G5 P1 less the two unloaded hires at 18.4%, mean 23.9%. Three GPT Sol 5.6
   are owed for the record. `qc/archive_run_set.py` and
   `qc/score_run_set.py` archive and score them from the output alone.
3. **The BambooHR time-off tools write the rows the plan reads**: measured on G1 and G3.
   `employees_create` returned ids 59 and 60 for TRT-0153 and TRT-0155, `time_off_assign_policy`
   returned the assignment and `time_off_update_balance` returned the new balance, through the
   toolbelt on G1 and through the shell on G3. Closed.
4. **The pages and BambooHR tables' shape in a grading snapshot**, still unmeasured. The exports
   carry no snapshot; the record rebuilds the BambooHR state from the app's own returned results.
5. **The rubric half.** The five Gemini runs read 23.9%: built next from `build/rubric_plan.csv`.
6. **The platform task's verifier set is T1's.** The twenty rows on the exports target the two T1
   pages. Before any platform grading is read, they have to be replaced by the plan's rows or removed.
   The prompt AutoQC round of 09/20/2026 raised the same mismatch and was disputed on the platform:
   the verifiers are not editable until the next task stage.
