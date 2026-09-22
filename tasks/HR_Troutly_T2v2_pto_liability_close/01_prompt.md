# Task Prompt (T2 v2)

**Task name:** `PTO Liability at 08/31/2026`

Built 09/22/2026. A rescope of T2 at `../HR_Troutly_T2_pto_liability_close`: the same world, the
same determination, a narrower ask and a rubric priced by what a cell moves.

---

## Prompt (as delivered to the agent)

> Complete the request (using the HRIS time off report and the rest of the Troutly files) about the August 2026 close by publishing the Wiki.js page PTO Liability - 08/31/2026.

`build/build_package_artifacts.py` asserts this blockquote against its `PROMPT` constant on every
build and prints the live character count and md5. The shape is T1's: one sentence, the ask
first, the one named source plus the open tail in a parenthetical, the request by subject, then
the one deliverable with the page title named exactly. Everything instructional lives in the
request memo, where Spec 1B puts it. T2's sentence named two sources and two deliverables; the
BambooHR half is out of the ask, so it is out of the sentence.

**The dash in the title is a hyphen**, and the verifiers normalise an en or em dash to a hyphen
before matching a title, as T1's did.

**The named source carries the wrong numbers, and that is the design.** The HRIS time off report
prints every balance the load carried, uncapped, at the loaded tiers, with four contractors and
three ended employees on it and the two unloaded hires off it. Unnamed by the prompt and by the
memo: the cutover memo of 06/20/2026, the handbook, the SplinterHR archive, the roster, the
crosswalk, the promotion approval, the compensation amendment, the rehire offer, the historical
offer letters, the schedule change form and the July close's method. BambooHR is no longer named
either, and its salaries are still where a rate comes from for the 50 loaded people.

## Why the ask is narrower than T2's

T2's rubric was 55 rows and 105 points. 14 of those points were the page and its form and 29 more
were BambooHR rows at weight 1 each, and a response that got the determination wrong earned every
one of them. Grader feedback on another world states the rule: a criterion whose failure
materially changes the output has to weigh more than 2, weight 2 suits extraction and weight 1
suits formatting. The owner's decision of 09/22/2026 was a full rescope and not a reweighting,
because a row cannot be repriced above 2 while the ask that draws it is a line of the memo any
reader satisfies. The free content is cut out of the ASK, and the rows go with it.

Each line below was an explicit ask in T2's memo. It is gone from v2's memo, and
`build/build_task_input.py` bars it from returning.

| Line removed from T2's memo | The T2 rubric row it drew | Weight |
|---|---|---|
| "with a short summary above one table" | row 13, the summary above one table of employee rows | 1 |
| the "name" column | row 8, a name on every employee row | 1 |
| the "department" column | row 9, a department on every employee row | 1 |
| the "annual PTO tier in hours" column | row 10, an annual PTO tier in hours on every employee row | 1 |
| the "dollar liability" column | row 6, a total dollar liability equal to the sum of the rows | 1 |
| "The summary states the number of employees on the schedule" | row 7, a summary with the employee count, the total hours and the total dollar liability | 1 |
| the whole BambooHR section | rows 27 to 55, one policy or balance row per record | 29 |
| "Dates MM/DD/YYYY" | row 12, every date in MM/DD/YYYY form | 1 |
| "Hours to two decimals" | row 3, hours to two decimals | 1 |
| "Hourly rates to four decimals" | row 4, hourly rates to four decimals | 1 |
| "Dollars to the cent" | row 5, dollars to the cent | 1 |
| "An employee ID on every row" | row 11, an employee ID on every row | 1 |

42 of T2's 105 points, 13 of them free and 29 of them records a run moves with no rule applied.
One more row went without a memo line going with it: T2's row 2, the 52 current employees as the
only employee rows, weight 2. The memo still defines a current employee, because the population is
what the totals run over. The rubric grades no exclusion, for the reason in the next section.

What survives in the memo is the page title, the measurement date, the two totals, the employee
ID, the PTO balance in hours, the hourly rate and the definition of a current employee. Nothing
else. Five negative controls in `build/negative_controls.py` plant the Form section, the BambooHR
ask, the summary count, a dropped column and the one-table shape back one at a time and confirm
the build goes red, alongside the controls that hold the fence, the deadline and the retention
line out.

