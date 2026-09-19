# Task Prompt

**Task name:** `Approved Hiring and Staffed Role Views`

---

## Prompt (as delivered to the agent)

> Complete the request (using the ATS requisition export, the BambooHR employee records, and
> the rest of the Troutly files) about the August 31, 2026 operating review by publishing the two
> Wiki.js pages Approved Hiring View - August 2026 and Staffed Role View - August 2026.

`build/build_package_artifacts.py` asserts this blockquote against its `PROMPT` constant on every
build, prints the live character count and md5, and asserts that the constant names both page
titles and carries no folder, no path and no login detail. Byte-verify the delivered string on
every export.

**The house form**, carried from HR 79 T1's author's-voice pass: one sentence, the ask first, the
named sources plus the open tail in a parenthetical, the request by subject and date, then the
deliverable with both page titles named exactly. Everything instructional lives in the request
memo, where Spec 1B puts it. The prompt carries no persona, no step, no workflow, no format
convention and no app credential, which is the Domain Lead's 09/19/2026 reminder taken in full.

**The dash in the titles is a hyphen.** The request as first drafted carried em dashes in the
page titles. The house register is ASCII, so both titles read `Approved Hiring View - August
2026` and `Staffed Role View - August 2026` everywhere, and every verifier normalises an en or em
dash to a hyphen before matching a title, so a run that types the other dash has still named the
page.

**The two named sources carry no graded conclusion.** The ATS requisition export of 08/31/2026
prints the eight open requisitions with their owner, opening date and source-plan column; it
decides nothing about Board approval and nothing about the population. The BambooHR employee
records are the population the determination is made against, and they are wrong in three ways
the response has to find. Unnamed, and the response's work to find: the Board-approved plan and
the Board minutes of 06/20/2026, the August org chart, the master employee roster, the employee
ID crosswalk, the SplinterHR final archive, the offer letters, the start-date email thread, the
IT ticket, the Finance cost memo, the leveling guide, and the three wiki pages the memo names as
lookups.

## Prompt goal

The request asks for **two Wiki.js pages for an operating review: every open requisition with its
Board approval and hiring status, and every current employee by department and role with the
open requisition that carries the same title** from a requester who carries three figures of his
own: 57 people, 8 open requisitions and 8 roles at $868,000.00. Two of the three are wrong, and
the correct pages contradict them on the world's own authority. The request never says a
contradiction is available.

The cell families, and the bytes behind them:

