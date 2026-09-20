# The task AutoQC register - T2, PTO Liability Schedule and BambooHR PTO Records

**One prompt round, the five Gemini runs and the first rubric round have landed on T2, 09/20/2026.** Prompt AutoQC now runs in the
Trajectories section, so the first round landed beside the first runs; the rubric round ran on the
21-row import the same day. Archive each
round verbatim to `findings/prompt_roundN_MM-DD-YYYY.md` or `findings/task_roundN_MM-DD-YYYY.md`
before triaging it, and keep the verdicts here.

| Round | Date | Findings | Verdict |
|---|---|---|---|
| Prompt round 1, finding 1 | 09/20/2026 | P0 Completeness and Relevance, Self-Contained Tasks, two major: the roster lists TRT-0153 and TRT-0155 as Active, the crosswalk marks both Never Loaded, neither is on the HRIS report or in BambooHR, so their 08/31/2026 balance cannot be determined; add an authoritative balance and BambooHR records, or a stated derivation. Transcribed from the Major tab to `findings/prompt_round1_09-20-2026.md`; the Passed and Neutral tabs not captured | **Disputed on the platform 09/20/2026: "Providing these is what the task asks for."** Both balances are determined by the world: the roster and the signed offers carry each start date and salary, the cutover memo the accrual, tier and valuation rules, the payroll procedures memo the posted pay dates, the onboarding standards the adjusted service date, and BambooHR's own row for TRT-0150 a period containing the start credited in full. Never Loaded is the ask: creating the two rows is the BambooHR half of the request, and the catalogue carries `employees_create`, `time_off_assign_policy` and `time_off_update_balance`. A balance or a derivation in the memo hands the tier the determination. G1 and G3 both derived the two, 6.15 and 3.08 hours, and created both rows; G2 took the round's reading, a missing record as a missing liability, and left both off the page, which is the failure the row grades |
| Prompt round 1, finding 2 | 09/20/2026 | Outcome-Determining Choices Pinned in the Prompt, consolidated: the assigned verifiers require the two T1 pages while the prompt asks for the PTO page, so a solver could defensibly produce either; and the memo should name the authoritative population and the reconciliation treatment for records present in one source | **Disputed on the platform 09/20/2026: "The ask has been altered slightly from the original synth task in order to meet the difficulty bar, and the assigned verifiers are not accessible until the next task stage."** The verifier set is T1's twenty, open item 6 in `../02_task_metadata.md`; no platform grading against it is read, and the plan's rows replace it at the next stage. The population ask is v2's round again: the memo defines a current employee, and a source hierarchy handed to the tier is a rule it applies. All three runs produced the memo's 52 from the roster, and G2 then dropped two on the crosswalk's Never Loaded, which is the failure row 2 grades |
| Task round 1, Verifiers Grade Only What the Prompt Asks For | 09/20/2026 | P1: criteria 8, 9, 16, 17 and 18 carry service-date bridging, accrual breakdowns, posting-period counts and leave-deduction clauses the memo does not ask for; retain the table values | **Accepted.** Each clause was the rule behind the value and the code reads the cell alone, so the clause belongs in the explanation, where the register puts the governing fact. The five criteria now state the cell's value and nothing else, and one was wrong in kind: old row 9 stated an accrual of 20.0000 hours on a page that carries no accrual column, and it now states Thornbury's balance of 60.00 hours, the cell the reviewer rule reads |
| Task round 1, Prompt-Rubric Alignment | 09/20/2026 | P0: no row requires the ID, name, department or tier column on every row or the summary-above-one-table layout, and no row checks "Change nothing in Greenhouse" | **Accepted in part, disputed in part.** Accepted: the ID keys every row and the tier, balance, rate and liability cells are what rows 7 to 24 read, and name, department and the layout were the two explicit asks with no row. Row 5 reads a name and a department on every row and row 6 reads the summary above one table, 1 point each, the layout row tagged Style / formatting as HR 79 T1's form rows are. Disputed: the Greenhouse fence. Paste-ready: *A clause that fences work out of scope asks for nothing. None of the five Gemini runs touched Greenhouse, so a row on it is a point every run earns and Spec 2A counts it against the tier's mean. HR 79 T1 retired the same kind of row in its task round 7 and the rubric passed round 7 without it.* |
| Task round 1, No Stacked Criteria | 09/20/2026 | P0, four findings: rows 6 and 7 bundle five employees each, 15 and 16 bundle four and two, 19 bundles six policies, 20 and 21 overlap | **Accepted, with no registered weight moved.** Each rule now has one row on one employee: the cap on Hosana at 5, the loaded date on Kastellanos at 5, the four ended records one row each at 1, the two hires one row each at 2 on the page and 1 in BambooHR. The two BambooHR set rows read the 50 loaded records and exclude TRT-0153 and TRT-0155 in terms, so nothing overlaps the two created rows. 21 rows became 28 and 87 points became 89, the 2 being the two alignment rows above. The house's own design note in `02_task_metadata.md` is rewritten to the new shape and dated |
| Task round 1, Rubric Completeness | 09/20/2026 | P0: all 21 entries carry `verifier_custom_field_values = {}`, so Reference Artifacts and Grading Target are empty | **Measured, half disputed.** Paste-ready: *Every row is App DB Programatic and grades app state, not a file, so Grading Target is empty by the guide's own rule and by HR 79 T1's registered position, whose round 7 passed with it empty on every App DB row. Reference Artifacts are in the import file, 92 citations as the picker's resolved objects with both snapshot ids; the importer did not populate the field, so they are entered in the Structured view from the package's build/rubric_plan.csv.* This is the first measurement of what the import populates and open item 7 in `../02_task_metadata.md` records it |
| Task round 1, Criteria Count Justified by Scope | 09/20/2026 | P1 minor: C21 is covered by C20 | **Accepted by the same change.** Rows 25 and 26 read the 50 loaded records other than TRT-0153 and TRT-0155, and rows 27 and 28 read the two created rows' balances, so no row covers another |
| Task round 1, Verifier Tag Coverage | 09/20/2026 | Minor: all 21 criteria untagged, read as judge-style rows | **Measured, and a platform step.** Paste-ready: *The import carries Final Response on 26 rows and Style / formatting on the two form rows; the importer did not populate the Tags field, which HR 79 T24 measured on 09/11/2026 too, so the tags are set in the interface from build/rubric_plan.csv. The rows read as judge-style because they carry no code yet; every row is App DB Programatic and the code is the next step, tested against a fixture before it is pasted.* |
| Run set, G1 to G5 | 09/20/2026 | Five of five Gemini 3.8 Flash: G1, G3 and G4 P1 row for row, $111,455.78, 24 of 87, 27.6%; G2 and G5 P1 less the two unloaded hires, $111,100.39, 16 of 87, 18.4%; mean 23.9% | Scored from the output alone by `score_run_set.py`; `../06_failure_analysis.md` carries the record. G5's BambooHR writes at step 184 ran in a loop the archiver could not parse and are flagged; its own printed results show they touched only CTR-2002, CTR-2003, CTR-2004, TRT-0037, TRT-0049, TRT-0064, outside the schedule, so no graded row moves. Under 40%: the rubric half is built next. Three GPT Sol 5.6 owed for the record. Re-scored on the 28-row set of task round 1 at 25.6%, three at 29.2% and two at 20.2%, the same rules failing under new numbers |

