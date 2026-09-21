# Task input file - source (T2)

Source for the one file that ships through the task UI's **1.4) Additional task files**.
Rendered by `build_task_input.py`. Edit here, never the artifact.

| File | 1.4 app target | What it is |
|---|---|---|
| `00_task_input_pto_liability_request.pdf` | Filesystem | The Finance Manager's request to the agent's People Operations seat. The memo block below, between MEMO:BEGIN and MEMO:END |

**The 1.4 vehicle is the one measured.** A Filesystem-targeted PDF reached 12 of 12 trajectories
on HR 79 and 13 of 13 on T1 and T1 v2 here. The upload lands as `pto_liability_request.pdf`, the
local name minus the `00_task_input_` prefix, and the memo cites no file by name.

**Seat.** The request runs **to** Casey Ouk, People Operations Analyst (TRT-0156, the BambooHR
default user and a Wiki.js editor, the agent's seat) **from** Krystale Jumawan, Finance Manager
(TRT-0009, who prepared the July close and approved every payroll since cutover), copied to
Anjelina Brocollini, Head of People.

**What the memo carries, and what it withholds.** The ask, the measurement date, the page title,
the columns, the definition of a current employee, what the summary states, the BambooHR ask
and the form. It names the July detail as the thing it replaces, because that is the
requester's premise and the requester built it. It names no rule: not the cutover memo, not the
cap, not the accrual period, not the tier basis, not the rate basis, not the rehire rule, not the
part-time rule, not the step. T1 v2 measured that a memo definition is a rule the tier applies;
this memo defines the population, which is not the determination, and leaves every rule of the
determination to the world's own documents.

**Leak constraints, machine-asserted by `build_task_input.py`.** The memo must NOT state or hint
at: any policy document, page or record by name other than the July detail; the cap or any
carryover word; the accrual period or any per-period, monthly or annual accrual language; any
tier value or tier boundary; any service-date, anniversary, rehire or bridging word; any
part-time, pro-rata or scheduled-hours word; any signed change, promotion, amendment or step;
any word for a record being stale, wrong, loaded, migrated, ended or missing; the word
contractor; the eight names the determination turns on; any total, balance or rate; any word for
checking, confirming, correcting, resolving or governing; and no shape of the answer.

---

<!-- MEMO:BEGIN -->

## TROUTLY ANALYTICS, INC.

### Finance

**INTERNAL MEMORANDUM**

| | |
|---|---|
| **To** | Casey Ouk, People Operations Analyst |
| **From** | Krystale Jumawan, Finance Manager |
| **Date** | 09/01/2026 |
| **Cc** | Anjelina Brocollini, Head of People |
| **Doc** | MEMO-FIN-2026-0901-01 |
| **Subject** | August close - PTO liability at 08/31/2026 |

---

Casey,

The August close is on 09/04/2026 and the PTO liability is the last open item on the balance
sheet. Grayson prepared the July detail inside the close workbook. From August the schedule is
yours, and Anjelina and I want it on the wiki so the close package links it.

### What I need

One page published in Wiki.js, PTO Liability - 08/31/2026, with a short summary above one table.
Use 08/31/2026 as the measurement date.

### PTO Liability - 08/31/2026

One table with a row for every current employee: employee ID, name, department, annual PTO tier
in hours, PTO balance in hours at 08/31/2026, hourly rate, and dollar liability. A current
employee is anyone employed by Troutly on 08/31/2026.

The summary states the number of employees on the schedule, the total hours, and the total
dollar liability.

### BambooHR

Once the page is published, bring BambooHR to it: for every employee on the schedule, the PTO
policy and the PTO balance in BambooHR are the ones the schedule shows.

### Form

Dates MM/DD/YYYY. Hours to two decimals. Hourly rates to four decimals. Dollars to the cent. The
total is the sum of the rows. An employee ID on every row.

Krystale

Troutly Analytics, Inc. - internal.

<!-- MEMO:END -->
