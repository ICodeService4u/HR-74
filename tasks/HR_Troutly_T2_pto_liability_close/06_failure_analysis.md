# Failure analysis - predictions registered before any run (09/20/2026)

**The five Gemini trajectories have run and decided; the measured record is at the end.** Everything
above it is a prediction with a date on it. When the run
set lands, archive each run's page and its BambooHR rows under `qc/findings/run_set_MM-DD-YYYY/`
with a `runs.json`, score it against the registered paths, and write the measured record under
these predictions rather than over them, the way T1's and v2's records do.

## The plan the predictions are scored against

21 planned rows, 87 points, one gate, as registered before the runs. The determination carried 70 points, 80.5%. BambooHR
brought to the schedule carried 12, 13.8%. The page and its form carried 5, 5.7%. Task round 1 of 09/20/2026 restructured the set to 28 rows and 89 points with no registered weight moved, and the re-scored tables sit under the measured record below. The rows are in `02_task_metadata.md` and `build/rubric_plan.csv`.

## The registered paths

Every path is the golden schedule with rules dropped, recomputed by `build/build_package_artifacts.py`
and scored by the plan's own predicates, so the arithmetic here recomputes on every build.

| Path | What the run does | Rows | Total it prints | Score |
|---|---|---|---|---|
| P0 | the July close method rolled forward: the HRIS report's rows and balances, the loaded tiers and rates, contractors and ended records inside, the two unloaded hires outside | 57 | $119,758.03 | 8 of 87, 9.2% |
| P1 | the HRIS report with the population fixed: 52 rows, balances uncapped, the loaded tiers and rates | 52 | $111,455.78 | 24 of 87, 27.6% |
| P2 | P1 with the 40.0-hour cap applied at 06/30/2026 | 52 | $90,983.94 | 29 of 87, 33.3% |
| P3 | P2 with tiers from the archive's service dates, the rehire unbridged, the tier change not timed, the rates as loaded | 52 | $92,804.10 | 34 of 87, 39.1% |
| P4 | P3 with the two signed pay changes applied | 52 | $92,934.50 | 47 of 87, 54.0% |
| P5 | P4 with the rehire bridged and the tier change timed; the step and the part-time schedule still missed | 52 | $92,789.47 | 65 of 87, 74.7% |
| P6 | the heal | 52 | $92,739.54 | 87 of 87, 100.0% |

**Corrected 09/20/2026, found by the scorer's self-check while G1 was being scored.** Rows 6, 8 and 9
were planned with predicates reading the opening balance, the bridged accrual and Thornbury's
accrual, none of which the page carries. The reviewer decision rules read the balance cell and the
tier cell, and the predicates now read what the rules read, so every row grades the output alone.
P2 fell from 29 to 24, P3 from 34 to 29 and P4 from 47 to 42; G1 and G3 score the same under both
readings. The registered mean of 45% below was computed on the earlier numbers and stands as
written; the same mix, two runs on P3, two on P4 and one past P5, reads 52.2% under the corrected
table, on the same side of the 40% line. Also corrected 09/20/2026: the gate was planned at 15
on a platform scale of 1 to 10. It carries 10, the top of the scale, the plan totals 87, and
every score in this record is restated on 87. No path and no run changes side of the 40% line. Also corrected 09/20/2026, from the question
of whether the rows stack. Read on the balance, row 6 had come to depend on the tier rules
through TRT-0018 and TRT-0043 and failed on P2, P3 and P4 with rows 7 and 9. It now names the
five capped employees whose balance the cap alone moves, so the cap row fails on the cap and
nothing else. P2 reads 29, P3 34 and P4 47. The five runs are unchanged, all uncapped.

**The modal failing path is P3 or P4.** A run that reads the cutover memo applies the cap and the
four periods, because both are explicit; a run that reads the archive takes the service dates
off it; a run that reads the archive's salary history finds two rates that differ from BambooHR
and may or may not go looking for the signed documents. P3 sits under 40% and P4 over it.

## The honest prediction, and what thirteen T1 trajectories say about it

