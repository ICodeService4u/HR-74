# The task AutoQC register - T1, Approved Hiring and Staffed Role Views

**No task round has run.** This register is opened on 09/19/2026 with the build, so the first
round has somewhere to land. Archive each round verbatim to `findings/task_roundN_MM-DD-YYYY.md`
before triaging it, and keep the verdicts here. The builder's `check_docs()` asserts that every
archived round has a register row, so the two cannot drift.

| Round | Date | Findings | Verdict |
|---|---|---|---|
| none yet | | | |

## The verifier harness, which is the one measurement this package already has

Every rubric row is an App DB row on the Wiki.js `pages` table, and HR 79 measured that verifier
code which passes its test-run can still grade wrongly more often than not. So every row here was
run against a fixture with the answer known before any of it goes near Studio.

`python3 qc/verifier_harness.py`, 09/19/2026: **1295 of 1295 verdicts correct**, 35 rows across
37 scenarios. The scenarios that matter most:

| Scenario | What it proves |
|---|---|
| the golden pages | the golden scores 100 on every row |
| real column names, placeholder column names, a 20-column snapshot | the engine works on both branches, and takes the false zero on the exists rows where a shape it cannot validate hides the published flag |
| titles with an em dash, HTML content, a wider column header, a surname-first key | a correct run in another form is not failed |
| nothing written, the golden only in page history | a check reading the wrong table passes a run that did nothing |
| REQ-2026-036 marked Approved, or Approved with a qualifier | the determination, and the leading-token rule |
| the staffed page from BambooHR taken whole | the registered modal failing path fails 14 rows and passes the rest |
| the contractors added, TRT-0064 added, the tables right but the summary unnamed | every absence row and every count row |
| a second page under the same title with the wrong reading | a wrong duplicate fails |

**Two defects the battery found before it found none**, recorded because a guard that has never
gone red is not a guard:

1. The count rows counted TRT-keyed rows only, so a contractor row on the staffed tables slipped
   past the 31-employee count by an arithmetic coincidence: 57 less 4 contractors is 53, and 53
   less the 22 matched titles is 31. Every count now counts every ID-keyed row.
2. The department rows and the contractor row accepted a mention anywhere on the page, so the
   golden's own intro sentence satisfied them with the summary emptied. Each now requires the
   figure stated in the prose, as the request asks.

Both are the false-pass class, the one that silently credits a run that did nothing.

## What a round is likely to raise, and the answer already on file

- **Rubric Realism, that no row grades a file.** True and by design: the deliverable is two wiki
  pages and no file, the HR row allows one output type, and a wiki page is not a file the judge
  can open. `01_prompt.md` carries the output-restriction row.
- **Verifier Type, that every row is App DB.** Same answer. File existence is an App DB check by
  the 09/15/2026 EPM direction, and page content is a content-match check by the platform's own
  check-type list.
- **The dash in the titles.** The request as first drafted carried em dashes; the house register
  is ASCII, so the titles carry hyphens and every verifier normalises the dash before matching.
- **The recruiting table naming Okonkwo and Ibarra as working with no BambooHR record.** That is
  the ask: the memo defines the table as recruiting records with no matching BambooHR employee
  record, and the two are exactly that.
