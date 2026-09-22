# Failure analysis - predictions registered before any run (09/22/2026)

**No v2 trajectory has run.** Everything in this file is a prediction with a date on it. Ten
Gemini 3.8 Flash trajectories exist against T2's wider ask and are re-scored here under v2's
rubric, which is evidence about the rubric's pricing and not a v2 run set; the section that
carries them says so in its own words. When a v2 run set lands, archive each run's page under
`qc/findings/run_set_MM-DD-YYYY/` with a `runs.json`, score it with `qc/score_run_set.py`, and
write the measured record under these predictions rather than over them, the way T1's, T1 v2's
and T2's records do.

## The rescope moved the ask, not the rubric around a failure

T2's rubric was 55 rows and 105 points. 14 of those points were free - the page existing, its
form, its column names, its date spelling - and 29 more were BambooHR rows at weight 1 each. A
run that printed the load's own wrong numbers earned them in full. The grader feedback the owner
carried in on 09/22/2026, measured on another world, is that a criterion whose failure materially
changes the output has to weigh more than 2; weight 2 suits extraction and weight 1 suits
formatting.

The owner's decision of 09/22/2026 was a full rescope rather than a reweighting: cut the free
content out of the **ask**, not only out of the rubric. Gone from the memo: the summary's
employee count, the name, department, tier and dollar-liability columns, the whole BambooHR
instruction, and the entire Form section. Review round 1, the same day and still before any v2
run, took two more lines out: the row per current employee, 156 values no 25-criterion rubric
covers, and the measurement-date sentence, an ask no row read. The memo now asks for one page, a
stated total dollar liability, stated total PTO hours, and the PTO hours and PTO liability for
five department lines, Sales and Marketing joined. `build/build_task_input.py` bars every removed
line from returning and `build/negative_controls.py` plants each one back and reads the guard red.

This is the test that separates a rescope from a rubric rescoped around a failure, and v2 passes
it on all four counts:

- **Every row that left was a row the failing runs passed, or a row no rubric could hold.** The
  free base falls from 14 of 105, 13.3%, to 1 of 79, 1.3%.
- **Every row that stayed is a determination those runs failed.** 78 of 79 points are the gate,
  the hours figure and ten line figures the load carries wrong. No row weighs 2.
- **The determination did not move.** Same rules from the cutover memo of 06/20/2026, same 52
  current employees, same 1,522.17 hours, same $92,739.54, same seven registered paths.
- **Review round 1 answered a reviewer, not a result.** It came on a feasibility finding about
  the ask's size, before any run against the ask, and the ten archived pages score the same 1 of
  79 before and after their rows are summed onto the lines.

## The rubric the predictions are scored against

13 rows, 79 points, every row App DB Programatic on the Wiki.js pages table, 12 primary. Row 1 is
the only row that is not a determination, the page published under the title, at weight 1, 1.3%
of the total. Row 2 is the gate, the total dollar liability of $92,739.54, weight 10, Critical
value. Row 3 is the total PTO hours of 1,522.17, weight 8. Rows 4 to 13 are the five lines' hours
and dollars, in the memo's order, each priced by the dollars it moves off the load: 7 for
Engineering, Finance and Corporate, and Sales and Marketing, rows 6 to 9, 12 and 13; 6 for
Customer Success, rows 4 and 5; 3 for Product, rows 10 and 11, whose cap and bridge net to $27.34.
Movement across the ten figures is $36,991.13. The rows are in `02_task_metadata.md` and
`build/rubric_plan.csv`, and every value in them recomputes from the world's bytes on each build.

## Nothing grades absence

A response that also prints every employee, or Sales and Marketing apart beside the joined line,
scores exactly what the golden scores. No row reads a row's absence. Two battery scenarios hold
it, "every employee, a line per department and a summary block" and "the lines as prose bullets",
each required to score every point.

## The registered paths

Every path is the golden schedule with rules dropped, recomputed by
`build/build_package_artifacts.py` and scored twice, once by the plan's predicates and once by
the generated row files, which `qc/score_run_set.py --self-check` prints side by side.