**Registered Gemini 3.8 Flash mean: 45%.** Not the convenient number. It assumes two runs on P3,
two on P4 and one that heals past P5, and it rests on this reading of the T1 and v2 traces:

- The tier reads the whole tree by shell and applies explicit rules once it holds them. The cap,
  the biweekly period and the exclusion of ended employees are explicit in the cutover memo, so
  P1 and P2 are unlikely to be the modal paths, and 26% is not the number to expect.
- The tier applies a definition it is handed. This memo hands it one, the population, which is
  not the determination and carries 12 points inside the determination family.
- What the tier has not been measured on is a rule it has to assemble from two documents
  against three records that agree with each other and are wrong: the rehire bridged (the
  handbook and the archive against BambooHR, the roster and the load), the anniversary inside the
  window (the memo's timing rule against BambooHR's policy date), the signed rates (two signed
  documents and the archive against BambooHR, the roster and four registers), the part-time
  schedule (a form and the handbook against the roster), and the step (an offer letter and the
  handbook against BambooHR). Each is a fact the run can get right on its own; the gate needs all
  of them.
- G4 on v2 attributed to the memo a sentence it does not carry and landed right anyway. A run
  that rationalises the recorded rate as the rate on file is the failure mode this ask measures.

**The decision rule, registered with the predictions.** Under 40% on five Gemini runs: the rubric
half is built and the package ships. 40% to 60%: the package is held with the traces for the pod
lead's call, and the rubric is never rescoped around whatever failed. Over 60%: the tier
assembles implicit rules from the tree as it assembles explicit ones, the lever is measured
insufficient in this world for this tier, and the package retires. The house rule is that the
failure has to be the ask: if the set reads over 60%, the honest record is that a rule
application over 52 people is not a determination this tier gets wrong when every rule and every
record sit in the tree.

## The step gate

The EPM's line of 09/19/2026 is 90 steps on the platform's count in at least one Gemini
trajectory. v2 reached 91 on 74 to 90 tool calls with a 52-row page. This ask adds a rule set to
read, 52 rows of four-decimal arithmetic, and 52 BambooHR writes with two rows to create, so the
prediction is over 100 on every run. If a run stays under 90 it will be because it wrote the
BambooHR rows in bulk or skipped them, and the record will say which.

## What to read in each trajectory before scoring it

1. **Which rule documents it opened, and in what order.** The cutover memo, the handbook, the 2025
   policy and the wiki page decide the method; note which it read first and which it quoted.
2. **Which balance it took as the opening balance when two disagreed.** The report's uncapped
   figure or the archive's capped, and whether the cap was applied at all.
3. **Which service date it took for the nine migrated records**, and whether it bridged
   TRT-0071 or reset him.
4. **Which rate it took for TRT-0088 and TRT-0117**, and whether it found the signed documents or
   only the archive's history.
5. **How it published, and how it wrote BambooHR.** Title, published flag, the policy tool and the
   balance tool it used, and whether it created the two missing rows.
6. **The step count** on the platform's own view.

## What the platform's own grading run has to show before the scores are trusted

Every planned row is an App DB row. Before reading a zero as a failure of the run, read the row's
`details` string: it names the table it found, its column list, the resolution route and every
row it considered. T1's harness fixture matched the platform's `get_page` route on thirteen of
thirteen runs; the BambooHR tables' shape in a grading snapshot is unmeasured.

## Measured 09/20/2026 - the five Gemini 3.8 Flash runs

