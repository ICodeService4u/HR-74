# Prompt AutoQC round 1 - 09/19/2026

Archived from the interface on 09/19/2026 by the package owner, verbatim but for the register:
the round's curly quotes and em dashes are ASCII here. Two findings, both marked major. The
verdicts are in `../README.md`.

## [P1] Prompt Validity - Long-Horizon and Realistic

The attached operating-review request, which the prompt directs the agent to complete,
prescribes the analysis method: "For Board approval, read the 06/20/2026 Board-approved hiring
plan and the Board minutes of that meeting, and no other record," and it further directs which
pages and org chart govern specific determinations. It also gives the stale People Metrics and
Hiring Plan figures ("57 people and 8 open requisitions" and "8 roles at $868,000.00"),
signaling the reconciliation conflict instead of leaving it to be discovered. Replace these
source-priority instructions and baseline findings with an outcome-focused request that lets the
agent identify the relevant evidence and reconciliation issues.

## Outcome-Determining Choices Pinned in the Prompt (consolidated)

The operating-review memo's Staffed Role View instruction says to "Count people the way the
People Metrics page describes," and People Metrics defines that as "HRIS active records as of the
page date." Yet the August 31 Master Employee Roster states that its Employees tab covers "All
active employees as of the as-of date," producing 52 employees, while BambooHR supplies 53 active
employee records excluding contractors; the prompt never states which source controls the
published count and rows. It also leaves REQ-2026-038 ambiguous: the ATS export shows it "Open"
while the signed offer shows it was accepted on 08/20/2026, so the required hiring-status field
can defensibly be Open or Offer accepted; specify a source hierarchy and status precedence to fix
both defects.