## Why this ask, and the measurement behind it

T1 and T1 v2 measured, on thirteen Gemini 3.8 Flash trajectories, that a population
reconciliation is not a determination this tier gets wrong in this world: it reads the tree whole
and applies any definition it is handed. T2 measured the determination itself, ten trajectories
across 09/20/2026 and 09/21/2026, every one of them failing the gate and failing the cap.

This ask is a rule application over 52 people where every file the run opens offers a number that
looks finished and is wrong. The HRIS report's balance is uncapped. The July close's schedule,
prepared by the requester, uses the HRIS tier, the HRIS rate and the HRIS balance and carries
three ended employees. The wiki page and the 2025 policy say monthly accrual and unlimited
carryover. The roster and BambooHR carry 07/01/2026 as the service date on nine migrated records.
BambooHR and every payroll register carry the pre-promotion and pre-amendment rates for two
people. The right number exists only after eight rules are applied in sequence, and the memo
states none of them.

## Prompt goal

The request asks for **the PTO liability at 08/31/2026: one page stating the total dollars and
the total hours, with a row per current employee carrying the ID, the balance in hours and the
hourly rate**. The determination is the liability, 1,522.17 hours and $92,739.54 across 52
current employees; the July close booked $90,862.13 under the old method, and the load's own
figures total 1,751.71 hours and $111,100.39.

The rubric is 27 rows and 143 points, 26 of them primary, every row App DB Programatic on the
Wiki.js pages table.

1. **The page.** Row 1, published under the exact title. 1 point of 143, 0.7%, and the only row
   in the set that is not a determination. It is the whole of what a response earns for
   publishing a page with the wrong numbers on it.
2. **The two totals.** Row 2, the total dollar liability $92,739.54, weight 10 and the Critical
   value gate. Row 3, the total PTO hours 1,522.17, weight 8. 18 points. Row 2 grades every rule
   across the whole population at once, because the total matches only if every entry is right,
   and row 3 reads the same population on the hours axis.
3. **The 24 moved cells.** Rows 4 to 27, 124 points, 19 balances and 5 rates over 22 employees.
   A cell is graded only where the figure the world gives at 08/31/2026 is **not** the figure the
   load carries, so a response that copies the report earns none of them and a response that
   applies the rules earns them all.

The cell families, and the bytes behind them:

- **The 40.0-hour cap at 06/30/2026**, from the cutover memo. Eleven employees are capped and ten
  of them move a graded balance: TRT-0005, TRT-0009, TRT-0012, TRT-0014, TRT-0021, TRT-0023,
  TRT-0029, TRT-0031, TRT-0040 and TRT-0043. The HRIS report prints the uncapped figure.
- **The migrated service dates.** Nine records read 07/01/2026 in BambooHR and on the roster and
  six accrue at the wrong tier there; four move a graded balance, TRT-0051, TRT-0058, TRT-0079
  and TRT-0083, against the archive's real hire dates.
- **The rehire bridge.** TRT-0071's rehire bridges a 241-day break to 03/08/2021 under the
  handbook's 7.6 and the 160-hour tier, 51.87 hours against the report's 39.56.
- **The timed tier change.** TRT-0018 crosses five years on 08/09/2026, inside the fourth posted
  period, so three periods accrue at 4.6154 and one at 6.1538.
- **The two unloaded hires.** TRT-0153 started 07/22/2026 and TRT-0155 on 08/03/2026, both marked
  Never Loaded on the crosswalk. Four cells, a balance and a rate each, from the roster and the
  offer letters.
- **The part-time schedule change.** TRT-0141 was scheduled 25 hours until 08/09/2026 and 32 from
  08/10/2026, pro-rata under 30 by the handbook's 2.2. The report accrues her at a full week.
- **The signed pay changes and the step.** TRT-0088's promotion at $118,000.00 from 06/16/2026 and
  TRT-0117's amendment at $148,200.00 from 05/16/2026 were dropped by the load; TRT-0096's offer
  letter carries the $3,000.00 anniversary step effective 08/17/2026. Three rates.

