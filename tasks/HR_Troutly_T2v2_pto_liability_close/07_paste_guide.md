# 07 - the paste, row by row (T2 v2, 09/22/2026)

The rubric import registers criteria, explanations, weights and criterion types and nothing else,
measured by task round 1. Everything below is what the interface still needs per row, generated
from the same rows that wrote `05_rubric_import.xlsx` (md5 `923fcbdd7bdf474a702e26c5e6142039`, 13 rows, 79 points) by
`qc/write_paste_guide.py`, so a rebuild rewrites it and `check_docs()` holds it to the plan.

## The procedure

1. **Load the import** and count the rows Studio holds against 13. Read the import toast: a value
   outside a control's list is dropped with a warning, not an error.
2. **Structured view, per row**: set Tags and Reference Artifacts from the row's block below. The
   picker lists world files under `filesystem/` and the upload as `filesystem/pto_liability_request.pdf`;
   the app tables a block names are for the record and are not in the picker.
3. **Code verifier form, per row**: set Target app, Check type, Expected Content, Target Table,
   Target Record ID, Target Record Label and Fallback Strategy **DB only** from the block, leave
   Additional Notes empty, and paste the row file whole into the code box. Every row file is the
   engine with the row's SPEC on top, 381 to 384 lines; if the box balks at the size, say so and the
   builder stamps only the half a row uses. **Target database apps on a wiki row is `wiki_js_mcp`**,
   the service whose tools every archived run called, `wiki_js_mcp_wikijs_mcp_create_page` among
   them, and the picker offers Wiki.js and Wiki.js MCP as two entries. The 09/21/2026 paste took
   Wiki.js and every wiki row read fail on a page the app had returned under the exact title.
   Two causes fit that equally, the service and a ctx without `has_table`, and the row's own
   details line separates them: `no pages table in this snapshot` is the service, an
   `AttributeError` on `has_table` is a row file older than round 6. Select both services until
   a grading names the one that holds the pages table.
4. **Run the per-verifier test-run on the untouched task** and compare with the block's expected
   verdict and last `details` line. 13 of 13 rows fail on the untouched task by design, every one
   on no page under the title. A row that passes there, or fails on anything else, is a defect to
   read before the next row is pasted.
5. **Paste rows 1 and 2 first.** Row 1 proves the route to the pages table and the gate proves the
   reader every other row leans on. Their `details` name every table and column the code resolved
   and the route it took, which is the measurement open item 3 in `02_task_metadata.md` owes, so
   copy those lines into the record.
6. If the form offers a dropdown for Target Table, pick the table the block names and record the
   names the dropdown lists; they are the live shape the fixture could not measure.

## One line per row

| # | Wt | Target app | Check type | Target Record ID | Expected Content | Test-run on the untouched task |
|---|---|---|---|---|---|---|
| 1 | 1 | wiki_js_mcp | Existence Check | PTO Liability - 08/31/2026 | one pages row titled PTO Liability - 08/31/2026 with isPublished true | FAILED |
| 2 | 10 | wiki_js_mcp | Content Match | PTO Liability - 08/31/2026 | $92,739.54, or $92,772.88 under posted rounding, within 0.5 | FAILED |
| 3 | 8 | wiki_js_mcp | Content Match | PTO Liability - 08/31/2026 | 1,522.17 hours, or 1,522.77 under posted rounding, within 0.05 | FAILED |
| 4 | 6 | wiki_js_mcp | Content Match | PTO Liability - 08/31/2026 | 297.79 hours on the Customer Success line, or 297.93 under posted rounding, within 0.05 | FAILED |
| 5 | 6 | wiki_js_mcp | Content Match | PTO Liability - 08/31/2026 | $12,627.20 on the Customer Success line, or $12,633.97 under posted rounding, within 0.5 | FAILED |
| 6 | 7 | wiki_js_mcp | Content Match | PTO Liability - 08/31/2026 | 558.31 hours on the Engineering line, or 558.56 under posted rounding, within 0.05 | FAILED |
| 7 | 7 | wiki_js_mcp | Content Match | PTO Liability - 08/31/2026 | $41,542.16 on the Engineering line, or $41,558.43 under posted rounding, within 0.5 | FAILED |
| 8 | 7 | wiki_js_mcp | Content Match | PTO Liability - 08/31/2026 | 121.53 hours on the Finance and Corporate line, or 121.51 under posted rounding, within 0.05 | FAILED |
| 9 | 7 | wiki_js_mcp | Content Match | PTO Liability - 08/31/2026 | $8,187.68 on the Finance and Corporate line, or $8,185.08 under posted rounding, within 0.5 | FAILED |
| 10 | 3 | wiki_js_mcp | Content Match | PTO Liability - 08/31/2026 | 170.50 hours on the Product line, or 170.54 under posted rounding, within 0.05 | FAILED |
| 11 | 3 | wiki_js_mcp | Content Match | PTO Liability - 08/31/2026 | $10,984.34 on the Product line, or $10,987.86 under posted rounding, within 0.5 | FAILED |
| 12 | 7 | wiki_js_mcp | Content Match | PTO Liability - 08/31/2026 | 374.04 hours on the Sales and Marketing line, or 374.23 under posted rounding, within 0.05 | FAILED |
| 13 | 7 | wiki_js_mcp | Content Match | PTO Liability - 08/31/2026 | $19,398.16 on the Sales and Marketing line, or $19,407.54 under posted rounding, within 0.5 | FAILED |

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

