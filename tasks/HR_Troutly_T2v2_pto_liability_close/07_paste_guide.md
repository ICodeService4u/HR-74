# 07 - the paste, row by row (T2, 09/20/2026)

The rubric import registers criteria, explanations, weights and criterion types and nothing else,
measured by task round 1. Everything below is what the interface still needs per row, generated
from the same rows that wrote `05_rubric_import.xlsx` (md5 `12b9c24b04a769ebbfa56ebfb032692d`, 27 rows, 143 points) by
`qc/write_paste_guide.py`, so a rebuild rewrites it and `check_docs()` holds it to the plan.

## The procedure

1. **Load the import** and count the rows Studio holds against 27. Read the import toast: a value
   outside a control's list is dropped with a warning, not an error.
2. **Structured view, per row**: set Tags and Reference Artifacts from the row's block below. The
   picker lists world files under `filesystem/` and the upload as `filesystem/pto_liability_request.pdf`;
   the app tables a block names are for the record and are not in the picker.
3. **Code verifier form, per row**: set Target app, Check type, Expected Content, Target Table,
   Target Record ID, Target Record Label and Fallback Strategy **DB only** from the block, leave
   Additional Notes empty, and paste the row file whole into the code box. Every row file is the
   engine with the row's SPEC on top, 326 to 329 lines; if the box balks at the size, say so and the
   builder stamps only the half a row uses. **Target database apps on a wiki row is `wiki_js_mcp`**,
   the service whose tools every archived run called, `wiki_js_mcp_wikijs_mcp_create_page` among
   them, and the picker offers Wiki.js and Wiki.js MCP as two entries. The 09/21/2026 paste took
   Wiki.js and every wiki row read fail on a page the app had returned under the exact title.
   Two causes fit that equally, the service and a ctx without `has_table`, and the row's own
   details line separates them: `no pages table in this snapshot` is the service, an
   `AttributeError` on `has_table` is a row file older than round 6. Select both services until
   a grading names the one that holds the pages table.
4. **Run the per-verifier test-run on the untouched task** and compare with the block's expected
   verdict and last `details` line. 27 rows fail on the untouched task by design, 0 on no page
   under the title and 0 on a BambooHR record as loaded or absent; the two guards over the records
   the schedule leaves as loaded, rows , pass. A verdict that differs is a defect to read before
   the next row is pasted.
5. **Paste rows 1, 2 first.** They are the two routes: the pages table and the BambooHR tables.
   Their `details` name every table and column the code resolved and the route it took, which is
   the measurement open item 4 in `02_task_metadata.md` owes, so copy those lines into the record.
6. If the form offers a dropdown for Target Table, pick the table the block names and record the
   names the dropdown lists; they are the live shape the fixture could not measure.

## One line per row

