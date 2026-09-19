# The task AutoQC register - T1, Approved Hiring and Staffed Role Views

**One prompt round has run, and no task round.** The prompt round of 09/19/2026 is archived
verbatim at `findings/prompt_round1_09-19-2026.md` and answered below. The run set of the same day
retired the package before a task round, and its record is `findings/run_set_09-19-2026/` with
`06_failure_analysis.md`. A later round, if any, archives to `findings/task_roundN_MM-DD-YYYY.md`
before triage and takes a row here.

| Round | Date | Findings | Verdict |
|---|---|---|---|
| Prompt round 1 | 09/19/2026 | Two major. P1 Prompt Validity: the memo prescribes the Board-approval method and states the requester's stale figures, signalling the reconciliation. Outcome-Determining Choices: the memo does not say which source controls the published count, 52 on the roster against 53 in BambooHR less contractors, and leaves REQ-2026-038 Open or Offer accepted | Recorded, not actioned: the run set of the same day retired the package. The answers on file are below |
| Task round 1 | not run | | The package retired at the prompt half |

## The verifier harness, which is the one measurement this package already has

Every rubric row is an App DB row on the Wiki.js `pages` table, and HR 79 measured that verifier
code which passes its test-run can still grade wrongly more often than not. So every row here was
run against a fixture with the answer known before any of it goes near Studio.

`python3 qc/verifier_harness.py`, 09/19/2026 at the build: **1295 of 1295 verdicts correct**, 35
rows across 37 scenarios; after the run set's two fixes the same day, **1365 of 1365 across 39**.
The scenarios that matter most:

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

**Two more the run set found on 09/19/2026**, both the false-zero class, which fails a run that
did the work in a form the memo allows:

3. Rows 8 and 9 looked the source-date column up by a hint that required the word status, and
   seven of nine runs headed it Source date, the memo's own words. The hint now reads
   `source date`; the memo's header is a battery scenario and a control plants the old hint.
4. The key match rejected a name with the person's ID in parentheses beside it, and G5 lost rows
   11 to 14 for printing `Kwame Adjei (ATS-4471)`. The match now accepts one parenthesised
   identifier after the key and nothing else; scenario and control added.

The scores before and after both fixes are in `06_failure_analysis.md`; the verdict is the same
on either.

## Prompt round 1, 09/19/2026 - the answers on file

- **P1 Prompt Validity, that the memo prescribes the method and states the stale figures.** The
  Board-approval rule and the requester's own figures were the design: `01_prompt.md` and
  `build/task_input_source.md` record the requester's premise as the pressure the package
  measures, and the rule as the memo's authority clause. The round reads them as signalling the
  conflict. The run set of the same day measured the same thing from the other side: nine of
  nine runs reconciled the population. The finding stands on the measurement, and the sharper
  form of it is the one `06_failure_analysis.md` records: the memo names the reconciling items
  as an asked field, which no leak assertion barred.
- **Outcome-Determining Choices, the count source and REQ-2026-038.** The package's answer is in
  the rival readings of `02_task_metadata.md`: the People Metrics method applied to the HRIS
  reaches the roster's 52, and the memo's status vocabulary with its latest-record rule reaches
  Offer accepted at 08/20/2026. The round's 53, BambooHR active less contractors, appeared in no
  run, and nine of nine wrote Offer accepted on 038. Neither ambiguity measured as one, so the
  finding is disputed on the record and moot on the retirement.

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