### Row 4, weight 6, Expert Assessment, primary

States, on the PTO liability page, PTO hours of 297.79 for Customer Success.

| Field | Value |
|---|---|
| Target app | `wiki_js_mcp` |
| Check type | Content Match |
| Expected Content | 297.79 hours on the Customer Success line, or 297.93 under posted rounding, within 0.05 |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | PTO Liability - 08/31/2026 |
| Target Record Label | the Customer Success line on PTO Liability - 08/31/2026 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); filesystem/HR/Policies/Employee_Handbook_v3.pdf (world); filesystem/HR/Benefits/2026-08-10_Schedule_Change_TRT-0141.pdf (world); filesystem/HR/Data/2026-08-31_Master_Employee_Roster.xlsx (world); filesystem/HR/Data/2026-08-28_Employee_ID_Crosswalk.xlsx (world); filesystem/HR/Data/HRIS_Time_Off_Report_2026-08-31.xlsx (world) |
| Code | `qc/verifiers/row04_states_on_the_pto_liability_page_pto_hours_of_29.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 5, weight 6, Expert Assessment, primary

States, on the PTO liability page, a PTO liability of $12,627.20 for Customer Success.

| Field | Value |
|---|---|
| Target app | `wiki_js_mcp` |
| Check type | Content Match |
| Expected Content | $12,627.20 on the Customer Success line, or $12,633.97 under posted rounding, within 0.5 |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | PTO Liability - 08/31/2026 |
| Target Record Label | the Customer Success line on PTO Liability - 08/31/2026 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Comp/Promotions/2026-06-10_Promotion_Approval_TRT-0088.docx (world); filesystem/HR/Policies/Employee_Handbook_v3.pdf (world); filesystem/HR/People/Offer_Letters/Historical_Offer_Letters_2020-2026.pdf (world); filesystem/HR/Data/2026-08-31_Master_Employee_Roster.xlsx (world); filesystem/Recruiting/Offers/2026-07-02_Offer_TRT-0153_SIGNED.pdf (world); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); bamboohr/Employee.csv (app table, not in the picker) |
| Code | `qc/verifiers/row05_states_on_the_pto_liability_page_a_pto_liability.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 6, weight 7, Expert Assessment, primary

States, on the PTO liability page, PTO hours of 558.31 for Engineering.

| Field | Value |
|---|---|
| Target app | `wiki_js_mcp` |
| Check type | Content Match |
| Expected Content | 558.31 hours on the Engineering line, or 558.56 under posted rounding, within 0.05 |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | PTO Liability - 08/31/2026 |
| Target Record Label | the Engineering line on PTO Liability - 08/31/2026 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); filesystem/HR/Payroll/2026-06-25_Payroll_Procedures_Memo.docx (world); filesystem/HR/Data/HRIS_Time_Off_Report_2026-08-31.xlsx (world) |
| Code | `qc/verifiers/row06_states_on_the_pto_liability_page_pto_hours_of_55.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 7, weight 7, Expert Assessment, primary

States, on the PTO liability page, a PTO liability of $41,542.16 for Engineering.

| Field | Value |
|---|---|
| Target app | `wiki_js_mcp` |
| Check type | Content Match |
| Expected Content | $41,542.16 on the Engineering line, or $41,558.43 under posted rounding, within 0.5 |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | PTO Liability - 08/31/2026 |
| Target Record Label | the Engineering line on PTO Liability - 08/31/2026 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Comp/Amendments/2026-05-12_Comp_Amendment_TRT-0117.pdf (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); bamboohr/Employee.csv (app table, not in the picker) |
| Code | `qc/verifiers/row07_states_on_the_pto_liability_page_a_pto_liability.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 8, weight 7, Expert Assessment, primary

States, on the PTO liability page, PTO hours of 121.53 for Finance and Corporate.

