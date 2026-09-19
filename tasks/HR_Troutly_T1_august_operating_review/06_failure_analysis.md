# Failure analysis - predictions registered before any run (09/19/2026)

**The predictions below were registered before any run**, on 09/19/2026, which is the only
thing that separates them from a rationalisation. The run set arrived the same day and is scored
under them, at the end of this file. When the
set lands, score every run against the 35-row rubric by hand, row by row, and write the measured
record under the predictions rather than over them. HR 79 T1's `06_failure_analysis.md` is the
shape: the predictions kept, the set scored beneath them, the divergence named.

## The rubric the predictions are scored against

35 verifiers, 113 points, one gate. The determination carries 78 of the 113:

| Determination | Rows | Points |
|---|---|---|
| The population: 52 current employees, the two unloaded hires in, the three ended records and the four contractors out | 18, 19, 20, 21, 22, 23, 24 | 44 |
| The Board reading of REQ-2026-036 | 3 | 9 |
| The two workbook requisitions and the accepted offer | 4, 5, 11 | 15 |
| The staffing split, which turns on the population | 29 | 5 |
| The derivative counts and the two unloaded hires' managers | 25, 26, 27, 30, 31, 32 | 12 |
| The asked fields a run prints correctly on the way | the rest | 28 |

## The registered paths

Every path is scored from the row list in `02_task_metadata.md`. A path names what the run does,
which rows it passes, and the score.

| Path | What the run does | Score |
|---|---|---|
| **P1** BambooHR taken whole | Lists the 57 active rows as current employees, contractors and ended records inside, the two unloaded hires outside. Reads REQ-2026-036 as the Board's backfill and marks it Approved. Reads 037 and 038 as Not approved off the ATS export's source column. Builds the recruiting table from the open requisitions only, so it carries Adjei and nobody else. Prints the Board budget from the plan | **37 of 113, 32.7%** |
| **P1b** P1 with the contractors out | The People Metrics method and the Finance memo both say contractors out, and the CTR prefix and the Contract titles make them visible | 42 of 113, 37.2% |
| **P1c** P1b with TRT-0064 caught | The resignation email, the Board minutes and the requisition's own Backfill note all name the departure, so a run can drop her and still miss TRT-0037 and TRT-0049, which only the crosswalk, the archive and the org chart's silence carry | 47 of 113, 41.6% |
| **P3** P1b with the recruiting table diffed | Reads all three hired applications, finds no BambooHR row for any of them, lists Okonkwo and Ibarra with their start dates, but keeps the staffed page on BambooHR | 48 of 113, 42.5% |
| **P4** the population healed, 036 missed | Reconciles the roster, the org chart and the crosswalk to 52, names every reconciling item, and still reads 036 as the approved backfill | 104 of 113, 92.0% |
| **P2** the heal | Everything | 113 of 113, 100% |
| **P5** the pages not published, or published under other titles | Both existence rows and every content row fail | 0 to 3 of 113 |

**The modal path is P1 or P1b.** Both sit under the bar. P1c and P3 sit just over it, and one
run on either in a set of five pulls the mean over 40% if the other four are P1b.

**Registered Gemini 3.8 Flash mean: 38%.** The honest number rather than the convenient one. It
assumes four runs on P1 or P1b and one on P1c or P3. A single P4 in the set puts the mean near
50%, and the tier has shown on HR 79 that it reads a record carefully when the request points at
it; the memo points at BambooHR and the org chart in the same sentence, so P4 is possible.

**The decision rule, registered with the predictions.** If the next five Gemini runs mean under
40%, the package ships. If they mean 40% to 60%, the honest reading is that the population is a
lever the tier sometimes takes, and the package returns with the free rows cut further and the
weight kept on the determination, not with the rubric rescoped around whatever failed. If they
mean over 60%, the population has healed, and the package retires with the lever recorded as
measured insufficient. That is HR 32's T24 rule and HR 79 T1's, and the reason this record
carries the arithmetic rather than a hope.

## What to read in each trajectory before scoring it