## What is graded: the output, and only the output

`archive_run_set.py` reads each export for what the apps hold at the end of the run: the page as
the app returned it to the run's own get_page, or as the create or update call carried it, and
every BambooHR write with the result the app returned, through the toolbelt or through the
shell, since G3 called the MCP servers directly. `score_run_set.py` reads the archived page and
the BambooHR state rebuilt from the seed tables and those results, by the reviewer decision
rules in `../02_task_metadata.md`, and nothing else: not the final answer, not the narration,
not which tool was used, not the step count. A run whose page or writes the export does not
show is flagged, and the platform's grading snapshot decides those rows. Both scripts carry a
`--self-check`: the scorer reads the seven registered paths as the plan's predicates do and
goes red on a planted defect; the archiver reads both routes and flags what it cannot see.

The twenty verifiers the exports carry are T1's synth set, targeting two pages this task never
writes. A platform grading of a T2 run is against those rows and is not read.

## The verifier harness

Owed. The rubric import was built 09/20/2026 from the plan's rows, `05_rubric_import.xlsx`, with
the explanations in the house register and both snapshot ids read off the five exports. Every
row's code is generated next from the same rows and tested against a fixture with the answer
known before it is imported, as T1's and v2's were, with the five archived pages and the
BambooHR tables in the fixture beside the pages table.

## What a round is likely to raise, and the answer already on file

- **Outcome-determining choices pinned in the prompt.** v2's round asked for a source hierarchy on
  the population; this memo defines the population and names no rule, and the rules are dated
  policy the world states. A round that asks the memo to say which balance, which tier basis or
  which rate governs is asking for the determination, and the answer is the record of 09/20/2026:
  a rule handed to the tier is a rule it applies.
- **That the memo names the July detail.** It is the requester's own premise, prepared by the
  requester, and it carries the wrong method. The memo names it as the thing replaced, not as
  the rule.
- **Rubric Realism and Verifier Type, that no row grades a file.** The deliverable is a wiki page
  and BambooHR rows and no file. Task round 1 read the rows as judge-style because they carried no
  code; the code is the next step.
- **That the Greenhouse fence needs a row.** Raised by task round 1 and disputed above: a fence
  asks for nothing, no run of five touched Greenhouse, and HR 79 T1 retired the same kind of row.
- **That a set row stacks.** Rows 2, 25 and 26 each state one claim over one set, the 52 IDs and
  the 50 loaded records, and task round 1 accepted row 2 in that form while asking the
  per-employee bundles to split, which they did.
- **That the two unloaded hires have no balance to reconcile.** Raised 09/20/2026 and answered above:
  the world determines both, and creating their rows is the ask.
- **That 22 world files exceed the general ceiling of ten.** Each decides a planned row or carries
  a number a failing path prints; `02_task_metadata.md` says which.