| Field | Value |
|---|---|
| Target app | `wiki_js_mcp` |
| Check type | Content Match |
| Expected Content | 121.53 hours on the Finance and Corporate line, or 121.51 under posted rounding, within 0.05 |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | PTO Liability - 08/31/2026 |
| Target Record Label | the Finance and Corporate line on PTO Liability - 08/31/2026 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); filesystem/HR/Data/HRIS_Time_Off_Report_2026-08-31.xlsx (world) |
| Code | `qc/verifiers/row08_states_on_the_pto_liability_page_pto_hours_of_12.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 9, weight 7, Expert Assessment, primary

States, on the PTO liability page, a PTO liability of $8,187.68 for Finance and Corporate.

| Field | Value |
|---|---|
| Target app | `wiki_js_mcp` |
| Check type | Content Match |
| Expected Content | $8,187.68 on the Finance and Corporate line, or $8,185.08 under posted rounding, within 0.5 |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | PTO Liability - 08/31/2026 |
| Target Record Label | the Finance and Corporate line on PTO Liability - 08/31/2026 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); filesystem/HR/Data/2026-08-31_Master_Employee_Roster.xlsx (world); bamboohr/Employee.csv (app table, not in the picker) |
| Code | `qc/verifiers/row09_states_on_the_pto_liability_page_a_pto_liability.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 10, weight 3, Expert Assessment, primary

States, on the PTO liability page, PTO hours of 170.50 for Product.

| Field | Value |
|---|---|
| Target app | `wiki_js_mcp` |
| Check type | Content Match |
| Expected Content | 170.50 hours on the Product line, or 170.54 under posted rounding, within 0.05 |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | PTO Liability - 08/31/2026 |
| Target Record Label | the Product line on PTO Liability - 08/31/2026 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Policies/Employee_Handbook_v3.pdf (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); filesystem/HR/People/Offer_Letters/2024-04-08_Rehire_Offer_TRT-0071.pdf (world); filesystem/HR/Data/HRIS_Time_Off_Report_2026-08-31.xlsx (world) |
| Code | `qc/verifiers/row10_states_on_the_pto_liability_page_pto_hours_of_17.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 11, weight 3, Expert Assessment, primary

States, on the PTO liability page, a PTO liability of $10,984.34 for Product.

| Field | Value |
|---|---|
| Target app | `wiki_js_mcp` |
| Check type | Content Match |
| Expected Content | $10,984.34 on the Product line, or $10,987.86 under posted rounding, within 0.5 |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | PTO Liability - 08/31/2026 |
| Target Record Label | the Product line on PTO Liability - 08/31/2026 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Policies/Employee_Handbook_v3.pdf (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); filesystem/HR/People/Offer_Letters/2024-04-08_Rehire_Offer_TRT-0071.pdf (world); filesystem/HR/Data/2026-08-31_Master_Employee_Roster.xlsx (world); bamboohr/Employee.csv (app table, not in the picker) |
| Code | `qc/verifiers/row11_states_on_the_pto_liability_page_a_pto_liability.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 12, weight 7, Expert Assessment, primary

States, on the PTO liability page, PTO hours of 374.04 for Sales and Marketing.

| Field | Value |
|---|---|
| Target app | `wiki_js_mcp` |
| Check type | Content Match |
| Expected Content | 374.04 hours on the Sales and Marketing line, or 374.23 under posted rounding, within 0.05 |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | PTO Liability - 08/31/2026 |
| Target Record Label | the Sales and Marketing line on PTO Liability - 08/31/2026 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); filesystem/HR/Payroll/2026-06-25_Payroll_Procedures_Memo.docx (world); filesystem/HR/Data/2026-08-31_Master_Employee_Roster.xlsx (world); filesystem/HR/Data/2026-08-28_Employee_ID_Crosswalk.xlsx (world); filesystem/HR/Data/HRIS_Time_Off_Report_2026-08-31.xlsx (world) |
| Code | `qc/verifiers/row12_states_on_the_pto_liability_page_pto_hours_of_37.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 13, weight 7, Expert Assessment, primary

States, on the PTO liability page, a PTO liability of $19,398.16 for Sales and Marketing.

| Field | Value |
|---|---|
| Target app | `wiki_js_mcp` |
| Check type | Content Match |
| Expected Content | $19,398.16 on the Sales and Marketing line, or $19,407.54 under posted rounding, within 0.5 |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | PTO Liability - 08/31/2026 |
| Target Record Label | the Sales and Marketing line on PTO Liability - 08/31/2026 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Data/2026-08-31_Master_Employee_Roster.xlsx (world); filesystem/HR/Data/2026-08-28_Employee_ID_Crosswalk.xlsx (world); filesystem/HR/People/Offer_Letters/Historical_Offer_Letters_2020-2026.pdf (world); bamboohr/Employee.csv (app table, not in the picker) |
| Code | `qc/verifiers/row13_states_on_the_pto_liability_page_a_pto_liability.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |
