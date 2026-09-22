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
content out of the **ask**, not only out of the rubric. The memo now asks for one page, a stated
total dollar liability, stated total PTO hours, and a row per current employee with the employee
ID, the PTO balance in hours and the hourly rate. Gone from the memo: the summary's employee
count, the name, department, tier and dollar-liability columns, the whole BambooHR instruction,
and the entire Form section, which is the dates, the decimals, the sum rule and the ID rule.
`build/build_task_input.py` bars each of them from returning and `build/negative_controls.py`
plants each one back and reads the guard red.

This is the test that separates a rescope from a rubric rescoped around a failure, and v2 passes
it on all four counts:

- **Every row that left was a row the failing runs passed.** The free base falls from 14 of 105,
  13.3%, to 1 of 143, 0.7%. Nothing that a failing response earned in full survives.
- **Every row that stayed is a determination those runs failed.** 142 of 143 points are the gate,
  the hours figure and 24 cells where the world's figure at 08/31/2026 is not the figure the load
  carries. No row weighs 2.
- **The determination did not move.** Same rules from the cutover memo of 06/20/2026, same 52
  current employees, same 1,522.17 hours, same $92,739.54, same seven registered paths.
- **The ten measured pages are read as they were published.** They lose points for content the
  rubric no longer buys, not for content the memo no longer asks for; nothing in v2 grades
  absence, so their extra columns and extra rows cost them nothing.

The one honest asymmetry: 19 of a copying run's 143 points, rows 19, 20, 23, 24, are the two
hires the load never carried, where there is no wrong number on file to copy. The other 124
points all require a rule applied against a record that already prints a finished answer.

## The rubric the predictions are scored against

27 rows, 143 points, every row App DB Programatic on the Wiki.js pages table, 26 primary. Row 1
is the only row that is not a determination, the page published under the title, at weight 1,
0.7% of the total. Row 2 is the gate, the total dollar liability of $92,739.54, weight 10,
Critical value. Row 3 is the total PTO hours of 1,522.17, weight 8. Rows 4 to 27 are the 24
cells the load has wrong, 19 balances and 5 hourly rates over 22 employees, each priced by the
dollars that cell moves: 7 where it moves $2,000.00 or more, four rows; 6 at $800.00 or more,
six rows; 5 at $250.00 or more, seven rows; 4 at $80.00 or more, four rows; 3 below that, three
rows. Gross movement across the 24 cells is $23,184.21. The rows are in `02_task_metadata.md` and
`build/rubric_plan.csv`, and every value in them recomputes from the world's bytes on each build.

## Nothing grades absence

A response that prints all 52 employees scores exactly what a response that prints only the 22
the load has wrong scores. No row reads a row's absence, and no row reads a column the memo no
longer asks for. This was an explicit constraint from the owner: an exclusion criterion would
invalidate the golden, because a correct response over-delivers anyway. Two battery scenarios
hold both ends, "every employee, seven columns and a summary block" and "only the rows the load
has wrong", each required to score every point.

## The registered paths

Every path is the golden schedule with rules dropped, recomputed by
`build/build_package_artifacts.py` and scored twice, once by the plan's predicates and once by
the generated row files, which `qc/score_run_set.py --self-check` prints side by side.

| Path | What the run does | Rows | Total it prints | Score |
|---|---|---|---|---|
| P0 | the July close method rolled forward: the HRIS report's rows and balances, the loaded tiers and rates, contractors and ended records inside, the two unloaded hires outside | 57 | $119,758.03 | 1 of 143, 0.7% |
| P1 | the HRIS report with the population fixed: 52 rows, balances uncapped, the loaded tiers and rates | 52 | $111,455.78 | 19 of 143, 13.3% |
| P2 | P1 with the 40.0-hour cap applied at 06/30/2026 | 52 | $90,983.94 | 76 of 143, 53.1% |
| P3 | P2 with tiers from the archive's service dates, the rehire unbridged, the tier change not timed, the rates as loaded | 52 | $92,804.10 | 100 of 143, 69.9% |
| P4 | P3 with the two signed pay changes applied | 52 | $92,934.50 | 107 of 143, 74.8% |
| P5 | P4 with the rehire bridged and the tier change timed; the step and the part-time schedule still missed | 52 | $92,789.47 | 119 of 143, 83.2% |
| P6 | the heal | 52 | $92,739.54 | 143 of 143, 100.0% |

