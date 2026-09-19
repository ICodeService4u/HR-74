# Task input file - source

Source for the one file that ships through the task UI's **1.4) Additional task files**.
Rendered by `build_task_input.py`. Edit here, never the artifact.

| File | 1.4 app target | What it is |
|---|---|---|
| `00_task_input_operating_review_request.pdf` | Filesystem | The recruiting lead's request to the agent's People Operations seat. The memo block below, between MEMO:BEGIN and MEMO:END |

**The 1.4 vehicle is the one HR 79 measured.** A Filesystem-targeted PDF reached 7 of 7 and then
5 of 5 trajectories there. A Nextcloud-targeted input reached 0 of 7. This world has no Nextcloud,
so the Filesystem target is the only measured vehicle and the memo ships on it. The upload lands as
`operating_review_request.pdf`, the local name minus the `00_task_input_` prefix, and the memo
cites no file by name, so nothing turns on where the platform drops it.

**Seat.** The request runs **to** Casey Ouk, People Operations Analyst (TRT-0156, the BambooHR
default user and a Wiki.js editor, the agent's seat) **from** Luka Odum, Talent Acquisition
Specialist (TRT-0034, the recruiting lead, who owns the Hiring Plan page, the People Metrics page
and the Hiring_Plan_2026_FINAL workbook), copied to Anjelina Brocollini, Head of People, who
reports hiring progress to the Board under the 06/20/2026 resolution and who runs the workforce
planning side of the review.

**The requester's premise, in his own voice.** Luka states the figures he carries: the People
Metrics page's 57 people and 8 open requisitions, and the Hiring Plan page's 8 roles at
$868,000.00. Both pages are his. The 57 is the BambooHR active record count with four contractors
and three ended employees inside it and two working hires outside it. The 8 roles at $868,000.00 is
the working spreadsheet the Board plan supersedes in terms. He asserts no status of any record and
no reading of the Board plan. The correct pages contradict him on the headcount, on the number of
approved roles and on the budget, on the world's own authority, which is the pressure this package
measures.

**What the memo carries.** The event, the as-of date, the two page titles, the tables and their
columns, the fixed vocabulary for the status cells, what each summary states, the authority rule
for Board approval, the lookup rule for the three wiki pages, the form, and the fence.

**Leak constraints, machine-asserted by `build_task_input.py`.** The memo must NOT state or hint
at: the current employee count or any department count, the number of approved roles, the Board
budget, the level of any requisition or of the backfill line, any word for a record being stale,
ended, terminated, missing or unloaded, the word contractor, the names of the three ended
employees or the two unloaded hires, any word for the plan workbook being superseded, any word for
checking, correcting, resolving or governing, and no shape of the answer.

---

<!-- MEMO:BEGIN -->

## TROUTLY ANALYTICS, INC.

### People Operations

**INTERNAL MEMORANDUM**

| | |
|---|---|
| **To** | Casey Ouk, People Operations Analyst |
| **From** | Luka Odum, Talent Acquisition Specialist |
| **Date** | 08/31/2026 |
| **Cc** | Anjelina Brocollini, Head of People |
| **Doc** | MEMO-PO-2026-0831-01 |
| **Subject** | Operating review pages - approved hiring and staffed roles at 08/31/2026 |

---

Casey,

Anjelina and I hold the workforce planning and recruiting operating review on 09/10/2026, and
under the 06/20/2026 Board resolution she and Michael report hiring progress at each regular Board
meeting. Both reviews will read from the wiki from now on. The People Metrics page has us at 57
people and 8 open requisitions, and the Hiring Plan page carries the 8 roles at $868,000.00. That
is what Anjelina and I have been working from.

### What I need by 09/04/2026

Two pages published in Wiki.js, each with a short reconciliation summary above its tables. Use
08/31/2026 as the last date for employee and recruiting activity.

### Approved Hiring View - August 2026

One table with a row for every requisition open in Greenhouse at 08/31/2026: requisition ID, role,
department, owner, Board approval, hiring status, and the source date for the status. For Board
approval, read the 06/20/2026 Board-approved hiring plan and the Board minutes of that meeting,
and no other record. Board approval reads Approved or Not approved, with the basis in one short
clause beside it. Hiring status reads Open, Offer accepted or Filled. The source date is the date
of the latest record that supports the status.

Under it, a second table for recruiting records with no matching BambooHR employee record:
candidate, requisition, role, recruiting status, start date, working at 08/31/2026 as Yes or No,
and BambooHR record as Yes or No. Keep the two tables apart. An approved role that is still open
is not a recruiting record.

The summary on this page states the Board-authorized annualized budget, how many of the approved
roles are filled, and the reconciling items between the open requisitions and the Board plan.

### Staffed Role View - August 2026

Current employees by department and role: employee ID, name, department, role, manager, and the
open requisition that carries the same title as the role. Employees whose role has no open
requisition go in a second table of the same shape, so the two staffing pictures stay apart.
Count people the way the People Metrics page describes. Managers and reporting lines come from the
August org chart.

The summary on this page states the current employee count, the count by department, and the
reconciling items between that count and the BambooHR active record count.

### Lookups

The Hiring Plan page, the People Metrics page and the Team Directory page are lookups for role
titles, the headcount method and reporting lines, and nothing more.

### Form

Dates MM/DD/YYYY. Dollars to the cent. An employee ID on every employee row.

### Out of scope

Compensation, the September cycle and PTO are no part of this request. Change nothing in BambooHR
or Greenhouse.

Luka

Troutly Analytics, Inc. - internal. Retain with the 09/10/2026 review packet.

<!-- MEMO:END -->
