# 09 - the file that registers, and the mappings it carries (T2, 09/20/2026)

`05_rubric_import.xlsx` is the artifact the task interface loads. `build/rubric_plan.csv` is
this package's own record and carries two columns of its own, Family and Gate, which the
interface does not read. Both are generated from `build/build_package_artifacts.py`'s
`_rubric()`, read off the plan's rows, and `check_import()` asserts row by row that the
criteria, explanations, weights, criterion types, primary flags and verifier types in the two
are the same strings.

The shape is HR 32 T24's, carried by HR 79 T1 and by T1 and T1 v2 here: thirteen columns in
HR 79 T1's order, one row per verifier, the sheet named `Rubric`. **55 rows, 105 points, 1 gate,
34 primary**, md5 `132b10edfb5f835facbb529522427bb8`, the md5 a property of the content because
the builder freezes every timestamp in the file. The rows are the plan's of 09/20/2026 as task
rounds 1 to 5 left them, no page rule's weight moved after the five Gemini runs read 23.9%, so
every score in `06_failure_analysis.md` stands and the five re-scores sit beside it.

**Loaded once, and what landed.** The world snapshot id is `snap_c6f6a0879f3d47a19048ee80d7529157`,
unchanged across the eighteen exports of T1, T1 v2 and T2. The task data id is
`snap_45e68b376f2547dca61408b65d8ba774`, read off all five T2 exports of 09/20/2026.
`check_import()` refuses to build the file on a sentinel id. The 21-row file of the first build
was loaded on 09/20/2026 and task round 1 read it back: 21 rows landed, with their criteria,
explanations, weights and criterion types, and every row carried
`verifier_custom_field_values = {}` and no tag. So the Tags, Reference Artifacts and Grading
Target columns do not populate through the import, which is what HR 79 T24 measured on the tag
field on 09/11/2026. The 28-row file was loaded next and task round 2 read it, then the 43-row
file, which task round 3 read, then the 44-row file, which task round 4 read, then the 48-row
file, which task round 5 read. This 55-row file replaces it; count the rows Studio holds against
55, then set Tags and Reference Artifacts in the
Structured view from `build/rubric_plan.csv`, which carries both per row. Grading Target stays
empty on an App DB row.

| Column | What this package writes |
|---|---|
| Index, Criteria, Numerical Weight | The plan's 55 rows: 105 points, one gate at 10, the only 9 or 10 in the file |
| Criteria Explanation | The house register, held by `check_register()` on every build: 55 explanations, 107 to 239 characters, 189 average, every figure the build's own |
| Verifier Type | **`App DB Programatic`** on every row. One "m", the picker's spelling, not the guide's. `check_import()` refuses a type containing "Programmatic" |
| Tags | `Final Response` on 49 rows, **`Style / formatting` on the six form rows**, rows 3, 4 and 5, hours, rates and dollars at the request's precision, row 11, an ID on every row, row 12, dates MM/DD/YYYY, and row 13, the summary above one table. Set by hand after import, see above |
| Criterion Type | `Expert Assessment` on the 34 rows that apply a rule against a record carrying a finished number, `Objective Compliance` on the 21 that read a stated value, a stated set or a stated record. The code-verifier form's own list, `Process` unused |
| Severity Level | `Critical` on the 34 primary rows, `Major` on the other 21 |
| Is this a primary criterion? | `Yes` on the 34 rows the determination turns on and the registered paths short of the heal fail: the gate, the cap, the loaded date, the bridge, the timed anniversary, the three rates, the part-time schedule, each unloaded hire, and the 23 BambooHR rows that carry a policy or a balance the schedule moves |
| Reference Artifacts | The picker's resolved objects, 167 citations over 17 of the 22 selected world files and the one 1.4 upload. Not populated by the import, set by hand, see above |
| Grading Target | Empty on every row: no row grades a file. HR 79 T1's registered position, and its round 7 passed with it empty on every App DB row |
| Output Dependencies | Empty on every row: the deliverable is a wiki page and BambooHR state, and 1.5 carries nothing |
| Depends on | `None` on every row |

## The weights, and the guide's importance table

The plan's weights were registered 09/20/2026 before any run and do not move after it.
`check_rubric()` holds them to the guide's table by criterion type: a compliance row at 1 to 5,
a reasoning row at 1 to 10, and 9 or 10 on the gate alone. HR 79 T1 and T1 v2 each pinned a
narrower set of values for their own rows; the rule here is the table's own bands, so that the
registered weights stand as scored. The 2 is the two unloaded hires, one row each after task
round 1, a reasoning row on one cell that moves the total by under a third of a percent. The 1
on a reasoning row is task round 2's: a BambooHR row that mirrors one page rule on one record,
priced so the mirror never outweighs the rule it mirrors. Expert Assessment carries 80 of 105,
76.2%, and a row is primary if and only if it is a reasoning row, which `check_rubric()` also
holds.

