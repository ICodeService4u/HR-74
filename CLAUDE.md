# HR 74 - Troutly Analytics, Inc.

Task workspace for a Julius world. The world arrived finished as `HR 74.zip` and is **frozen**:
`filesystem/` (69 files) and `apps_data/` (31 seed tables across `bamboohr/`, `greenhouse/` and
`wiki_js/`) are the archive's bytes extracted in place, and `world/checks/world_manifest.py`
holds the tree to the archive entry by entry. **A task never edits the world.** A rule a task
needs that the world lacks ships as a 1.4 task input file, which is what keeps every other task
in this world valid.

This repository was built on 09/19/2026 from the HR 79 record, and the packages here follow the
HR 79 T1 shape exactly. Read `tasks/README.md` first, then `../HR-79/tasks/README.md` and
`../HR-79/tasks/EPM_GUIDANCE_09-15-2026.md`, which carry the measured lessons the packages here
are built on. The four that no world-side rule covers:

- **The failure has to be the ask, not sit beside it.** Ask of every candidate whether the central
  asked determination is one the tier gets wrong. If the honest answer is no, no rubric edit
  rescues it. Say so in the package rather than discovering it in a run set.
- **Generate every artifact from one builder and machine-assert everything you would otherwise
  promise.** Hand-edited artifacts drift; a guard you have never seen fail is a guard you do not
  have, so every package carries negative controls that plant a defect and confirm the guard goes
  red. That includes the verifier code, which HR 79 measured scoring 13 of 15, 8 of 10 and 4 of
  10 on its first generation.
- **Write the weighting, the fences, the reviewer decision rules and the failure predictions
  before any run**, dated. The difference between a prediction and a rationalisation is the date.
- **Ship every task input on the Filesystem target.** HR 79 measured a Filesystem-targeted PDF
  reaching 7 of 7 and then 5 of 5 trajectories and a Nextcloud-targeted CSV reaching 0 of 7.

## The house register

Everything written here, from the prompt to the rubric explanations to these notes, is in the
house register: maximally concise and simple, plain ASCII, no em dashes, no en dashes, no smart
quotes, dates MM/DD/YYYY, a person's name spelled as the world spells it. The builders assert
ASCII on every artifact and every package document. A hyphen with spaces around it is the only
dash.

## The world in one paragraph

Troutly Analytics is a 52-employee Austin analytics company that moved its HRIS from SplinterHR to
BambooHR on 07/01/2026 and lost its Office Manager, who owned the migration and onboarding, on
07/25/2026. BambooHR carries 57 active rows: four contractors loaded as employees, three people
whose employment ended (03/20, 05/08 and 06/15/2026) and who still read Active and still draw
pay, and none of the two hires who started after cutover. The Board approved five second-half
roles on 06/20/2026 at $612,000.00; the recruiting lead's working spreadsheet and wiki page carry
eight at $868,000.00, and three requisitions were opened from it, one of them now holding an
accepted offer. The agent's seat is Casey Ouk, People Operations Analyst, TRT-0156, the BambooHR
default user and a Wiki.js editor.

## Rules that are not negotiable here

- **No world byte moves for a task.** Run `python3 world/checks/world_manifest.py` and check
  `git status filesystem apps_data` before every commit.
- **Edit the builder, never the artifact.** One `_rubric()` generates the rubric, the import, the
  golden pages, the show-your-work and the verifier files.
- **Every guard has a negative control.** `build/negative_controls.py` in each package.
- **Every graded value recomputes from the world's own bytes on every build.**
- **The prompt string is asserted**, in the builder and in every document that quotes it.
- **Predictions before runs.** If the surface heals, retire the package and record the lever as
  measured insufficient rather than rescoping the rubric.
- **An App DB row is read from a route the run cannot rewrite, and its code is tested against a
  fixture with the answer known before it is imported.** `qc/verifier_harness.py` in each package.

## What is measured in this world

