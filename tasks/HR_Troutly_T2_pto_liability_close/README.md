# T2 - PTO Liability Schedule and BambooHR PTO Records

**Status: built 09/20/2026 at the prompt half; the five Gemini runs landed the same day at a 23.9% mean,
three on the registered P1 path and two under it, the registered rule fired, the rubric import
shipped the same day in the HR 79 T1 shape, and the first rubric round read it the same day: the
set is rebuilt to 28 rows and 89 points with no registered weight moved, and the runs re-score
at 25.6%. The verifier code, the battery and the golden page shipped the same day, 1764 of 1764
verdicts correct on 63 snapshots; the paste and the three GPT Sol runs are owed.** The second HR 74 ask, built on the
measured record of T1 and T1 v2: thirteen Gemini trajectories healed a population reconciliation
with and without pointers, so the next ask had to be a determination the tier gets wrong, not a
lookup. This one is the PTO liability at 08/31/2026, a rule application over 52 people where
every record the run opens prints a finished wrong number. By the decision of 09/20/2026 the
prompt half ships first, the five Gemini trajectories decide, and the rubric half is built only
if they fail.

| Event | Date | Result |
|---|---|---|
| Built | 09/20/2026 | the memo, the prompt, 31 selections, 22 world files, the golden schedule recomputed from the world, a 21-row plan at 87 points, seven registered paths, predictions dated |
| Negative controls | 09/20/2026 | see the table below, from `build/negative_controls.py` |
| Run set | 09/20/2026, five of eight | Gemini 3.8 Flash: G1, G3 and G4 P1 row for row, $111,455.78, 24 of 87, 27.6%; G2 and G5 P1 less the two unloaded hires, $111,100.39, 16 of 87, 18.4%; mean 23.9%, scored from the output alone; three GPT Sol 5.6 owed for the record |
| Prompt round 1 | 09/20/2026 | Two major findings: Self-Contained Tasks on TRT-0153 and TRT-0155, and Outcome-Determining Choices on the T1 verifier set and the population. Both disputed on the platform the same day; transcribed to `qc/findings/prompt_round1_09-20-2026.md`, answered in `qc/README.md` |
| Rubric import | 09/20/2026 | `05_rubric_import.xlsx` in the HR 79 T1 shape: one sheet named Rubric, thirteen columns, 21 rows, 87 points, 12 primary, every row App DB Programatic, the explanations in the house register, both snapshot ids read off the exports. Loaded on the task the same day. `09_rubric_import.md` carries the mappings |
| Task round 1 | 09/20/2026 | Four major, two minor, on the 21-row import; `qc/findings/task_round1_09-20-2026.md`. Accepted: the calculation-path clauses out of five criteria, one row per employee where five rows bundled people, two rows for the request's last explicit asks; the set is 28 rows, 89 points, 13 primary, no registered weight moved, md5 in `02_task_metadata.md`. Disputed: a row on the Greenhouse fence, and Grading Target on App DB rows. Measured: the import does not populate Tags, Reference Artifacts or Grading Target, so both are set by hand from `build/rubric_plan.csv`. The runs re-score at 25.6% |
| Verifier code and battery | 09/20/2026 | 28 row files generated from the rows onto `build/verifier_engine.py`; `qc/verifier_harness.py` reads **1764 of 1764 verdicts correct** across 63 snapshots, the golden and BambooHR brought to the schedule the correct state, the archived G1 and G2 and the paths P2 to P5 among the planted defects. Two engine defects found and fixed by the battery before the paste |
| Golden page | 09/20/2026 | `04_golden_output_PTO_Liability.md`, generated from the schedule, the battery's correct state |

## The ask, in one paragraph

The Finance Manager asks the People Operations Analyst for the PTO liability at 08/31/2026 for
the August close: one wiki page with a row per current employee, the tier, the balance, the
hourly rate and the dollar liability, a summary with the count and the totals, and BambooHR
brought to the schedule. The memo names the July detail it replaces and no rule. The cutover
memo of 06/20/2026 caps carryover at 40.0 hours, accrues biweekly at the tier over 26 by adjusted
service date, and values at the rate on file over 2,080; the HRIS report is uncapped at the
loaded tiers, nine service dates were loaded as 07/01/2026, a rehire bridges, an anniversary
falls inside the window, two signed pay changes were dropped by the load, a step fell due, and a
part-time schedule changed. 1,522.17 hours and $92,739.54; the July close booked $90,862.13.

