# Onboarding Data Standards

*Status: ACTIVE*

This page covers how we enter new hires into the HRIS. It's the short version — if you need the field-by-field detail, see the [Field Mapping Workbook](/HR/Data/Migration/2026-06-24_Field_Mapping_Workbook.xlsx). Everything here applies from the 07/01/2026 cutover forward.

## Who this is for

Anyone adding a new record to BambooHR — People Ops, the Office Manager, or whoever is covering onboarding that week. Keep it consistent so payroll, benefits, and PTO all pick the record up cleanly on the next cycle.

## Hire date

Enter the hire date in **MM/DD/YYYY** format. Pull it straight from the **signed offer letter** — not the acceptance email, not the calendar invite, not what the candidate told you on a call. If the start date got pushed after signing, the amendment or the confirmation email that both parties acknowledged is what governs, but the offer letter is still the anchor document in the file.

We don't backdate. If someone starts on a Tuesday because Monday was a holiday, the hire date is the Tuesday.

## Legal name

The legal name in the HRIS has to **match the I-9** exactly — same spelling, same hyphens, same middle name (or lack of one). Preferred name goes in the preferred name field, not the legal name field. Payroll and benefits both key off legal name, so a mismatch here creates work later.

## Job title

Pick a title that is on the **current leveling guide**. If a hiring manager wants to use a title that isn't listed (Staff Engineer, Senior CSM, Lead X, etc.), map it to the recognized level per the leveling guide synonyms and enter that. Free-text titles break comp-band reporting and slow down the census.

## Adjusted service date

Default the **adjusted service date** to the hire date. The exception is rehires: if the break in service was less than **365 days**, the adjusted service date **bridges** back to the original hire date so PTO tier and tenure recognitions carry through. If the break is 365 days or more, the adjusted service date resets to the rehire date.

If you're not sure whether a rehire falls inside or outside 365 days, count from last day worked to first day back and check with People before saving the record.

## Manager

Pull the manager assignment from the current **org chart**. Don't guess from the offer letter — offer letters sometimes name a hiring manager who isn't the direct people manager once the person actually starts. The org chart is the tiebreaker.

## Data validation

For the July 2026 HRIS migration, all 56 loaded records were validated via the 07/22/2026 close-out memo; hire dates and salaries were spot-checked and confirmed clean. Follow-up validation is not required. See the [Migration Close-Out Memo](/HR/Data/Migration/2026-07-22_Migration_Closeout_Memo.docx) for the full write-up.

For net-new hires added after cutover, the two things worth eyeballing before you save are the hire date (against the signed offer) and the salary (against the signed offer, in annual dollars, not per-period). Everything else the system will validate on its own.

## Where things live

- Signed offer letters: `/HR/Comp/Offer_Letters/`
- I-9 and onboarding packet: `/HR/People/Onboarding/`
- Leveling guide: Wiki → Compensation Authority
- Org chart: `/HR/Org/` (dated PDF, use the latest)

## Related pages

- [Field Mapping Workbook](/HR/Data/Migration/2026-06-24_Field_Mapping_Workbook.xlsx)
- [Migration Close-Out Memo](/HR/Data/Migration/2026-07-22_Migration_Closeout_Memo.docx)
- Compensation Authority
- Offboarding Checklist

---

*Last edited: 07/25/2026 by Grayson Oshimoto*
