# 09 - the file that registers, and the mappings it carries (T2, 09/20/2026)

`05_rubric_import.xlsx` is the artifact the task interface loads. `build/rubric_plan.csv` is
this package's own record and carries two columns of its own, Family and Gate, which the
interface does not read. Both are generated from `build/build_package_artifacts.py`'s
`_rubric()`, read off the plan's 21 rows, and `check_import()` asserts row by row that the
criteria, explanations, weights, criterion types, primary flags and verifier types in the two
are the same strings.

The shape is HR 32 T24's, carried by HR 79 T1 and by T1 and T1 v2 here: thirteen columns in
HR 79 T1's order, one row per verifier, the sheet named `Rubric`. **28 rows, 89 points, 1 gate,
13 primary**, md5 `65c0814cd454787c5a5ea3203200deb1`, the md5 a property of the content because
the builder freezes every timestamp in the file. The rows are the plan's of 09/20/2026 as task
round 1 left them the same day, the weights unchanged after the five Gemini runs read 23.9%, so
every score in `06_failure_analysis.md` stands and the round-1 re-score sits beside it.

**Loaded once, and what landed.** The world snapshot id is `snap_c6f6a0879f3d47a19048ee80d7529157`,
unchanged across the eighteen exports of T1, T1 v2 and T2. The task data id is
`snap_45e68b376f2547dca61408b65d8ba774`, read off all five T2 exports of 09/20/2026.
`check_import()` refuses to build the file on a sentinel id. The 21-row file of the first build
was loaded on 09/20/2026 and task round 1 read it back: 21 rows landed, with their criteria,
explanations, weights and criterion types, and every row carried
`verifier_custom_field_values = {}` and no tag. So the Tags, Reference Artifacts and Grading
Target columns do not populate through the import, which is what HR 79 T24 measured on the tag
field on 09/11/2026. This 28-row file replaces the loaded one; count the rows Studio holds against
28, then set Tags and Reference Artifacts in the Structured view from `build/rubric_plan.csv`,
which carries both per row. Grading Target stays empty on an App DB row.

| Column | What this package writes |
|---|---|
| Index, Criteria, Numerical Weight | The plan's 28 rows: 89 points, one gate at 10, the only 9 or 10 in the file |
| Criteria Explanation | The house register, held by `check_register()` on every build: 28 explanations, 107 to 239 characters, 189 average, every figure the build's own |
| Verifier Type | **`App DB Programatic`** on every row. One "m", the picker's spelling, not the guide's. `check_import()` refuses a type containing "Programmatic" |
| Tags | `Final Response` on 26 rows, **`Style / formatting` on the two form rows**, row 3, the decimals the request sets, and row 6, the summary above one table. Set by hand after import, see above |
| Criterion Type | `Expert Assessment` on the 13 rows that apply a rule against a record carrying a finished number, `Objective Compliance` on the 15 that read a stated value or a stated set. The code-verifier form's own list, `Process` unused |
| Severity Level | `Critical` on the 13 primary rows, `Major` on the other 15 |
| Is this a primary criterion? | `Yes` on the 13 rows the determination turns on and the registered paths short of the heal fail: the gate, the cap, the loaded date, the bridge, the timed anniversary, the three rates, the part-time schedule, each unloaded hire, and the two BambooHR set rows that carry the schedule's values |
| Reference Artifacts | The picker's resolved objects, 92 citations over 17 of the 22 selected world files and the one 1.4 upload. Not populated by the import, set by hand, see above |
| Grading Target | Empty on every row: no row grades a file. HR 79 T1's registered position, and its round 7 passed with it empty on every App DB row |
| Output Dependencies | Empty on every row: the deliverable is a wiki page and BambooHR state, and 1.5 carries nothing |
| Depends on | `None` on every row |

## The weights, and the guide's importance table

The plan's weights were registered 09/20/2026 before any run and do not move after it.
`check_rubric()` holds them to the guide's table by criterion type: a compliance row at 1 to 5,
a reasoning row at 2 to 10, and 9 or 10 on the gate alone. HR 79 T1 and T1 v2 each pinned a
narrower set of values for their own rows; the rule here is the table's own bands, so that the
registered weights stand as scored. The 2 is the two unloaded hires, one row each after task
round 1, a reasoning row on one cell that moves the total by under a third of a percent. Expert
Assessment carries 67 of 89, 75.3%, and a row is primary if and only if it is a reasoning row,
which `check_rubric()` also holds.

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

## The verifier code

Built 09/20/2026. Every row's code is generated into `qc/verifiers/` from the same rows that
wrote this file: the row's spec stamped onto `build/verifier_engine.py`, so a row file is never
edited by hand and `check_rubric()` holds each spec to its criterion, the key it names and the
value it states. `qc/verifier_harness.py` proves the set on 63 snapshots with the answer known,
**1764 of 1764 verdicts correct**: the golden page and BambooHR brought to the schedule as the
correct state, real and placeholder column names, the page as HTML, the title with an em dash,
the BambooHR tables keyed on the app's integer ids, on the seed's strings and under other names,
the two archived runs G1 and G2 and the paths P2 to P5 as pages, and one planted defect per way a
row can be wrong, the stated values' neighbours among them. Two defects the battery found in the
engine before anything was pasted: a table's own id column read as the employee reference, the
R3 class, and the policy table mistaken for the assignment table when the loader keeps the seed's
strings. No Additional Notes are written: the route is T1 v2's, generated code pasted per row,
because HR 79 measured Studio's own generation from notes grading wrongly on three rows of three.

**The form fields at paste time**, per row in `build/rubric_plan.csv`: Target App `wiki_js` on
rows 1 to 24 and `bamboohr` on rows 25 to 28, Check Type by kind, Target Record ID the page title
or the employee number, Fallback Strategy **DB only** on every row, the Verifier File to paste.
Grading Target stays empty.

**What the fixture rests on, and what it does not know.** The pages table follows the documented
Wiki.js layout, 21 columns with the title at index 3, the published flag at 6 and the content at
10, which T1 v2 built to and thirteen `get_page` reads agreed with. The BambooHR tables follow the
six seed CSV columns with the app's integer ids as the five runs observed them, 1 to 58 in the
seed's row order and 59 and 60 for the two rows a run creates; the fixture asserts that map
against G1's own listing. The live app's table names and column order are unmeasured, which is
why the engine finds the employee table by its employee numbers and email column, the policy
table by its three names appearing once each, and the assignment and balance tables by their
references into those two, and why the first grading run's `details` strings are owed to open
item 4 in `02_task_metadata.md`.