1. **The population.** BambooHR carries 57 active rows. Four are contractors loaded as employee
   rows (CTR-2001 to CTR-2004, on the roster's own Contractors tab and dotted on the org chart).
   Three are employees whose employment ended and whose records still read Active: TRT-0037
   (03/20/2026), TRT-0049 (05/08/2026) and TRT-0064 (06/15/2026), Terminated on the crosswalk,
   dated on the SplinterHR archive, absent from the August org chart and the master roster. Two
   working employees have no BambooHR row at all: TRT-0153 Simone Okonkwo (started 07/22/2026)
   and TRT-0155 Rafael Ibarra (started 08/03/2026), Never Loaded on the crosswalk, on the org
   chart and the roster. **52 current employees**, Engineering 19, Customer Success 11, Sales 8,
   Marketing 5, Product 4, Finance and Corporate 5. This is the gate and the largest share of the
   weight.
2. **The Board reading of REQ-2026-036.** The Board authorised one conditional Customer Success
   backfill at CSM I. The requisition was opened as Customer Success Manager II at CSM II, citing
   TRT-0064's departure. The plan requires every requisition to trace line-for-line and bars an
   offer at any level other than the one listed, so the requisition does not trace and is held.
   The ATS export's Backfill note and the Board's backfill line together make Approved the
   reading a run reaches without opening page 2 of the plan.
3. **The two workbook requisitions and the accepted offer.** REQ-2026-037 and REQ-2026-038 were
   opened from Hiring_Plan_2026_FINAL, which the Board plan supersedes in terms. REQ-2026-038
   holds Kwame Adjei's accepted offer of 08/20/2026 with a 09/08/2026 start: a recruiting record,
   not an employee, and not authorised.
4. **The recruiting records with no BambooHR match.** Adjei, Okonkwo and Ibarra. The second and
   third are working; the first is not. Okonkwo's start date is 07/22/2026 on the email thread,
   the IT ticket, the Greenhouse note and the roster, and 07/13/2026 on the signed offer letter.
5. **The staffing split.** Five open titles match a roster title, so 21 current employees hold a
   role with an open requisition and 31 do not, in a table of their own.

## Spec compliance notes

| Spec | How the ask meets it |
|---|---|
| **1A** Realistic and complex | An HRIS cutover two months old, the Office Manager who owned it gone, three ended employees still Active and still paid, two post-cutover hires never loaded, a recruiting lead whose own wiki pages carry the wrong headcount and the wrong plan, a Board plan that supersedes the working spreadsheet three requisitions were opened from, and one of those requisitions holding a signed offer |
| **1B** Natural prompting | One sentence in the owner's register; the request referenced by subject and date; both page titles stated exactly; two realistic source references and an open tail; no step, order, workflow, persona, credential or format convention |
| **1C** Unique correct answer | Every graded value is a document's printed line or a document's application: the Board lines and levels on page 2 of the plan, the requisition levels on the ATS export, the population on the roster and the org chart, the crosswalk's Terminated and Never Loaded, the archive's termination dates, the offer and the thread. The memo fixes the vocabulary of every status cell and defines a current employee, so no defensible second reading exists |
| **1D** Timeless | The request dates itself 08/31/2026 and sets that date as the last day of activity; every other date is a world date. No "Today is" opener |
| **1E** Tightly scoped outputs | Two pages, two tables each, one summary each. 35 verifiers, all App DB, on ten world files and eleven app tables |
| **1F** Self-sufficient | Solvable from the request, the world files and the three apps alone. The one input uploads through 1.4 on the Filesystem target, which is the one HR 79 measured to deliver |
| **1G** Purposeful | No persona. The prompt names the request, the two sources and the two deliverables; everything instructional lives in the request memo |
| **2A** Genuinely challenging | **Unmeasured, predicted.** The registered modal failing path scores 37 of 113, 32.7%, and the registered Gemini mean is 38% against a bar of under 40%. The decision rule and the retirement branch are in `02_task_metadata.md` and `06_failure_analysis.md`, dated before any run |
| **Output restriction** | The HR row allows one output type. The deliverable is one stateful app update, two pages in one app, and no file. Grading is App DB Programatic on every row, because a wiki page is not a file the judge can open |
| **Apps** | Three-app world; the Domain Lead's 09/19/2026 reminder requires at least two used. BambooHR is read for the population, Greenhouse is read for the requisitions, applications and hiring teams, Wiki.js is read for the three lookup pages and written for the two deliverables |
| **Requester seat** | The request runs **to** the agent's seat, Casey Ouk, People Operations Analyst, TRT-0156, BambooHR's default user and a Wiki.js editor, **from** Luka Odum, Talent Acquisition Specialist, copied to Anjelina Brocollini, Head of People. Asserted by `build/build_task_input.py` |

**Withheld from the prompt and from the task input** (machine-asserted by
`build/build_task_input.py`): the current employee count and every department count, the number
of approved roles, the Board budget, any requisition level or the backfill line's level, any word
for a record being stale, ended, terminated, missing or unloaded, the word contractor, the names
and numbers of the three ended employees, the two unloaded hires and the accepted-offer candidate,
any word for the workbook being superseded, every word for checking, confirming, correcting,
resolving or governing, **and the shape of the answer**: "whether", "if any", "only", "except",
"unless", "instead", "rather than", "either", "differ", "conflict", "override" and their
neighbours are word-boundary-banned from the request.

**Required of the request**: the requester states his own figures, 57 people, 8 open
requisitions and 8 roles at $868,000.00, as what he and the Head of People have been working
from. He asserts no Board reading and no status of any record.
