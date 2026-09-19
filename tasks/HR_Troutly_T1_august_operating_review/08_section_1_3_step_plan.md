# 08 - The section 1.3 step plan in the checkpoint form the guide asks for (09/19/2026)

The field is a numbered **Checkpoints** table, one column headed "Checkpoint - what the model must
do", each row naming the work, what it produces and the later rows it feeds. The guide's HR3
example runs to fifteen rows. This plan runs to fourteen.

## The threshold, and what is measured

The target is 90 or more steps in at least one Gemini trajectory, with 80 or more acceptable
where the failure analysis shows the run stopped short of the work. **No trajectory has run on
this task**, so the count below is an estimate from the nearest measurement: HR 79 T1's nine
rescoped Gemini runs on a fourteen-employee, one-period ask landed between 148 and 316 steps.
This ask reads 52 employees across three sources, eight requisitions across two, writes two
pages, and cannot be done in one sweep. Verify the count from the first completed Gemini
trajectory's reasoning sequence and replace the estimate here with the measurement.

From the guide's "Steps vs. Tool Calls": a step is the transition from one reasoning trace to the
next. Do not count prompt instructions, files, rows or requested outputs as steps, and do not
estimate from tool-call volume.

---

## Paste-ready - the section 1.3 Checkpoints table

**Paste the table only.** Everything outside it is repo notes.

| # | Checkpoint - what the model must do |
|:---:|:---|
| 1 | Read the recruiting lead's 08/31/2026 request and take from it the two pages, the tables and columns each carries, the fixed vocabulary of the status cells, what each summary states, the authority rule for Board approval, the lookup rule for the three wiki pages, the as-of date and the form. Hold the three figures it asserts, 57 people, 8 open requisitions and 8 roles at $868,000.00, as the state of the requester's own pages rather than as the determination being asked for. Everything below is seeded here. |
| 2 | Read the Board-approved hiring plan of 06/20/2026 and the Board minutes of the same meeting. Take the five authorised lines with their titles, levels, departments and hiring managers, the $612,000.00 budget, the conditional Customer Success backfill at CSM I with its 09/30/2026 condition, the requisition-discipline rule that a requisition must trace line-for-line, and the clause that the plan supersedes any working spreadsheet or draft. These are the only two records Board approval is read from. |
| 3 | List the requisitions open in Greenhouse at 08/31/2026 with the ATS export beside them: eight, each with its title, level, department, hiring manager, opening date and source-plan column. Read the two closed second-quarter requisitions and the three applications, all hired, with their candidates and notes. |
| 4 | Match each open requisition to a Board line by title, level and department. Five trace. Establish that REQ-2026-036 was opened at CSM II against a CSM I backfill line, and that REQ-2026-037 and REQ-2026-038 were opened from the working spreadsheet the plan supersedes. Decide Board approval for all eight on the rule from checkpoint 2 and write the basis for each. |
| 5 | Establish the hiring status of each open requisition at 08/31/2026 and the latest record that supports it: no offer and no application on seven, and on REQ-2026-038 the offer letter accepted 08/20/2026 with a 09/08/2026 start. Read the offer letter itself for the acceptance date and the start date. |
| 6 | Diff the three hired applications against the BambooHR employee table. Establish that none of the three candidates has a BambooHR row, that Kwame Adjei has not started, and that Simone Okonkwo and Rafael Ibarra have. Take Okonkwo's start date from the 07/09/2026 email thread and the IT ticket rather than from the signed offer letter, which carries the earlier date. |
| 7 | Read the People Metrics page for the counting method and the Finance cost memo for the same rule: active employees, contractors out, accepted offers with future start dates out, ended employment out. Carry this forward as the test every row of the staffed page is decided by. |
| 8 | List the BambooHR active rows: 57, with department, title, supervisor and status. Establish which rows are contractors by their CTR numbers, their Contract titles and the roster's Contractors tab. |
| 9 | Read the August org chart and the master employee roster of 08/31/2026. Establish the 52 employees they carry, the four contractors hung as dotted boxes, and the reporting line of every person. Reconcile the two against each other so they tie. |
| 10 | Reconcile BambooHR against checkpoint 9 in both directions. Three active rows are on neither the chart nor the roster: TRT-0037, TRT-0049 and TRT-0064. Two chart and roster employees have no BambooHR row: TRT-0153 and TRT-0155. Read the employee ID crosswalk for the Terminated and Never Loaded status of each, and the SplinterHR final archive for the three termination dates. Establish the 52 current employees and the count by department. |
| 11 | For each current employee, take the manager from the org chart and the roster, and name the open requisition, if there is one, that carries the same title as the employee's role. Five open titles match roster titles. Split the 52 into the 21 whose role has an open requisition and the 31 whose role does not. |
| 12 | Write the Approved Hiring View page: the summary with the Board budget, the number of approved roles filled and the reconciling items between the open requisitions and the Board plan, the requisition table with Approved or Not approved on every row, and the recruiting-record table with Adjei, Okonkwo and Ibarra. Publish it in Wiki.js under the exact title. |
| 13 | Write the Staffed Role View page: the summary with the current employee count, the count by department and the reconciling items between 52 and BambooHR's 57, then the two tables of the same shape. Publish it in Wiki.js under the exact title. |
| 14 | Read both pages back from Wiki.js and confirm each is published under its exact title with its tables intact, from the page record rather than from the arguments of the call that wrote it. |

---

## The dependency chain, stated

The chain the guide asks for runs through checkpoints 2, 4 and 10, and it is a chain rather than
a list:

- **1 seeds everything.** The vocabulary, the definition of a current employee and the authority
  rule all come from the request, and nothing below can be written without them.
- **4 cannot precede 2 and 3.** A requisition is matched to a Board line by title, level and
  department, and the level is on the ATS export while the line is on page 2 of the plan. A run
  that has 3 and not 2 reads the Backfill note and stops; that is the registered failure on
  REQ-2026-036.
- **5 and 6 depend on 3.** The accepted offer is on one requisition and the three hires are on two
  closed ones, so a run that lists open requisitions only never reaches Okonkwo and Ibarra.
- **10 depends on 7, 8 and 9, and it cannot be done from BambooHR alone.** BambooHR carries no
  flag that distinguishes an ended employee from a working one, and no row at all for the two
  unloaded hires. The reconciling items exist only in the difference between two sources, so 10
  is a comparison and then three further reads to name what each item is.
- **11 depends on 3 and 10.** The open titles come from the requisitions and the roles from the
  reconciled population, so a run that carries 57 into 11 carries the wrong split out of it.
- **12 depends on 4, 5 and 6; 13 depends on 10 and 11.** Neither page can be written before its
  determination, and the summaries are where the requester's three figures are contradicted.
- **14 is a read-back, and it is part of the work.** The row that grades publication reads the
  page record's published flag, and a run that confirms from its own call arguments confirms
  nothing.

## What is deliberately not in the table

**The page format.** The titles, the tables, the columns and the vocabulary are all stated in the
request, and they are graded by the two form rows and by the content rows themselves. The guide's
counting rule is not to count requested outputs as steps.

**A read-back of the pages against the request.** Hygiene rather than a reasoning milestone,
apart from the published flag in checkpoint 14, which the platform's own tools may not report
and which decides two rows.
