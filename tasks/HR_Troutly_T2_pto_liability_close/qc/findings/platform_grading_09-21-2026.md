# The first platform grading of T2, 09/21/2026 - what it measured and what it did not

Five Gemini runs landed on the 55-row set with the verifier code pasted, G1 and G2 on task
version 29 and G3, G4 and G5 on 30, and G5's grading pane was read back row by row into
`run_set_09-21-2026/G5_platform_grade.json`. It reports 2 passes of 55, a weighted 2 of 105,
1.9%. The same run's archived bytes, the page as the app returned it to the run's own get_page
and the BambooHR writes with the app's results, score 19 of 105, 18.1%, by the same 55 row files.

The gap is not a rounding of judgment. `qc/compare_platform_grade.py` recomputes both readings
and prints them row by row, and the disagreement is clean:

| Row | Target | Weight | The platform | The archived bytes |
|---|---|---|---|---|
| 1 | wiki | 1 | fail | pass |
| 2 | wiki | 2 | fail | fail |
| 3 | wiki | 1 | fail | pass |
| 4 | wiki | 1 | fail | pass |
| 5 | wiki | 1 | fail | pass |
| 6 | wiki | 1 | fail | pass |
| 7 | wiki | 1 | fail | pass |
| 8 | wiki | 1 | fail | pass |
| 9 | wiki | 1 | fail | pass |
| 10 | wiki | 1 | fail | pass |
| 11 | wiki | 1 | fail | pass |
| 12 | wiki | 1 | fail | pass |
| 13 | wiki | 1 | fail | pass |
| 14 | wiki | 10 | fail | fail |
| 15 | wiki | 5 | fail | fail |
| 16 | wiki | 5 | fail | fail |
| 17 | wiki | 7 | fail | fail |
| 18 | wiki | 6 | fail | fail |
| 19 | wiki | 7 | fail | fail |
| 20 | wiki | 6 | fail | fail |
| 21 | wiki | 3 | fail | fail |
| 22 | wiki | 4 | fail | fail |
| 23 | wiki | 2 | fail | fail |
| 24 | wiki | 2 | fail | fail |
| 25 | wiki | 3 | fail | pass |
| 26 | wiki | 2 | fail | pass |
| 27 | bamboohr | 1 | fail | fail |
| 28 | bamboohr | 1 | fail | fail |
| 29 | bamboohr | 1 | fail | fail |
| 30 | bamboohr | 1 | fail | fail |
| 31 | bamboohr | 1 | fail | fail |
| 32 | bamboohr | 1 | fail | fail |
| 33 | bamboohr | 1 | pass | pass |
| 34 | bamboohr | 1 | fail | fail |
| 35 | bamboohr | 1 | fail | fail |
| 36 | bamboohr | 1 | fail | fail |
| 37 | bamboohr | 1 | fail | fail |
| 38 | bamboohr | 1 | fail | fail |
| 39 | bamboohr | 1 | fail | fail |
| 40 | bamboohr | 1 | fail | fail |
| 41 | bamboohr | 1 | fail | fail |
| 42 | bamboohr | 1 | fail | fail |
| 43 | bamboohr | 1 | fail | fail |
| 44 | bamboohr | 1 | fail | fail |
| 45 | bamboohr | 1 | fail | fail |
| 46 | bamboohr | 1 | fail | fail |
| 47 | bamboohr | 1 | fail | fail |
| 48 | bamboohr | 1 | fail | fail |
| 49 | bamboohr | 1 | fail | fail |
| 50 | bamboohr | 1 | fail | fail |
| 51 | bamboohr | 1 | pass | pass |
| 52 | bamboohr | 1 | fail | fail |
| 53 | bamboohr | 1 | fail | fail |
| 54 | bamboohr | 1 | fail | fail |
| 55 | bamboohr | 1 | fail | fail |

G5, 09/21/2026: the platform scored 2 of 105, 1.9%; the archived bytes score 19 of 105, 18.1%
41 rows agree, 14 differ, 17 points
  wiki: rows 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 25, 26, every one of them read on the wiki target
  bamboohr rows: 29 of 29 agree, 27 of the agreements a fail on both readings
  wiki rows: 12 of 26 agree, 12 of the agreements a fail on both readings

Every BambooHR row agrees, including the two set rows that returned their metrics on the pane,
`{"wrong": 0, "employees": 44}` and `{"wrong": 0, "employees": 33}`. Those two are the only rows
in the set that a run which touched nothing can pass, and G5 touched four records outside the
schedule, so they are the rows the platform and the archive both read as passing.

Every wiki row that should have passed read fail, and the twelve wiki rows that agree agree
because G5's own arithmetic fails them on both readings, so they say nothing about the read. On
the pane every failing row printed `Metrics: {}` and an empty stdout box.

## What is measured

- The pasted code is the package's code. The export carries all 55 verifiers with their stored
  source, and each is byte for byte the row file in `qc/verifiers/` under a CRLF line ending,
  in the plan's order, row 1 at verifier index 0 through row 55 at index 54.
