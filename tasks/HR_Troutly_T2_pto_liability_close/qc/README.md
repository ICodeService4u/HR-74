# The task AutoQC register - T2, PTO Liability Schedule and BambooHR PTO Records

**One prompt round and two runs have landed on T2, 09/20/2026.** Prompt AutoQC now runs in the
Trajectories section, so the first round landed beside the first runs. Archive each
round verbatim to `findings/prompt_roundN_MM-DD-YYYY.md` or `findings/task_roundN_MM-DD-YYYY.md`
before triaging it, and keep the verdicts here.

| Round | Date | Findings | Verdict |
|---|---|---|---|
| Prompt round 1 | 09/20/2026 | Two major, seen so far in a screenshot of the Major tab; the verbatim text with the Passed and Neutral tabs is owed to `findings/prompt_round1_09-20-2026.md`. P0 Completeness and Relevance, Self-Contained Tasks: the roster lists TRT-0153 and TRT-0155 as Active, the crosswalk marks both Never Loaded, neither is on the HRIS report or in BambooHR, so their 08/31/2026 balance cannot be determined; add an authoritative balance and BambooHR records, or a stated derivation | **Disputed, and the run set decides.** Both balances are determined by the world: the roster and the signed offers carry each start date and salary, the cutover memo the accrual, tier and valuation rules, the payroll procedures memo the posted pay dates, the onboarding standards the adjusted service date, and BambooHR's own row for TRT-0150 a period containing the start credited in full. Never Loaded is the ask: creating the two rows is the BambooHR half of the request, and the catalogue carries `employees_create`, `time_off_assign_policy` and `time_off_update_balance`. A balance or a derivation in the memo hands the tier the determination. G1 and G3 both derived the two, 6.15 and 3.08 hours, and created both rows |
| Run set, G1 and G3 | 09/20/2026 | Two of five Gemini 3.8 Flash: both P1 row for row, $111,455.78, 24 of 92, 26.1% | Scored from the output alone by `score_run_set.py`; `../06_failure_analysis.md` carries the record. Three Gemini and three GPT Sol 5.6 owed |

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

Not built at the prompt half. When the rubric half is built, every planned row's code is tested
against a fixture with the answer known before it is imported, as T1's and v2's were, with the
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
  and BambooHR rows and no file.
- **That the two unloaded hires have no balance to reconcile.** Raised 09/20/2026 and answered above:
  the world determines both, and creating their rows is the ask.
- **That 22 world files exceed the general ceiling of ten.** Each decides a planned row or carries
  a number a failing path prints; `02_task_metadata.md` says which.
