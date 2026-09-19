# HR 74 task packages

Phase 2. The world is finished and frozen: `filesystem/` and `apps_data/` are the bytes of
`HR 74.zip`, held in place by `world/checks/world_manifest.py`, and a rule a task needs that the
world lacks ships as a 1.4 task input rather than as a world edit. That is the rule that keeps
every other task in the world valid, and it is the lever HR 32 proved on its T24 and T25 and HR 79
proved on its T1.

**Two packages exist: T1, retired on its first run set, and T1 v2, built from that measurement.** Both are built to the HR 79 T1 shape, which twenty-two
packages, four hundred pull requests and seven task AutoQC rounds bought, and everything in
`../HR-79/tasks/README.md` that is not about HR 79's own apps applies here. The four rules from it
that no world-side rule covers are in the root `CLAUDE.md`.

| Package | Request | Status |
|---|---|---|
| `HR_Troutly_T1_august_operating_review` | The recruiting lead's 08/31/2026 request for two Wiki.js pages, an approved-hiring view and a staffed-role view, for the 09/10/2026 operating review | Built and **retired 09/19/2026**. 35 verifiers, 113 points, 1 gate, every row App DB on the Wiki.js pages table, battery 1365 of 1365, one 1.4 input on the Filesystem target, two golden pages. Registered modal failing path 32.7% and Gemini mean 38%; **measured Gemini mean 96.5%** on five runs, nine of nine runs reconciling the population, so the rule registered before the runs retired it. The record, the run set and the lesson are kept |
| `HR_Troutly_T1v2_august_operating_review` | The same request with the memo stripped of every source, figure and reconciliation it had named, and a current employee and each status value defined instead | Built 09/19/2026 from T1's traces. **24 verifiers, 83 points, 1 gate**, the population 67% of the points, the free base 8%; battery **864 of 864** with the three failing paths as pages, P1 32.5% and P1b 37.3%. Registered Gemini mean 58% with the honest note that T1's runs found the roster and the crosswalk by listing the tree. Run set and task data id owed |

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

Measured here on 09/19/2026, off the nine trajectory exports of T1's first run set:

| Was unmeasured | Measured |
|---|---|
| The platform's tool catalogue for BambooHR, Greenhouse and Wiki.js | `tasks/APP_TOOL_SURFACE.md`: 254 tools on a toolbelt agent that pulls each one in with `toolbelt_add_tool`, 39 of them Wiki.js, `wiki_js_mcp_wikijs_mcp_create_page` the page writer. T1's `check_tools()` reads it green |
| Whether a page created through the platform's Wiki.js tools lands in `pages` under the title the run gives it | Yes. Nine of nine runs created both pages with `create_page`, ids 11 and 12 after the ten seed pages, title exact, published by default, path the run's own. No grading run on the package's rubric happened, so the grading snapshot's column names are still unmeasured |
| The world and task-data snapshot ids | `snap_c6f6a0879f3d47a19048ee80d7529157` and `snap_dc228e8bba9d423fbe9f3dd35862f658`, the same pair on all nine exports |
| The step count | Gemini 3.8 Flash 74, 78, 95, 84 and 90 tool calls; GPT Sol 5.6 176, 137 and 98; Opus 4.8 49. Two of five Gemini runs reach 90 |
| Whether 1.5 accepts an empty list | Read only from the task reaching Trajectories with no file named; the export's task schema carries no field labelled for it |

Write each answer into this file the way HR 79's root `CLAUDE.md` rule 6 was written, naming
what landed wrong as well as what worked.

**Measured 09/19/2026, the first run set.** What landed wrong: the population lever. The memo
names "the reconciling items between that count and the BambooHR active record count" as an asked
field, and a run told to list reconciling items finds them; nine of nine did, and the Gemini mean
was 96.5% against a registered 38%. T1 retired on the rule it had registered. Also wrong, in the
verifiers: a column hint that demanded a word the memo does not use, and a key that rejected a
name with the ID beside it, both the false-zero class, both found by the set and fixed with a
scenario and a control each. What worked: the Filesystem-targeted PDF reached nine of nine runs,
the page-create tool landed every page under its exact title, and the harness's fixture matched
the platform's route. The tier also reads files by code now: every Gemini run parsed the roster,
the crosswalk and the org chart in a shell, 47 to 64 calls a run, so a lever that rests on a
record the run is not pointed at does not hold in this world.

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