1. **Which surfaces it opened.** The roster, the org chart PDF, the crosswalk and the archive are
   the four that decide the population. A run that opens none of them and lists BambooHR is P1;
   note which of the four it opened and what it did with each.
2. **Whether it noticed the three ended records.** The tells are the crosswalk's Terminated column,
   the org chart's silence and the archive's TerminationDate. A run that drops TRT-0064 on the
   resignation email alone is P1c, and the scoring should say which record it used.
3. **Whether it diffed the hired applications against BambooHR**, or only the open requisitions.
   The recruiting table's definition points at the diff; whether the tier follows it is the
   measurement.
4. **Where it read the backfill.** Page 2 of the Board plan carries the CSM I level; the ATS export
   carries CSM II. A run that cites both and still writes Approved is the failure worth quoting.
5. **How it published.** The title it used, the path it chose, whether it saved a draft or
   published, and whether it wrote markdown or HTML. Row 1 and row 17 read the published flag, and
   a run that saved drafts fails two rows and nothing else, which is a platform tell and not a
   reasoning failure.
6. **The step count.** The requirement is 90+ in at least one Gemini trajectory. HR 79 T1 measured
   148 to 316 on a 14-employee ask; this ask has 52 employees, 8 requisitions and two pages to
   write, so the estimate is that every run clears 90.

## What the platform's own grading run has to show before the scores are trusted

Every row here is an App DB row, and HR 79 measured that a snapshot may carry placeholder column
names and that Studio's generated code scored 13 of 15, 8 of 10 and 4 of 10 on its first attempt.
So before reading a zero as a failure of the run, read the row's `details` string: it names the
pages table it found, its column list, which resolution route it took, every page row matching
the title and every table row it considered. A zero whose details say `no page titled` on a run
that plainly published the page is a title mismatch or a snapshot that does not carry the live
`pages` table, and it is a grading defect rather than a difficulty measurement. `qc/README.md`
carries the harness record: 1295 of 1295 verdicts correct across 37 scenarios, including the
placeholder-name branch, the HTML branch and the em-dash title.

## The probe, and what it settles for free

Nothing in this package rides on an unmeasured vehicle: the one input is a PDF on the Filesystem
target, measured on HR 79 at 12 of 12. What the first run set settles for free is whether a
Wiki.js page created through the platform's tools lands in the `pages` table under the title the
run gives it, and under what path. Read it off the transcripts' page-create calls and the
grading run's `details`, and write the answer into `tasks/README.md` the way HR 79's rule 6 was
written, naming what landed wrong as well as what worked.


## The measured record - the first run set, 09/19/2026

**Nine trajectories ran on 09/19/2026 on the prompt as registered**, byte-identical to the
`PROMPT` constant in every export: five Gemini 3.8 Flash, three GPT Sol 5.6 and one Claude Opus
4.8, every one on the React Toolbelt Agent (500 steps) against the platform `Ergon - bamboohr +
greenhouse + wiki_js (MCP, auto)`, world snapshot `snap_c6f6a0879f3d47a19048ee80d7529157`, task
data `snap_dc228e8bba9d423fbe9f3dd35862f658`. Each run's two published pages are archived as the
export carries them under `qc/findings/run_set_09-19-2026/`, with `runs.json` holding the model,
the trajectory id and the step count read off the export. `python3 qc/score_run_set.py` grades
the archive with the verifier files and prints the table below. Nothing in it is typed.

| Run | Model | Steps | Score | Rows failed |
|---|---|---|---|---|
| G1 | gemini-3.8-flash | 74 | 105 of 113, 92.9% | 9, 25, 26, 27, 28 |
| G2 | gemini-3.8-flash | 78 | 112 of 113, 99.1% | 9 |
| G3 | gemini-3.8-flash | 95 | 111 of 113, 98.2% | 9, 35 |
| G4 | gemini-3.8-flash | 84 | 112 of 113, 99.1% | 9 |
| G5 | gemini-3.8-flash | 90 | 105 of 113, 92.9% | 9, 25, 26, 27, 28 |
| O1 | gpt-5.6-sol | 176 | 96 of 113, 85.0% | 3, 8, 29, 30 |
| O2 | gpt-5.6-sol | 137 | 93 of 113, 82.3% | 3, 9, 13, 16, 25, 26, 27, 28 |
| O3 | gpt-5.6-sol | 98 | 113 of 113, 100.0% | none |
| Opus | claude-opus-4-8 | 49 | 97 of 113, 85.8% | 3, 25, 26, 27, 28 |

