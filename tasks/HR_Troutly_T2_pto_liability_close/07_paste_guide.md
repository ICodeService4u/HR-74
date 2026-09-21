# 07 - the paste, row by row (T2, 09/20/2026)

The rubric import registers criteria, explanations, weights and criterion types and nothing else,
measured by task round 1. Everything below is what the interface still needs per row, generated
from the same rows that wrote `05_rubric_import.xlsx` (md5 `132b10edfb5f835facbb529522427bb8`, 55 rows, 105 points) by
`qc/write_paste_guide.py`, so a rebuild rewrites it and `check_docs()` holds it to the plan.

## The procedure

1. **Load the import** and count the rows Studio holds against 55. Read the import toast: a value
   outside a control's list is dropped with a warning, not an error.
2. **Structured view, per row**: set Tags and Reference Artifacts from the row's block below. The
   picker lists world files under `filesystem/` and the upload as `filesystem/pto_liability_request.pdf`;
   the app tables a block names are for the record and are not in the picker.
3. **Code verifier form, per row**: set Target app, Check type, Expected Content, Target Table,
   Target Record ID, Target Record Label and Fallback Strategy **DB only** from the block, leave
   Additional Notes empty, and paste the row file whole into the code box. Every row file is the
   engine with the row's SPEC on top, 761 to 814 lines; if the box balks at the size, say so and the
   builder stamps only the half a row uses.
4. **Run the per-verifier test-run on the untouched task** and compare with the block's expected
   verdict and last `details` line. 53 rows fail on the untouched task by design, 26 on no page
   under the title and 27 on a BambooHR record as loaded or absent; the two guards over the records
   the schedule leaves as loaded, rows 33, 51, pass. A verdict that differs is a defect to read before
   the next row is pasted.
5. **Paste rows 1, 33 first.** They are the two routes: the pages table and the BambooHR tables.
   Their `details` name every table and column the code resolved and the route it took, which is
   the measurement open item 4 in `02_task_metadata.md` owes, so copy those lines into the record.
6. If the form offers a dropdown for Target Table, pick the table the block names and record the
   names the dropdown lists; they are the live shape the fixture could not measure.

## One line per row

| # | Wt | Target app | Check type | Target Record ID | Expected Content | Test-run on the untouched task |
|---|---|---|---|---|---|---|
| 1 | 1 | wiki_js | Existence Check | PTO Liability - 08/31/2026 | one pages row titled PTO Liability - 08/31/2026 with isPublished true | FAILED |
| 2 | 2 | wiki_js | Count Check | PTO Liability - 08/31/2026 | an employee row keyed on each of the roster's 52 IDs | FAILED |
| 3 | 1 | wiki_js | Content Match | PTO Liability - 08/31/2026 | every balance 0.00 | FAILED |
| 4 | 1 | wiki_js | Content Match | PTO Liability - 08/31/2026 | every rate 0.0000 | FAILED |
| 5 | 1 | wiki_js | Content Match | PTO Liability - 08/31/2026 | every liability 0.00 | FAILED |
| 6 | 1 | wiki_js | Content Match | PTO Liability - 08/31/2026 | a stated dollar total equal to the sum of the liability cells, within 0.01 | FAILED |
| 7 | 1 | wiki_js | Content Match | PTO Liability - 08/31/2026 | 52, 1,522.17 hours and a dollar total in the prose | FAILED |
| 8 | 1 | wiki_js | Content Match | PTO Liability - 08/31/2026 | a name on every keyed row | FAILED |
| 9 | 1 | wiki_js | Content Match | PTO Liability - 08/31/2026 | a department on every keyed row | FAILED |
| 10 | 1 | wiki_js | Content Match | PTO Liability - 08/31/2026 | a tier of 80, 120 or 160, or its policy name, on every keyed row | FAILED |
| 11 | 1 | wiki_js | Content Match | PTO Liability - 08/31/2026 | no named row without a TRT- ID | FAILED |
| 12 | 1 | wiki_js | Content Match | PTO Liability - 08/31/2026 | every date MM/DD/YYYY, no ISO, spelled or dotted date | FAILED |
| 13 | 1 | wiki_js | Content Match | PTO Liability - 08/31/2026 | the count and a dollar figure above the one employee table | FAILED |
| 14 | 10 | wiki_js | Content Match | PTO Liability - 08/31/2026 | $92,739.54, or $92,772.88 under posted rounding | FAILED |
| 15 | 5 | wiki_js | Content Match | TRT-0005 | 64.62 hours, or 64.60 under posted rounding, within 0.005 | FAILED |
| 16 | 5 | wiki_js | Content Match | TRT-0043 | 120, or the policy name for 120 hours | FAILED |
| 17 | 7 | wiki_js | Content Match | TRT-0071 | 160, or the policy name for 160 hours | FAILED |
| 18 | 6 | wiki_js | Content Match | TRT-0018 | 60.00 hours, or 60.01 under posted rounding, within 0.005 | FAILED |
| 19 | 7 | wiki_js | Content Match | TRT-0088 | $56.7308 within 0.00005 | FAILED |
| 20 | 6 | wiki_js | Content Match | TRT-0117 | $71.2500 within 0.00005 | FAILED |
| 21 | 3 | wiki_js | Content Match | TRT-0096 | $29.3269 within 0.00005 | FAILED |
| 22 | 4 | wiki_js | Content Match | TRT-0141 | 29.60 hours, or 29.59 under posted rounding, within 0.005 | FAILED |
| 23 | 2 | wiki_js | Content Match | TRT-0153 | 6.15 hours, or 6.16 under posted rounding, within 0.005 | FAILED |
| 24 | 2 | wiki_js | Content Match | TRT-0155 | 3.08 hours under either rounding, within 0.005 | FAILED |
| 25 | 3 | wiki_js | Content Match | TRT-0002 | 62.62 hours, or 62.60 under posted rounding, within 0.005 | FAILED |
| 26 | 2 | wiki_js | Content Match | TRT-0001 | 22.87 hours, or 22.85 under posted rounding, within 0.005 | FAILED |
| 27 | 1 | bamboohr | Content Match | TRT-0043 | current policy PTO 2 to 5 Years | FAILED |
| 28 | 1 | bamboohr | Content Match | TRT-0051 | current policy PTO 2 to 5 Years | FAILED |
| 29 | 1 | bamboohr | Content Match | TRT-0058 | current policy PTO 2 to 5 Years | FAILED |
| 30 | 1 | bamboohr | Content Match | TRT-0071 | current policy PTO 5 Plus Years | FAILED |
| 31 | 1 | bamboohr | Content Match | TRT-0079 | current policy PTO 2 to 5 Years | FAILED |
| 32 | 1 | bamboohr | Content Match | TRT-0083 | current policy PTO 2 to 5 Years | FAILED |
| 33 | 1 | bamboohr | Content Match | TRT-0001, TRT-0002, TRT-0005, TRT-000... | the policy the criterion names on each of the 44 records, which is the loaded one | PASSED |
| 34 | 1 | bamboohr | Content Match | TRT-0005 | 64.62 hours, or 64.60 under posted rounding, within 0.005 | FAILED |
| 35 | 1 | bamboohr | Content Match | TRT-0043 | 34.46 hours, or 34.48 under posted rounding, within 0.005 | FAILED |
| 36 | 1 | bamboohr | Content Match | TRT-0071 | 51.87 hours, or 51.85 under posted rounding, within 0.005 | FAILED |
| 37 | 1 | bamboohr | Content Match | TRT-0018 | 60.00 hours, or 60.01 under posted rounding, within 0.005 | FAILED |
| 38 | 1 | bamboohr | Content Match | TRT-0141 | 29.60 hours, or 29.59 under posted rounding, within 0.005 | FAILED |
| 39 | 1 | bamboohr | Content Match | TRT-0009 | 64.62 hours, or 64.60 under posted rounding, within 0.005 | FAILED |
| 40 | 1 | bamboohr | Content Match | TRT-0012 | 18.46 hours, or 18.48 under posted rounding, within 0.005 | FAILED |
| 41 | 1 | bamboohr | Content Match | TRT-0014 | 58.46 hours, or 58.48 under posted rounding, within 0.005 | FAILED |
| 42 | 1 | bamboohr | Content Match | TRT-0021 | 42.46 hours, or 42.48 under posted rounding, within 0.005 | FAILED |
| 43 | 1 | bamboohr | Content Match | TRT-0023 | 58.46 hours, or 58.48 under posted rounding, within 0.005 | FAILED |
| 44 | 1 | bamboohr | Content Match | TRT-0029 | 50.46 hours, or 50.48 under posted rounding, within 0.005 | FAILED |
| 45 | 1 | bamboohr | Content Match | TRT-0031 | 26.46 hours, or 26.48 under posted rounding, within 0.005 | FAILED |
| 46 | 1 | bamboohr | Content Match | TRT-0040 | 58.46 hours, or 58.48 under posted rounding, within 0.005 | FAILED |
| 47 | 1 | bamboohr | Content Match | TRT-0051 | 6.71 hours, or 6.73 under posted rounding, within 0.005 | FAILED |
| 48 | 1 | bamboohr | Content Match | TRT-0058 | 40.96 hours, or 40.98 under posted rounding, within 0.005 | FAILED |
| 49 | 1 | bamboohr | Content Match | TRT-0079 | 24.96 hours, or 24.98 under posted rounding, within 0.005 | FAILED |
| 50 | 1 | bamboohr | Content Match | TRT-0083 | 18.71 hours, or 18.73 under posted rounding, within 0.005 | FAILED |
| 51 | 1 | bamboohr | Content Match | TRT-0001, TRT-0002, TRT-0027, TRT-003... | the balance the criterion states on each of the 33 records, the loaded one, within 0.005 | PASSED |
| 52 | 1 | bamboohr | Existence Check | TRT-0153 | 6.15 hours, or 6.16 under posted rounding, within 0.005 | FAILED |
| 53 | 1 | bamboohr | Existence Check | TRT-0155 | 3.08 hours under either rounding, within 0.005 | FAILED |
| 54 | 1 | bamboohr | Content Match | TRT-0153 | current policy PTO Under 2 Years | FAILED |
| 55 | 1 | bamboohr | Content Match | TRT-0155 | current policy PTO Under 2 Years | FAILED |

