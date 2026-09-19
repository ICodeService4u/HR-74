# Failure analysis - predictions registered before any run (09/19/2026)

**No trajectory has run on this task.** Everything below is a prediction with a date on it, which
is the only thing that separates it from a rationalisation once the run set arrives. When the
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
