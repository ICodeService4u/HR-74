# Failure analysis - predictions registered before any run (09/20/2026)

**No trajectory has run on T2.** Everything below is a prediction with a date on it. When the run
set lands, archive each run's page and its BambooHR rows under `qc/findings/run_set_MM-DD-YYYY/`
with a `runs.json`, score it against the registered paths, and write the measured record under
these predictions rather than over them, the way T1's and v2's records do.

## The plan the predictions are scored against

21 planned rows, 92 points, one gate. The determination carries 75 points,
81.5%; BambooHR brought to the schedule 12, 13.0%; the page and its
form 5, 5.4%. The rows are in `02_task_metadata.md` and `build/rubric_plan.csv`.

## The registered paths

Every path is the golden schedule with rules dropped, recomputed by `build/build_package_artifacts.py`
and scored by the plan's own predicates, so the arithmetic here recomputes on every build.

| Path | What the run does | Rows | Total it prints | Score |
|---|---|---|---|---|
| P0 | the July close method rolled forward: the HRIS report's rows and balances, the loaded tiers and rates, contractors and ended records inside, the two unloaded hires outside | 57 | $119,758.03 | 8 of 92, 8.7% |
| P1 | the HRIS report with the population fixed: 52 rows, balances uncapped, the loaded tiers and rates | 52 | $111,455.78 | 24 of 92, 26.1% |
| P2 | P1 with the 40.0-hour cap applied at 06/30/2026 | 52 | $90,983.94 | 29 of 92, 31.5% |
| P3 | P2 with tiers from the archive's service dates, the rehire unbridged, the tier change not timed, the rates as loaded | 52 | $92,804.10 | 34 of 92, 37.0% |
| P4 | P3 with the two signed pay changes applied | 52 | $92,934.50 | 47 of 92, 51.1% |
| P5 | P4 with the rehire bridged and the tier change timed; the step and the part-time schedule still missed | 52 | $92,789.47 | 65 of 92, 70.7% |
| P6 | the heal | 52 | $92,739.54 | 92 of 92, 100.0% |

**The modal failing path is P3 or P4.** A run that reads the cutover memo applies the cap and the
four periods, because both are explicit; a run that reads the archive takes the service dates
off it; a run that reads the archive's salary history finds two rates that differ from BambooHR
and may or may not go looking for the signed documents. P3 sits under 40% and P4 over it.

## The honest prediction, and what thirteen T1 trajectories say about it

**Registered Gemini 3.8 Flash mean: 45%.** Not the convenient number. It assumes two runs on P3,
two on P4 and one that heals past P5, and it rests on this reading of the T1 and v2 traces:

- The tier reads the whole tree by shell and applies explicit rules once it holds them. The cap,
  the biweekly period and the exclusion of ended employees are explicit in the cutover memo, so
  P1 and P2 are unlikely to be the modal paths, and 26% and 32% are not the numbers to expect.
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