## The rows

### Row 1, weight 1, Objective Compliance, paste first

States that a Wiki.js page titled PTO Liability - 08/31/2026 is published.

| Field | Value |
|---|---|
| Target app | `wiki_js` |
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

### Row 2, weight 2, Objective Compliance

States, on the PTO liability page, the 52 current employees at 08/31/2026 as the only employee rows.

| Field | Value |
|---|---|
| Target app | `wiki_js` |
| Check type | Count Check |
| Expected Content | an employee row keyed on each of the roster's 52 IDs |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | PTO Liability - 08/31/2026 |
| Target Record Label | PTO Liability - 08/31/2026 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Data/2026-08-31_Master_Employee_Roster.xlsx (world); filesystem/HR/Data/2026-08-28_Employee_ID_Crosswalk.xlsx (world); bamboohr/Employee.csv (app table, not in the picker) |
| Code | `qc/verifiers/row02_states_on_the_pto_liability_page_the_52_current.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 3, weight 1, Objective Compliance

States, on the PTO liability page, hours to two decimals.

| Field | Value |
|---|---|
| Target app | `wiki_js` |
| Check type | Content Match |
| Expected Content | every balance 0.00 |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | PTO Liability - 08/31/2026 |
| Target Record Label | PTO Liability - 08/31/2026 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Style / formatting |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task) |
| Code | `qc/verifiers/row03_states_on_the_pto_liability_page_hours_to_two_de.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 4, weight 1, Objective Compliance

States, on the PTO liability page, hourly rates to four decimals.

| Field | Value |
|---|---|
| Target app | `wiki_js` |
| Check type | Content Match |
| Expected Content | every rate 0.0000 |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | PTO Liability - 08/31/2026 |
| Target Record Label | PTO Liability - 08/31/2026 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Style / formatting |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task) |
| Code | `qc/verifiers/row04_states_on_the_pto_liability_page_hourly_rates_to.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 5, weight 1, Objective Compliance

States, on the PTO liability page, dollars to the cent.

| Field | Value |
|---|---|
| Target app | `wiki_js` |
| Check type | Content Match |
| Expected Content | every liability 0.00 |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | PTO Liability - 08/31/2026 |
| Target Record Label | PTO Liability - 08/31/2026 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Style / formatting |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task) |
| Code | `qc/verifiers/row05_states_on_the_pto_liability_page_dollars_to_the.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 6, weight 1, Objective Compliance

States, on the PTO liability page, a total dollar liability equal to the sum of the rows.

| Field | Value |
|---|---|
| Target app | `wiki_js` |
| Check type | Content Match |
| Expected Content | a stated dollar total equal to the sum of the liability cells, within 0.01 |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | PTO Liability - 08/31/2026 |
| Target Record Label | PTO Liability - 08/31/2026 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Policies/Employee_Handbook_v3.pdf (world) |
| Code | `qc/verifiers/row06_states_on_the_pto_liability_page_a_total_dollar.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 7, weight 1, Objective Compliance

States, on the PTO liability page, a summary with the employee count, the total hours and the total dollar liability.

| Field | Value |
|---|---|
| Target app | `wiki_js` |
| Check type | Content Match |
| Expected Content | 52, 1,522.17 hours and a dollar total in the prose |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | PTO Liability - 08/31/2026 |
| Target Record Label | PTO Liability - 08/31/2026 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task) |
| Code | `qc/verifiers/row07_states_on_the_pto_liability_page_a_summary_with.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 8, weight 1, Objective Compliance