- The run created the page. G5's `wikijs_mcp_create_page` at call 402 carried the title
  `PTO Liability - 08/31/2026`, the path `pto-liability-08-31-2026` and `is_published: true`,
  and the app returned `{"success": true, "page_id": 11}`. All five runs created it under the
  exact title.
- Three ctx primitives are measured to work on a graded run: `list_tables`, `table_columns` and
  `query_db`. The BambooHR rows read the tables by content through those three and returned
  their metrics, so the harness serves them.
- Nothing measures `has_table`. It was the one primitive only the page rows read, on the first
  line of `_pages_table`, and an AttributeError there fails every wiki row and no BambooHR row,
  which is the shape of this grading exactly.
- The app the runs wrote to is `wiki_js_mcp`, and the app the wiki rows are grounded on is
  Wiki.js. Every wiki tool all five runs called carries the service prefix `wiki_js_mcp`,
  `wiki_js_mcp_wikijs_mcp_create_page` and `wiki_js_mcp_wikijs_mcp_get_page` among them, beside
  `bamboohr_bamboo_...` and `greenhouse_...` for the other two, and the platform is named
  `Ergon - bamboohr + greenhouse + wiki_js (MCP, auto)`. The Target database apps picker offers
  Wiki.js and Wiki.js MCP as two services, and the 26 wiki rows were pasted on Wiki.js, read off
  a screenshot of row 1 on 09/21/2026. The export carries two service ids,
  `svc_4a38acf9625d44b5a1aa6ba9fd6d1060` on the 26 wiki rows and
  `svc_24d85d95faa04fd7a5514dd1a227046a` on the 29 BambooHR rows, and names neither app, so the
  id itself cannot be resolved from the export; the tool prefixes can, and they say the pages
  the runs create live in the MCP service.

## What was done about it, 09/21/2026

The engine no longer reads `has_table`: `_pages_table` resolves the table from `list_tables`
alone, the three primitives the graded run measured. `qc/ctx.py` drops `has_table` with it, so
the stand-in carries the measured surface and nothing else, and a check that reaches for more
raises in the battery instead of on a graded run. A control plants the read back and the battery
goes red.

The engine also prints its notes now. The pane shows a verifier's stdout beside its metrics, and
the notes name the tables in the snapshot, the pages table, its column count and route, and the
reason each candidate row was taken or rejected. A page row that fails on the next grading will
say whether it saw a pages table at all and what it saw instead, which is the one thing this
grading could not tell us. The battery and the paste guide set `T2_VERIFIER_QUIET=1`, so 55 rows
over 73 snapshots stay readable.

Page rows now carry `page_rows` in their metrics, the number of rows in the pages table under
the title. On the pane that number alone separates a page the check could not reach, 0, from a
page it read and graded.

## The reading, 09/22/2026, after the pasted code was re-run here

Two candidates fit the shape, the primitive and the target app, and **neither is ruled out by
the score**, because both produce the same one: every wiki row fails on the first read and no
BambooHR row is touched.

The pasted code was run here against the archived G5 page, present and published, on two
stand-ins that differ in one method:

| The ctx | What the pasted code scores | Rows it passes |
|---|---|---|
| carries `has_table` | 19 of 105 | 1, 3 to 13, 25, 26, 33, 51 |
| does not carry `has_table` | **2 of 105** | **33, 51** |

The second line is the grading pane's own number and its own two rows. So the pasted code, on a
harness whose ctx has no `has_table`, reproduces the 09/21/2026 grading exactly, and row 1's
details in that case read `unexpected error: AttributeError: ... has no attribute 'has_table'`.
A verifier grounded on the wrong service reproduces the same 2 of 105 by a different route, and
its row 1 details read `no pages table in this snapshot: [...]` with the tables it was handed.

**The details string of one test run separates them, on the code already pasted**, because the
two cases cannot both print the same line:

- `AttributeError ... has_table` - the primitive. Switching the target app does not help; the 26
  wiki rows need the round-6 file, which reads the table from `list_tables` alone.
- `no pages table in this snapshot: [...]` - the service. The pasted code is sound as it stands
  and the 26 rows need Wiki.js MCP on Target database apps, nothing else.
- `table pages: 21 columns [...], 10 rows` then `no row of pages carries the title` - both are
  fine and this is the line the untouched task should give; the cause is then neither and the
  next grading's notes decide it.

## What is owed

- One test run of row 1 as pasted, read for the line above. It costs nothing, changes nothing,
  and it says whether the 26 rows need a new service or a new file.
- Then either the 26 wiki rows re-grounded on Wiki.js MCP, the service whose tools every run
  called, or the round-6 file pasted into them, and a re-grading. The next pane's `page_rows`
  metric and the `tables in the snapshot` line in its stdout box confirm it either way.
- The grading panes for G1 to G4, read back the same way. G1 and G3 moved records the schedule
  moves, so their BambooHR rows carry information G5's cannot: if their policy rows pass on the
  platform, the graded snapshot holds the run's writes and the wiki rows alone are unreached.