| # | Wt | Target app | Check type | Target Record ID | Expected Content | Test-run on the untouched task |
|---|---|---|---|---|---|---|
| 1 | 1 | wiki_js_mcp | Existence Check | PTO Liability - 08/31/2026 | one pages row titled PTO Liability - 08/31/2026 with isPublished true | FAILED |
| 2 | 10 | wiki_js_mcp | Content Match | PTO Liability - 08/31/2026 | $92,739.54, or $92,772.88 under posted rounding, within 0.5 | FAILED |
| 3 | 8 | wiki_js_mcp | Content Match | PTO Liability - 08/31/2026 | 1,522.17 hours, or 1,522.77 under posted rounding, within 0.05 | FAILED |
| 4 | 7 | wiki_js_mcp | Content Match | TRT-0005 | 64.62 hours, or 64.60 under posted rounding, within 0.005 | FAILED |
| 5 | 7 | wiki_js_mcp | Content Match | TRT-0009 | 64.62 hours, or 64.60 under posted rounding, within 0.005 | FAILED |
| 6 | 7 | wiki_js_mcp | Content Match | TRT-0012 | 18.46 hours, or 18.48 under posted rounding, within 0.005 | FAILED |
| 7 | 7 | wiki_js_mcp | Content Match | TRT-0018 | 60.00 hours, or 60.01 under posted rounding, within 0.005 | FAILED |
| 8 | 6 | wiki_js_mcp | Content Match | TRT-0021 | 42.46 hours, or 42.48 under posted rounding, within 0.005 | FAILED |
| 9 | 6 | wiki_js_mcp | Content Match | TRT-0014 | 58.46 hours, or 58.48 under posted rounding, within 0.005 | FAILED |
| 10 | 6 | wiki_js_mcp | Content Match | TRT-0023 | 58.46 hours, or 58.48 under posted rounding, within 0.005 | FAILED |
| 11 | 6 | wiki_js_mcp | Content Match | TRT-0031 | 26.46 hours, or 26.48 under posted rounding, within 0.005 | FAILED |
| 12 | 6 | wiki_js_mcp | Content Match | TRT-0029 | 50.46 hours, or 50.48 under posted rounding, within 0.005 | FAILED |
| 13 | 6 | wiki_js_mcp | Content Match | TRT-0040 | 58.46 hours, or 58.48 under posted rounding, within 0.005 | FAILED |
| 14 | 5 | wiki_js_mcp | Content Match | TRT-0071 | 51.87 hours, or 51.85 under posted rounding, within 0.005 | FAILED |
| 15 | 5 | wiki_js_mcp | Content Match | TRT-0051 | 6.71 hours, or 6.73 under posted rounding, within 0.005 | FAILED |
| 16 | 5 | wiki_js_mcp | Content Match | TRT-0079 | 24.96 hours, or 24.98 under posted rounding, within 0.005 | FAILED |
| 17 | 5 | wiki_js_mcp | Content Match | TRT-0058 | 40.96 hours, or 40.98 under posted rounding, within 0.005 | FAILED |
| 18 | 5 | wiki_js_mcp | Content Match | TRT-0083 | 18.71 hours, or 18.73 under posted rounding, within 0.005 | FAILED |
| 19 | 5 | wiki_js_mcp | Content Match | TRT-0153 | 6.15 hours, or 6.16 under posted rounding, within 0.005 | FAILED |
| 20 | 5 | wiki_js_mcp | Content Match | TRT-0153 | $44.2308 within 0.005 | FAILED |
| 21 | 4 | wiki_js_mcp | Content Match | TRT-0043 | 34.46 hours, or 34.48 under posted rounding, within 0.005 | FAILED |
| 22 | 4 | wiki_js_mcp | Content Match | TRT-0088 | $56.7308 within 0.005 | FAILED |
| 23 | 4 | wiki_js_mcp | Content Match | TRT-0155 | 3.08 hours under either rounding, within 0.005 | FAILED |
| 24 | 4 | wiki_js_mcp | Content Match | TRT-0155 | $27.0673 within 0.005 | FAILED |
| 25 | 3 | wiki_js_mcp | Content Match | TRT-0141 | 29.60 hours, or 29.59 under posted rounding, within 0.005 | FAILED |
| 26 | 3 | wiki_js_mcp | Content Match | TRT-0117 | $71.2500 within 0.005 | FAILED |
| 27 | 3 | wiki_js_mcp | Content Match | TRT-0096 | $29.3269 within 0.005 | FAILED |

## The rows

### Row 1, weight 1, Objective Compliance, paste first

States that a Wiki.js page titled PTO Liability - 08/31/2026 is published.

