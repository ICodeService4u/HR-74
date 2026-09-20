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
and the next package needs a different ask. T2, the PTO liability schedule at 08/31/2026, was built on 09/20/2026 at the prompt half on that lesson: a rule application over 52 people where every record the run opens prints a finished wrong number, the memo naming no rule. Its five Gemini runs of 09/20/2026 read 23.9%, so the rubric half is being built: the import shipped the same day in the HR 79 T1 shape from the plan's rows, was loaded, and its first rubric round reshaped it to 28 rows with no registered weight moved; the verifier code, the battery and the golden page shipped the same day, 1764 of 1764 on 63 snapshots; its second rubric round read the 28-row file and reshaped it to 43 rows and 96 points, one BambooHR record a row with guards over the records the schedule leaves, the request's ID, date and Greenhouse lines as rows, 3268 of 3268 on 76 snapshots, the runs re-scoring at 29.4%, and the paste is owed. Measured off that round: the import populates criteria, explanations, weights and criterion types and not Tags, Reference Artifacts or Grading Target. What is still unmeasured, a grading snapshot's column
names, is recorded there as open. Do not invent any of it.