| Path | What the run does | Rows | Total it prints | Score |
|---|---|---|---|---|
| P0 | the July close method rolled forward: the HRIS report's rows and balances, the loaded tiers and rates, contractors and ended records inside, the two unloaded hires outside | 57 | $119,758.03 | 1 of 79, 1.3% |
| P1 | the HRIS report with the population fixed: 52 rows, balances uncapped, the loaded tiers and rates | 52 | $111,455.78 | 1 of 79, 1.3% |
| P2 | P1 with the 40.0-hour cap applied at 06/30/2026 | 52 | $90,983.94 | 15 of 79, 19.0% |
| P3 | P2 with tiers from the archive's service dates, the rehire unbridged, the tier change not timed, the rates as loaded | 52 | $92,804.10 | 22 of 79, 27.8% |
| P4 | P3 with the two signed pay changes applied | 52 | $92,934.50 | 29 of 79, 36.7% |
| P5 | P4 with the rehire bridged and the tier change timed; the step and the part-time schedule still missed | 52 | $92,789.47 | 49 of 79, 62.0% |
| P6 | the heal | 52 | $92,739.54 | 79 of 79, 100.0% |

P0 and P1 earn the page row alone: the two unloaded hires no longer carry cells of their own, so
a run that fixes the population and copies the report has nothing to show for it. The cap alone
is worth Finance and Corporate, 14 points, P1 to P2. Engineering's hours follow the archive's
tiers at P3 and its dollars the signed amendment at P4. Product and Sales and Marketing need the
bridge and the timed tier change, P5, and Customer Success, the one line carrying the step and
the part-time schedule, needs the heal.

## The honest prediction

**Registered Gemini 3.8 Flash mean for a v2 set of five: 5%.** It assumes four runs on P1 and one
on P2, the shape the ten measured runs make. The mixes that decide the package, registered now so
no one computes them after the fact:

| Mix of five | Mean |
|---|---|
| five on P1 | 1.3% |
| four on P1, one on P2 | 4.8% |
| three on P1, two on P2 | 8.4% |
| two on P1, three on P2 | 11.9% |
| one on P1, four on P2 | 15.4% |
| five on P2 | 19.0% |

Every run must apply the cap and more before a set reaches 40%. The rubric now moves with the
determination and with nothing else.

The reading behind the number, with ten trajectories under it:

- Ten of ten measured runs held the cutover memo, printed its cap sentence in their own traces,
  and applied the cap to nobody. Where a record printed a finished number, the memo lost to the
  record on every rule.
- The tier applies an explicit rule where no record answers first, which is why eight of ten
  derived both unloaded hires correctly. Under the lines those hires sit inside Customer Success
  and Sales and Marketing beside capped balances, so they earn nothing on their own.
- v2's ask is shorter, and a department line is a sum a run has to build. The prediction
  registered here is that the budget goes to the arithmetic rather than to the memo, and the run
  set decides it.

**Predicted failing rows, registered before the runs.** Rows 2 and 3 fail five of five, the gate
and the hours figure. Rows 4 to 13, every line figure, fail five of five, because the cap moves
every line and ten of ten measured runs missed it. Rows 8 and 9, Finance and Corporate, are the
first to pass on a run that applies the cap and nothing else.

## What the ten already-measured trajectories score under this rubric

Five runs of 09/20/2026 and five of 09/21/2026 ran against T2's wider ask. Their pages carry a
balance and an hourly rate per employee and no department line, so they are read twice by
`qc/score_run_set.py` from the archived bytes: as printed, and with `--as-lines`, which sums each
run's own employee rows onto the five lines with the engine's own row reader.

| Set | Run | Total it prints | As printed | Own rows summed onto the lines |
|---|---|---|---|---|
| 09/20/2026 | G1 | $111,455.78 | 1 of 79, 1.3% | 1 of 79, 1.3% |
| 09/20/2026 | G2 | $111,100.39 | 1 of 79, 1.3% | 1 of 79, 1.3% |
| 09/20/2026 | G3 | $111,455.78 | 1 of 79, 1.3% | 1 of 79, 1.3% |
| 09/20/2026 | G4 | $111,455.78 | 1 of 79, 1.3% | 1 of 79, 1.3% |
| 09/20/2026 | G5 | $111,100.39 | 1 of 79, 1.3% | 1 of 79, 1.3% |
| 09/21/2026 | G1 | $111,497.27 | 1 of 79, 1.3% | 1 of 79, 1.3% |
| 09/21/2026 | G2 | $111,455.78 | 1 of 79, 1.3% | 1 of 79, 1.3% |
| 09/21/2026 | G3 | $113,515.83 | 1 of 79, 1.3% | 1 of 79, 1.3% |
| 09/21/2026 | G4 | $111,455.78 | 1 of 79, 1.3% | 1 of 79, 1.3% |
| 09/21/2026 | G5 | $111,100.39 | 1 of 79, 1.3% | 1 of 79, 1.3% |