P0 earns the page row alone. P1's 19 points are the two unloaded hires' two cells each. The cap
is worth 57 points on its own, P1 to P2, which is the shape the pricing was built for: the rule
every measured run set aside moves more of the rubric than every other rule together.

## The honest prediction

**Registered Gemini 3.8 Flash mean for a v2 set of five: 21%.** Not the convenient number, but
close to it, and the record says why it is registered anyway. It assumes four runs on P1 and one
on P2, which is 30.4 points of 143. The mixes that decide the package, registered now so no one
computes them after the fact:

| Mix of five | Mean |
|---|---|
| five on P1 | 13.3% |
| four on P1, one on P2 | 21.3% |
| three on P1, two on P2 | 29.2% |
| two on P1, three on P2 | 37.2% |
| one on P1, four on P2 | 45.2% |

Four of five runs must apply the 40.0-hour cap before the set crosses the 40% line. That is the
sensitivity the rescope bought: the rubric now moves with the determination and with almost
nothing else.

The reading behind the number, unchanged in substance from T2's and now with ten trajectories
under it:

- Ten of ten measured runs held the cutover memo, printed its cap sentence in their own traces,
  and applied the cap to nobody. Where a record printed a finished number, the memo lost to the
  record on every rule.
- The tier applies an explicit rule where no record answers first. Both unloaded hires were
  derived correctly by eight of the ten, from the roster and the offer letters, at 6.15 and 3.08
  hours. That is the whole of P1's 19 points and it is the failure mode stated exactly.
- Four of the five runs of 09/20/2026 opened the signed promotion approval and the comp
  amendment and printed the loaded rates anyway. Rows 22 and 26 measure that directly.
- v2's ask is shorter, so a run has more budget for the rules and less to copy. The prediction
  registered here is that the budget goes to more rows on the page rather than to the memo, and
  the run set decides it.

**Predicted failing rows, registered before the runs.** Rows 2 and 3 fail five of five, the gate
and the hours figure. Rows 4 to 13 and row 21, the eleven capped openings, fail five of five.
Rows 14 to 18 pass only on a run that takes the archive's service dates, which one of ten did.
Rows 19, 20, 23 and 24 pass on every run that prints the two hires, which eight of ten did. Rows
22, 25, 26 and 27 fail unless the run puts a signed document, an offer letter or a schedule
change form over the record; one of ten did, on row 26.

## What the ten already-measured trajectories score under this rubric

Five runs of 09/20/2026 and five of 09/21/2026 ran against T2's wider ask. Their pages carry a
balance and an hourly rate per employee, the two cells v2 grades, so v2's row files read them
directly with no restatement. Scored by `qc/score_run_set.py` from the archived bytes:

| Set | Run | Total it prints | Score under v2 | Rows passed |
|---|---|---|---|---|
| 09/20/2026 | G1 | $111,455.78 | 19 of 143, 13.3% | 1, 19, 20, 23, 24 |
| 09/20/2026 | G2 | $111,100.39 | 1 of 143, 0.7% | 1 |
| 09/20/2026 | G3 | $111,455.78 | 19 of 143, 13.3% | 1, 19, 20, 23, 24 |
| 09/20/2026 | G4 | $111,455.78 | 19 of 143, 13.3% | 1, 19, 20, 23, 24 |
| 09/20/2026 | G5 | $111,100.39 | 1 of 143, 0.7% | 1 |
| 09/21/2026 | G1 | $111,497.27 | 22 of 143, 15.4% | 1, 19, 20, 23, 24, 26 |
| 09/21/2026 | G2 | $111,455.78 | 19 of 143, 13.3% | 1, 19, 20, 23, 24 |
| 09/21/2026 | G3 | $113,515.83 | 44 of 143, 30.8% | 1, 14, 15, 16, 17, 18, 19, 20, 23, 24 |
| 09/21/2026 | G4 | $111,455.78 | 19 of 143, 13.3% | 1, 19, 20, 23, 24 |
| 09/21/2026 | G5 | $111,100.39 | 1 of 143, 0.7% | 1 |