**Gemini 3.8 Flash mean 96.5%, against a registered 38%.** GPT Sol 5.6 mean 89.1%, Opus 85.8%.

### The decision rule, applied

The rule registered above reads: over 60% on five Gemini runs, the population has healed, and
the package retires with the lever recorded as measured insufficient. The measured mean is 96.5%
and the lowest Gemini run is 92.9%. **The package retired on 09/19/2026.** Nothing in the rubric
is rescoped. The record stays as the measurement of a lever that did not hold.

### Which path each run took

None of the nine took P1, P1b, P1c or P3. Rows 18 to 24, the 44 population points, pass on all
nine: every run reconciled to 52, and every run named the four contractors, the three ended
records and the two unloaded hires, which those rows require. Every run opened the master
roster, the August org chart and the crosswalk. O1 published a first staffed page at 54, with
Engineering 18 and Finance and Corporate 8, and corrected it to 52 by `update_page` before it
finished, the one run that healed in flight rather than on first sight.

| Path | Runs | What decided it |
|---|---|---|
| P2, the heal | O3 at 113; G2 and G4 at 112; G3 at 111; G1 and G5 at 105 | The population and REQ-2026-036 both right; the points lost are form rows, listed below |
| P4, the population healed and 036 missed | Opus at 97, O1 at 96, O2 at 93 | Approved on REQ-2026-036 as the triggered backfill, row 3 at 9 points |

The one determination that split the tiers ran the wrong way for the package: five of five
Gemini runs held REQ-2026-036 to the level mismatch and wrote Not approved, and three of the
four frontier runs waived it as the triggered backfill. The failure the predictions said was
worth quoting, a run that cites both levels and still writes Approved, appeared on Opus, O1 and
O2 and on no Gemini run.

### The rows that failed, and what each was

         G1   G2   G3   G4   G5   O1   O2   O3   Opus
row 03 w9  .    .    .    .    .    X    X    .    X
row 08 w1  .    .    .    .    .    X    .    .    .
row 09 w1  X    X    X    X    X    .    X    .    .
row 13 w2  .    .    .    .    .    .    X    .    .
row 16 w1  .    .    .    .    .    .    X    .    .
row 25 w2  X    .    .    .    X    .    X    .    X
row 26 w2  X    .    .    .    X    .    X    .    X
row 27 w2  X    .    .    .    X    .    X    .    X
row 28 w1  X    .    .    .    X    .    X    .    X
row 29 w5  .    .    .    .    .    X    .    .    .
row 30 w2  .    .    .    .    .    X    .    .    .
row 35 w1  .    .    X    .    .    .    .    .    .

- **Row 3, 9 points.** Opus, O1 and O2 wrote Approved on REQ-2026-036, basis the 06/15/2026
  departure meeting the backfill condition. The reading the package graded against.
- **Row 9, 1 point.** Six runs dated an open requisition's status from its opening date rather
  than from the 08/31/2026 export. A reading of "the latest record that supports the status".
- **Rows 25 to 28, 7 points.** G1, G5, O2 and Opus put the count by department in a small table
  inside the summary rather than in a sentence, and the verifier reads prose. The details say the
  same thing on every one: the table count is right but the summary does not state it. Recorded
  as a strictness of the verifier and left as built, since the package retires; a later package
  should let a table under the summary heading state a figure.
- **Rows 29 and 30, 7 points.** O1's staffed tables carry 20 rows with a requisition and 32
  without, one employee on the wrong table.
