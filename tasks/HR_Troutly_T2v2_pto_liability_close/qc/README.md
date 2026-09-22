# The AutoQC register - T2 v2, PTO Liability at 08/31/2026

**No round has run against v2 yet.** The package was built 09/22/2026 and the import is not
loaded. Archive each round verbatim to `findings/prompt_roundN_MM-DD-YYYY.md` or
`findings/task_roundN_MM-DD-YYYY.md` before triaging it, and keep the verdicts here.

What v2 already answers, because T2 met it round after round:

| The finding a round is likely to raise | The answer on file |
|---|---|
| Verifiers grade only what the prompt asks for | Every row reads a figure the request asks the page to state. The request asks for the two totals and three columns, and the rubric grades the two totals and cells in two of those columns |
| No stacked criteria | One row reads one cell of one employee, or one stated total. Nothing bundles |
| Prompt-rubric alignment | The request's lines are the page, the two totals and the three columns. There is no form line, no summary count and no second app, so there is no explicit ask without a row and no row without an ask |
| Criteria count justified by scope | 27 rows over a deliverable of 52 rows and two totals. A cell is graded only where the load carries it wrong, which is 24 cells over 22 employees |
| A fence needs a row | There is no fence. The memo carries no out-of-scope block, no deadline and no retention line, and the builder bars each from returning |
| Exclusions | Nothing grades the absence of content. A response that prints all 52 employees rather than the 22 the load has wrong loses nothing, which is what keeps the golden valid when a response over-delivers |

## What is graded: the output, and only the output

`archive_run_set.py` reads each export for what the apps hold at the end of the run, and
`score_run_set.py` reads the archived page with the generated row files and nothing else: not the
final answer, not the narration, not which tool was used, not the step count. Both carry a
`--self-check`.

## The verifier harness

Built 09/22/2026. `verifier_harness.py` runs every row file under `verifiers/` against the 31
snapshots in `scenarios.py`, each with the rows it must fail named in advance: **837 of 837
verdicts correct**. Eleven of the snapshots are correct answers in different shapes, four of them
pages that carry more than the request asks for, because the one thing this battery exists to
prove beyond the verdicts is that no row grades the absence of content.

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
