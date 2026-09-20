# 08 - The section 1.3 step plan in the checkpoint form the guide asks for (T2, 09/20/2026)

The field is a numbered **Checkpoints** table, one column headed "Checkpoint - what the model must
do". Fourteen rows. The step count was predicted over 100 on the platform's count and measured on
09/20/2026 at 209, 165 and 213 tool calls on G1, G2 and G3, one assistant turn each. Entered at
the midpoint of the run set, three of five Gemini runs at a 23.2% mean.

---

## Paste-ready - the section 1.3 Checkpoints table

**Paste the table only.** Everything outside it is repo notes.

| # | Checkpoint - what the model must do |
|:---:|:---|
| 1 | Read the Finance Manager's 09/01/2026 request and take from it the page, the seven columns, the definition of a current employee, what the summary states, the BambooHR ask, the form and the fence. |
| 2 | Establish who is employed by Troutly on 08/31/2026: 52 on the roster and the org chart; BambooHR's 57 active rows hold four contractors and three ended records and lack two hires. |
| 3 | Find the rules that govern PTO at 08/31/2026. The cutover memo of 06/20/2026, effective 07/01/2026, replaces the 2025 policy; the handbook incorporates it and says wiki pages do not set policy; the Paid Time Off page and the 2025 policy say monthly accrual and unlimited carryover and are superseded. |
| 4 | Establish each employee's opening balance: the SplinterHR archive's 06/30/2026 balance, capped at 40.0 hours. The HRIS report, the load file and the July close carry the balances uncapped; eleven exceed the cap. |
| 5 | Establish the periods posted by 08/31/2026: four biweekly pay dates, 07/10, 07/24, 08/07 and 08/21/2026, from the payroll procedures memo; the fifth pays 09/04/2026. |
| 6 | Establish each employee's adjusted service date. Nine migrated records read 07/01/2026 in BambooHR and on the roster and carry their true dates in the archive and the historical offer letters. TRT-0071 rehired 04/22/2024 after a 241-day break and bridges to 03/08/2021 under handbook 7.6. |
| 7 | Establish each period's tier from the adjusted service date: 80 under two years, 120 under five, 160 at five and over, the change in the period containing the anniversary. TRT-0018 reaches five years on 08/09/2026 inside the fourth period. Six BambooHR policies are wrong. |
| 8 | Establish the part-time accrual: TRT-0141 at 25 hours until 08/09/2026 and 32 from 08/10/2026 per the schedule change form, pro-rata under 30 hours per handbook 2.2. |
| 9 | Deduct the approved time off recorded in BambooHR: 24 requests, 560 hours, all in July. |
| 10 | Establish the rate on file with the signed changes applied: TRT-0088 at $118,000.00 from 06/16/2026 by the promotion approval, TRT-0117 at $148,200.00 from 05/16/2026 by the amendment, TRT-0096 at $61,000.00 from the 08/17/2026 step her offer letter and handbook 5.4 carry. BambooHR, the roster and every register carry the old rates. |
| 11 | Compute each row: the balance to two decimals, the hourly rate to four, the liability to the cent; total the rounded rows. |
| 12 | Write the page: the summary with the count, the total hours and the total liability, then the table with the seven columns, an employee ID on every row; publish under the exact title. |
| 13 | Bring BambooHR to the schedule: assign the six policies, set the 52 balances, create the rows for TRT-0153 and TRT-0155. |
| 14 | Read the page and the BambooHR rows back and confirm each against the schedule, from the records rather than from the arguments of the calls that wrote them. |

---

## The dependency chain, stated

- **3 is a choice between documents, and nothing in the request makes it.** A run that stops at
  the wiki page or the July detail carries monthly accrual, no cap and the loaded tiers into 4,
  5 and 7.
- **4 cannot precede 3.** The cap is in the memo and nowhere on the report.
- **6 is a comparison the request does not announce.** The roster and BambooHR agree on
  07/01/2026 for nine people; only the archive and the offer letters disagree.
- **7 depends on 6, and 13 depends on 7.** A tier carried wrong into 7 is a policy written wrong
  into BambooHR.
- **10 is a choice between a record and a signed document.** Three records agree and are wrong.
- **11 depends on 4 to 10; 12 and 13 on 11.** One rule missed is a wrong total and a wrong
  BambooHR row.
- **14 is a read-back, and it is part of the work.** The rows that grade publication and the
  BambooHR state read the records.