| Field | Value |
|---|---|
| Target app | `wiki_js_mcp` |
| Check type | Existence Check |
| Expected Content | one pages row titled PTO Liability - 08/31/2026 with isPublished true |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | PTO Liability - 08/31/2026 |
| Target Record Label | PTO Liability - 08/31/2026 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); wiki_js/Page.csv (app table, not in the picker) |
| Code | `qc/verifiers/row01_states_that_a_wiki_js_page_titled_pto_liability.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 2, weight 10, Expert Assessment, primary, paste first

States, on the PTO liability page, a total dollar liability of $92,739.54.

| Field | Value |
|---|---|
| Target app | `wiki_js_mcp` |
| Check type | Content Match |
| Expected Content | $92,739.54, or $92,772.88 under posted rounding, within 0.5 |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | PTO Liability - 08/31/2026 |
| Target Record Label | PTO Liability - 08/31/2026 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Policies/Employee_Handbook_v3.pdf (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); filesystem/HR/Data/2026-08-31_Master_Employee_Roster.xlsx (world); filesystem/HR/Payroll/2026-06-25_Payroll_Procedures_Memo.docx (world); filesystem/HR/Comp/Promotions/2026-06-10_Promotion_Approval_TRT-0088.docx (world); filesystem/HR/Comp/Amendments/2026-05-12_Comp_Amendment_TRT-0117.pdf (world); filesystem/HR/People/Offer_Letters/Historical_Offer_Letters_2020-2026.pdf (world); filesystem/HR/Benefits/2026-08-10_Schedule_Change_TRT-0141.pdf (world) |
| Code | `qc/verifiers/row02_states_on_the_pto_liability_page_a_total_dollar.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 3, weight 8, Expert Assessment, primary

States, on the PTO liability page, total PTO hours of 1,522.17.

| Field | Value |
|---|---|
| Target app | `wiki_js_mcp` |
| Check type | Content Match |
| Expected Content | 1,522.17 hours, or 1,522.77 under posted rounding, within 0.05 |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | PTO Liability - 08/31/2026 |
| Target Record Label | PTO Liability - 08/31/2026 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); filesystem/HR/Data/2026-08-31_Master_Employee_Roster.xlsx (world); filesystem/HR/Payroll/2026-06-25_Payroll_Procedures_Memo.docx (world); filesystem/HR/Data/HRIS_Time_Off_Report_2026-08-31.xlsx (world) |
| Code | `qc/verifiers/row03_states_on_the_pto_liability_page_total_pto_hours.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 4, weight 7, Expert Assessment, primary

States, on the PTO liability page, a balance of 64.62 hours for Mikelle Hosana, TRT-0005.

| Field | Value |
|---|---|
| Target app | `wiki_js_mcp` |
| Check type | Content Match |
| Expected Content | 64.62 hours, or 64.60 under posted rounding, within 0.005 |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | TRT-0005 |
| Target Record Label | Mikelle Hosana, TRT-0005 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Data/HRIS_Time_Off_Report_2026-08-31.xlsx (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Payroll/2026-06-25_Payroll_Procedures_Memo.docx (world) |
| Code | `qc/verifiers/row04_states_on_the_pto_liability_page_a_balance_of_64.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 5, weight 7, Expert Assessment, primary

States, on the PTO liability page, a balance of 64.62 hours for Krystale Jumawan, TRT-0009.