T1's first run set, nine trajectories on 09/19/2026, captured the tool catalogue into
`tasks/APP_TOOL_SURFACE.md`, read the snapshot ids off the exports, and saw the Wiki.js page tool
create pages under exact titles. It also retired T1: nine of nine runs reconciled the population,
Gemini 3.8 Flash meaning 96.5% against a registered 38%. `tasks/README.md` carries the measured
record and what landed wrong. T1 v2 was built from that record, the memo naming no source and no
reconciliation, and retired on 09/20/2026 on four Gemini runs meaning 98.5%: with the pointers
gone the tier still reads the tree whole and applies the memo's own definition of a current
employee. A population reconciliation is not a determination this tier gets wrong in this world,
and the next package needs a different ask. T2, the PTO liability schedule at 08/31/2026, was built on 09/20/2026 at the prompt half on that lesson: a rule application over 52 people where every record the run opens prints a finished wrong number, the memo naming no rule. Its five Gemini runs of 09/20/2026 read 23.9%, so the rubric half is being built: the import shipped the same day in the HR 79 T1 shape from the plan's rows, was loaded, and its first rubric round reshaped it to 28 rows with no registered weight moved; the verifier code, the battery and the golden page shipped the same day, 1764 of 1764 on 63 snapshots; its second rubric round read the 28-row file and reshaped it to 43 rows and 96 points, one BambooHR record a row with guards over the records the schedule leaves, the request's ID, date and Greenhouse lines as rows, 3268 of 3268 on 76 snapshots, the runs re-scoring at 29.4%; its third rubric round asked for payroll, compensation and benefits guards, the fence argument a third time, and the memo's out-of-scope block is gone as HR 79 T1's went in its round 9, the Greenhouse row with it and a policy row per created record added, 44 rows and 97 points, 3124 of 3124 on 71 snapshots, 29.3%; its fourth rubric round split the last two form rows three ways each, narrowed the population row to presence, had the two BambooHR set rows state every record and value, and asked for a deadline and a retention verifier, which went the way the fence went, 48 rows and 101 points, 3408 of 3408 on 71 snapshots, 32.1%, the free base 14 under a seventh; its fifth rubric round, 09/21/2026, added a BambooHR balance row for each of the twelve moved balances the five mirrored rules had left and, on the owner's decision, retired the five exclusion rows for the set row, 55 rows and 105 points, 23.2%, the fall stated in the record. The memo re-upload and the paste both landed on 09/21/2026, a second Gemini set of five meaning 38.1% with the gate and the cap failed five of five, and the first platform grading came back: G5 reads 1.9% on the pane against 18.1% on the archived bytes, 29 of 29 BambooHR rows agreeing and every wiki row reading fail, which its sixth rubric round answered by enforcing one page under the title, dropping the one ctx primitive no graded run has been measured to serve, and printing the engine's notes into the pane, 4015 of 4015 on 73 snapshots with no weight moved. Measured off those rounds: the import populates criteria, explanations, weights and criterion types and not Tags, Reference Artifacts or Grading Target; a graded run serves `list_tables`, `table_columns` and `query_db`; a 1.4 re-upload mints a new task data id. T2 v2 was built on 09/22/2026 on the owner's decision, after grader feedback carried from another world: a criterion whose failure materially changes the output weighs more than 2, and T2's rubric was full of rows under that bar, 14 points of page form and 29 BambooHR rows at 1 that a failing response earned in full. The remedy is the rescope and not a reweighting, because the lines that drew those rows are out of the memo now: the summary count, the name, department, tier and liability columns, the BambooHR instruction and the whole Form section, each barred from returning with a control. Its review round 1 the same day read the 27-row file and found the row per current employee over the platform's 25-criterion limit, 156 values, and the measurement-date sentence an ask no row read; both are out of the memo and barred, and five department lines are in, Sales and Marketing joined because Marketing alone is a figure the load already carries right. 13 rows, 79 points, one row that is not a determination at 1 point, no row at 2, every line figure one the load carries wrong and priced by the dollars it moves, nothing grading the absence of content, 793 of 793 verdicts on 61 snapshots, 79 of 79 controls red, the verifiers rebuilt to the app-db-verifier skill and stripped of `import os` on 09/23/2026 after the platform's AST gate rejected it, the page read off the run's own Wiki.js calls since a grading the same day showed the dump carries no Wiki.js table, and no row that passes on an untouched task. T2's ten archived trajectories re-score at 1.3% each there, as printed and with their own rows summed onto the lines. The first v2 trajectory landed on 09/23/2026 on the memo's own task data id, 106 steps on the platform's count, the load's own figures line for line at 1.3%, the cap quoted at step 22, computed at step 89 and set aside for the report; the record and the task-field paragraph are in the package's `06_failure_analysis.md`. What is still unmeasured, four Gemini runs, three GPT Sol runs and the wiki half of a grading snapshot, is recorded there as open. Do not invent any of it.
