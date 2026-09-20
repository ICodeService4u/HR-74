# 09 - the file that registers, and the mappings it carries (T1 v2, 09/19/2026)

`05_rubric_import.xlsx` is the artifact the task interface loads. `build/rubric_preview.csv` is
this package's own record. Both are generated from `build/build_package_artifacts.py`'s
`_rubric()`, and `check_import()` asserts row by row that the criteria, explanations, weights,
primary flags and verifier types in the two are the same strings.

The shape is HR 32 T24's, carried by HR 79 T1 and T1 here: thirteen columns, one row per
verifier, the sheet named `Rubric`. **Twenty-four rows, 83 points.**

**Loadable, never loaded.** The world snapshot id is the one T1's nine exports carried,
`snap_c6f6a0879f3d47a19048ee80d7529157`, and the world has not changed. The task data id is
`snap_fbf9dc06005743a28e8d6fd2238c7f5f`, read off the four v2 exports of 09/20/2026, and `check_import()`
stopped printing its warning on that build. The package retired on the run set before the import
was due, so the task record still carries the synth's twenty verifiers.

| Column | What this package writes |
|---|---|
| Index, Criteria, Numerical Weight | The set on the show-your-work's Verifiers tab, unchanged: 24 rows, 83 points, 10 primary |
| Criteria Explanation | The same set's explanations, in the house register, guarded by `check_register()` |
| Verifier Type | **`App DB Programatic`** on every row. One "m", the picker's spelling, not the guide's |
| Tags | `Final Response` on 22 rows, **`Style / formatting` on the two form rows** (23 and 24) |
| Criterion Type | `Objective Compliance` or `Expert Assessment`, the code-verifier form's own list |
| Severity Level | `Critical` on the 10 primary rows, `Major` on the other 14 |
| Is this a primary criterion? | `Yes` on the 10 rows the determination turns on: the gate, the two unloaded hires, the three ended records, the count by department, and REQ-2026-036, 037 and 038 |
| Reference Artifacts | The picker's resolved objects over thirteen world files and the one 1.4 upload |
| Grading Target | Empty on every row: no row grades a file |
| Output Dependencies | Empty on every row: the deliverable is two wiki pages and 1.5 carries nothing |
| Depends on | `None` on every row |

## Reference Artifacts

Each citation ships as the picker's own object, `{"name": "filesystem/<path>", "index": null,
"source": "world", "snapshotId": "<id>", "transformations": []}`, and the task upload as
`filesystem/operating_review_request.pdf` with `"source": "task"`. A bare string has no `source`
for the judge to dereference, which HR 32 measured at every trajectory 0%.

## The verifier code

Every row's code is generated into `qc/verifiers/` from the same spec that wrote the row, and the
harness proves the set on 36 snapshots before any of it is pasted: `python3 qc/verifier_harness.py`.
The two population kinds new in v2, the set gate and the populated-table absence, each carry a
negative control in `build/negative_controls.py`.