| Field | Value |
|---|---|
| Target app | `wiki_js_mcp` |
| Check type | Content Match |
| Expected Content | 64.62 hours, or 64.60 under posted rounding, within 0.005 |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | TRT-0009 |
| Target Record Label | Krystale Jumawan, TRT-0009 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Data/HRIS_Time_Off_Report_2026-08-31.xlsx (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Payroll/2026-06-25_Payroll_Procedures_Memo.docx (world) |
| Code | `qc/verifiers/row05_states_on_the_pto_liability_page_a_balance_of_64.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 6, weight 7, Expert Assessment, primary

States, on the PTO liability page, a balance of 18.46 hours for Jessica Ko, TRT-0012.

| Field | Value |
|---|---|
| Target app | `wiki_js_mcp` |
| Check type | Content Match |
| Expected Content | 18.46 hours, or 18.48 under posted rounding, within 0.005 |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | TRT-0012 |
| Target Record Label | Jessica Ko, TRT-0012 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Data/HRIS_Time_Off_Report_2026-08-31.xlsx (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Payroll/2026-06-25_Payroll_Procedures_Memo.docx (world) |
| Code | `qc/verifiers/row06_states_on_the_pto_liability_page_a_balance_of_18.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 7, weight 7, Expert Assessment, primary

States, on the PTO liability page, a balance of 60.00 hours for Marisela Thornbury, TRT-0018.

| Field | Value |
|---|---|
| Target app | `wiki_js_mcp` |
| Check type | Content Match |
| Expected Content | 60.00 hours, or 60.01 under posted rounding, within 0.005 |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | TRT-0018 |
| Target Record Label | Marisela Thornbury, TRT-0018 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Payroll/2026-06-25_Payroll_Procedures_Memo.docx (world); filesystem/HR/Data/HRIS_Time_Off_Report_2026-08-31.xlsx (world) |
| Code | `qc/verifiers/row07_states_on_the_pto_liability_page_a_balance_of_60.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 8, weight 6, Expert Assessment, primary

States, on the PTO liability page, a balance of 42.46 hours for Edith Bustamante, TRT-0021.

| Field | Value |
|---|---|
| Target app | `wiki_js_mcp` |
| Check type | Content Match |
| Expected Content | 42.46 hours, or 42.48 under posted rounding, within 0.005 |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | TRT-0021 |
| Target Record Label | Edith Bustamante, TRT-0021 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Data/HRIS_Time_Off_Report_2026-08-31.xlsx (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Payroll/2026-06-25_Payroll_Procedures_Memo.docx (world) |
| Code | `qc/verifiers/row08_states_on_the_pto_liability_page_a_balance_of_42.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 9, weight 6, Expert Assessment, primary

States, on the PTO liability page, a balance of 58.46 hours for Rohan Iyer, TRT-0014.

| Field | Value |
|---|---|
| Target app | `wiki_js_mcp` |
| Check type | Content Match |
| Expected Content | 58.46 hours, or 58.48 under posted rounding, within 0.005 |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | TRT-0014 |
| Target Record Label | Rohan Iyer, TRT-0014 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Data/HRIS_Time_Off_Report_2026-08-31.xlsx (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Payroll/2026-06-25_Payroll_Procedures_Memo.docx (world) |
| Code | `qc/verifiers/row09_states_on_the_pto_liability_page_a_balance_of_58.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 10, weight 6, Expert Assessment, primary

States, on the PTO liability page, a balance of 58.46 hours for Maeve Oyinlola, TRT-0023.

| Field | Value |
|---|---|
| Target app | `wiki_js_mcp` |
| Check type | Content Match |
| Expected Content | 58.46 hours, or 58.48 under posted rounding, within 0.005 |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | TRT-0023 |
| Target Record Label | Maeve Oyinlola, TRT-0023 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Data/HRIS_Time_Off_Report_2026-08-31.xlsx (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Payroll/2026-06-25_Payroll_Procedures_Memo.docx (world) |
| Code | `qc/verifiers/row10_states_on_the_pto_liability_page_a_balance_of_58.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 11, weight 6, Expert Assessment, primary

States, on the PTO liability page, a balance of 26.46 hours for Zephyr Adebayo, TRT-0031.

| Field | Value |
|---|---|
| Target app | `wiki_js_mcp` |
| Check type | Content Match |
| Expected Content | 26.46 hours, or 26.48 under posted rounding, within 0.005 |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | TRT-0031 |
| Target Record Label | Zephyr Adebayo, TRT-0031 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Data/HRIS_Time_Off_Report_2026-08-31.xlsx (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Payroll/2026-06-25_Payroll_Procedures_Memo.docx (world) |
| Code | `qc/verifiers/row11_states_on_the_pto_liability_page_a_balance_of_26.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 12, weight 6, Expert Assessment, primary

States, on the PTO liability page, a balance of 50.46 hours for Emeka Thorsen, TRT-0029.

| Field | Value |
|---|---|
| Target app | `wiki_js_mcp` |
| Check type | Content Match |
| Expected Content | 50.46 hours, or 50.48 under posted rounding, within 0.005 |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | TRT-0029 |
| Target Record Label | Emeka Thorsen, TRT-0029 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Data/HRIS_Time_Off_Report_2026-08-31.xlsx (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Payroll/2026-06-25_Payroll_Procedures_Memo.docx (world) |
| Code | `qc/verifiers/row12_states_on_the_pto_liability_page_a_balance_of_50.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 13, weight 6, Expert Assessment, primary

States, on the PTO liability page, a balance of 58.46 hours for Ilse Van der Kolk, TRT-0040.

| Field | Value |
|---|---|
| Target app | `wiki_js_mcp` |
| Check type | Content Match |
| Expected Content | 58.46 hours, or 58.48 under posted rounding, within 0.005 |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | TRT-0040 |
| Target Record Label | Ilse Van der Kolk, TRT-0040 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Data/HRIS_Time_Off_Report_2026-08-31.xlsx (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Payroll/2026-06-25_Payroll_Procedures_Memo.docx (world) |
| Code | `qc/verifiers/row13_states_on_the_pto_liability_page_a_balance_of_58.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 14, weight 5, Expert Assessment, primary

States, on the PTO liability page, a balance of 51.87 hours for Samuel Burkenham, TRT-0071.

| Field | Value |
|---|---|
| Target app | `wiki_js_mcp` |
| Check type | Content Match |
| Expected Content | 51.87 hours, or 51.85 under posted rounding, within 0.005 |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | TRT-0071 |
| Target Record Label | Samuel Burkenham, TRT-0071 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); filesystem/HR/Policies/Employee_Handbook_v3.pdf (world); filesystem/HR/People/Offer_Letters/2024-04-08_Rehire_Offer_TRT-0071.pdf (world); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Data/HRIS_Time_Off_Report_2026-08-31.xlsx (world) |
| Code | `qc/verifiers/row14_states_on_the_pto_liability_page_a_balance_of_51.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 15, weight 5, Expert Assessment, primary

States, on the PTO liability page, a balance of 6.71 hours for Priyamvada Raghunath, TRT-0051.

| Field | Value |
|---|---|
| Target app | `wiki_js_mcp` |
| Check type | Content Match |
| Expected Content | 6.71 hours, or 6.73 under posted rounding, within 0.005 |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | TRT-0051 |
| Target Record Label | Priyamvada Raghunath, TRT-0051 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); bamboohr/Employee.csv (app table, not in the picker); filesystem/HR/Data/HRIS_Time_Off_Report_2026-08-31.xlsx (world) |
| Code | `qc/verifiers/row15_states_on_the_pto_liability_page_a_balance_of_6.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 16, weight 5, Expert Assessment, primary

States, on the PTO liability page, a balance of 24.96 hours for Wren Takahashi-Bell, TRT-0079.

| Field | Value |
|---|---|
| Target app | `wiki_js_mcp` |
| Check type | Content Match |
| Expected Content | 24.96 hours, or 24.98 under posted rounding, within 0.005 |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | TRT-0079 |
| Target Record Label | Wren Takahashi-Bell, TRT-0079 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); bamboohr/Employee.csv (app table, not in the picker); filesystem/HR/Data/HRIS_Time_Off_Report_2026-08-31.xlsx (world) |
| Code | `qc/verifiers/row16_states_on_the_pto_liability_page_a_balance_of_24.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 17, weight 5, Expert Assessment, primary

States, on the PTO liability page, a balance of 40.96 hours for Callum Oyelaran, TRT-0058.

| Field | Value |
|---|---|
| Target app | `wiki_js_mcp` |
| Check type | Content Match |
| Expected Content | 40.96 hours, or 40.98 under posted rounding, within 0.005 |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | TRT-0058 |
| Target Record Label | Callum Oyelaran, TRT-0058 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); bamboohr/Employee.csv (app table, not in the picker); filesystem/HR/Data/HRIS_Time_Off_Report_2026-08-31.xlsx (world) |
| Code | `qc/verifiers/row17_states_on_the_pto_liability_page_a_balance_of_40.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 18, weight 5, Expert Assessment, primary

States, on the PTO liability page, a balance of 18.71 hours for Desmond Achterberg, TRT-0083.

| Field | Value |
|---|---|
| Target app | `wiki_js_mcp` |
| Check type | Content Match |
| Expected Content | 18.71 hours, or 18.73 under posted rounding, within 0.005 |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | TRT-0083 |
| Target Record Label | Desmond Achterberg, TRT-0083 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); bamboohr/Employee.csv (app table, not in the picker); filesystem/HR/Data/HRIS_Time_Off_Report_2026-08-31.xlsx (world) |
| Code | `qc/verifiers/row18_states_on_the_pto_liability_page_a_balance_of_18.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 19, weight 5, Expert Assessment, primary

States, on the PTO liability page, a balance of 6.15 hours for Simone Okonkwo, TRT-0153.

| Field | Value |
|---|---|
| Target app | `wiki_js_mcp` |
| Check type | Content Match |
| Expected Content | 6.15 hours, or 6.16 under posted rounding, within 0.005 |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | TRT-0153 |
| Target Record Label | Simone Okonkwo, TRT-0153 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Data/2026-08-31_Master_Employee_Roster.xlsx (world); filesystem/HR/Data/2026-08-28_Employee_ID_Crosswalk.xlsx (world); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Payroll/2026-06-25_Payroll_Procedures_Memo.docx (world) |
| Code | `qc/verifiers/row19_states_on_the_pto_liability_page_a_balance_of_6.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 20, weight 5, Expert Assessment, primary

States, on the PTO liability page, an hourly rate of $44.2308 for Simone Okonkwo, TRT-0153.

| Field | Value |
|---|---|
| Target app | `wiki_js_mcp` |
| Check type | Content Match |
| Expected Content | $44.2308 within 0.005 |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | TRT-0153 |
| Target Record Label | Simone Okonkwo, TRT-0153 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Data/2026-08-31_Master_Employee_Roster.xlsx (world); filesystem/HR/Data/2026-08-28_Employee_ID_Crosswalk.xlsx (world); filesystem/Recruiting/Offers/2026-07-02_Offer_TRT-0153_SIGNED.pdf (world); bamboohr/Employee.csv (app table, not in the picker) |
| Code | `qc/verifiers/row20_states_on_the_pto_liability_page_an_hourly_rate.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 21, weight 4, Expert Assessment, primary

States, on the PTO liability page, a balance of 34.46 hours for Oren Kastellanos, TRT-0043.

| Field | Value |
|---|---|
| Target app | `wiki_js_mcp` |
| Check type | Content Match |
| Expected Content | 34.46 hours, or 34.48 under posted rounding, within 0.005 |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | TRT-0043 |
| Target Record Label | Oren Kastellanos, TRT-0043 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Data/HRIS_Time_Off_Report_2026-08-31.xlsx (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Payroll/2026-06-25_Payroll_Procedures_Memo.docx (world) |
| Code | `qc/verifiers/row21_states_on_the_pto_liability_page_a_balance_of_34.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 22, weight 4, Expert Assessment, primary

States, on the PTO liability page, an hourly rate of $56.7308 for Yolanda Featherstone, TRT-0088.

| Field | Value |
|---|---|
| Target app | `wiki_js_mcp` |
| Check type | Content Match |
| Expected Content | $56.7308 within 0.005 |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | TRT-0088 |
| Target Record Label | Yolanda Featherstone, TRT-0088 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Comp/Promotions/2026-06-10_Promotion_Approval_TRT-0088.docx (world); filesystem/HR/Policies/Employee_Handbook_v3.pdf (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); bamboohr/Employee.csv (app table, not in the picker) |
| Code | `qc/verifiers/row22_states_on_the_pto_liability_page_an_hourly_rate.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 23, weight 4, Expert Assessment, primary

States, on the PTO liability page, a balance of 3.08 hours for Rafael Ibarra, TRT-0155.

| Field | Value |
|---|---|
| Target app | `wiki_js_mcp` |
| Check type | Content Match |
| Expected Content | 3.08 hours under either rounding, within 0.005 |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | TRT-0155 |
| Target Record Label | Rafael Ibarra, TRT-0155 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Data/2026-08-31_Master_Employee_Roster.xlsx (world); filesystem/HR/Data/2026-08-28_Employee_ID_Crosswalk.xlsx (world); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Payroll/2026-06-25_Payroll_Procedures_Memo.docx (world) |
| Code | `qc/verifiers/row23_states_on_the_pto_liability_page_a_balance_of_3.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 24, weight 4, Expert Assessment, primary

States, on the PTO liability page, an hourly rate of $27.0673 for Rafael Ibarra, TRT-0155.

| Field | Value |
|---|---|
| Target app | `wiki_js_mcp` |
| Check type | Content Match |
| Expected Content | $27.0673 within 0.005 |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | TRT-0155 |
| Target Record Label | Rafael Ibarra, TRT-0155 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Data/2026-08-31_Master_Employee_Roster.xlsx (world); filesystem/HR/Data/2026-08-28_Employee_ID_Crosswalk.xlsx (world); filesystem/HR/People/Offer_Letters/Historical_Offer_Letters_2020-2026.pdf (world); bamboohr/Employee.csv (app table, not in the picker) |
| Code | `qc/verifiers/row24_states_on_the_pto_liability_page_an_hourly_rate.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 25, weight 3, Expert Assessment, primary

States, on the PTO liability page, a balance of 29.60 hours for Beatriz Quintanilla, TRT-0141.

| Field | Value |
|---|---|
| Target app | `wiki_js_mcp` |
| Check type | Content Match |
| Expected Content | 29.60 hours, or 29.59 under posted rounding, within 0.005 |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | TRT-0141 |
| Target Record Label | Beatriz Quintanilla, TRT-0141 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Benefits/2026-08-10_Schedule_Change_TRT-0141.pdf (world); filesystem/HR/Policies/Employee_Handbook_v3.pdf (world); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Data/HRIS_Time_Off_Report_2026-08-31.xlsx (world) |
| Code | `qc/verifiers/row25_states_on_the_pto_liability_page_a_balance_of_29.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 26, weight 3, Expert Assessment, primary

States, on the PTO liability page, an hourly rate of $71.2500 for Belaviv Luk, TRT-0117.

| Field | Value |
|---|---|
| Target app | `wiki_js_mcp` |
| Check type | Content Match |
| Expected Content | $71.2500 within 0.005 |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | TRT-0117 |
| Target Record Label | Belaviv Luk, TRT-0117 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Comp/Amendments/2026-05-12_Comp_Amendment_TRT-0117.pdf (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); filesystem/HR/Policies/Employee_Handbook_v3.pdf (world); bamboohr/Employee.csv (app table, not in the picker) |
| Code | `qc/verifiers/row26_states_on_the_pto_liability_page_an_hourly_rate.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 27, weight 3, Expert Assessment, primary

States, on the PTO liability page, an hourly rate of $29.3269 for Delphine Marchetti, TRT-0096.

| Field | Value |
|---|---|
| Target app | `wiki_js_mcp` |
| Check type | Content Match |
| Expected Content | $29.3269 within 0.005 |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | TRT-0096 |
| Target Record Label | Delphine Marchetti, TRT-0096 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/People/Offer_Letters/Historical_Offer_Letters_2020-2026.pdf (world); filesystem/HR/Policies/Employee_Handbook_v3.pdf (world); bamboohr/Employee.csv (app table, not in the picker) |
| Code | `qc/verifiers/row27_states_on_the_pto_liability_page_an_hourly_rate.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |
