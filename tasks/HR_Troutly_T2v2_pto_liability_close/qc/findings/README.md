# findings

Each AutoQC round is archived here verbatim before it is triaged, and the register beside this
folder, `../README.md`, carries the verdicts. No AutoQC round has run against v2 yet.

`run_set_09-23-2026/` is v2's own first run set: G1, a Gemini 3.8 Flash trajectory of 09/22/2026
exported on 09/23/2026 against task version 34, archived by `../archive_run_set.py` as the page
the app returned to the run's get_page call, its BambooHR writes, of which there are none, and
`runs.json` read off the export. `../score_run_set.py --set run_set_09-23-2026` scores it and
`../../06_failure_analysis.md` records it. `platform_grading_09-23-2026.md` is row 1's and row
2's grading on the platform the same day, on a different Gemini run.

`run_set_09-20-2026/` and `run_set_09-21-2026/` are T2's two run sets, ten Gemini 3.8 Flash
trajectories against T2's wider ask, carried into this package because the pages they hold are
the same deliverable in kind: a row per employee with a balance and an hourly rate beside it. They
are what `score_run_set.py` reads to measure what v2's rubric does to a response that copies the
load. They are not a v2 run set and the record never calls them one; their own history stays in
the T2 package.