States, on the PTO liability page, a name on every employee row.

| Field | Value |
|---|---|
| Target app | `wiki_js` |
| Check type | Content Match |
| Expected Content | a name on every keyed row |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | PTO Liability - 08/31/2026 |
| Target Record Label | PTO Liability - 08/31/2026 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Data/2026-08-31_Master_Employee_Roster.xlsx (world) |
| Code | `qc/verifiers/row08_states_on_the_pto_liability_page_a_name_on_every.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 9, weight 1, Objective Compliance

States, on the PTO liability page, a department on every employee row.

| Field | Value |
|---|---|
| Target app | `wiki_js` |
| Check type | Content Match |
| Expected Content | a department on every keyed row |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | PTO Liability - 08/31/2026 |
| Target Record Label | PTO Liability - 08/31/2026 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Data/2026-08-31_Master_Employee_Roster.xlsx (world) |
| Code | `qc/verifiers/row09_states_on_the_pto_liability_page_a_department_on.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 10, weight 1, Objective Compliance

States, on the PTO liability page, an annual PTO tier in hours on every employee row.

| Field | Value |
|---|---|
| Target app | `wiki_js` |
| Check type | Content Match |
| Expected Content | a tier of 80, 120 or 160, or its policy name, on every keyed row |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | PTO Liability - 08/31/2026 |
| Target Record Label | PTO Liability - 08/31/2026 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world) |
| Code | `qc/verifiers/row10_states_on_the_pto_liability_page_an_annual_pto_t.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 11, weight 1, Objective Compliance

States, on the PTO liability page, an employee ID on every row.

| Field | Value |
|---|---|
| Target app | `wiki_js` |
| Check type | Content Match |
| Expected Content | no named row without a TRT- ID |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | PTO Liability - 08/31/2026 |
| Target Record Label | PTO Liability - 08/31/2026 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Style / formatting |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Data/2026-08-31_Master_Employee_Roster.xlsx (world) |
| Code | `qc/verifiers/row11_states_on_the_pto_liability_page_an_employee_id.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 12, weight 1, Objective Compliance

States, on the PTO liability page, every date in MM/DD/YYYY form.

| Field | Value |
|---|---|
| Target app | `wiki_js` |
| Check type | Content Match |
| Expected Content | every date MM/DD/YYYY, no ISO, spelled or dotted date |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | PTO Liability - 08/31/2026 |
| Target Record Label | PTO Liability - 08/31/2026 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Style / formatting |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Data/2026-08-31_Master_Employee_Roster.xlsx (world); filesystem/HR/Payroll/2026-06-25_Payroll_Procedures_Memo.docx (world) |
| Code | `qc/verifiers/row12_states_on_the_pto_liability_page_every_date_in_m.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 13, weight 1, Objective Compliance

States, on the PTO liability page, the summary above one table of employee rows.

| Field | Value |
|---|---|
| Target app | `wiki_js` |
| Check type | Content Match |
| Expected Content | the count and a dollar figure above the one employee table |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | PTO Liability - 08/31/2026 |
| Target Record Label | PTO Liability - 08/31/2026 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Style / formatting |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task) |
| Code | `qc/verifiers/row13_states_on_the_pto_liability_page_the_summary_abo.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 14, weight 10, Expert Assessment, primary

States, on the PTO liability page, a total dollar liability of $92,739.54.

| Field | Value |
|---|---|
| Target app | `wiki_js` |
| Check type | Content Match |
| Expected Content | $92,739.54, or $92,772.88 under posted rounding |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | PTO Liability - 08/31/2026 |
| Target Record Label | PTO Liability - 08/31/2026 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Policies/Employee_Handbook_v3.pdf (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); filesystem/HR/Data/2026-08-31_Master_Employee_Roster.xlsx (world); filesystem/HR/Payroll/2026-06-25_Payroll_Procedures_Memo.docx (world); filesystem/HR/Comp/Promotions/2026-06-10_Promotion_Approval_TRT-0088.docx (world); filesystem/HR/Comp/Amendments/2026-05-12_Comp_Amendment_TRT-0117.pdf (world); filesystem/HR/People/Offer_Letters/Historical_Offer_Letters_2020-2026.pdf (world); filesystem/HR/Benefits/2026-08-10_Schedule_Change_TRT-0141.pdf (world) |
| Code | `qc/verifiers/row14_states_on_the_pto_liability_page_a_total_dollar.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 15, weight 5, Expert Assessment, primary

States, on the PTO liability page, a balance of 64.62 hours for Mikelle Hosana, TRT-0005.

| Field | Value |
|---|---|
| Target app | `wiki_js` |
| Check type | Content Match |
| Expected Content | 64.62 hours, or 64.60 under posted rounding, within 0.005 |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | TRT-0005 |
| Target Record Label | Mikelle Hosana, TRT-0005 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); filesystem/HR/Data/HRIS_Time_Off_Report_2026-08-31.xlsx (world); filesystem/HR/Data/Migration/HRIS_Import_Load_2026-07-01.csv (world); filesystem/HR/Data/Migration/2026-06-24_Field_Mapping_Workbook.xlsx (world) |
| Code | `qc/verifiers/row15_states_on_the_pto_liability_page_a_balance_of_64.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 16, weight 5, Expert Assessment, primary

States, on the PTO liability page, the 120-hour tier for Oren Kastellanos, TRT-0043.

| Field | Value |
|---|---|
| Target app | `wiki_js` |
| Check type | Content Match |
| Expected Content | 120, or the policy name for 120 hours |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | TRT-0043 |
| Target Record Label | Oren Kastellanos, TRT-0043 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); filesystem/HR/People/Offer_Letters/Historical_Offer_Letters_2020-2026.pdf (world); filesystem/HR/Data/Migration/HRIS_Import_Load_2026-07-01.csv (world); bamboohr/EmployeePolicy.csv (app table, not in the picker) |
| Code | `qc/verifiers/row16_states_on_the_pto_liability_page_the_120_hour_ti.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 17, weight 7, Expert Assessment, primary

States, on the PTO liability page, the 160-hour tier for Samuel Burkenham, TRT-0071.

| Field | Value |
|---|---|
| Target app | `wiki_js` |
| Check type | Content Match |
| Expected Content | 160, or the policy name for 160 hours |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | TRT-0071 |
| Target Record Label | Samuel Burkenham, TRT-0071 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/HR/Policies/Employee_Handbook_v3.pdf (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); filesystem/HR/People/Offer_Letters/2024-04-08_Rehire_Offer_TRT-0071.pdf (world); filesystem/Wiki/Onboarding_Data_Standards.md (world) |
| Code | `qc/verifiers/row17_states_on_the_pto_liability_page_the_160_hour_ti.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 18, weight 6, Expert Assessment, primary

