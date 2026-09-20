# The task AutoQC register - T1 v2, Approved Hiring and Staffed Role Views

**One prompt round has run on v2, and no task round.** The prompt round of 09/20/2026 is archived
verbatim at `findings/prompt_round1_09-20-2026.md` and answered below. It landed before any v2
trajectory. The run set of the same day is at `findings/run_set_09-20-2026/` and retired the
package; `../06_failure_analysis.md` carries it. Archive each later round verbatim to `findings/prompt_roundN_MM-DD-YYYY.md` or
`findings/task_roundN_MM-DD-YYYY.md` before triaging it, and keep the verdicts here. T1's prompt
round of 09/19/2026 is answered in v2's design and recorded in `../01_prompt.md`.

| Round | Date | Findings | Verdict |
|---|---|---|---|
| Prompt round 1 | 09/20/2026 | One major. Outcome-Determining Choices: the memo never says the roster overrides BambooHR, BambooHR carries 53 non-contractor active rows against the roster's 52, and the round reads the two as defensible outputs. It asks for a source hierarchy naming the roster as authoritative | **Disputed, and the run set decides.** The hierarchy asked for is the clause T1 carried and measured: nine of nine runs healed the population when the memo named the sources. The memo's definition is a fact, not a choice. Three of the 53 read Terminated on the crosswalk, with termination dates of 03/20/2026, 05/08/2026 and 06/15/2026 on the SplinterHR archive, and are on neither the August org chart nor the roster. Two of the 52 read Never Loaded, each with a Greenhouse hire and an org chart box. Handbook 3.2 makes the HRIS the system of record and in the same clause says a record can disagree with a signed document and be corrected. A stale Active flag is not employment. The verifiers the round read are the synth's twenty; the package's rubric grades the set of 52, not a count. Under 40% on five Gemini runs the finding is the measured failure; over 60% the package retires on its own rule and the finding is moot. The set of 09/20/2026 decided it: four of four runs produced 52 and none carried 53 past a sentence |

## The verifier harness

`python3 qc/verifier_harness.py`, 09/19/2026: **864 of 864 verdicts correct**, 24 rows across
36 scenarios. The scenarios that matter most:

| Scenario | What it proves |
|---|---|
| the golden pages, under real and placeholder column names, with em-dash titles and as HTML | the golden scores 100 on every row in every form |
| P1, P1b and P1c as pages | the three registered failing paths score 27 of 83, 32.5%, 31 of 83, 37.3% and 40 of 83, 48.2% by the verifier files themselves |
| the wiki page's eight roles read as the Board plan | the second failing path fails the three Board rows and the budget |
| the staffed tables emptied, and thinned to five rows | a table with no rows is no table to the parser; five rows are, and absence from five rows shows nothing, which is the populated-table floor |
| P1c | 52 rows by arithmetic with three wrong people: the gate reads the set, not the count |
| a requisition keyed with a note beside it, the summary in a bulleted list | the forms T1's runs used are not failed |
| nothing written, the golden only in page history | a check reading the wrong table passes a run that did nothing |

**What the battery found on the way.** The first expected sets were wrong twice and the engine
was right both times: BambooHR less the contractors is 53 rows with 31 of them holding no open
title, so the no-requisition split passes on P1b by arithmetic; and a summary that states 57 for
the total still states the six department counts. Both are in the scenarios' own rationale. The controls found a third: the populated-table
guard's control went green against the emptied page, because a table with no rows never reaches
the guard; the thin-table scenario is the one that exercises it, and the control went red on it.

## What a round is likely to raise, and the answer already on file

- **Rubric Realism, that no row grades a file.** The deliverable is two wiki pages and no file.
- **Verifier Type, that every row is App DB.** Same answer.
- **The count source and the status of REQ-2026-038**, T1's prompt round. The memo defines a
  current employee and each status value; it names no source, and the world's records settle
  the rest. The v2 round of 09/20/2026 raised the count source again and is answered above.
- **That the memo names no source.** That is the design: T1 measured nine of nine runs following
  the sources the memo named. `../01_prompt.md` carries the record.
