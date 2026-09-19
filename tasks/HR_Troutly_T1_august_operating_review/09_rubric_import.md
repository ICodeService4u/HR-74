# 09 - the file that registers, and the mappings it carries (09/19/2026)

`05_rubric_import.xlsx` is the artifact the task interface loads. `build/rubric_preview.csv` is
this package's own record and carries the package's own columns, the gate kind and the check kind,
which the interface does not read. Both are generated from `build/build_package_artifacts.py`'s
`_rubric()`, so the file that registers cannot drift from the file the record publishes, and
`check_import()` asserts row by row that the criteria, explanations, weights, primary flags and
verifier types in the two are the same strings.

The shape is HR 32 T24's, carried by HR 79 T1: thirteen columns, one row per verifier, the sheet
named `Rubric`. **Thirty-five rows, 113 points.**

**Do not load this file yet.** Both snapshot ids carry the sentinel `SNAPSHOT_ID_NOT_YET_READ`,
because no trajectory has run in this world and a snapshot id is read off an export, never
invented. `check_import()` prints the warning on every build until both are replaced. Read
`world_snapshot_id` and `task_data_id` off the first export, set `SNAP` and `TASK_SNAP` in the
builder, rebuild, and only then import.

| Column | What this package writes |
|---|---|
| Index, Criteria, Numerical Weight | The set on the show-your-work's Verifiers tab, unchanged: 35 rows, 113 points, 13 primary |
| Criteria Explanation | The same set's explanations, in the house register, guarded by `check_register()`: 35 explanations, 122 to 235 characters, 168 average |
| Verifier Type | **`App DB Programatic`** on every row. One "m", the picker's spelling, not the guide's. HR 32 lost a row to the other spelling twice, on a warning rather than an error, and `check_import()` refuses any type containing "Programmatic" |
| Tags | `Final Response` on 33 rows, **`Style / formatting` on the two form rows** (34 and 35), the tag HR 79's task round 7 asked for. The string has not yet been seen accepted by an import here: read the toast, and fall back to `Final Response` if it is dropped |
| Criterion Type | The code-verifier form's own list, `Objective Compliance`, `Expert Assessment`, `Process`, which is what the picker offers on an App DB row. HR 32 T24 imported `Extraction` on one and had the field dropped |
| Severity Level | `Critical` on the 13 primary rows, `Major` on the other 22 |
| Is this a primary criterion? | `Yes` on the 13 rows the determination turns on: the gate, the two unloaded hires, the three ended records, the contractors, REQ-2026-036, 037 and 038, Adjei, and the 21-employee split |
| Reference Artifacts | The picker's resolved objects, 78 citations over 14 world files and the one 1.4 upload, each carrying the snapshot sentinel until the ids are read |
| Grading Target | Empty on every row: no row grades a file |
| Output Dependencies | Empty on every row: the deliverable is two wiki pages and 1.5 Expected Output Files carries nothing |
| Depends on | `None` on every row |

## Reference Artifacts, and the app tables the import does not carry

The field stores a **resolved object**, not a path. A bare string has no `source` for the judge
to dereference and fails the whole grading run, which HR 32 measured at every trajectory 0%. So
each citation ships as the picker's own object, `{"name": "filesystem/<path>", "index": null,
"source": "world", "snapshotId": "<id>", "transformations": []}`, and the task upload as
`filesystem/operating_review_request.pdf` with `"source": "task"`.

The eleven app seed tables the rows rest on stay in `build/rubric_preview.csv` and out of the
import, for HR 79's reason: the picker's browser lists world files, no measurement exists for an
app table as a reference object, and an unresolvable value in this field is the defect class
above. Every row still cites the world documents that decide it.

## The verifier form's own fields, set by hand after the import

A re-import does not restore them. Every row takes the same values but for the check type and the
record id:

| Field | What to put |
|---|---|
| Target database apps | `wiki_js`, the app registration the seed loads into |
| Check type | `Content Match` on the cell, count, summary, vocabulary and date rows; `Existence Check` on rows 1 and 17; `Guard (Negative Check)` on rows 21, 22, 23 and 24, with the allow-list empty because nothing on the staffed tables may carry those keys |
| Target Table | `pages` |
| Target Record ID | The page title for rows 1 and 17; the requisition ID, employee ID or candidate name the row is keyed on for the rest |
| Target Record Label | The criterion's subject in plain words |
| Expected Content | The literal the check asserts, as `SPEC` carries it in the row file |
| Fallback Strategy | **DB only.** `DB with trajectory fallback` fires when the table is empty, which pays a run for narrating a write it never made |
| Verifier code | The row's file under `qc/verifiers/`, pasted whole. It is standalone: the row's `SPEC` on top of the shared engine |
| Additional Notes | The block below, with the row's kind named |

## The Additional Notes block, one for every row

Every row file already carries the code, so the notes exist for the generator and for the
reviewer. The block, with the row's check kind substituted:

```
The snapshot may carry no real column names: ctx.table_columns("pages") has been measured on
another world returning col0, col1, ... Never name a column in SQL. SELECT * and resolve columns
by content: the page is the row whose any cell equals the title, dashes and case normalised, on a
whole-field match. Content is the `content` column where names are real, index 10 of the
documented Wiki.js layout where the row has 21 columns and the title sits at index 3, and
otherwise the longest table-bearing string cell. The published flag is `isPublished` or index 6
under the same validation, and unknown otherwise, which fails an existence row rather than
assuming. Read the pages table only, never pageHistory, never a file, never the trajectory.

A table row is found by a whole-cell match on its key, never a substring. A status cell carries
the asked value as its leading token followed by nothing or a separator, so Not approved never
satisfies Approved and Approved with a qualifier never satisfies Not approved. A count is the
number of distinct ID-keyed rows on the staffed-role tables, the tables carrying an open
requisition column, never a substring tally. A summary figure is read from the prose outside
the tables. An absence row requires the key on no staffed-role table AND the record named on the
page. Every page row carrying the title must satisfy; a wrong duplicate fails.

Never raise. Report every table tested with its column list and row count, the resolution route,
every page row matching the title, and every table row considered with the reason it was
accepted or rejected, on pass and on fail. The seed carries ten pages and neither title, so an
untouched database fails every row.
```

## The harness record

`qc/verifier_harness.py` runs all 35 row files against `qc/scenarios.py`: 37 snapshots, the
golden pages first, then one planted defect per way a row can be wrong. **1295 of 1295 verdicts
correct on 09/19/2026.** The battery found two defects in the engine before it found none: the
count rows counted TRT-keyed rows only, so a contractor row on the staffed tables slipped past the
31-employee count by coincidence of arithmetic, and the department and contractor rows accepted a
mention in the page's intro where the request asks the summary to state the figure. Both are the
false-pass class, and both are in the battery now.

Studio's per-verifier test-run is still owed after the import: it catches whether the code
imports and whether the real `ctx` exposes what the engine assumes, which the harness cannot.