States, on the PTO liability page, a balance of 60.00 hours for Marisela Thornbury, TRT-0018.

| Field | Value |
|---|---|
| Target app | `wiki_js` |
| Check type | Content Match |
| Expected Content | 60.00 hours, or 60.01 under posted rounding, within 0.005 |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | TRT-0018 |
| Target Record Label | Marisela Thornbury, TRT-0018 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); filesystem/HR/Payroll/2026-06-25_Payroll_Procedures_Memo.docx (world); bamboohr/EmployeePolicy.csv (app table, not in the picker) |
| Code | `qc/verifiers/row18_states_on_the_pto_liability_page_a_balance_of_60.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 19, weight 7, Expert Assessment, primary

States, on the PTO liability page, an hourly rate of $56.7308 for Yolanda Featherstone, TRT-0088.

| Field | Value |
|---|---|
| Target app | `wiki_js` |
| Check type | Content Match |
| Expected Content | $56.7308 within 0.00005 |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | TRT-0088 |
| Target Record Label | Yolanda Featherstone, TRT-0088 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/HR/Comp/Promotions/2026-06-10_Promotion_Approval_TRT-0088.docx (world); filesystem/HR/Policies/Employee_Handbook_v3.pdf (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); bamboohr/Employee.csv (app table, not in the picker) |
| Code | `qc/verifiers/row19_states_on_the_pto_liability_page_an_hourly_rate.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 20, weight 6, Expert Assessment, primary

States, on the PTO liability page, an hourly rate of $71.2500 for Belaviv Luk, TRT-0117.

| Field | Value |
|---|---|
| Target app | `wiki_js` |
| Check type | Content Match |
| Expected Content | $71.2500 within 0.00005 |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | TRT-0117 |
| Target Record Label | Belaviv Luk, TRT-0117 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/HR/Comp/Amendments/2026-05-12_Comp_Amendment_TRT-0117.pdf (world); filesystem/HR/Policies/Employee_Handbook_v3.pdf (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); bamboohr/Employee.csv (app table, not in the picker) |
| Code | `qc/verifiers/row20_states_on_the_pto_liability_page_an_hourly_rate.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 21, weight 3, Expert Assessment, primary

States, on the PTO liability page, an hourly rate of $29.3269 for Delphine Marchetti, TRT-0096.

| Field | Value |
|---|---|
| Target app | `wiki_js` |
| Check type | Content Match |
| Expected Content | $29.3269 within 0.00005 |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | TRT-0096 |
| Target Record Label | Delphine Marchetti, TRT-0096 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/HR/People/Offer_Letters/Historical_Offer_Letters_2020-2026.pdf (world); filesystem/HR/Policies/Employee_Handbook_v3.pdf (world); filesystem/Wiki/Compensation_Authority.md (world); bamboohr/Employee.csv (app table, not in the picker) |
| Code | `qc/verifiers/row21_states_on_the_pto_liability_page_an_hourly_rate.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 22, weight 4, Expert Assessment, primary

States, on the PTO liability page, a balance of 29.60 hours for Beatriz Quintanilla, TRT-0141.

| Field | Value |
|---|---|
| Target app | `wiki_js` |
| Check type | Content Match |
| Expected Content | 29.60 hours, or 29.59 under posted rounding, within 0.005 |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | TRT-0141 |
| Target Record Label | Beatriz Quintanilla, TRT-0141 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/HR/Benefits/2026-08-10_Schedule_Change_TRT-0141.pdf (world); filesystem/HR/Policies/Employee_Handbook_v3.pdf (world); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Data/2026-08-31_Master_Employee_Roster.xlsx (world) |
| Code | `qc/verifiers/row22_states_on_the_pto_liability_page_a_balance_of_29.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 23, weight 2, Expert Assessment, primary

States, on the PTO liability page, a balance of 6.15 hours for Simone Okonkwo, TRT-0153.

| Field | Value |
|---|---|
| Target app | `wiki_js` |
| Check type | Content Match |
| Expected Content | 6.15 hours, or 6.16 under posted rounding, within 0.005 |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | TRT-0153 |
| Target Record Label | Simone Okonkwo, TRT-0153 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/HR/Data/2026-08-31_Master_Employee_Roster.xlsx (world); filesystem/HR/Data/2026-08-28_Employee_ID_Crosswalk.xlsx (world); filesystem/Recruiting/Offers/2026-07-02_Offer_TRT-0153_SIGNED.pdf (world); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); greenhouse/candidates.csv (app table, not in the picker) |
| Code | `qc/verifiers/row23_states_on_the_pto_liability_page_a_balance_of_6.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 24, weight 2, Expert Assessment, primary

States, on the PTO liability page, a balance of 3.08 hours for Rafael Ibarra, TRT-0155.

| Field | Value |
|---|---|
| Target app | `wiki_js` |
| Check type | Content Match |
| Expected Content | 3.08 hours under either rounding, within 0.005 |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | TRT-0155 |
| Target Record Label | Rafael Ibarra, TRT-0155 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/HR/Data/2026-08-31_Master_Employee_Roster.xlsx (world); filesystem/HR/Data/2026-08-28_Employee_ID_Crosswalk.xlsx (world); filesystem/HR/People/Offer_Letters/Historical_Offer_Letters_2020-2026.pdf (world); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); greenhouse/candidates.csv (app table, not in the picker) |
| Code | `qc/verifiers/row24_states_on_the_pto_liability_page_a_balance_of_3.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 25, weight 3, Objective Compliance

States, on the PTO liability page, a balance of 62.62 hours for Sora Jackson, TRT-0002.

| Field | Value |
|---|---|
| Target app | `wiki_js` |
| Check type | Content Match |
| Expected Content | 62.62 hours, or 62.60 under posted rounding, within 0.005 |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | TRT-0002 |
| Target Record Label | Sora Jackson, TRT-0002 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/HR/Payroll/2026-06-25_Payroll_Procedures_Memo.docx (world); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world) |
| Code | `qc/verifiers/row25_states_on_the_pto_liability_page_a_balance_of_62.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 26, weight 2, Objective Compliance

States, on the PTO liability page, a balance of 22.87 hours for Michael Labeson, TRT-0001.

| Field | Value |
|---|---|
| Target app | `wiki_js` |
| Check type | Content Match |
| Expected Content | 22.87 hours, or 22.85 under posted rounding, within 0.005 |
| Target Table | pages, the documented Wiki.js table |
| Target Record ID | TRT-0001 |
| Target Record Label | Michael Labeson, TRT-0001 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); bamboohr/TimeOffRequest.csv (app table, not in the picker) |
| Code | `qc/verifiers/row26_states_on_the_pto_liability_page_a_balance_of_22.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no page titled 'PTO Liability - 08/31/2026'` |