## Measured so far

G1, G3 and G4 print the HRIS report's numbers over the memo's population: P1 row for row, 24 of 87.
G2 and G5 print the same numbers less the two unloaded hires, which they read as carrying no
liability because they carried no record: 16 of 87. All five opened the cutover memo, four opened
both signed pay documents, and none applied a rule where a record already carried a number. Five
of five under 40%: the registered rule fired, the rubric import is built, task round 1 has reshaped it to 28 rows, and the verifier code and battery are next. The scorer reads the page as the app returned it and the
BambooHR state from the app's own results, and nothing the run said. The exports carry T1's twenty
synth verifiers, so no platform score on these runs means anything; `06_failure_analysis.md`
carries the record and `qc/README.md` the register.

## What ships

| File | Purpose |
|---|---|
| `00_task_input_pto_liability_request.pdf` | The 1.4 input, Filesystem target, uploads as `pto_liability_request.pdf` |
| `03_show_your_work.xlsx` | The show-your-work, generated by the builder: the sources, the 21 planned rows, the assembly and the golden schedule, names in the world's spelling and everything else ASCII |
| `01_prompt.md` | The prompt verbatim, the shape reasoning, why this ask, the cell families, the Spec table, the withheld list |
| `02_task_metadata.md` | Identity, the weights and the registered paths, graded values, the selection block, fences, rival readings, reviewer decision rules, the asks table, the rubric with its explanations, the checkpoints, the time estimate, the predictions, the platform state, the open items |
| `04_golden_output_PTO_Liability.md` | The golden page, generated from the schedule in the request's shape |
| `05_rubric_import.xlsx` / `09_rubric_import.md` | The file that registers, and its mappings, with the verifier record |
| `06_failure_analysis.md` | The predictions, dated, with the honest note and the decision rule |
| `08_section_1_3_step_plan.md` | The checkpoint table, held until the bar is measured |
| `build/build_task_input.py`, `build/task_input_source.md` | The memo source and its renderer with the leak guards |
| `build/build_package_artifacts.py` | The one builder: the schedule from the world's bytes, the paths, the plan, the import, the golden page, the row files, the guards |
| `build/verifier_engine.py` | The engine every row file stamps its spec into |
| `build/schedule_preview.csv`, `build/rubric_plan.csv` | The golden schedule, and the plan with the import's columns beside its own, the tag and the reference artifacts per row for the hand entry the interface needs, regenerated on every build |
| `build/negative_controls.py` | Every guard made to fail once |
| `qc/README.md`, `qc/findings/` | The AutoQC register and the verbatim archive |
| `qc/ctx.py`, `qc/run_battery.py` | The verifier skill's stand-in `ctx` and battery runner |
| `qc/scenarios.py`, `qc/verifier_harness.py` | The 63-snapshot battery and the runner over all rows |
| `qc/verifiers/` | The 28 generated row files |
| `qc/archive_run_set.py`, `qc/score_run_set.py` | The archiver and the scorer, each with a `--self-check`: the page and the BambooHR writes read off either route as the app returned them, scored by the reviewer decision rules against the registered paths |
| `qc/findings/run_set_09-20-2026/` | The five Gemini runs' pages, their BambooHR writes and `runs.json`, read off the exports |

Everything ships from 09/20/2026: the show-your-work, the rubric import, the golden page, the
verifier engine and its 28 row files, and the battery; the archiver and the scorer are in `qc/`.

## Running the checks

From the package root:

```
python3 build/build_task_input.py
python3 build/build_package_artifacts.py --docs
python3 build/build_package_artifacts.py --table     # the path table and the rubric table 02 carries
python3 qc/verifier_harness.py             # every verifier against every scenario
python3 build/negative_controls.py
python3 ../check_selection_blocks.py
python3 qc/archive_run_set.py --self-check
python3 qc/score_run_set.py --self-check
python3 qc/archive_run_set.py --set run_set_09-20-2026 G1=/path/G1.json G2=/path/G2.json G3=/path/G3.json G4=/path/G4.json G5=/path/G5.json
python3 qc/score_run_set.py --details
```

## Negative controls