- **Row 8, 1 point.** O1 dated REQ-2026-038's status 08/31/2026 off the export rather than
  08/20/2026 off the acceptance.
- **Rows 13 and 16, 3 points.** O2 read the Customer Success backfill as filled by Okonkwo on
  07/22/2026, so it did not state that none of the approved roles is filled, and its recruiting table carries no row keyed on Rafael Ibarra.
- **Row 35, 1 point.** G3 wrote one date on the staffed page as August 24, 2026.

### Two false zeros the run set found in the verifiers, fixed in the builder before the scores above

1. **The source-date column hint.** Rows 8 and 9 looked the column up by the hint
   `status source date`, every word required. Seven of nine runs headed it `Source date`, the
   memo's own words, and as first graded both rows failed on those seven for the header alone.
   The hint is now `source date`, the battery carries the memo's header as a scenario, and a
   negative control plants the old hint and confirms the red.
2. **A key with an identifier beside it.** The key match accepted the name and nothing else, so
   `Kwame Adjei (ATS-4471)` and `Simone Okonkwo (TRT-0153)` keyed no row and G5 lost rows 11 to
   14, 11 points, for printing the ID the memo asks for beside the name. The match now accepts
   one parenthesised identifier after the key and nothing else. Scenario and control added.

As first graded, before the two fixes: G1 92.0, G2 98.2, G3 97.3, G4 98.2, G5 82.3, O1 85.0,
O2 81.4, O3 100.0, Opus 85.8, a Gemini mean of 93.6%. The verdict is the same on either set.
Harness after the fixes: 1365 of 1365 verdicts across 39 scenarios.

### Why the lever did not hold, as far as the transcripts show

1. **The request names the reconciliation.** The staffed page's summary is defined as "the
   reconciling items between that count and the BambooHR active record count", and the hiring
   page's as "the reconciling items between the open requisitions and the Board plan". A run told
   to list the reconciling items goes looking for them. The prompt AutoQC round of the same day
   read the same clauses as signalling the conflict, from the other side
   (`qc/findings/prompt_round1_09-19-2026.md`). The leak assertions on the memo barred the counts
   and every word for a record being stale or missing; they did not bar the word reconciling,
   which is the one that gave the answer its shape.
2. **"Count people the way the People Metrics page describes"** points at a method that excludes
   contractors, terminations and future-dated hires by name.
3. **The tier reads files by code.** Every Gemini run pulled the toolbelt's shell and parsed the
   roster, the crosswalk and the org chart PDF in Python, 47 to 64 shell calls a run. A run that
   lists a directory and parses everything in it does not need to be pointed at a workbook.
4. **What was left of the failure is 9 points.** REQ-2026-036 split the tiers, the frontier
   runs on the wrong side. A package carried by that determination alone is not a task.

### The step count

Tool calls a run: Gemini 74, 78, 95, 84 and 90; GPT 176, 137 and 98; Opus 49. Two of the five
Gemini runs reach 90. The threshold is met, and moot.

### The platform tells, recorded for the next package

- **A page created through `wiki_js_mcp_wikijs_mcp_create_page` lands in `pages`** with ids 11
  and 12 after the ten seed pages, the title exactly as the run gave it, `isPublished` true by
  default and the content type markdown. The path is the run's choice: seven used the slug of the
  title, two prefixed it with `operating-review/`. No row here reads a path.
- **No run saved a draft, wrote HTML or typed an em dash in a title.** Opus typed an em dash in
  the H1 inside the content while giving the title field a hyphen, which no row reads.
- **Every run read its pages back with `get_page`** after writing them.
- **The memo reached nine of nine runs** on the Filesystem target, and every run's tool calls
  name it. The export's task schema carries no field labelled for 1.5, so its acceptance of an empty list is read only from the task reaching Trajectories with no file named.
- **The task on the platform carried the synth's twenty verifiers**, em-dash titles and all,
  through the run set. No run was graded by this rubric on the platform. The 35-row import,
  loadable now that its snapshot ids are real, was never loaded and now need not be.