### Row 27, weight 1, Expert Assessment, primary

States, in BambooHR, the PTO 2 to 5 Years policy for Oren Kastellanos, TRT-0043.

| Field | Value |
|---|---|
| Target app | `bamboohr` |
| Check type | Content Match |
| Expected Content | current policy PTO 2 to 5 Years |
| Target Table | the employee policy assignment table, found by its references into the employee and policy tables |
| Target Record ID | TRT-0043 |
| Target Record Label | Oren Kastellanos, TRT-0043 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); filesystem/HR/Data/Migration/HRIS_Import_Load_2026-07-01.csv (world); bamboohr/EmployeePolicy.csv (app table, not in the picker) |
| Code | `qc/verifiers/row27_states_in_bamboohr_the_pto_2_to_5_years_policy_f.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - policy 'pto under 2 years'` |

### Row 28, weight 1, Expert Assessment, primary

States, in BambooHR, the PTO 2 to 5 Years policy for Priyamvada Raghunath, TRT-0051.

| Field | Value |
|---|---|
| Target app | `bamboohr` |
| Check type | Content Match |
| Expected Content | current policy PTO 2 to 5 Years |
| Target Table | the employee policy assignment table, found by its references into the employee and policy tables |
| Target Record ID | TRT-0051 |
| Target Record Label | Priyamvada Raghunath, TRT-0051 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); filesystem/HR/Data/Migration/HRIS_Import_Load_2026-07-01.csv (world); bamboohr/EmployeePolicy.csv (app table, not in the picker) |
| Code | `qc/verifiers/row28_states_in_bamboohr_the_pto_2_to_5_years_policy_f.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - policy 'pto under 2 years'` |

### Row 29, weight 1, Expert Assessment, primary

States, in BambooHR, the PTO 2 to 5 Years policy for Callum Oyelaran, TRT-0058.

| Field | Value |
|---|---|
| Target app | `bamboohr` |
| Check type | Content Match |
| Expected Content | current policy PTO 2 to 5 Years |
| Target Table | the employee policy assignment table, found by its references into the employee and policy tables |
| Target Record ID | TRT-0058 |
| Target Record Label | Callum Oyelaran, TRT-0058 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); filesystem/HR/Data/Migration/HRIS_Import_Load_2026-07-01.csv (world); bamboohr/EmployeePolicy.csv (app table, not in the picker) |
| Code | `qc/verifiers/row29_states_in_bamboohr_the_pto_2_to_5_years_policy_f.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - policy 'pto under 2 years'` |

### Row 30, weight 1, Expert Assessment, primary

States, in BambooHR, the PTO 5 Plus Years policy for Samuel Burkenham, TRT-0071.

| Field | Value |
|---|---|
| Target app | `bamboohr` |
| Check type | Content Match |
| Expected Content | current policy PTO 5 Plus Years |
| Target Table | the employee policy assignment table, found by its references into the employee and policy tables |
| Target Record ID | TRT-0071 |
| Target Record Label | Samuel Burkenham, TRT-0071 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); filesystem/HR/Data/Migration/HRIS_Import_Load_2026-07-01.csv (world); bamboohr/EmployeePolicy.csv (app table, not in the picker) |
| Code | `qc/verifiers/row30_states_in_bamboohr_the_pto_5_plus_years_policy_f.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - policy 'pto under 2 years'` |

### Row 31, weight 1, Expert Assessment, primary

States, in BambooHR, the PTO 2 to 5 Years policy for Wren Takahashi-Bell, TRT-0079.

| Field | Value |
|---|---|
| Target app | `bamboohr` |
| Check type | Content Match |
| Expected Content | current policy PTO 2 to 5 Years |
| Target Table | the employee policy assignment table, found by its references into the employee and policy tables |
| Target Record ID | TRT-0079 |
| Target Record Label | Wren Takahashi-Bell, TRT-0079 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); filesystem/HR/Data/Migration/HRIS_Import_Load_2026-07-01.csv (world); bamboohr/EmployeePolicy.csv (app table, not in the picker) |
| Code | `qc/verifiers/row31_states_in_bamboohr_the_pto_2_to_5_years_policy_f.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - policy 'pto under 2 years'` |

### Row 32, weight 1, Expert Assessment, primary

States, in BambooHR, the PTO 2 to 5 Years policy for Desmond Achterberg, TRT-0083.

| Field | Value |
|---|---|
| Target app | `bamboohr` |
| Check type | Content Match |
| Expected Content | current policy PTO 2 to 5 Years |
| Target Table | the employee policy assignment table, found by its references into the employee and policy tables |
| Target Record ID | TRT-0083 |
| Target Record Label | Desmond Achterberg, TRT-0083 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); filesystem/HR/Data/Migration/HRIS_Import_Load_2026-07-01.csv (world); bamboohr/EmployeePolicy.csv (app table, not in the picker) |
| Code | `qc/verifiers/row32_states_in_bamboohr_the_pto_2_to_5_years_policy_f.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - policy 'pto under 2 years'` |

### Row 33, weight 1, Objective Compliance, paste first

States, in BambooHR, for the 44 employees whose loaded policy is the tier's at 08/31/2026, the PTO Under 2 Years policy for TRT-0096, TRT-0099, TRT-0102, TRT-0105, TRT-0108, TRT-0110, TRT-0113, TRT-0119, TRT-0122, TRT-0128, TRT-0131, TRT-0135, TRT-0141, TRT-0150, TRT-0154, TRT-0156, the PTO 2 to 5 Years policy for TRT-0012, TRT-0014, TRT-0021, TRT-0023, TRT-0027, TRT-0029, TRT-0031, TRT-0034, TRT-0040, TRT-0045, TRT-0047, TRT-0052, TRT-0055, TRT-0062, TRT-0066, TRT-0069, TRT-0074, TRT-0076, TRT-0086, TRT-0088, TRT-0091, TRT-0093, TRT-0117, the PTO 5 Plus Years policy for TRT-0001, TRT-0002, TRT-0005, TRT-0009, TRT-0018.