| Control | Result |
|---|---|
| memo: the cap leaked | RED |
| memo: the accrual period leaked | RED |
| memo: a tier value leaked | RED |
| memo: a policy document named | RED |
| memo: the service-date basis leaked | RED |
| memo: the rehire rule leaked | RED |
| memo: the part-time rule leaked | RED |
| memo: a signed change leaked | RED |
| memo: one of the eight names | RED |
| memo: the total leaked | RED |
| memo: a record called wrong | RED |
| memo: a word for checking | RED |
| memo: the shape of the answer | RED |
| memo: the definition of a current employee dropped | RED |
| memo: the seat | RED |
| memo: an unlicensed date | RED |
| names: the upload name the record publishes | RED |
| world: the cap | RED |
| world: the posted periods | RED |
| world: the rehire bridging rule | RED |
| world: the step | RED |
| world: the tier boundaries | RED |
| world: a signed rate dropped | RED |
| world: the part-time schedule | RED |
| world: a phrase the cutover memo must carry | RED |
| world: the population | RED |
| plan: weight band | RED |
| plan: the gate demoted off the total | RED |
| plan: a row not opening on States | RED |
| plan: the free base over a tenth | RED |
| plan: the golden not scoring every point | RED |
| plan: a hours row read off a column the page does not carry | RED |
| plan: P0 scoring over a fifth | RED |
| rubric: weight band | RED |
| rubric: a compliance row flagged primary | RED |
| rubric: a stacked criterion | RED |
| register: punctuation | RED |
| register: a spaced dash | RED |
| register: a spelled month | RED |
| register: an ISO date | RED |
| register: grading vocabulary | RED |
| register: self-reference | RED |
| register: no source named | RED |
| register: over 240 characters | RED |
| register: two rows carrying one explanation verbatim | RED |
| import: the layout row losing its Style / formatting tag | RED |
| world: the loaded population | RED |
| plan: a set row reading the two created rows too | RED |
| plan: a created-row row passing with the row absent | RED |
| register: two explanations opening alike | RED |
| import: the guide's spelling of the App DB type | RED |
| import: a criterion type outside the code-verifier dropdown | RED |
| import: the form row losing its Style / formatting tag | RED |
| import: a grading target on an App DB row | RED |
| import: a reference artifact as a bare path | RED |
| import: a world reference dropped | RED |
| import: the 1.4 upload dropped from every row | RED |
| import: a citation outside the selection block | RED |
| import: a snapshot id not read off an export | RED |
| import: the sheet not named Rubric | RED |
| import: a column out of the HR 79 T1 order | RED |
| verifier: the key matched as a substring | RED |
| verifier: the employee table taken by count alone | RED |
| verifier: a band around a stated balance | RED |
| verifier: the gate falling back to the rows' sum past a stated total 1763 of 1764 verdicts correct across 63 scenarios and 28 rows | RED |
| verifier: the layout row passing two tables | RED |
| verifier: the absence floor removed | RED |
| verifier: a table's own id column read as the employee reference 1547 of 1764 verdicts correct across 63 scenarios and 28 rows | RED |
| verifier: the policy table taken as the first carrying the names 1762 of 1764 verdicts correct across 63 scenarios and 28 rows | RED |
| verifier: a duplicate balance row read as the first | RED |
| verifier: a run's narration read instead of the database | RED |
| battery: an expectation planted wrong | RED |
| battery: the fixture's ids not the ids G1 observed | RED |
| spec: a value row keyed on another employee | RED |
| spec: a set row reading the created rows | RED |
| golden: a total the schedule did not give | RED |
| syw: a total the build did not write | RED |
| syw: a semicolon joining two clauses | RED |
| docs: the prompt blockquote | RED |
| docs: a stale figure in the record | RED |
| docs: a stale path score in the predictions | RED |
| docs: a planned row missing from the record | RED |
| docs: a selection dropped from the block | RED |
| docs: a file missing from the README | RED |
| docs: a non-ASCII character in a package document | RED |
| docs: a stale explanation in the record's rubric table | RED |
| docs: a stale import md5 in the record | RED |
| docs: a stale import md5 in the mappings document | RED |
| docs: a stale citation count in the mappings document | RED |
| selection: a wildcard in the block | RED |

**90 of 90 controls went red**, 09/20/2026, the verifier controls among them: a defect planted in the engine, the battery, a spec or the golden fails the harness or the builder, and the closing rebuild left the tree clean at the published md5s and the battery at 1764 of 1764. Three of the verifier controls came back green on their first run, each a battery that could not see the planted defect, and the battery was sharpened rather than the control dropped.
