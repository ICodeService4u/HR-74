# 09 - the file that registers, and the mappings it carries (T2 v2, 09/22/2026)

`05_rubric_import.xlsx` is the artifact the task interface loads. `build/rubric_plan.csv` is this
package's own record and carries two columns of its own, Family and Gate, which the interface
does not read, plus the five paste fields. Both are generated from
`build/build_package_artifacts.py`'s `_rubric()`, read off the plan's rows, and `check_import()`
asserts row by row that the criteria, explanations, weights, criterion types, primary flags and
verifier types in the two are the same strings.

The shape is HR 32 T24's, carried by HR 79 T1 and by T1, T1 v2 and T2 here: thirteen columns in
HR 79 T1's order, one row per verifier, the sheet named `Rubric`. **13 rows, 79 points, 1 gate,
12 primary**, md5 `923fcbdd7bdf474a702e26c5e6142039`, the md5 a property of the content because
the builder freezes every timestamp in the file. The rows are the plan's after review round 1 of
09/22/2026, which took the per-employee table and the measurement-date sentence out of the memo
and put five department lines in, so the 27-row file of the same morning is superseded whole.

**What the rescope took out of the import.** T2's 55 rows carried 14 points of page and form and
29 BambooHR rows at 1 each, and v2's first file carried 24 per-employee cells. This file grades
the page, the two totals and the five lines. There is no BambooHR row, so no row targets
`bamboohr`, and there is no form row, so the `Style / formatting` tag goes on nothing. `FORM_ROWS` and
`FORM_TAG` stay in the builder as the bar: `check_import()` still computes the wanted tag from the
criterion text, and `build/build_task_input.py` bars every form line from the memo with a control
each. Nothing in the import grades absence: a page that also carries every employee, or Sales and
Marketing apart beside the joined line, takes every point.

**The ids, and what the import populates.** The world snapshot id is
`snap_c6f6a0879f3d47a19048ee80d7529157`, unchanged across the exports of T1, T1 v2 and T2. The
task data id is `snap_1e12795ed0df4d489a36382afdb63279`, read off T2's 09/21/2026 re-upload and
carried here; a 1.4 re-upload mints a new task data id, so v2's memo will mint its own and the id
is re-read off v2's first export. `check_import()` refuses to build the file on a sentinel id.
What the import does and does not populate is T2's measurement, not a guess: its five loads of
09/20 and 09/21/2026 each read back criteria, explanations, weights and criterion types, and
every row came back with `verifier_custom_field_values = {}` and no tag. So Tags, Reference
Artifacts and Grading Target do not populate through the import, which is what HR 79 T24 measured
on the tag field on 09/11/2026. Count the rows Studio holds against 13, then set Reference
Artifacts in the Structured view from `build/rubric_plan.csv`, which carries them per row. Tags
are `Final Response` on all 13 rows. Grading Target stays empty on an App DB row.

| Column | What this package writes |
|---|---|
| Index, Criteria, Numerical Weight | The plan's 13 rows: 79 points, one gate at 10, the only 9 or 10 in the file |
| Criteria Explanation | The house register, held by `check_register()` on every build: 13 explanations, 108 to 234 characters, 197 average, every figure the build's own |
| Verifier Type | **`App DB Programatic`** on every row. One "m", the picker's spelling, not the guide's. `check_import()` refuses a type containing "Programmatic" |
| Tags | `Final Response` on all 13 rows. **`Style / formatting`** is in the allowed set and on no row, because the memo carries no Form section. Set by hand after import, see above |
| Criterion Type | `Expert Assessment` on the 12 rows that apply a rule against a record carrying a finished number, `Objective Compliance` on row 1, which reads a page's existence. The code-verifier form's own list, `Process` unused |
| Severity Level | `Critical` on the 12 primary rows, `Major` on row 1 |
| Is this a primary criterion? | `Yes` on the 12 determination rows, which every registered path short of the heal fails at least one of: the gate, the hours total and the ten line figures, every one a figure the load carries wrong. `No` on row 1 |
| Reference Artifacts | The picker's resolved objects, 71 citations over 13 of the 22 selected world files and the one 1.4 upload. Not populated by the import, set by hand, see above |
| Grading Target | Empty on every row: no row grades a file. HR 79 T1's registered position, and its round 7 passed with it empty on every App DB row |
| Output Dependencies | Empty on every row: the deliverable is one wiki page and 1.5 carries nothing |
| Depends on | `None` on every row |

## The weights, and the guide's importance table

The weights were registered 09/22/2026 before any v2 run and do not move after one.
`check_rubric()` holds them to the guide's table by criterion type: a compliance row at 1 to 5, a
reasoning row at 1 to 10, and 9 or 10 on the gate alone, which is row 2, the total dollar
liability, Critical value. Every other weight is priced by materiality, the dollars the line figure
moves: 7 at $2,000.00 or more, 6 at $800.00 or more, 5 at $250.00 or more, 4 at $80.00 or more
and 3 below that, from `MONEY_BANDS` in the builder.

| Weight | Rows | Points | What carries it |
|---|---|---|---|
| 10 | 1 | 10 | The gate, the total dollar liability |
| 8 | 1 | 8 | The total PTO hours |
| 7 | 6 | 42 | A line figure moving $2,000.00 or more, Engineering, Finance and Corporate, and Sales and Marketing |
| 6 | 2 | 12 | A line figure moving $800.00 or more, Customer Success |
| 3 | 2 | 6 | A line figure moving less than $80.00, Product |
| 1 | 1 | 1 | The page published, the only row that is not a determination |