| Field | Value |
|---|---|
| Target app | `bamboohr` |
| Check type | Content Match |
| Expected Content | the policy the criterion names on each of the 44 records, which is the loaded one |
| Target Table | the employee policy assignment table, found by its references into the employee and policy tables |
| Target Record ID | TRT-0001, TRT-0002, TRT-0005, TRT-0009, TRT-0012, TRT-0014, TRT-0018, TRT-0021, TRT-0023, TRT-0027, TRT-0029, TRT-0031, TRT-0034, TRT-0040, TRT-0045, TRT-0047, TRT-0052, TRT-0055, TRT-0062, TRT-0066, TRT-0069, TRT-0074, TRT-0076, TRT-0086, TRT-0088, TRT-0091, TRT-0093, TRT-0096, TRT-0099, TRT-0102, TRT-0105, TRT-0108, TRT-0110, TRT-0113, TRT-0117, TRT-0119, TRT-0122, TRT-0128, TRT-0131, TRT-0135, TRT-0141, TRT-0150, TRT-0154, TRT-0156 |
| Target Record Label | 44 loaded records the schedule leaves as loaded |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); filesystem/HR/Data/Migration/HRIS_Import_Load_2026-07-01.csv (world); bamboohr/EmployeePolicy.csv (app table, not in the picker); bamboohr/TimeOffPolicy.csv (app table, not in the picker) |
| Code | `qc/verifiers/row33_states_in_bamboohr_for_the_44_employees_whose_lo.py`, the whole file |
| Test-run on the untouched task | **PASSED**, last line `PASSED - 44 of 44 policies match the schedule` |

### Row 34, weight 1, Expert Assessment, primary

States, in BambooHR, a PTO balance of 64.62 hours for Mikelle Hosana, TRT-0005.

| Field | Value |
|---|---|
| Target app | `bamboohr` |
| Check type | Content Match |
| Expected Content | 64.62 hours, or 64.60 under posted rounding, within 0.005 |
| Target Table | the time-off balance table, found by its references into the employee and policy tables |
| Target Record ID | TRT-0005 |
| Target Record Label | Mikelle Hosana, TRT-0005 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); bamboohr/TimeOffBalance.csv (app table, not in the picker) |
| Code | `qc/verifiers/row34_states_in_bamboohr_a_pto_balance_of_64_62_hours.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - balance 117.1152 against [64.62, 64.6]` |

### Row 35, weight 1, Expert Assessment, primary

States, in BambooHR, a PTO balance of 34.46 hours for Oren Kastellanos, TRT-0043.

| Field | Value |
|---|---|
| Target app | `bamboohr` |
| Check type | Content Match |
| Expected Content | 34.46 hours, or 34.48 under posted rounding, within 0.005 |
| Target Table | the time-off balance table, found by its references into the employee and policy tables |
| Target Record ID | TRT-0043 |
| Target Record Label | Oren Kastellanos, TRT-0043 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); bamboohr/TimeOffBalance.csv (app table, not in the picker) |
| Code | `qc/verifiers/row35_states_in_bamboohr_a_pto_balance_of_34_46_hours.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - balance 31.8076 against [34.46, 34.48]` |

### Row 36, weight 1, Expert Assessment, primary

States, in BambooHR, a PTO balance of 51.87 hours for Samuel Burkenham, TRT-0071.

| Field | Value |
|---|---|
| Target app | `bamboohr` |
| Check type | Content Match |
| Expected Content | 51.87 hours, or 51.85 under posted rounding, within 0.005 |
| Target Table | the time-off balance table, found by its references into the employee and policy tables |
| Target Record ID | TRT-0071 |
| Target Record Label | Samuel Burkenham, TRT-0071 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); bamboohr/TimeOffBalance.csv (app table, not in the picker) |
| Code | `qc/verifiers/row36_states_in_bamboohr_a_pto_balance_of_51_87_hours.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - balance 39.5576 against [51.87, 51.85]` |

### Row 37, weight 1, Expert Assessment, primary

States, in BambooHR, a PTO balance of 60.00 hours for Marisela Thornbury, TRT-0018.

| Field | Value |
|---|---|
| Target app | `bamboohr` |
| Check type | Content Match |
| Expected Content | 60.00 hours, or 60.01 under posted rounding, within 0.005 |
| Target Table | the time-off balance table, found by its references into the employee and policy tables |
| Target Record ID | TRT-0018 |
| Target Record Label | Marisela Thornbury, TRT-0018 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); bamboohr/TimeOffBalance.csv (app table, not in the picker) |
| Code | `qc/verifiers/row37_states_in_bamboohr_a_pto_balance_of_60_00_hours.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - balance 87.8654 against [60.0, 60.01]` |

### Row 38, weight 1, Expert Assessment, primary

States, in BambooHR, a PTO balance of 29.60 hours for Beatriz Quintanilla, TRT-0141.

| Field | Value |
|---|---|
| Target app | `bamboohr` |
| Check type | Content Match |
| Expected Content | 29.60 hours, or 29.59 under posted rounding, within 0.005 |
| Target Table | the time-off balance table, found by its references into the employee and policy tables |
| Target Record ID | TRT-0141 |
| Target Record Label | Beatriz Quintanilla, TRT-0141 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); bamboohr/TimeOffBalance.csv (app table, not in the picker) |
| Code | `qc/verifiers/row38_states_in_bamboohr_a_pto_balance_of_29_60_hours.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - balance 33.0576 against [29.6, 29.59]` |

### Row 39, weight 1, Expert Assessment, primary

States, in BambooHR, a PTO balance of 64.62 hours for Krystale Jumawan, TRT-0009.

| Field | Value |
|---|---|
| Target app | `bamboohr` |
| Check type | Content Match |
| Expected Content | 64.62 hours, or 64.60 under posted rounding, within 0.005 |
| Target Table | the time-off balance table, found by its references into the employee and policy tables |
| Target Record ID | TRT-0009 |
| Target Record Label | Krystale Jumawan, TRT-0009 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); bamboohr/TimeOffBalance.csv (app table, not in the picker) |
| Code | `qc/verifiers/row39_states_in_bamboohr_a_pto_balance_of_64_62_hours.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - balance 108.6152 against [64.62, 64.6]` |

### Row 40, weight 1, Expert Assessment, primary

States, in BambooHR, a PTO balance of 18.46 hours for Jessica Ko, TRT-0012.

| Field | Value |
|---|---|
| Target app | `bamboohr` |
| Check type | Content Match |
| Expected Content | 18.46 hours, or 18.48 under posted rounding, within 0.005 |
| Target Table | the time-off balance table, found by its references into the employee and policy tables |
| Target Record ID | TRT-0012 |
| Target Record Label | Jessica Ko, TRT-0012 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); bamboohr/TimeOffBalance.csv (app table, not in the picker) |
| Code | `qc/verifiers/row40_states_in_bamboohr_a_pto_balance_of_18_46_hours.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - balance 49.9615 against [18.46, 18.48]` |

### Row 41, weight 1, Expert Assessment, primary

States, in BambooHR, a PTO balance of 58.46 hours for Rohan Iyer, TRT-0014.

| Field | Value |
|---|---|
| Target app | `bamboohr` |
| Check type | Content Match |
| Expected Content | 58.46 hours, or 58.48 under posted rounding, within 0.005 |
| Target Table | the time-off balance table, found by its references into the employee and policy tables |
| Target Record ID | TRT-0014 |
| Target Record Label | Rohan Iyer, TRT-0014 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); bamboohr/TimeOffBalance.csv (app table, not in the picker) |
| Code | `qc/verifiers/row41_states_in_bamboohr_a_pto_balance_of_58_46_hours.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - balance 84.4615 against [58.46, 58.48]` |