## Reference Artifacts

Each citation ships as the picker's own object, `{"name": "filesystem/<path>", "index": null,
"source": "world", "snapshotId": "<id>", "transformations": []}`, and the task upload as
`filesystem/pto_liability_request.pdf` with `"source": "task"`. A bare string has no `source`
for the judge to dereference, which HR 32 measured at every trajectory 0%. Every world citation
is held to the selection block in `02_task_metadata.md`, so a row cannot cite a file the run is
not given. The five selected files no row cites are the traps: the 2025 policy, the closeout
memo, the payroll history, the July close package and the Paid Time Off wiki page. Each carries
a number a failing path prints, and the selection keeps them in the run's reach. The nine app
tables sit in the plan's references for the record and not in the picker, whose browser does not
list them.

## The explanation column

This column is what the interface publishes beside each row, so every explanation states the
governing fact and names its source, in the house register: ASCII, no colon, semicolon or
bracket, no spaced dash, no spelled month, no ISO date, no grading word, no reference to the
rubric's own rows, at most three sentences and 240 characters, no two rows opening alike or
carrying one text. The rules are HR 79 T1's, and the first build here failed them: the gate's
row ran to 243 characters and three more rows were over 240. The texts were cut to the rule and
the rule was not moved. Every number in an explanation is formatted from the schedule the
builder recomputes, so a world byte that moved would move the explanation with it.

## Task round 1, 09/20/2026

The round read the 21-row file and the set was rebuilt the same day: rows 6, 7, 15, 16 and 19 of
that file read the cap on five employees, the loaded date on five, the four ended records, the
two hires and the six policies each in one row, and the round read each as stacked. Every one now
names one person, or, in BambooHR, one set the two created rows are carved out of, and no
registered weight moved. The calculation-path clauses left the criteria for the explanations, and
the request's last two explicit asks, a name and a department on every row and the summary above
one table, are rows at 1. The Greenhouse fence, the Grading Target on App DB rows and the fields
the import does not populate are answered in `qc/README.md`.

## Task round 2, 09/20/2026

The round read the 28-row file and raised six findings under two P0 dimensions, all six
accepted, none disputed and no ask changed. No Stacked Criteria: row 3 carried the precision and
the reconciliation as one claim and is now rows 3 and 4; rows 25 and 26 read 50 records each and
are now one record a row, the six policies the schedule moves and the five balances that mirror
a page rule at 1 each, with a guard at 1 over the 44 policies and another over the 33 balances
the schedule leaves as loaded, so a record the request asks nothing of still has a row that
reads it. Prompt-Rubric Alignment: the tier joins the name and the department on row 6, and the
request's own form lines, an employee ID on every row and dates MM/DD/YYYY, are rows 7 and 8;
Change nothing in Greenhouse is row 43, a state-preservation guard over the fourteen seed tables
read by content. The Greenhouse row reverses task round 1's dispute on the owner's call, because
the round asked twice and the row costs the tier one point it earns on every path; if the first
grading run shows the guard false-zeroing the golden state, the memo's line and the row go
together rather than the guard loosening. The two set rows at 5 became thirteen rows at 1, so
the BambooHR family carries 15 against 12; no page weight moved.

## Task round 3, 09/20/2026

The round read the 43-row file and raised one P0 with two asks and one P1. The P0's first ask,
no-change checks on payroll, the September compensation cycle and benefits, was the third round
running on the memo's out-of-scope block, after the Greenhouse line in rounds 1 and 2, and the
same finding HR 79 T1 met in its rounds 6, 7 and 9 and closed only by removing the block. It is
closed here the same way, on the owner's decision: the block is gone from the memo, row 43 with
it, and `build/build_task_input.py` bars a fence from returning. The P0's second ask is taken,
a policy row at 1 for each record the run creates, rows 43 and 44, on the same `policy` kind as
the six moved-policy rows. The P1, that rows 34 and 40 graded a no-change the request never
asked, is taken as wording: the code compared the final policy and balance to the schedule's
already, and the criteria now state the schedule's state on those records. 44 rows, 97 points,
22 primary, the BambooHR family 17 against 15, no page weight moved; the runs re-score at
29.3%. The re-rendered memo, md5 `9693455bbb61d3c225047a3d98f1118d`, was re-uploaded the same day.

## Task round 4, 09/20/2026

The round read the 44-row file and raised three findings. No Stacked Criteria: the precision row
and the column row each stacked three independently failable requirements and are three rows at
1 each, rows 3 to 5 and 8 to 10; and the population row decided the same absences the five
exclusion rows decide, so it reads presence alone, an employee row for each of the 52, and rows
23 to 27 decide absence. Verifier Wording Convention: the two BambooHR set rows named a schedule
a grader could not resolve, so each states every record and its value in the criterion, 44
policies by name on row 38 and 33 balances by figure on row 44, one row each so the inaction
points stay at 2. Prompt-Rubric Alignment, a verifier for the memo's deadline heading and its
retention line: the fence pattern again, closed on the owner's decision as the fence was, both
lines gone from the memo and the memo builder barring a deadline or a filing line from
returning. 48 rows, 101 points, 22 primary, the free base 14 under a seventh; the runs re-score
at 32.1%. The re-rendered memo, md5 `5a4089293b429961e17e67e309251fde`, is owed to 1.4.

## Task round 5, 09/21/2026

The round read the 48-row file and raised two findings. Prompt-Rubric Alignment: the BambooHR
ask covers every employee on the schedule and twelve moved balances had no BambooHR row, eight
capped openings and four wrong-tier records, so each has one at 1, Expert Assessment, on the
code the five mirrored rows use, rows 34 to 50 with the five. Verifiers Grade Only What the
Prompt Asks For: the four ended records and the contractors, one row each since task round 1,
were read as grading a negative the memo never states; on the owner's decision the five rows are
gone and row 2 reads the 52 as the only rows again, so the memo's definition of a current employee
is graded once, on the set. 55 rows, 105 points, 34 primary; the runs re-score at 23.2%, and
`06_failure_analysis.md` states the arithmetic of the fall.

## The verifier code

Built 09/20/2026. Every row's code is generated into `qc/verifiers/` from the same rows that
wrote this file: the row's spec stamped onto `build/verifier_engine.py`, so a row file is never
edited by hand and `check_rubric()` holds each spec to its criterion, the key it names and the
value it states. `qc/verifier_harness.py` proves the set on 71 snapshots with the answer known,
**3905 of 3905 verdicts correct**: the golden page and BambooHR brought to the schedule as the
correct state, real and placeholder column names, the page as HTML, the title with an em dash,
the BambooHR tables keyed on the app's integer ids, on the seed's strings and under other names,
the Greenhouse seed tables beside them as a third app's that no row reads, the two archived runs
G1 and G2 and the paths P2 to P5 as pages, and one planted defect per way a row can be wrong, the stated values' neighbours
among them. Two defects the battery found in the engine before anything was pasted: a table's
own id column read as the employee reference, the R3 class, and the policy table mistaken for
the assignment table when the loader keeps the seed's strings. Task round 2's rows found two
more: G2's bold total line, two pipes on one line, read as a row carrying a name and no ID, and
an employee row with its ID blank dropping out of the count and the sums the summary, the
reconciliation and the layout read. An employee row is now a keyed row or an unkeyed row that
carries a name and a figure, a name being a cell with no digit and no total word, so a total line
neither counts nor sums and a row missing its ID fails the ID row and the set and nothing else.
The battery also measured that G1, G3 and G5 wrote August 31, 2026 in their prose, so the date
row fails three of the five archived runs, and the expectation records it. No Additional
Notes are written: the route is T1 v2's, generated code pasted per row,
because HR 79 measured Studio's own generation from notes grading wrongly on three rows of three.

**The form fields at paste time**, per row in `build/rubric_plan.csv`: Target App `wiki_js` on
rows 1 to 26 and `bamboohr` on rows 27 to 55, Check Type by kind, Target Record ID the page
title, the employee number or the loaded records a set row states, Fallback Strategy **DB only** on
every row, the Verifier File to paste. Grading Target stays empty.

**What the fixture rests on, and what it does not know.** The pages table follows the documented
Wiki.js layout, 21 columns with the title at index 3, the published flag at 6 and the content at
10, which T1 v2 built to and thirteen `get_page` reads agreed with. The BambooHR tables follow the
six seed CSV columns with the app's integer ids as the five runs observed them, 1 to 58 in the
seed's row order and 59 and 60 for the two rows a run creates; the fixture asserts that map
against G1's own listing. The live app's table names and column order are unmeasured, which is
why the engine finds the employee table by its employee numbers and email column, the policy
table by its three names appearing once each, and the assignment and balance tables by their
references into those two, and why the first grading run's `details` strings are owed to open
item 4 in `02_task_metadata.md`. The fourteen Greenhouse seed tables stay in the fixture as a
third app's tables that no row reads since task round 3, so the discovery has to pass over them.
