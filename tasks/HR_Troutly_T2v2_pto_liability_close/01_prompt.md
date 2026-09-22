# Task Prompt (T2 v2)

**Task name:** `PTO Liability at 08/31/2026`

Built 09/22/2026. A rescope of T2 at `../HR_Troutly_T2_pto_liability_close`: the same world, the
same determination, a narrower ask and a rubric priced by what a figure moves. Review round 1,
the same day, narrowed the ask again, from a row per current employee to five department lines.

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

**Review round 1, 09/22/2026, took two more lines out.** The row per current employee with its
ID, balance and rate was 52 rows of three values, 156 requirements no 25-criterion rubric can
cover, and the 27-row rubric that sampled it was itself over the limit. The sentence "Use
08/31/2026 as the measurement date" was an explicit ask no row read, and the page title and the
subject already carry the date. Both are out of the memo and barred from returning. In the
table's place the memo asks for five department lines, each line's PTO hours and PTO liability.

What survives in the memo is the page title, the two totals, the five lines and the definition
of a current employee. Nothing else. The negative controls in `build/negative_controls.py` plant
every removed line back one at a time, the per-employee table and the date sentence among them,
and confirm the build goes red, alongside the controls that hold the fence, the deadline and the
retention line out.

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
states none of them. A department line is the same determination summed: every current employee
sits on exactly one line, so a line is right only if every balance and rate on it is right.

## Prompt goal

The request asks for **the PTO liability at 08/31/2026: one page stating the total dollars and
the total hours, and the PTO hours and the PTO liability for each of five lines, Customer
Success, Engineering, Finance and Corporate, Product, and Sales and Marketing**. The
determination is the liability, 1,522.17 hours and $92,739.54 across 52 current employees; the
July close booked $90,862.13 under the old method, and the load's own figures total 1,751.71
hours and $111,100.39.

The rubric is 13 rows and 79 points, 12 of them primary, every row App DB Programatic on the
Wiki.js pages table.

1. **The page.** Row 1, published under the exact title. 1 point of 79, 1.3%, and the only row in
   the set that is not a determination.
2. **The two totals.** Row 2, the total dollar liability $92,739.54, weight 10 and the Critical
   value gate. Row 3, the total PTO hours 1,522.17, weight 8. 18 points.
3. **The five lines.** Rows 4 to 13, 60 points, each line's PTO hours and PTO liability. Every
   line figure is one the load carries wrong, so a response that copies the report earns none of
   them, and each line is off in the load for a different mix of rules:

| Line | Hours | Liability | The load carries | What moves it |
|---|---|---|---|---|
| Customer Success | 297.79 | $12,627.20 | 322.95 hours, $14,023.72 | the cap on TRT-0021, the archive's tier for TRT-0083, the part-time schedule of TRT-0141, the unloaded TRT-0153, the signed promotion of TRT-0088 and the step of TRT-0096 |
| Engineering | 558.31 | $41,542.16 | 694.66 hours, $52,936.56 | five capped balances, the archive's tier for TRT-0051 and the signed amendment of TRT-0117 |
| Finance and Corporate | 121.53 | $8,187.68 | 165.53 hours, $11,121.71 | the cap on TRT-0009 alone |
| Product | 170.50 | $10,984.34 | 161.54 hours, $10,957.00 | the cap on TRT-0040 against the bridged TRT-0071 and the archive's tier for TRT-0079, netting to $27.34 |
| Sales and Marketing | 374.04 | $19,398.16 | 407.03 hours, $22,061.40 | the cap on TRT-0018, TRT-0029 and TRT-0043, TRT-0018's timed tier change, the archive's tier for TRT-0043 and TRT-0058, and the unloaded TRT-0155 |

**Why Sales and Marketing are one line.** Marketing alone is a figure the load already carries
right, so its two figures would have been points a copy of the load earns. Joined to Sales the
line is wrong on every registered path from P0 to P4.

Each line figure is priced by the dollars it moves off the load, $36,991.13 across the ten: 7
where it moves $2,000.00 or more (Engineering, Finance and Corporate, and Sales and Marketing,
six figures), 6 at $800.00 or more (Customer Success, two) and 3 below $80.00 (Product, two). No
row in the set weighs 2.

**Nothing grades absence.** A response that also prints every employee, or Sales and Marketing
apart beside the joined line, loses nothing by it. The battery proves it.

## Spec compliance notes

| Spec | How the ask meets it |
|---|---|
| **1A** Realistic and complex | A policy cutover two months old, an HRIS load that capped nothing and moved nine service dates, an Office Manager gone who owned the policy page and the July schedule, a Finance Manager who booked July on the loaded numbers, and a handbook that incorporates a dated memo the wiki contradicts |
| **1B** Natural prompting | One sentence in the owner's register; the request referenced by subject; the page title stated exactly; no step, order, workflow, persona, credential or format convention. The memo names the July detail it replaces and no rule |
| **1C** Unique correct answer | Every graded value is a document's printed rule applied to a document's printed record, recomputed from the world's bytes by `check_world()` on every build. The two rounding conventions the cutover memo permits are both computed and both accepted; the reviewer decision rules in `02_task_metadata.md` settle the remaining readings |
| **1D** Timeless | The request dates itself 09/01/2026 and names the page for 08/31/2026; every other date is a world date |
| **1E** Tightly scoped outputs | One page with two stated totals and five stated lines. 13 rows, all App DB Programatic on the Wiki.js pages table, every explicit ask in the memo read by a row and no row reading anything the memo does not ask for. Wiki.js is written, BambooHR is read, and nothing else is touched |
| **1F** Self-sufficient | Solvable from the request, the world files and the apps alone. The one input uploads through 1.4 on the Filesystem target, measured at 13 of 13 here |
| **1G** Purposeful | No persona. The prompt names the request, the one source and the one deliverable |
| **2A** Genuinely challenging | The registered failing paths score 1 of 79 (P0 and P1, 1.3%), 15 (P2, 19.0%), 22 (P3, 27.8%), 29 (P4, 36.7%) and 49 (P5, 62.0%); the free base is 1 of 79. T2's ten Gemini trajectories re-scored under this rubric read 1.3% each, as printed and with their own rows summed onto the lines, because none applied the cap. Those are runs against a different ask, so they are evidence about the pricing and not a v2 run set. **A v2 run set is owed.** The decision rule is registered in `06_failure_analysis.md`, dated before any run |

**Tolerances.** A stated total or line figure is graded to half a dollar and a stated hours
figure to a twentieth of an hour, because v2's memo carries no Form section and nothing tells a
response how many decimals to print. No rounding of a right answer fails a band and no registered
path reaches one.

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

**Required of the request**: the page title, the two totals, the five lines and the definition
of a current employee. The out-of-scope block the memo carried through T2's task round 2 is gone
since round 3, the deadline heading and the retention line went the same way in round 4, and the
builder bars all three. v2 adds the twelve bars in the table above, and review round 1 adds the
per-employee table and the measurement-date sentence, so the ask states the determination and
nothing beside it.