**No row weighs 2**, which is the point of the rescope: the grader's rule is that a criterion
whose failure materially changes the output weighs more than 2, and every row here but row 1 does
change the output. Row 1 is 1 point of 79, 1.3%, and it is the whole of what a response
earns for publishing a page with the wrong numbers on it. Expert Assessment carries 78 of 79,
98.7%, and a row is primary if and only if it is a reasoning row, which `check_rubric()`
also holds. The bands 5 and 4 are in `MONEY_BANDS` and on no row: no line moves between $80.00
and $800.00.

## Reference Artifacts

Each citation ships as the picker's own object, `{"name": "filesystem/<path>", "index": null,
"source": "world", "snapshotId": "<id>", "transformations": []}`, and the task upload as
`filesystem/pto_liability_request.pdf` with `"source": "task"`. A bare string has no `source` for
the judge to dereference, which HR 32 measured at every trajectory 0%. Every world citation is
held to the selection block in `02_task_metadata.md`, so a row cannot cite a file the run is not
given, and `check_import()` refuses an app seed table cited as a world file. Row 1 cites the
request and the wiki's seed table; the gate cites nine, the most in the file; a line row cites
4 to 8, the request and the documents behind the rules that land in its line.

The nine selected files no row cites are the traps: the 2025 policy, the load file, the field
mapping workbook, the closeout memo, the payroll history, the July close package, the Paid Time
Off wiki page, the Compensation Authority page and the Onboarding Data Standards page. Each
carries a number a failing path prints, and the selection keeps them in the run's reach. The nine
app tables sit in the plan's references for the record and not in the picker, whose browser does
not list them.

## The explanation column

This column is what the interface publishes beside each row, so every explanation states the
governing fact and names its source, in the house register: ASCII, no colon, semicolon or
bracket, no spaced dash, no spelled month, no ISO date, no grading word, no reference to the
rubric's own rows, at most three sentences and 240 characters, no two rows opening alike or
carrying one text, and the set averaging at most 200. The rules are HR 79 T1's, carried from T2
unchanged. Every number in an explanation is formatted from the schedule the builder recomputes,
so a world byte that moved would move the explanation with it.

## The verifier record

Built 09/22/2026 and rebuilt for review round 1 the same day. Every row's code is generated into
`qc/verifiers/` from the same rows that wrote this file: the row's spec stamped onto
`build/verifier_engine.py`, so a row file is never edited by hand and `check_rubric()` holds each
spec to its criterion, the line it names and the value it states. The engine is 373 lines and
reads one app with five check kinds: `exists`, `total`, `hours`, `line_hours` and `line_total`.

**How a line is read.** A line is stated where the page names it: a table row keyed on no
employee, one of whose cells is the line's name, whole-cell and with case, markup, an ampersand
and a trailing `total` or `subtotal` normalised; or a prose line that opens on the name. Sales
alone never reads as Sales and Marketing, a figure inside an employee row is that employee's and
never a line's, and a line a reader would have to add up from the employees is not stated.

Tolerances, from the engine's own constants: a stated dollar total or line to half a dollar and a
stated hours figure to a twentieth of an hour, `TOL_TOTAL_MONEY` and `TOL_LINE_MONEY` 0.5,
`TOL_TOTAL_HOURS` and `TOL_LINE_HOURS` 0.05. The bands are wide because v2's memo carries no Form
section and nothing tells a response how many decimals to print. No registered path comes within
either band, which `06_failure_analysis.md` states path by path.

`qc/verifier_harness.py` proves the set on 40 snapshots with the answer known, **520 of 520
verdicts correct**, 13 rows against every snapshot: the golden page, real and placeholder column
names, the page as HTML, the title with an em dash, a 20-column pages table, a second page under
the same title, a note page carrying the title in its description, the paths P0 to P5 as pages,
the load copied whole, and one planted defect per way a row can be wrong: a line a tenth of an
hour or a dollar out, a line dropped, Sales and Marketing given only apart, the joined figures labelled Sales alone in a table and in prose, the lines left to
the reader, a line's figures inside an employee row, a prose sentence naming Sales, a total a
dollar out, an hours total a tenth out. Three scenarios carry the over-delivery constraint and
fail no row: every employee with a line per department and a summary block, the lines as prose,
and a second table beside the lines. No Additional Notes are written: the route is T1 v2's and
T2's, generated code pasted per row, because HR 79 measured Studio's own generation from notes
grading wrongly on three rows of three.

**The form fields at paste time**, per row in `build/rubric_plan.csv`: Target App `wiki_js_mcp` on
every row, Check Type `Existence Check` on row 1 and `Content Match` on rows 2 to 13, Target
Record ID the page title on every row, Fallback Strategy **DB only** on every row, and the
Verifier File to paste. Grading Target stays empty.

**What the fixture rests on, and what it does not know.** The pages table follows the documented
Wiki.js layout, 21 columns with the title at index 3, the published flag at 6 and the content at
10, which T1 v2 built to and thirteen `get_page` reads agreed with. The live app's table names
and column order are unmeasured, which is why the engine finds the pages table by those columns
and not by a name, and why the first grading run's `details` strings are owed to the open items
in `02_task_metadata.md`. The BambooHR and Greenhouse seed tables stay in the fixture as other
apps' tables that no row reads, so the discovery has to pass over them.