### Row 42, weight 1, Expert Assessment, primary

States, in BambooHR, a PTO balance of 42.46 hours for Edith Bustamante, TRT-0021.

| Field | Value |
|---|---|
| Target app | `bamboohr` |
| Check type | Content Match |
| Expected Content | 42.46 hours, or 42.48 under posted rounding, within 0.005 |
| Target Table | the time-off balance table, found by its references into the employee and policy tables |
| Target Record ID | TRT-0021 |
| Target Record Label | Edith Bustamante, TRT-0021 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); bamboohr/TimeOffBalance.csv (app table, not in the picker) |
| Code | `qc/verifiers/row42_states_in_bamboohr_a_pto_balance_of_42_46_hours.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - balance 76.4615 against [42.46, 42.48]` |

### Row 43, weight 1, Expert Assessment, primary

States, in BambooHR, a PTO balance of 58.46 hours for Maeve Oyinlola, TRT-0023.

| Field | Value |
|---|---|
| Target app | `bamboohr` |
| Check type | Content Match |
| Expected Content | 58.46 hours, or 58.48 under posted rounding, within 0.005 |
| Target Table | the time-off balance table, found by its references into the employee and policy tables |
| Target Record ID | TRT-0023 |
| Target Record Label | Maeve Oyinlola, TRT-0023 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); bamboohr/TimeOffBalance.csv (app table, not in the picker) |
| Code | `qc/verifiers/row43_states_in_bamboohr_a_pto_balance_of_58_46_hours.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - balance 78.9615 against [58.46, 58.48]` |

### Row 44, weight 1, Expert Assessment, primary

States, in BambooHR, a PTO balance of 50.46 hours for Emeka Thorsen, TRT-0029.

| Field | Value |
|---|---|
| Target app | `bamboohr` |
| Check type | Content Match |
| Expected Content | 50.46 hours, or 50.48 under posted rounding, within 0.005 |
| Target Table | the time-off balance table, found by its references into the employee and policy tables |
| Target Record ID | TRT-0029 |
| Target Record Label | Emeka Thorsen, TRT-0029 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); bamboohr/TimeOffBalance.csv (app table, not in the picker) |
| Code | `qc/verifiers/row44_states_in_bamboohr_a_pto_balance_of_50_46_hours.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - balance 67.4615 against [50.46, 50.48]` |

### Row 45, weight 1, Expert Assessment, primary

States, in BambooHR, a PTO balance of 26.46 hours for Zephyr Adebayo, TRT-0031.

| Field | Value |
|---|---|
| Target app | `bamboohr` |
| Check type | Content Match |
| Expected Content | 26.46 hours, or 26.48 under posted rounding, within 0.005 |
| Target Table | the time-off balance table, found by its references into the employee and policy tables |
| Target Record ID | TRT-0031 |
| Target Record Label | Zephyr Adebayo, TRT-0031 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); bamboohr/TimeOffBalance.csv (app table, not in the picker) |
| Code | `qc/verifiers/row45_states_in_bamboohr_a_pto_balance_of_26_46_hours.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - balance 38.4615 against [26.46, 26.48]` |

### Row 46, weight 1, Expert Assessment, primary

States, in BambooHR, a PTO balance of 58.46 hours for Ilse Van der Kolk, TRT-0040.

| Field | Value |
|---|---|
| Target app | `bamboohr` |
| Check type | Content Match |
| Expected Content | 58.46 hours, or 58.48 under posted rounding, within 0.005 |
| Target Table | the time-off balance table, found by its references into the employee and policy tables |
| Target Record ID | TRT-0040 |
| Target Record Label | Ilse Van der Kolk, TRT-0040 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); bamboohr/TimeOffBalance.csv (app table, not in the picker) |
| Code | `qc/verifiers/row46_states_in_bamboohr_a_pto_balance_of_58_46_hours.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - balance 67.9616 against [58.46, 58.48]` |

### Row 47, weight 1, Expert Assessment, primary

States, in BambooHR, a PTO balance of 6.71 hours for Priyamvada Raghunath, TRT-0051.

| Field | Value |
|---|---|
| Target app | `bamboohr` |
| Check type | Content Match |
| Expected Content | 6.71 hours, or 6.73 under posted rounding, within 0.005 |
| Target Table | the time-off balance table, found by its references into the employee and policy tables |
| Target Record ID | TRT-0051 |
| Target Record Label | Priyamvada Raghunath, TRT-0051 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); bamboohr/TimeOffBalance.csv (app table, not in the picker) |
| Code | `qc/verifiers/row47_states_in_bamboohr_a_pto_balance_of_6_71_hours_f.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - balance 0.5576000000000008 against [6.71, 6.73]` |

### Row 48, weight 1, Expert Assessment, primary

States, in BambooHR, a PTO balance of 40.96 hours for Callum Oyelaran, TRT-0058.

| Field | Value |
|---|---|
| Target app | `bamboohr` |
| Check type | Content Match |
| Expected Content | 40.96 hours, or 40.98 under posted rounding, within 0.005 |
| Target Table | the time-off balance table, found by its references into the employee and policy tables |
| Target Record ID | TRT-0058 |
| Target Record Label | Callum Oyelaran, TRT-0058 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); bamboohr/TimeOffBalance.csv (app table, not in the picker) |
| Code | `qc/verifiers/row48_states_in_bamboohr_a_pto_balance_of_40_96_hours.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - balance 34.8076 against [40.96, 40.98]` |

### Row 49, weight 1, Expert Assessment, primary

States, in BambooHR, a PTO balance of 24.96 hours for Wren Takahashi-Bell, TRT-0079.

| Field | Value |
|---|---|
| Target app | `bamboohr` |
| Check type | Content Match |
| Expected Content | 24.96 hours, or 24.98 under posted rounding, within 0.005 |
| Target Table | the time-off balance table, found by its references into the employee and policy tables |
| Target Record ID | TRT-0079 |
| Target Record Label | Wren Takahashi-Bell, TRT-0079 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); bamboohr/TimeOffBalance.csv (app table, not in the picker) |
| Code | `qc/verifiers/row49_states_in_bamboohr_a_pto_balance_of_24_96_hours.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - balance 18.8076 against [24.96, 24.98]` |

### Row 50, weight 1, Expert Assessment, primary

States, in BambooHR, a PTO balance of 18.71 hours for Desmond Achterberg, TRT-0083.