Each of the 24 rows is priced by the dollars that cell moves in the total: 7 where it moves
$2,000.00 or more (4 rows), 6 at $800.00 or more (6 rows), 5 at $250.00 or more (7 rows), 4 at
$80.00 or more (4 rows) and 3 below that (3 rows). Gross movement across the 24 cells is
$23,184.21. No row in the set weighs 2.

**Nothing grades absence.** A response that prints all 52 employees rather than the 22 the load
has wrong loses nothing by it, and a response that prints only those 22 scores every point. An
exclusion criterion would invalidate the golden, because the golden over-delivers on purpose: the
correct page carries all 52 rows. Two battery scenarios prove it in both directions.

## Spec compliance notes

| Spec | How the ask meets it |
|---|---|
| **1A** Realistic and complex | A policy cutover two months old, an HRIS load that capped nothing and moved nine service dates, an Office Manager gone who owned the policy page and the July schedule, a Finance Manager who booked July on the loaded numbers, and a handbook that incorporates a dated memo the wiki contradicts |
| **1B** Natural prompting | One sentence in the owner's register; the request referenced by subject; the page title stated exactly; no step, order, workflow, persona, credential or format convention. The memo names the July detail it replaces and no rule |
| **1C** Unique correct answer | Every graded value is a document's printed rule applied to a document's printed record, recomputed from the world's bytes by `check_world()` on every build. The two rounding conventions the cutover memo permits are both computed and both accepted; the reviewer decision rules in `02_task_metadata.md` settle the remaining readings |
| **1D** Timeless | The request dates itself 09/01/2026 and sets 08/31/2026 as the measurement date; every other date is a world date |
| **1E** Tightly scoped outputs | One page with two stated totals and one table of ID, hours and rate. 27 rows, all App DB Programatic on the Wiki.js pages table. No app but Wiki.js is written and none is graded |
| **1F** Self-sufficient | Solvable from the request, the world files and the three apps alone. The one input uploads through 1.4 on the Filesystem target, measured at 13 of 13 here |
| **1G** Purposeful | No persona. The prompt names the request, the one source and the one deliverable |
| **2A** Genuinely challenging | The registered failing paths score 1 of 143 (P0, 0.7%), 19 (P1, 13.3%), 76 (P2, 53.1%), 100 (P3, 69.9%), 107 (P4, 74.8%) and 119 (P5, 83.2%); the free base is 1 of 143, 0.7%. T2's ten Gemini trajectories re-scored under this rubric read 8.3% and 14.7% by set, against 23.9% and 38.1% under T2's own. Those are re-scorings of runs against a different ask, so they are evidence about the pricing and not a v2 run set. **A v2 run set is owed.** The decision rule is registered in `06_failure_analysis.md`, dated before any run |

**Tolerances.** A cell is graded to half a hundredth of an hour and half a cent of an hourly rate.
A stated total is graded to half a dollar and a stated hours figure to a twentieth of an hour,
because v2's memo carries no Form section and nothing tells a response how many decimals to
print. No rounding of a right answer fails a band and no registered path reaches one, the nearest
being P5 at $49.93 and 9.66 hours away.

## Withheld from the prompt and from the task input

Machine-asserted by `build/build_task_input.py`: every policy document, page and record by name
other than the July detail; the cap and every carryover word; the accrual period and every
per-period, monthly or annual accrual word; every tier value and boundary; every service-date,
anniversary, rehire and bridging word; every part-time, pro-rata and scheduled-hours word; every
signed change, promotion, amendment and step; every word for a record being stale, wrong, loaded,
migrated, ended or missing; the word contractor; the eight names the determination turns on;
every total, balance and rate; every word for checking, confirming, correcting, resolving or
governing; and the shape of the answer, with "whether", "only", "except", "instead", "differ",
"conflict", "override" and their neighbours word-boundary-banned.

**Required of the request**: the page title, the measurement date, the two totals, the three
columns and the definition of a current employee. The out-of-scope block the memo carried through
T2's task round 2 is gone since round 3, the deadline heading and the retention line went the
same way in round 4, and the builder bars all three. v2 adds the twelve bars in the table above,
so the ask states the determination and nothing beside it.
