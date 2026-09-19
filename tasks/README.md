# HR 74 task packages

Phase 2. The world is finished and frozen: `filesystem/` and `apps_data/` are the bytes of
`HR 74.zip`, held in place by `world/checks/world_manifest.py`, and a rule a task needs that the
world lacks ships as a 1.4 task input rather than as a world edit. That is the rule that keeps
every other task in the world valid, and it is the lever HR 32 proved on its T24 and T25 and HR 79
proved on its T1.

**One package exists, at the prompt half.** It is built to the HR 79 T1 shape, which twenty-two
packages, four hundred pull requests and seven task AutoQC rounds bought, and everything in
`../HR-79/tasks/README.md` that is not about HR 79's own apps applies here. The four rules from it
that no world-side rule covers are in the root `CLAUDE.md`.

| Package | Request | Status |
|---|---|---|
| `HR_Troutly_T1_august_operating_review` | The recruiting lead's 08/31/2026 request for two Wiki.js pages, an approved-hiring view and a staffed-role view, for the 09/10/2026 operating review | Built 09/19/2026. **35 verifiers, 113 points, 1 gate**, every row App DB on the Wiki.js pages table, verifier battery **1295 of 1295**, one 1.4 input on the Filesystem target, two golden pages. Registered modal failing path 37 of 113, 32.7%; registered Gemini mean 38%. Run set, snapshot ids and tool catalogue owed |

## The rules every package here is built to

**The Domain Lead's reminder of 09/19/2026, which governs synth tasks in full:** all regular
prompt rules apply. Prompts are natural. No app login information goes in a prompt. The failure
percentage rules apply, Gemini 3.8 Flash under a 40% mean across five runs with 90 or more steps
in one of them. A world with two or more apps uses at least two in the task. T1 uses three:
BambooHR and Greenhouse read, Wiki.js written.

**The HR 79 rules, unchanged:**

1. **No world byte moves for a task.** `python3 world/checks/world_manifest.py` and
   `git status filesystem apps_data` before every commit.
2. **Edit the builder, never the artifact.** One `_rubric()` generates the rubric, the import, the
   golden, the show-your-work and the verifier code.
3. **Every guard has a negative control.** A guard nobody has seen fail is a guard the package does
   not have.
4. **Every graded value recomputes from the world's own bytes on every build**, the requester's
   premises included.
5. **The prompt string is asserted**, in the builder and in every document that quotes it.
6. **Write the predictions before the runs and score them after.** If the surface heals, retire
   the package and record the lever as measured insufficient rather than rescoping the rubric.
7. **A verifier is tested against a fixture with the answer known before it is imported.** HR 79
   measured Studio's generated code at 13 of 15, 8 of 10 and 4 of 10 on its first attempt, five of
   the failures passing runs that had done nothing. Every App DB row here ships with a battery.

**The house register.** Everything written here is ASCII, no em or en dash, no smart quote, dates
MM/DD/YYYY, one fact a sentence. The builders assert it on every artifact and every document.

## What a package ships

The numbering is HR 32 T24's, carried by HR 79, so a reviewer can find things in the order they
were written.

| File | Purpose |
|---|---|
| `00_task_input_*` | The files the requester supplies, uploaded through 1.4, each on the Filesystem target. Only `.pdf`, `.csv`, `.png` or `.jpg`; the markdown source and the generator live in `build/` |
| `01_prompt.md` | The prompt verbatim, its shape reasoning, the cell families, the Spec table, the withheld list |
| `02_task_metadata.md` | Identity, graded values and sources, required files and the selection block, fences, the rival readings, reviewer decision rules, the asks table, the rubric, the plan checkpoints, the time estimate, the predictions, the platform state, the open items |
| `03_show_your_work.xlsx` | Sources, Verifiers, Row assembly |
| `04_golden_output_*` | The deliverable |
| `05_rubric_import.xlsx` / `09_rubric_import.md` | The file that registers, and its mappings |
| `06_failure_analysis.md` | Predictions written before the runs, then the measured record against them |
| `08_section_1_3_step_plan.md` | The checkpoint table the guide asks for |
| `build/` | The guarded builders, their sources, the verifier engine and the negative controls |
| `qc/` | The task AutoQC register and archive, the verifier battery and harness, the generated row files |

## What is carried from HR 79's platform record, and what is not yet measured here

Carried, because it was measured on trajectories and nothing about it is app-specific:

- **The 1.4 target decides delivery, the format does not.** Filesystem-targeted PDF and CSV
  reached 12 of 12 and 9 of 9; a Nextcloud-targeted CSV reached 0 of 7. Every input here ships on
  the Filesystem target.
- **A task input uploads under its local name minus the `00_task_input_` prefix.** Name the
  local file backwards from the name the record publishes.
- **1.5 Expected Output Files is a list of filename chips and nothing else**, so output placement
  lives in the request, and a task whose deliverable is app state has nothing to put there.
- **Confirm an upload by digest, never by the file browser.**
- **Files and data tables takes one selection per line**, a world file on its plain path and an
  app table as `<app>/<table>.csv`, no `apps_data/` prefix, no wildcard, no leading slash.
  `tasks/check_selection_blocks.py` holds every package's block to it.
- **The picker spells the code-verifier type `App DB Programatic`**, one "m", and drops an unknown
  value on a warning. Every import here spells it the picker's way.
- **A grading snapshot may carry placeholder column names**, and Studio's generated verifier
  code has been measured grading wrongly more often than not. Read
  `../HR-79/tasks/APP_DB_VERIFIER_PLAYBOOK.md` before touching a verifier.
- **An App DB row is read from a route the run cannot rewrite.** The pages table, never the
  app's own API, never the trajectory.

Not yet measured in this world, and recorded as open items rather than assumed:

| Unmeasured | How to settle it |
|---|---|
| The platform's tool catalogue for BambooHR, Greenhouse and Wiki.js | Capture the toolbelt offered to the first trajectory into `tasks/APP_TOOL_SURFACE.md` in HR 79's form. T1's `check_tools()` fails the build once it exists and lists no Wiki.js page-writing tool |
| Whether a page created through the platform's Wiki.js tools lands in `pages` under the title the run gives it | Read the first grading run's `details` and the transcripts' page-create calls |
| The world and task-data snapshot ids | Read `world_snapshot_id` and `task_data_id` off the first export; never invent one |
| The step count | Read off the longest of the first five Gemini trajectories; the threshold is 90+, 80+ conditionally |
| Whether 1.5 accepts an empty list | The interface, at entry |

Write each answer into this file the way HR 79's root `CLAUDE.md` rule 6 was written, naming
what landed wrong as well as what worked.

**Measured 09/19/2026, the Expected output picker.** It offers eight labels: Edit Existing and
Make New, each over Sheet, Doc, Slide Deck and App Data. A wiki-page deliverable is App Data, and
two pages the run creates are **Make New App Data**, which is what the synth's task record
arrived carrying pre-selected. What landed wrong: T1's `02_task_metadata.md` had recorded Edit
Existing App Data before the picker was seen, and was corrected the same day. Neither deliverable
title is in the seed `Page.csv`, so Edit Existing would have named an update the run never makes.

## Running the checks

From the repo root:

```
python3 world/checks/world_manifest.py       # the world is the archive, byte for byte
python3 tasks/check_selection_blocks.py      # every selection block in picker form
```

From a package root:

```
python3 build/build_task_input.py
python3 build/build_package_artifacts.py --docs
python3 qc/verifier_harness.py
python3 build/negative_controls.py
```