Five exports landed on 09/20/2026 and are archived under `qc/findings/run_set_09-20-2026/` by
`qc/archive_run_set.py`: each page as the app returned it to the run's own get_page call, every
BambooHR write with the app's result, and `runs.json` read off the exports. `python3
qc/score_run_set.py` prints the table from those bytes and nothing else: not the final answer, not
the narration, not the route the run took. All five carry the task data id
`snap_45e68b376f2547dca61408b65d8ba774`, the world snapshot, task version 17 on G1 and G3 and 18
on G2, G4 and G5, and the builder's PROMPT verbatim.

| Run | Model | Tool calls | Assistant turns | Rows | Total it prints | Path | Score | Rows failed |
|---|---|---|---|---|---|---|---|---|
| G1 | gemini-3.8-flash | 209 | 209 | 52 | $111,455.78 | P1 | 24 of 87, 27.6% | 5, 6, 7, 8, 9, 10, 11, 12, 13, 19, 20 |
| G2 | gemini-3.8-flash | 165 | 165 | 50 | $111,100.39 | none | 16 of 87, 18.4% | 2, 5, 6, 7, 8, 9, 10, 11, 12, 13, 16, 19, 20, 21 |
| G3 | gemini-3.8-flash | 213 | 213 | 52 | $111,455.78 | P1 | 24 of 87, 27.6% | 5, 6, 7, 8, 9, 10, 11, 12, 13, 19, 20 |
| G4 | gemini-3.8-flash | 192 | 192 | 52 | $111,455.78 | P1 | 24 of 87, 27.6% | 5, 6, 7, 8, 9, 10, 11, 12, 13, 19, 20 |
| G5 | gemini-3.8-flash | 197 | 197 | 50 | $111,100.39 | none | 16 of 87, 18.4% | 2, 5, 6, 7, 8, 9, 10, 11, 12, 13, 16, 19, 20, 21 |

**G1, G3 and G4 are P1 row for row, and G2 and G5 are P1 less the two unloaded hires.** G1, G3 and
G4 print 52 rows, the population fixed exactly as the memo defines it, the two unloaded hires in and the
contractors and the ended out, and every balance, tier and rate as the HRIS report and BambooHR
carry them: uncapped, at the loaded tiers, at the loaded rates. The total is the registered P1 figure to the cent, on all three. G2 and G5 print 50 rows at
$111,100.39, the P1 figure less the two hires'
$272.02 and $83.37, and on the 50 each prints every cell equals P1. Each read the crosswalk's Never Loaded as no
liability, put no row on the page and created no BambooHR row; G2's only two BambooHR calls were
a policy re-assignment on TRT-0001 that changed nothing and a zero-hour adjustment the app
rejected, and G5 removed the policies and balances of CTR-2002, CTR-2003, CTR-2004, TRT-0037, TRT-0049, TRT-0064 from BambooHR at
step 184 in a loop the archiver could not parse, records outside the schedule that no row grades. That is the reading the prompt AutoQC round of the same day took, a missing record
read as a missing liability, and it costs rows 2, 16 and 21 on top of P1's. Against the six
questions above:

1. All five opened the cutover memo early, at calls 24, 14, 18, 11 and 23, the wiki page just
   before it, and the HRIS report and the July close package before or beside it. All five opened
   the handbook later, at calls 126, 88, 48, 79 and 40. All five cite the memo and the handbook in
   their final answers for the tiers, the biweekly period and the 2,080 divisor, and none applied
   the cap, the service dates, the signed rates, the step or the part-time schedule.
2. All five took the report's uncapped balance as the opening balance on every migrated record; the
   eleven above 40.0 hours print uncapped.
3. All five printed the loaded tiers: the five migrated records at 80, and TRT-0071 at 80 unbridged.
4. Four of the five opened the promotion approval and the comp amendment, G1 at calls 113 and
   114, G2 at 124, G3 at 123 and G5 at 83, and printed the loaded rates, $50.0000 and $66.3462:
   the failure mode registered above, the record read as the rate on file. G4 never opened either
   and printed the same rates.
5. All five published under the exact title with the published flag true, one create and no
   update. G1 and G4 wrote BambooHR through the toolbelt, G3 and G5 through the shell, calling
   the same MCP server directly; the app returned the same results either way. G1, G3 and G4
   created the missing rows (ids 59 and 60), assigned PTO Under 2 Years to both and set 6.15 and
   3.08 hours. G1 and G4 also made a test write and reverted it. G2 wrote nothing that held, and
   G5's writes touched only records outside the schedule. Nothing else was written on any run:
   the six policies and the fifty other balances stand as loaded, so rows 19 and 20 fail on all
   five and row 21 passes on G1, G3 and G4. That closes open item 3: the three tools write the
   rows the plan reads.
6. 209, 165, 213, 192 and 197 tool calls, one assistant turn per call, 139, 119, 148, 134 and 143
   shell calls, 1,854, 1,830, 2,155, 2,172 and 2,133 seconds: over the 90-step gate and over the
   100 predicted, on all five.

**The five Gemini runs decide: 23.9%, under 40%.** Three runs on P1 at 27.6% and two under it at
17.4%, against a registered mean of 45% and a modal path of P3 or P4. By the rule registered
above the rubric half is built from `build/rubric_plan.csv`, the verifier code is tested against
a fixture with these five pages in it, and the package ships. The three GPT Sol 5.6 runs are still
owed for the record and do not move the decision.

**What was actually wrong in the prediction.** The prediction said the tier applies an explicit
rule once it holds it, and named the cap and the four periods as explicit. All five held the
memo; G1, G3 and G4 applied the periods to the two new hires only, where BambooHR gave them no
number to copy, and G2 and G5 applied no period at all, printing no row where there was no
record. Where a record printed a finished number, the memo lost to the record on every rule,
explicit or not. That is a sharper statement of the failure than the one registered: the tier does
not fail to assemble a rule, it fails to apply one against a record that already carries an
answer.

**The exports carry T1's verifiers.** The twenty verifiers on all five exports target Approved Hiring
View - August 2026 and Staffed Role View - August 2026, the synth's set for T1: the platform task
`PTO Liability Request` is T1's task re-pointed to this prompt and input. A platform grading of
these runs is against those rows and says nothing; the record scores from the archived bytes.

## The rubric half, 09/20/2026

The five runs read under 40%, so the rubric half was built the same day from the plan's 21 rows.
The weights are the ones registered above, unchanged, so every score in this record stands as
written; the set task round 1 left the same day is re-scored two sections below. Each row now carries a criterion type, a primary flag, an explanation in the house
register and the picker's reference artifacts, and `05_rubric_import.xlsx` is generated from
them in the HR 79 T1 shape with both snapshot ids read off these five exports. On the 21-row build twelve rows were
primary, the twelve the registered paths short of the heal fail, and Expert Assessment carried
77.0% of the points; on the round-1 set the figures are 13 and 75.3%. Still owed: the verifier code generated from the same rows, the battery
against a fixture that holds these five pages and the BambooHR tables, the golden page and the
three GPT Sol 5.6 runs.

## Re-scored on the set task round 1 left, 09/20/2026

The first rubric round read the 21-row import and the set was rebuilt the same day: one rule per
employee on the page, the four ended records and the two hires one row each, two set rows over
the 50 loaded records and two created rows in BambooHR, and two rows at 1 for the request's last
explicit asks, a name and a department on every row and the summary above one table. No
registered weight moved, and `qc/README.md` carries the verdicts. The paths and the five runs
re-score on the 28 rows and 89 points as the builder and `qc/score_run_set.py` print them, from
the same archived bytes:

| Path | What the run does | Rows | Total it prints | Score |
|---|---|---|---|---|
| P0 | the July close method rolled forward: the HRIS report's rows and balances, the loaded tiers and rates, contractors and ended records inside, the two unloaded hires outside | 57 | $119,758.03 | 11 of 89, 12.4% |
| P1 | the HRIS report with the population fixed: 52 rows, balances uncapped, the loaded tiers and rates | 52 | $111,455.78 | 26 of 89, 29.2% |
| P2 | P1 with the 40.0-hour cap applied at 06/30/2026 | 52 | $90,983.94 | 31 of 89, 34.8% |
| P3 | P2 with tiers from the archive's service dates, the rehire unbridged, the tier change not timed, the rates as loaded | 52 | $92,804.10 | 36 of 89, 40.4% |
| P4 | P3 with the two signed pay changes applied | 52 | $92,934.50 | 49 of 89, 55.1% |
| P5 | P4 with the rehire bridged and the tier change timed; the step and the part-time schedule still missed | 52 | $92,789.47 | 67 of 89, 75.3% |
| P6 | the heal | 52 | $92,739.54 | 89 of 89, 100.0% |

| Run | Model | Tool calls | Assistant turns | Rows | Total it prints | Path | Score | Rows failed |
|---|---|---|---|---|---|---|---|---|
| G1 | gemini-3.8-flash | 209 | 209 | 52 | $111,455.78 | P1 | 26 of 89, 29.2% | 7, 8, 9, 10, 11, 12, 13, 14, 15, 25, 26 |
| G2 | gemini-3.8-flash | 165 | 165 | 50 | $111,100.39 | none | 18 of 89, 20.2% | 2, 7, 8, 9, 10, 11, 12, 13, 14, 15, 21, 22, 25, 26, 27, 28 |
| G3 | gemini-3.8-flash | 213 | 213 | 52 | $111,455.78 | P1 | 26 of 89, 29.2% | 7, 8, 9, 10, 11, 12, 13, 14, 15, 25, 26 |
| G4 | gemini-3.8-flash | 192 | 192 | 52 | $111,455.78 | P1 | 26 of 89, 29.2% | 7, 8, 9, 10, 11, 12, 13, 14, 15, 25, 26 |
| G5 | gemini-3.8-flash | 197 | 197 | 50 | $111,100.39 | none | 18 of 89, 20.2% | 2, 7, 8, 9, 10, 11, 12, 13, 14, 15, 21, 22, 25, 26, 27, 28 |

**Mean 25.6%, against 23.9% on the 21-row plan.** The two added rows are ones every run passes,
so each run gains two points on two more; the failing rows are the same rules under new numbers.
P3 reads 40.4% on this set against 39.1% before, the two free points, and the five runs sit where
they sat, three on P1 and two under it.

## The task-field paragraph, 09/20/2026

Entered in the Additional Notes box on G1 on 09/20/2026, three sentences: what the run did and
the figure it reported, its own evidence and where it set the rule aside, what it should have
done, and why the output is unacceptable with the numbers. Steps here are the platform's
numbering, which runs one ahead of the export's tool-call count used elsewhere in this record:
the platform's step 25 is the export's call 24.

**G1, traj_4f6423feac9e4f80a389b67ad71a5b0d, as entered.** Gemini copies the HRIS time off report
into PTO Liability - 08/31/2026 and reports $111,455.78 of liability on 1,760.94 hours. Its own
step 25 prints the cutover memo's "Carryover into the new system is capped at 40.0 hours as of
06/30/2026; the excess is forfeited", but it sets the memo aside and takes every balance from the
report and confirms them at step 191 because they match BambooHR. It should have capped the
eleven openings at 40.00 hours, tiered the nine migrated records on their archive dates, valued
TRT-0088 and TRT-0117 at their signed rates, and carried $92,739.54 on 1,522.17 hours into the
page and BambooHR. The output is unacceptable because it overstates the liability by $18,716.24
and credits eleven of the 52 employees with hours the policy forfeited on 06/30/2026.

**G2, traj_43e4ed4770124156985eee8883199d9a, on file.** Gemini copies the HRIS time off report
into PTO Liability - 08/31/2026, drops Simone Okonkwo and Rafael Ibarra, and reports $111,100.39
on 1,751.71 hours for 50 employees. Its own step 15 prints the memo's 40.0-hour cap, but it takes
every balance from the report anyway at step 138, and at step 161 writes that the two hires "have
zero recorded PTO accruals/balances on file" because the crosswalk reads Never Loaded. It should
have capped the eleven openings, tiered the migrated records on their archive dates, accrued the
two hires from their start dates at 6.15 and 3.08 hours, and carried $92,739.54 on 52 rows into
the page and BambooHR. The output is unacceptable because it overstates the liability by
$18,360.85 on the rows it prints, omits two current employees, and leaves BambooHR untouched.

G3, traj_e0bfaf50ef7d451fbacfa96c7639178e, and G4, traj_75b173ce1cb641fc9fcf09419ee67caf, take
G1's shape: the cap printed at steps 19 and 12, every balance from the report at steps 167 and
150. G5, traj_8805c80d23144ec2bd53b3381f89acef, takes G2's: the cap at step 24, the report at
step 144, the two hires dropped.
