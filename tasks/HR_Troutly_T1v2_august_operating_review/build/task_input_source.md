# Task input file - source (T1 v2)

Source for the one file that ships through the task UI's **1.4) Additional task files**.
Rendered by `build_task_input.py`. Edit here, never the artifact.

| File | 1.4 app target | What it is |
|---|---|---|
| `00_task_input_operating_review_request.pdf` | Filesystem | The recruiting lead's request to the agent's People Operations seat. The memo block below, between MEMO:BEGIN and MEMO:END |

**The 1.4 vehicle is the one measured.** A Filesystem-targeted PDF reached 12 of 12 trajectories
on HR 79 and 9 of 9 on T1's first run set here. The upload lands as `operating_review_request.pdf`,
the local name minus the `00_task_input_` prefix, and the memo cites no file by name.

**Seat.** The request runs **to** Casey Ouk, People Operations Analyst (TRT-0156, the BambooHR
default user and a Wiki.js editor, the agent's seat) **from** Luka Odum, Talent Acquisition
Specialist (TRT-0034, the recruiting lead), copied to Anjelina Brocollini, Head of People.

**What v2 takes out, and why.** T1's first run set of 09/19/2026 read nine of nine runs healing
the population, and the traces show why: the memo named the Board plan and the minutes as the
only record for Board approval, named the August org chart for reporting lines, pointed at the
People Metrics page for the counting method, defined a table of recruiting records with no
BambooHR match, stated the requester's stale figures, and asked for the reconciling items
between the count and the BambooHR active record count. Every one of those told the run what to
find or where. The v2 memo names no source, no page, no figure and no reconciliation. It asks
for the two pages, their columns, the vocabulary of the status cells, what each summary states,
the form and the fence, and it defines the two terms the prompt AutoQC round of 09/19/2026 read
as pinned choices: what a current employee is, and what each hiring status means.

**Leak constraints, machine-asserted by `build_task_input.py`.** The memo must NOT state or hint
at: any source record, page, chart, roster, plan document or minutes by name; the current
employee count or any department count; the number of approved roles; the Board budget or the
workbook's; the level of any requisition or of the backfill line; any word for a record being
stale, ended, terminated, missing or unloaded; the word contractor; the names of the three ended
employees, the two unloaded hires or the accepted-offer candidate; any word for a document being
superseded; any word for reconciling, checking, correcting, resolving or governing; and no shape
of the answer.

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

Anjelina and I hold the workforce planning and recruiting operating review on 09/10/2026, and she
and Michael report hiring progress to the Board at each regular meeting. Both reviews will read
from the wiki from now on.

### What I need by 09/04/2026

Two pages published in Wiki.js, each with a short summary above its tables. Use 08/31/2026 as the
last date for employee and recruiting activity.

### Approved Hiring View - August 2026

One table with a row for every requisition open in Greenhouse at 08/31/2026: requisition ID, role,
department, owner, Board approval, and hiring status. Board approval reads Approved or Not
approved, with the basis in one short clause beside it. Hiring status reads Open, Offer accepted
or Filled. Open means no accepted offer. Offer accepted means a candidate has signed and has not
started. Filled means the hire has started.

The summary states the Board-authorized annualized budget for second-half hiring and how many of
the approved roles are filled.

### Staffed Role View - August 2026

Current employees by department and role: employee ID, name, department, role, manager, and the
open requisition that carries the same title as the role. Employees whose role has no open
requisition go in a second table of the same shape. A current employee is anyone employed by
Troutly on 08/31/2026.

The summary states the current employee count and the count by department.

### Form

Dates MM/DD/YYYY. Dollars to the cent. An employee ID on every employee row.

### Out of scope

Compensation, the September cycle and PTO are no part of this request. Change nothing in BambooHR
or Greenhouse.

Luka

Troutly Analytics, Inc. - internal. Retain with the 09/10/2026 review packet.

<!-- MEMO:END -->
