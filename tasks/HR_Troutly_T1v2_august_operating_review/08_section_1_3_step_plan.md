# 08 - The section 1.3 step plan in the checkpoint form the guide asks for (T1 v2, 09/19/2026)

The field is a numbered **Checkpoints** table, one column headed "Checkpoint - what the model must
do". Thirteen rows. The step count measured on the four v2 Gemini trajectories of 09/20/2026 is 74 to 90 tool calls and 69 to 90 assistant turns, G1 at 91 on the platform's own count, over the EPM's 90 line; T1 measured 74 to 95 tool calls on the same reads.

---

## Paste-ready - the section 1.3 Checkpoints table

**Paste the table only.** Everything outside it is repo notes.

| # | Checkpoint - what the model must do |
|:---:|:---|
| 1 | Read the recruiting lead's 08/31/2026 request and take from it the two pages, the columns each table carries, the vocabulary of the Board approval and hiring status cells with what each value means, what each summary states, the definition of a current employee, the date form and the fence. |
| 2 | Find what the Board approved. The Hiring Plan wiki page and Hiring_Plan_2026_FINAL say eight roles at $868,000.00, Board approved 06/20/2026; the Board-approved plan of 06/20/2026 and the Board minutes say five roles at $612,000.00 plus a conditional CSM I backfill, and the plan supersedes any working spreadsheet in terms. Take the five lines with title, level, department and hiring manager. |
| 3 | List the requisitions open in Greenhouse at 08/31/2026 with the ATS export beside them: eight, each with title, level, department, hiring manager and source-plan column. |
| 4 | Match each open requisition to a Board line by title, level and department. Five trace. REQ-2026-036 was opened at CSM II against a CSM I line; REQ-2026-037 and REQ-2026-038 were opened from the workbook. Not approved on all three, with the basis. |
| 5 | Establish the hiring status of each open requisition under the memo's definitions: no accepted offer on seven, Open; a signed acceptance of 08/20/2026 with a 09/08/2026 start on REQ-2026-038, Offer accepted, not Filled. None of the five approved roles is filled. |
| 6 | Establish who is employed by Troutly on 08/31/2026. BambooHR carries 57 active rows. The master roster of 08/31/2026 and the org chart of 08/24/2026 carry 52. The two disagree in both directions and the difference has to be resolved, not chosen. |
| 7 | Read the crosswalk and the SplinterHR archive. TRT-0037, TRT-0049 and TRT-0064 read Terminated with termination dates before 08/31/2026, are on neither the chart nor the roster, and are not employed at 08/31/2026 whatever BambooHR says. |
| 8 | Establish that CTR-2001 to CTR-2004 are contractors, on the roster's own Contractors tab, dotted on the org chart, engaged and not employed, and leave them off the staffed tables. |
| 9 | Establish that TRT-0153 and TRT-0155 are employed and working at 08/31/2026, on the roster, on the org chart, hired in Greenhouse, with no BambooHR row, and put them on the staffed tables with their managers from the org chart. |
| 10 | Take the 52 by department and the manager of each from the org chart and the roster, and name the open requisition, if there is one, that carries the same title as the role. Five open titles match 21 employees; 31 hold titles no open requisition carries. |
| 11 | Write the Approved Hiring View page: the summary with the Board-authorized budget and the number of approved roles filled, then the table of eight requisitions with Approved or Not approved and the basis beside each. |
| 12 | Write the Staffed Role View page: the summary with the current employee count and the count by department, then the two tables of the same shape, an employee ID on every row, every date MM/DD/YYYY. |
| 13 | Read both pages back from Wiki.js and confirm each is published under its exact title with its tables intact, from the page record rather than from the arguments of the call that wrote it. |

---

## The dependency chain, stated

- **2 is a choice between records, and nothing in the request makes it.** A run that stops at the
  wiki page carries eight approved roles and $868,000.00 into 4 and 11.
- **4 cannot precede 2 and 3.** The level is on the ATS export and the line is on page 2 of the
  plan.
- **6 is a comparison the request does not announce.** The memo defines a current employee and
  asks for the count; it does not say two records disagree. A run that builds the page from
  BambooHR alone never reaches 7, 8 or 9, and that is the registered failing path.
- **7, 8 and 9 each name a class of the difference**, and each is a fact a run can get right or
  wrong on its own; the rubric grades them separately.
- **10 depends on 6 to 9.** A run that carries 57 into 10 carries the wrong split out of it.
- **13 is a read-back, and it is part of the work.** The rows that grade publication read the
  page record's published flag.
