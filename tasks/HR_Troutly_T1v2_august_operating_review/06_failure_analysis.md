# Failure analysis - predictions registered before any v2 run (09/19/2026)

**No trajectory has run on T1 v2.** Everything below is a prediction with a date on it. When the
run set lands, archive each run's two pages under `qc/findings/run_set_MM-DD-YYYY/` with a
`runs.json`, run `python3 qc/score_run_set.py --set <folder>`, and write the measured record under
these predictions rather than over them, the way T1's `06_failure_analysis.md` does.

## The rubric the predictions are scored against

24 verifiers, 83 points, one gate. The population carries 56 points, 67.5%; the Board
reading 20, 24.1%; the fields a run prints on any path 7, 8.4%.

| Determination | Rows | Points |
|---|---|---|
| The set of 52 current employees, the two unloaded hires in, the three ended records and the four contractors out, the count by department, the split and the two managers | 11 to 22 | 56 |
| The Board reading of REQ-2026-036, 037 and 038, the budget, the filled count | 3, 4, 5, 8, 9 | 20 |
| The two pages published, the five Approved cells, the eight status cells, the two form rows | 1, 2, 6, 7, 10, 23, 24 | 7 |

## The registered paths

Every path is a page the battery carries, scored by the verifier files themselves
(`qc/scenarios.py`, the `bamboo_path` pages), so the arithmetic here recomputes on every build.

| Path | What the run does | Score |
|---|---|---|
| **P1** BambooHR taken whole | Lists the 57 active rows as current employees, contractors and ended records inside, the two unloaded hires outside. Reads the Board plan right | **27 of 83, 32.5%** |
| **P1b** P1 with the contractors out | The CTR prefix and the Contract titles make the class visible. 53 rows, and 31 of them without a requisition by arithmetic, so row 20 passes | **31 of 83, 37.3%** |
| **P1c** P1b with TRT-0064 caught | The resignation email, the minutes and the requisition's Backfill note all name her departure. 52 rows by arithmetic with TRT-0037 and TRT-0049 still on them; the gate matches the set and fails, the two split rows pass | 40 of 83, 48.2% |
| **P1x** P1 with the wiki page read as the Board plan | The Hiring Plan page says Board approved on 06/20/2026 over eight roles at $868,000.00, and the run reads no further | 8 of 83, 9.6% |
| **S2x** the population healed, the wiki page read as the Board plan | Everything on the staffed page right; three Approved cells and the budget wrong | 64 of 83, 77.1% |
| **P4** the population healed, 036 missed | Reconciles to 52 and reads 036 as the triggered backfill, which three of four frontier runs did on T1 | 76 of 83, 91.6% |
| **P2** the heal | Everything | 83 of 83, 100.0% |

**The modal failing path is P1 or P1b.** Both sit under 40%. P1c sits at 48.2%, the band the
decision rule reads as a lever the tier sometimes takes.

## The honest prediction, and what T1's traces say about it

**Registered Gemini 3.8 Flash mean: 58%.** Not the convenient number. It assumes two runs on P1
or P1b and three that heal the population, at roughly 92%, and it rests on this reading of the
nine T1 trajectories of the same day:

- Every Gemini run listed the directory tree and parsed everything in it by shell, 47 to 64
  calls a run, and reached the roster and the crosswalk without being pointed at them. The
  memo's pointers decided the order of the reads, not whether they happened.
- What the pointers did decide was the reading. The memo told the run there were reconciling
  items to list, and defined a table of recruiting records with no BambooHR match; a run that
  reads the roster's 52 against BambooHR's 57 without that instruction has to decide which is
  the population, and the handbook makes BambooHR the system of record.
- The Board side is the new exposure. With no authority clause, the run has to choose between a
  wiki page footed Board approved over eight roles and a Board plan that supersedes it in terms.
  T1 measured five of five Gemini reading the plan right when told where it was.

**The decision rule, registered with the predictions.** Under 40% on five Gemini runs: the
package ships. 40% to 60%: the population is a lever the tier sometimes takes, and the package
returns with the free rows cut further, never with the rubric rescoped around whatever failed.
Over 60%: the population has healed with the pointers gone as well, the lever is measured
insufficient in this world for this tier, and the package retires. The house rule is that the
failure has to be the ask, not sit beside it: if the run set reads over 60%, the honest record is
that a 52-employee reconciliation is not a determination this tier gets wrong when the deciding
files sit in the tree, and no third memo rescues it.

## T1's nine runs, graded by the v2 rubric

Those runs carried the T1 memo with every pointer in it, so they measure nothing about v2's
lever. They are here because they are the only real pages this world has, and the v2 verifiers
have to pass correct work in the forms real runs use: bulleted summaries, notes beside keys,
tables under the summary heading.

| Run | Model | Steps | Score | Rows failed |
|---|---|---|---|---|
| G1 | gemini-3.8-flash | 74 | 78 of 83, 94.0% | 18 |
| G2 | gemini-3.8-flash | 78 | 83 of 83, 100.0% | none |
| G3 | gemini-3.8-flash | 95 | 82 of 83, 98.8% | 24 |
| G4 | gemini-3.8-flash | 84 | 83 of 83, 100.0% | none |
| G5 | gemini-3.8-flash | 90 | 78 of 83, 94.0% | 18 |
| O1 | gpt-5.6-sol | 176 | 73 of 83, 88.0% | 3, 19, 20 |
| O2 | gpt-5.6-sol | 137 | 69 of 83, 83.1% | 3, 6, 9, 18 |
| O3 | gpt-5.6-sol | 98 | 83 of 83, 100.0% | none |
| Opus | claude-opus-4-8 | 49 | 71 of 83, 85.5% | 3, 18 |

Gemini mean 97.3%. The rows that fail are the Board reading on the three frontier runs that
waived REQ-2026-036, and the department line where a run put the counts in a table under the
summary heading, which rule 8 above accepts and the engine's prose reading does not yet.

## What to read in each trajectory before scoring it

1. **Which surfaces it opened, and in what order.** The roster, the org chart PDF, the crosswalk
   and the archive decide the population; the Board plan PDF and the minutes decide the Board
   reading. Note whether the run found each by listing the tree or by following a name.
2. **Which record it took as the population when two disagreed.** A run that saw 52 on the roster
   and 57 in BambooHR and kept 57 is P1 with the evidence in hand, and the quote is worth keeping.
3. **Which record it took as the Board plan.** The wiki page, the workbook or the PDF.
4. **How it published.** Title, path, published flag, markdown or HTML. Rows 1 and 10 read the
   flag.
5. **The step count.** 90 or more in at least one Gemini trajectory. T1 measured 74 to 95 tool
   calls; the reads are the same and the memo is shorter, so the estimate is the same range.

## What the platform's own grading run has to show before the scores are trusted

Every row is an App DB row. Before reading a zero as a failure of the run, read the row's
`details` string: it names the pages table it found, its column list, the resolution route, every
page row matching the title and every table row it considered. T1's harness fixture matched the
platform's `get_page` route on nine of nine runs; the grading snapshot's column names remain
unmeasured, and the engine handles real names, the documented layout and a fallback.