Means 8.3% on the first set and 14.7% on the second, against 23.9% and 38.1% under T2's own
rubric on the same bytes.

**What this proves.** The pricing does what the owner asked it to do. Every one of the ten fails
the gate and fails the cap, and no run earns a point for content that a failing response prints
correctly. The 09/21 set's 38.1% under T2 was 23 points of BambooHR rows and form rows sitting on
top of a wrong answer; under v2 that run set reads 14.7% and the two runs T2 measured within ten
points of the 40% line, G1 at 50.5% and G3 at 49.5%, read 15.4% and 30.8%. What the ten still
earn is the page row, the two unloaded hires' balances and rates, which a run computes from the
roster and the offer letters, and on G3 of 09/21/2026 the five service-date balances, rows 14 to
18. G1 of 09/21/2026 alone valued Luk at the signed rate.

**What this does not prove.** These are re-scorings of runs against a different ask. The memo
they read asked for seven columns, a summary count and 52 BambooHR records, and it carried a Form
section. A v2 run reads a shorter memo, spends fewer calls, and may land somewhere none of the
ten landed. Nothing here is a v2 run set, nothing here fires the decision rule, and a v2 run set
is owed before the package is called measured.

## The step gate

The EPM's line of 09/19/2026 is 90 steps on the platform's count in at least one Gemini
trajectory. T2's ten runs read 146 to 296 tool calls, one assistant turn per call, with the
floor on the two runs that wrote nothing to BambooHR. v2 removes 52 BambooHR writes, two record
creations and four columns of arithmetic, so the prediction registered here is that the count
falls and that the gate is the live risk on this package: over 90 on at least one run is expected,
and a run that copies the report into three columns could finish under it. If a set comes in
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
5. **How it published.** The title, the published flag, one page or two, and how many rows it
   printed. The row count is evidence about the run and is not a graded fact.
6. **The step count** on the platform's own view.

## What the platform's own grading run has to show before the scores are trusted

Every row is an App DB row on the Wiki.js pages table. Before reading a zero as a failure of the
run, read the row's `details` string: it names the table it found, its column list, the
resolution route, `page_rows`, and the engine's notes, all of which the round-6 remedies of
09/21/2026 put there.

This matters more here than it did on T2. T2's first platform grading, G5 on 09/21/2026, read
1.9% on the pane against 18.1% on the archived bytes: 29 of 29 BambooHR rows agreed and every
wiki row read fail. T2 could tell a broken read from a failing run because it had a BambooHR half
that agreed. **v2 has no such half.** All 143 points are wiki rows, so a wiki read that fails the
way G5's failed would print 0.7% for a perfect response and 0.7% for the worst one. The first
graded v2 run is therefore read from its details line before its score: a row that reports
`page_rows` and a table list has graded a page, and a row that reports neither has not. Until a
pane shows that, no platform score on this task is read as the run's score.

## The decision rule, registered with the predictions

Registered on 09/20/2026 for T2 and unchanged for v2. **Under 40% on five Gemini runs:** the
package ships. **40% to 60%:** the package is held with the traces for the pod lead's call, and
the rubric is never rescoped around whatever failed. **Over 60%:** the tier applies the cutover
memo's rules against records that already carry answers, the lever is measured insufficient in
this world for this tier, and the package retires.

The rescope of 09/22/2026 is not an exception to that rule and does not restart the clock on it.
It happened before any v2 run, on grader feedback about pricing rather than on a v2 result, it
moved the ask and not the rubric's treatment of a failure, and the ten re-scored trajectories it
is checked against are labelled in this file as what they are. If a v2 set reads over 60%, the
honest record is that a rule application over 52 people is not a determination this tier gets
wrong when every rule and every record sit in the tree, and the package retires rather than
narrowing again.