| Field | Value |
|---|---|
| Target app | `bamboohr` |
| Check type | Content Match |
| Expected Content | 18.71 hours, or 18.73 under posted rounding, within 0.005 |
| Target Table | the time-off balance table, found by its references into the employee and policy tables |
| Target Record ID | TRT-0083 |
| Target Record Label | Desmond Achterberg, TRT-0083 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); bamboohr/TimeOffBalance.csv (app table, not in the picker) |
| Code | `qc/verifiers/row50_states_in_bamboohr_a_pto_balance_of_18_71_hours.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - balance 12.5576 against [18.71, 18.73]` |

### Row 51, weight 1, Objective Compliance

States, in BambooHR, for the 33 employees whose loaded balance is the 08/31/2026 figure, a PTO balance of 22.87 hours for TRT-0001, 62.62 for TRT-0002, 26.71 for TRT-0027, 30.96 for TRT-0034, 7.96 for TRT-0045, 5.46 for TRT-0047, 4.46 for TRT-0052, 15.96 for TRT-0055, 21.21 for TRT-0062, 27.96 for TRT-0066, 46.21 for TRT-0069, 44.21 for TRT-0074, 35.21 for TRT-0076, 51.96 for TRT-0086, 13.21 for TRT-0088, 25.71 for TRT-0091, 20.21 for TRT-0093, 20.56 for TRT-0096, 37.06 for TRT-0099, 24.31 for TRT-0102, 15.81 for TRT-0105, 41.31 for TRT-0108, 23.81 for TRT-0110, 26.56 for TRT-0113, 8.46 for TRT-0117, 22.06 for TRT-0119, 31.31 for TRT-0122, 20.06 for TRT-0128, 4.31 for TRT-0131, 49.31 for TRT-0135, 12.31 for TRT-0150, 3.08 for TRT-0154, 0.00 for TRT-0156.

| Field | Value |
|---|---|
| Target app | `bamboohr` |
| Check type | Content Match |
| Expected Content | the balance the criterion states on each of the 33 records, the loaded one, within 0.005 |
| Target Table | the time-off balance table, found by its references into the employee and policy tables |
| Target Record ID | TRT-0001, TRT-0002, TRT-0027, TRT-0034, TRT-0045, TRT-0047, TRT-0052, TRT-0055, TRT-0062, TRT-0066, TRT-0069, TRT-0074, TRT-0076, TRT-0086, TRT-0088, TRT-0091, TRT-0093, TRT-0096, TRT-0099, TRT-0102, TRT-0105, TRT-0108, TRT-0110, TRT-0113, TRT-0117, TRT-0119, TRT-0122, TRT-0128, TRT-0131, TRT-0135, TRT-0150, TRT-0154, TRT-0156 |
| Target Record Label | 33 loaded records the schedule leaves as loaded |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx (world); filesystem/HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx (world); bamboohr/TimeOffBalance.csv (app table, not in the picker) |
| Code | `qc/verifiers/row51_states_in_bamboohr_for_the_33_employees_whose_lo.py`, the whole file |
| Test-run on the untouched task | **PASSED**, last line `PASSED - 33 of 33 balances match the schedule` |

### Row 52, weight 1, Objective Compliance

States, in BambooHR, a PTO balance of 6.15 hours for Simone Okonkwo, TRT-0153.

| Field | Value |
|---|---|
| Target app | `bamboohr` |
| Check type | Existence Check |
| Expected Content | 6.15 hours, or 6.16 under posted rounding, within 0.005 |
| Target Table | the time-off balance table, found by its references into the employee and policy tables |
| Target Record ID | TRT-0153 |
| Target Record Label | Simone Okonkwo, TRT-0153 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Data/2026-08-31_Master_Employee_Roster.xlsx (world); filesystem/HR/Data/2026-08-28_Employee_ID_Crosswalk.xlsx (world); bamboohr/TimeOffBalance.csv (app table, not in the picker) |
| Code | `qc/verifiers/row52_states_in_bamboohr_a_pto_balance_of_6_15_hours_f.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no employee row carries TRT-0153` |

### Row 53, weight 1, Objective Compliance

States, in BambooHR, a PTO balance of 3.08 hours for Rafael Ibarra, TRT-0155.

| Field | Value |
|---|---|
| Target app | `bamboohr` |
| Check type | Existence Check |
| Expected Content | 3.08 hours under either rounding, within 0.005 |
| Target Table | the time-off balance table, found by its references into the employee and policy tables |
| Target Record ID | TRT-0155 |
| Target Record Label | Rafael Ibarra, TRT-0155 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Data/2026-08-31_Master_Employee_Roster.xlsx (world); filesystem/HR/Data/2026-08-28_Employee_ID_Crosswalk.xlsx (world); bamboohr/TimeOffBalance.csv (app table, not in the picker) |
| Code | `qc/verifiers/row53_states_in_bamboohr_a_pto_balance_of_3_08_hours_f.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no employee row carries TRT-0155` |

### Row 54, weight 1, Objective Compliance

States, in BambooHR, the PTO Under 2 Years policy for Simone Okonkwo, TRT-0153.

| Field | Value |
|---|---|
| Target app | `bamboohr` |
| Check type | Content Match |
| Expected Content | current policy PTO Under 2 Years |
| Target Table | the employee policy assignment table, found by its references into the employee and policy tables |
| Target Record ID | TRT-0153 |
| Target Record Label | Simone Okonkwo, TRT-0153 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Data/2026-08-31_Master_Employee_Roster.xlsx (world); filesystem/HR/Data/2026-08-28_Employee_ID_Crosswalk.xlsx (world); bamboohr/EmployeePolicy.csv (app table, not in the picker); bamboohr/TimeOffPolicy.csv (app table, not in the picker) |
| Code | `qc/verifiers/row54_states_in_bamboohr_the_pto_under_2_years_policy.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no employee row carries TRT-0153` |

### Row 55, weight 1, Objective Compliance

States, in BambooHR, the PTO Under 2 Years policy for Rafael Ibarra, TRT-0155.

| Field | Value |
|---|---|
| Target app | `bamboohr` |
| Check type | Content Match |
| Expected Content | current policy PTO Under 2 Years |
| Target Table | the employee policy assignment table, found by its references into the employee and policy tables |
| Target Record ID | TRT-0155 |
| Target Record Label | Rafael Ibarra, TRT-0155 |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | Final Response |
| Reference Artifacts | filesystem/pto_liability_request.pdf (task); filesystem/HR/Data/2026-08-31_Master_Employee_Roster.xlsx (world); filesystem/HR/Data/2026-08-28_Employee_ID_Crosswalk.xlsx (world); bamboohr/EmployeePolicy.csv (app table, not in the picker); bamboohr/TimeOffPolicy.csv (app table, not in the picker) |
| Code | `qc/verifiers/row55_states_in_bamboohr_the_pto_under_2_years_policy.py`, the whole file |
| Test-run on the untouched task | **FAILED**, last line `FAILED - no employee row carries TRT-0155` |