**What this proves.** Every one of the ten fails the gate and fails the cap, and the cap moves
every line, so under the lines no run earns anything but the page. G3 of 09/21/2026, which took
the archive's service dates and read 30.8% under the 27-row rubric, sums to 700.81 hours on
Engineering against 558.31, because its five capped balances are uncapped.

**What this does not prove.** These are re-scorings of runs against a different ask. A v2 run
reads a shorter memo that names five lines, spends its budget differently, and may land somewhere
none of the ten landed. Nothing here is a v2 run set, nothing here fires the decision rule, and a
v2 run set is owed before the package is called measured.

## The step gate

The EPM's line of 09/19/2026 is 90 steps on the platform's count in at least one Gemini
trajectory. T2's ten runs read 146 to 296 tool calls, one assistant turn per call, with the
floor on the two runs that wrote nothing to BambooHR. v2 removes 52 BambooHR writes and two
record creations and asks for five sums in place of a 52-row table, so the prediction registered
here is that the count falls and that the gate is the live risk on this package: over 90 on at
least one run is expected, and a run that copies the report into five sums could finish under it. If a set comes in
under 90 on every run, the record says so and the package is held on that ground alone, not
rescoped.

## What to read in each trajectory before scoring it

1. **Which rule documents it opened, and in what order.** The cutover memo, the handbook, the 2025
   policy and the wiki page decide the method; note which it read first and which it quoted.
2. **Which balance it took as the opening balance when two disagreed**, the report's uncapped
   figure or the archive's capped, and whether the cap was applied at all.
3. **Which service date it took for the nine migrated records**, and whether it bridged TRT-0071
   or reset him.
4. **Which rate it took for TRT-0088 and TRT-0117**, whether it found the signed documents or only
   the archive's history, and whether it read Marchetti's step and Quintanilla's schedule change.
5. **How it published.** The title, the published flag, one page or two, whether it joined Sales
   and Marketing, and whether it printed employee rows beside the lines. Neither is a graded fact.
6. **The step count** on the platform's own view.

## What the platform's own grading run has to show before the scores are trusted

Every row is an App DB row on the Wiki.js pages table. Before reading a zero as a failure of the
run, read the row's `details` string: it names the table it found, its column list, the
resolution route, `page_rows`, and the engine's notes, all of which the round-6 remedies of
09/21/2026 put there.

This matters more here than it did on T2. T2's first platform grading, G5 on 09/21/2026, read
1.9% on the pane against 18.1% on the archived bytes: 29 of 29 BambooHR rows agreed and every
wiki row read fail. T2 could tell a broken read from a failing run because it had a BambooHR half
that agreed. **v2 has no such half.** All 79 points are wiki rows, so a wiki read that fails the
way G5's failed would print 0% for a perfect response and 0% for the worst one. The first
graded v2 run is therefore read from its details line before its score: a row that reports
`page_rows` and a table list has graded a page, and a row that reports neither has not. Until a
pane shows that, no platform score on this task is read as the run's score.

## The decision rule, registered with the predictions

Registered on 09/20/2026 for T2 and unchanged for v2. **Under 40% on five Gemini runs:** the
package ships. **40% to 60%:** the package is held with the traces for the pod lead's call, and
the rubric is never rescoped around whatever failed. **Over 60%:** the tier applies the cutover
memo's rules against records that already carry answers, the lever is measured insufficient in
this world for this tier, and the package retires.

The rescope of 09/22/2026 and its review round 1 are not an exception to that rule and do not
restart the clock on it. Both happened before any v2 run, on grader and reviewer feedback about
pricing and feasibility rather than on a v2 result, both moved the ask and not the rubric's
treatment of a failure, and the ten re-scored trajectories it
is checked against are labelled in this file as what they are. If a v2 set reads over 60%, the
honest record is that a rule application over 52 people is not a determination this tier gets
wrong when every rule and every record sit in the tree, and the package retires rather than
narrowing again.
