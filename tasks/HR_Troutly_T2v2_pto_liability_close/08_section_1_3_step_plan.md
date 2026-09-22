# 08 - The section 1.3 step plan in the checkpoint form the guide asks for (T2 v2, 09/22/2026)

The field is a numbered **Checkpoints** table, one column headed "Checkpoint - what the model must
do". Thirteen rows, against T2's fourteen. The BambooHR half is out of the ask, so T2's step 13 is
gone and its read-back folds into the page. Steps 1 to 11 are unchanged work: the determination is
the same and the rules are in the same documents.

**The step count.** Predicted over 100 on the platform's count, the same prediction T2 registered.
T2's five runs of 09/20/2026 measured 209, 165, 213, 192 and 197 tool calls, one assistant turn
each, at 1,854 to 2,172 seconds. Those runs spent the count on reading the tree and building the
schedule: no run wrote BambooHR more than about a dozen times, and two wrote nothing that held. So
the narrower deliverable takes about a dozen calls off the top, not a hundred, and the honest
estimate for v2 is **28 to 35 minutes and over 100 tool calls**, clearing the 90-step gate.

**What those runs score here.** The ten archived trajectories re-score under v2's rubric at a mean
of 8.3% on the 09/20/2026 set and 14.7% on the 09/21/2026 set, against 23.9% and 38.1% under T2's
own rubric. They were run against a wider ask, so they price the rubric and are not a v2 run set. A
v2 run set is owed.

---

## Paste-ready - the section 1.3 Checkpoints table

**Paste the table only.** Everything outside it is repo notes.

| # | Checkpoint - what the model must do |
|:---:|:---|
| 1 | Read the Finance Manager's 09/01/2026 request and take from it the page title, the 08/31/2026 measurement date, the two totals, the three columns and the definition of a current employee. |
| 2 | Establish who is employed by Troutly on 08/31/2026. The roster and the org chart carry 52. BambooHR's 57 active rows hold four contractors and three ended records and lack two hires. |
| 3 | Find the rules that govern PTO at 08/31/2026. The cutover memo of 06/20/2026, effective 07/01/2026, replaces the 2025 policy. The handbook incorporates it and says wiki pages do not set policy. The Paid Time Off page and the 2025 policy say monthly accrual and unlimited carryover and are superseded. |
| 4 | Establish each employee's opening balance. It is the SplinterHR archive's 06/30/2026 balance, capped at 40.0 hours. The HRIS report, the load file and the July close carry the balances uncapped. Eleven exceed the cap. |
| 5 | Establish the periods posted by 08/31/2026. The payroll procedures memo gives four biweekly pay dates, 07/10, 07/24, 08/07 and 08/21/2026. The fifth pays 09/04/2026. |
| 6 | Establish each employee's adjusted service date. Nine migrated records read 07/01/2026 in BambooHR and on the roster and carry their true dates in the archive and the historical offer letters. TRT-0071 rehired 04/22/2024 after a 241-day break and bridges to 03/08/2021 under handbook 7.6. |
| 7 | Establish each period's tier from the adjusted service date. The tiers are 80 hours under two years, 120 under five and 160 at five and over, each over 26 periods. The tier changes in the period containing the anniversary. TRT-0018 reaches five years on 08/09/2026 inside the fourth period. |
| 8 | Establish the part-time accrual. The schedule change form puts TRT-0141 at 25 hours until 08/09/2026 and 32 from 08/10/2026. Handbook 2.2 accrues pro-rata under 30 hours. |
| 9 | Deduct the approved time off recorded in BambooHR. It is 24 requests and 560 hours, all in July. |
| 10 | Establish the rate on file with the signed changes applied. The promotion approval sets TRT-0088 at $118,000.00 from 06/16/2026. The amendment sets TRT-0117 at $148,200.00 from 05/16/2026. Her offer letter and handbook 5.4 set TRT-0096 at $61,000.00 from the 08/17/2026 step. BambooHR, the roster and every register carry the old rates. |
| 11 | Compute each employee's PTO balance in hours and the hourly rate as the annual rate over 2,080, then the total PTO hours and the total dollar liability over the 52. |
| 12 | Publish the page under the exact title, stating the total dollar liability and the total PTO hours and carrying a row for every current employee with the employee ID, the balance in hours and the hourly rate. |
| 13 | Read the published page back and confirm each figure against the schedule, from the page record rather than from the arguments of the call that wrote it. |

---

## The dependency chain, stated

- **3 is a choice between documents, and nothing in the request makes it.** A run that stops at
  the wiki page or the July detail carries monthly accrual, no cap and the loaded tiers into 4,
  5 and 7.
- **4 cannot precede 3.** The cap is in the memo and nowhere on the report.
- **6 is a comparison the request does not announce.** The roster and BambooHR agree on
  07/01/2026 for nine people; only the archive and the offer letters disagree.
- **7 depends on 6.** A service date carried wrong into 6 is a tier carried wrong into 7 and a
  balance carried wrong into 11.
- **10 is a choice between a record and a signed document.** Three records agree and are wrong.
- **11 depends on 4 to 10, and 12 on 11.** One rule missed is a wrong total and a wrong cell.
- **13 is a read-back, and it is part of the work.** The one row that grades publication reads the
  page record.

## Three notes on the narrowed ask

- **The request sets no precision, so 11 and 12 carry none.** T2's memo asked for dates
  MM/DD/YYYY, hours to two decimals, rates to four and dollars to the cent. v2's memo carries no
  Form section and the builder bars one from returning, so the checkpoints ask for the figure and
  not for its shape. The verifiers read a cell within half a hundredth of an hour and half a cent
  of an hourly rate, and a stated total within half a dollar and a stated hours figure within a
  twentieth of an hour. No registered path lands inside either band.
- **Nothing in 12 asks the run to hold the page down.** The 24 cells the load has wrong sit inside
  the 52, over 22 people. A run that prints all 52 rows and a run that prints only the 22 stand
  identically, and 12 asks for every current employee because the totals run over all of them.
- **There is no BambooHR checkpoint.** 9 still reads BambooHR, for the 24 approved requests, and
  BambooHR is still where the annual rate comes from for the 50 loaded people. Nothing is written
  back to it, and no step asks for it.
