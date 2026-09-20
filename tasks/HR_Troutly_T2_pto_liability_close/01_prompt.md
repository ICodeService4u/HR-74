# Task Prompt (T2)

**Task name:** `PTO Liability Schedule and BambooHR PTO Records`

---

## Prompt (as delivered to the agent)

> Complete the request (using the HRIS time off report, the BambooHR records, and the rest of the Troutly files) about the August 2026 close by publishing the Wiki.js page PTO Liability - 08/31/2026 and updating the BambooHR PTO records to match it.

`build/build_package_artifacts.py` asserts this blockquote against its `PROMPT` constant on every
build and prints the live character count and md5. The shape is T1's: one sentence, the ask
first, the two named sources plus the open tail in a parenthetical, the request by subject, then
the two deliverables with the page title named exactly. Everything instructional lives in the
request memo, where Spec 1B puts it.

**The dash in the title is a hyphen**, and the verifiers, when built, normalise an en or em dash
to a hyphen before matching a title, as T1's did.

**The two named sources carry the wrong numbers, and that is the design.** The HRIS time off
report prints every balance the load carried, uncapped, at the loaded tiers, with four
contractors and three ended employees on it and the two unloaded hires off it. The BambooHR
records carry the loaded rates, two of them superseded by signed changes before cutover. Unnamed
by the prompt and by the memo: the cutover memo of 06/20/2026, the handbook, the SplinterHR
archive, the promotion approval, the compensation amendment, the rehire offer, the historical
offer letters, the schedule change form, the field mapping workbook and the July close's method.

## Why this ask, and the measurement behind it

T1 and T1 v2 measured, on thirteen Gemini 3.8 Flash trajectories, that a population
reconciliation is not a determination this tier gets wrong in this world: it reads the tree
whole and applies any definition it is handed. The record of 09/20/2026 says the next ask has to
be one where the failure is the determination itself.

This ask is a rule application over 52 people where every file the run opens offers a number
that looks finished and is wrong. The HRIS report's balance is uncapped. The July close's
schedule, prepared by the requester, uses the HRIS tier, the HRIS rate and the HRIS balance and
carries three ended employees. The wiki page and the 2025 policy say monthly accrual and
unlimited carryover. The roster and BambooHR carry 07/01/2026 as the service date on nine
migrated records. BambooHR and every payroll register carry the pre-promotion and
pre-amendment rates for two people. The right number exists only after eight rules are applied
in sequence, and the memo states none of them.

## Prompt goal

The request asks for **the PTO liability at 08/31/2026: one page with a row per current employee
and a summary, and BambooHR brought to it**. The determination is the liability, 1,522.17 hours
and $92,739.54 across 52 employees; the July close booked $90,862.13 for 51 rows under the old
method.

The cell families, and the bytes behind them:

1. **The determination.** The cutover memo of 06/20/2026 replaces the 2025 policy from
   07/01/2026: accrual per biweekly pay period at the tier over 26, posted on the pay date;
   carryover capped at 40.0 hours at 06/30/2026; tiers by adjusted service date with a tier change
   in the period containing the anniversary; valuation at the rate on file over 2,080; ended
   employees out. Eleven employees are capped. Nine migrated records read 07/01/2026 in BambooHR
   and on the roster, and six of them accrue at the wrong tier there; TRT-0071's rehire bridges a
   241-day break to 03/08/2021 and the 160-hour tier. TRT-0018 crosses five years on 08/09/2026,
   inside the fourth posted period. TRT-0088's signed promotion ($118,000.00 from 06/16/2026) and
   TRT-0117's signed amendment ($148,200.00 from 05/16/2026) were dropped by the load; TRT-0096's
   offer letter carries the $3,000.00 anniversary step effective 08/17/2026. TRT-0141 was
   scheduled 25 hours until 08/09/2026 and 32 from 08/10/2026, pro-rata under 30. Four periods
   are posted by 08/31/2026; 560 hours of approved time off are recorded. 75
   of 92 points, the gate among them.
2. **BambooHR brought to the schedule.** Six policy assignments and 52 balances, two of them on
   rows the run has to create. 12 points.
3. **The page and its form.** The page published, 52 rows keyed by ID, the form, the summary.
   5 points.

## Spec compliance notes

| Spec | How the ask meets it |
|---|---|
| **1A** Realistic and complex | A policy cutover two months old, an HRIS load that capped nothing and moved nine service dates, an Office Manager gone who owned the policy page and the July schedule, a Finance Manager who booked July on the loaded numbers, and a handbook that incorporates a dated memo the wiki contradicts |
| **1B** Natural prompting | One sentence in the owner's register; the request referenced by subject; the page title stated exactly; no step, order, workflow, persona, credential or format convention. The memo names the July detail it replaces and no rule |
| **1C** Unique correct answer | Every graded value is a document's printed rule applied to a document's printed record, recomputed from the world's bytes by `check_world()` on every build. The two rounding conventions the memo permits are both computed and both accepted; the reviewer decision rules in `02_task_metadata.md` settle the remaining readings |
| **1D** Timeless | The request dates itself 09/01/2026 and sets 08/31/2026 as the measurement date; every other date is a world date |
| **1E** Tightly scoped outputs | One page, one table, one summary, and the BambooHR rows it implies. A planned 21 rows, all App DB, on 22 world files and nine app tables |
| **1F** Self-sufficient | Solvable from the request, the world files and the three apps alone. The one input uploads through 1.4 on the Filesystem target, measured at 13 of 13 here |
| **1G** Purposeful | No persona. The prompt names the request, the two sources and the two deliverables |
| **2A** Genuinely challenging | **Unmeasured, predicted.** The registered failing paths score 34 of 92, 37.0% and 47 of 92, 51.1%; the free base is 5 of 92, 5.4%. The registered Gemini mean and the decision rule are in `06_failure_analysis.md`, dated before any run |

**Withheld from the prompt and from the task input** (machine-asserted by
`build/build_task_input.py`): every policy document, page and record by name other than the July
detail; the cap and every carryover word; the accrual period and every per-period, monthly or
annual accrual word; every tier value and boundary; every service-date, anniversary, rehire and
bridging word; every part-time, pro-rata and scheduled-hours word; every signed change, promotion,
amendment and step; every word for a record being stale, wrong, loaded, migrated, ended or
missing; the word contractor; the eight names the determination turns on; every total, balance
and rate; every word for checking, confirming, correcting, resolving or governing; and the shape
of the answer, "whether", "only", "except", "instead", "differ", "conflict", "override" and their
neighbours word-boundary-banned.

**Required of the request**: the page title, the columns, the definition of a current employee,
what the summary states, the BambooHR ask, the form and the fence.
