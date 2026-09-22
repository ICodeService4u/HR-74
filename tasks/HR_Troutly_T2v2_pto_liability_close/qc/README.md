# The AutoQC register - T2 v2, PTO Liability at 08/31/2026

**Review round 1, 09/22/2026, read the 27-row file.** Two findings, both accepted and archived in
the record of `../02_task_metadata.md`, section Review round 1:

| Finding | Verdict | What changed |
|---|---|---|
| P1 Prompt scope against rubric coverage: a row per current employee is 156 requirements, over the 25-criterion limit | Accepted | The per-employee table is out of the memo and five department lines are in, Sales and Marketing joined. 13 rows, 79 points |
| P0 Prompt-rubric alignment: the measurement-date sentence and the per-employee table were asks no row read | Accepted | The date sentence is out of the memo, the title and the subject carry the date, and the table went with the first finding |

Archive each later round verbatim to `findings/prompt_roundN_MM-DD-YYYY.md` or
`findings/task_roundN_MM-DD-YYYY.md` before triaging it, and keep the verdicts here.

What v2 already answers, because T2 and review round 1 met it:

| The finding a round is likely to raise | The answer on file |
|---|---|
| Verifiers grade only what the prompt asks for | Every row reads a figure the request asks the page to state: the two totals and each of the five lines' hours and dollars |
| No stacked criteria | One row reads one figure of one line, or one stated total. Nothing bundles |
| Prompt-rubric alignment | The request's lines are the page, the two totals, the five lines and the definition of a current employee, which the totals and lines run over. There is no form line, no measurement-date line, no summary count and no second app written, so there is no explicit ask without a row and no row without an ask |
| Criteria count justified by scope | 13 rows over a deliverable of two totals and five lines of two figures each, under the 25-criterion limit, which `check_rubric()` asserts |
| A fence needs a row | There is no fence. The memo carries no out-of-scope block, no deadline and no retention line, and the builder bars each from returning |
| Exclusions | Nothing grades the absence of content. A response that also prints every employee, or Sales and Marketing apart beside the joined line, loses nothing, which is what keeps the golden valid when a response over-delivers |

## What is graded: the output, and only the output

`archive_run_set.py` reads each export for what the apps hold at the end of the run, and
`score_run_set.py` reads the archived page with the generated row files and nothing else: not the
final answer, not the narration, not which tool was used, not the step count. Both carry a
`--self-check`.

## The verifier harness

Built 09/22/2026 and rebuilt for review round 1 the same day. `verifier_harness.py` runs every
row file under `verifiers/` against the 40 snapshots in `scenarios.py`, each with the rows it must
fail named in advance: **520 of 520 verdicts correct**. Twelve of the snapshots are correct answers
in different shapes, three of them pages that carry more than the request asks for, because the
one thing this battery exists to prove beyond the verdicts is that no row grades the absence of
content. Seven more hold the line reader to where a line is stated: not Sales alone, in a table or in prose, not a sum left
to the reader, not an employee row, not a prose word.

`ctx.py` is the platform's `ctx` stood in with placeholder column names by default and only the
three database primitives a graded run has been measured to serve, `list_tables`,
`table_columns` and `query_db`.

## What T2 measured that v2 inherits

- A graded run serves those three primitives. `has_table` is measured by nothing and no row reads it.
- The import populates criteria, explanations, weights and criterion types, and not Tags,
  Reference Artifacts or Grading Target, which are entered by hand from `build/rubric_plan.csv`.
- A 1.4 re-upload mints a new task data id.
- T2's first platform grading, 09/21/2026, failed every wiki row on a page the app had returned
  under the exact title, and two causes fit: the target app the rows are grounded on, or a ctx
  without `has_table`. The record and the one test run that separates them are in
  `../../HR_Troutly_T2_pto_liability_close/qc/findings/platform_grading_09-21-2026.md`. v2's rows
  are grounded the same way, so the answer carries straight over.
