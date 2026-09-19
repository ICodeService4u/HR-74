# Task Prompt (T1 v2)

**Task name:** `Approved Hiring and Staffed Role Views`

---

## Prompt (as delivered to the agent)

> Complete the request (using the ATS requisition export, the BambooHR employee records, and
> the rest of the Troutly files) about the August 31, 2026 operating review by publishing the
> two Wiki.js pages Approved Hiring View - August 2026 and Staffed Role View - August 2026.

`build/build_package_artifacts.py` asserts this blockquote against its `PROMPT` constant on every
build, prints the live character count and md5, and asserts that the constant names both page
titles and carries no folder, no path and no login detail. The prompt is v1's, unchanged: one
sentence, the ask first, the two named sources plus the open tail in a parenthetical, the request
by subject and date, then the deliverable with both page titles named exactly. Everything
instructional lives in the request memo, where Spec 1B puts it.

**The dash in the titles is a hyphen**, and every verifier normalises an en or em dash to a
hyphen before matching a title, so a run that types the other dash has still named the page.

**The two named sources carry no graded conclusion.** The ATS export prints the eight open
requisitions with their owner, level and source-plan column; the BambooHR employee records are
the population the determination is made against, and they are wrong in three ways the response
has to find. Unnamed by the prompt and, in v2, unnamed by the memo too: the Board-approved plan
and the Board minutes, the August org chart, the master roster, the crosswalk, the SplinterHR
archive, the offer letter, the IT ticket, the cost memo and the three wiki pages.

## What v2 changes, and the measurement behind it

T1's first run set, nine trajectories on 09/19/2026, read nine of nine runs reconciling the
population and a Gemini 3.8 Flash mean of 96.5%. The traces show every Gemini run going from the
memo straight to the Board minutes, the Board plan and the org chart, because the memo named them,
and reading the roster and the crosswalk after listing the directory. The prompt AutoQC round of
the same day read the memo's authority clause, its stale figures and its reconciling-items ask as
prescribing the method and signalling the conflict.

The v2 memo names no source, no page, no figure and no reconciliation. Gone: the People Metrics
and Hiring Plan figures the requester stated; "read the Board-approved hiring plan and the Board
minutes, and no other record"; "count people the way the People Metrics page describes";
"managers and reporting lines come from the August org chart"; the lookups paragraph; the table
of "recruiting records with no matching BambooHR employee record"; both "reconciling items"
clauses; the source-date column. Kept: the two pages, their columns, the vocabulary of the two
status cells, what each summary states, the form and the fence. Added, for the two choices the
round read as pinned: what a current employee is, "anyone employed by Troutly on 08/31/2026",
and what each hiring status means, Open with no accepted offer, Offer accepted once a candidate
has signed and before the start, Filled once the hire has started.

## Prompt goal

The request asks for **two Wiki.js pages for an operating review: every open requisition with its
Board approval and hiring status, and every current employee by department and role with the
open requisition that carries the same title**. The determination is the population: BambooHR
carries 57 active rows, and 52 people are employed by Troutly on 08/31/2026. The second
determination is what the Board approved: the recruiting lead's wiki page and workbook say eight
roles at $868,000.00, Board approved; the Board's own plan and minutes say five at $612,000.00
plus a conditional backfill, and supersede the workbook in terms.

The cell families, and the bytes behind them:

1. **The population.** Four contractors loaded as employee rows (CTR-2001 to CTR-2004). Three
   employees whose employment ended and whose records still read Active: TRT-0037 (03/20/2026),
   TRT-0049 (05/08/2026) and TRT-0064 (06/15/2026), Terminated on the crosswalk, dated on the
   archive, absent from the August org chart and the roster. Two working employees with no
   BambooHR row: TRT-0153 Simone Okonkwo (started 07/22/2026) and TRT-0155 Rafael Ibarra (started
   08/03/2026). **52 current employees**, Engineering 19, Customer Success 11, Sales 8, Marketing
   5, Product 4, Finance and Corporate 5. Twelve rows, 56 of 83 points, the gate among them.
2. **The Board reading.** REQ-2026-036 opened at CSM II against a CSM I backfill line; REQ-2026-037
   and REQ-2026-038 opened from the workbook the Board plan supersedes; the budget $612,000.00;
   none of the five approved roles filled. Five rows, 20 points.
3. **The asked fields a run prints on any path.** The two pages published, five Approved cells,
   seven Open cells, one Offer accepted cell, the two form rows. Seven rows, 7 points.

## Spec compliance notes

| Spec | How the ask meets it |
|---|---|
| **1A** Realistic and complex | An HRIS cutover two months old, the Office Manager who owned it gone, three ended employees still Active, two post-cutover hires never loaded, a recruiting lead whose own pages carry the wrong headcount and the wrong plan, and a Board plan that supersedes the working spreadsheet in terms |
| **1B** Natural prompting | One sentence in the owner's register; the request referenced by subject and date; both page titles stated exactly; no step, order, workflow, persona, credential or format convention. The memo names no source and prescribes no method |
| **1C** Unique correct answer | Every graded value is a document's printed line or a document's application, recomputed from the world's bytes by `check_world()` on every build. The memo's two definitions settle the two readings the prompt AutoQC round called pinned |
| **1D** Timeless | The request dates itself 08/31/2026 and sets that date as the last day of activity; every other date is a world date |
| **1E** Tightly scoped outputs | Two pages, one or two tables each, one summary each. 24 verifiers, all App DB, on thirteen world files and eleven app tables |
| **1F** Self-sufficient | Solvable from the request, the world files and the three apps alone. The one input uploads through 1.4 on the Filesystem target, measured at 9 of 9 on T1 |
| **1G** Purposeful | No persona. The prompt names the request, the two sources and the two deliverables |
| **2A** Genuinely challenging | **Unmeasured, predicted.** The registered modal failing paths score 27 of 83, 32.5% and 31 of 83, 37.3%; the free base is 7 of 83, 8.4%. The registered Gemini mean and the decision rule are in `06_failure_analysis.md`, dated before any v2 run, with the honest note that v1's traces make the heal likely |

**Withheld from the prompt and from the task input** (machine-asserted by
`build/build_task_input.py`): every source record, page, chart, roster, plan document and minutes
by name; the current employee count and every department count; the number of approved roles;
both budgets; any requisition level; any word for a record being stale, ended, terminated,
missing, unloaded or reconciled; the word contractor; the six names the determination turns on;
any word for a document being superseded; every word for checking, confirming, correcting,
resolving or governing; and the shape of the answer, "whether", "only", "except", "instead",
"differ", "conflict", "override" and their neighbours word-boundary-banned.

**Required of the request**: the two titles, the columns, the vocabulary with its definitions,
what each summary states, the definition of a current employee, the form and the fence.
