# findings

Each AutoQC round is archived here verbatim before it is triaged, and the register beside this
folder, `../README.md`, carries the verdicts. No round has run against v2 yet.

`run_set_09-20-2026/` and `run_set_09-21-2026/` are T2's two run sets, ten Gemini 3.8 Flash
trajectories against T2's wider ask, carried into this package because the pages they hold are
the same deliverable in kind: a row per employee with a balance and an hourly rate beside it. They
are what `score_run_set.py` reads to measure what v2's rubric does to a response that copies the
load. They are not a v2 run set and the record never calls them one; their own history stays in
the T2 package.
