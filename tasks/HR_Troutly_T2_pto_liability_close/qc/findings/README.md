# findings

Each AutoQC round is archived here verbatim before it is triaged, and the register beside this
folder, `../README.md`, carries the verdicts. A run set is archived as `run_set_MM-DD-YYYY/` by
`../archive_run_set.py`: each run's page as the app returned it, `<run>_pto_liability.md`, its
BambooHR writes with the app's results, `<run>_bamboohr_writes.json`, and a `runs.json` with the
model, trajectory id, tool-call count, snapshot ids and the verifier set read off the export.

`run_set_09-20-2026/` holds G1 to G5, the five Gemini 3.8 Flash runs. The prompt round of 09/20/2026 is at `prompt_round1_09-20-2026.md`, transcribed from two
screenshots of its Major tab with the disputes as posted; the Passed and Neutral tabs were not
captured. The first rubric round, run after the import was loaded, is at
`task_round1_09-20-2026.md`, transcribed from three screenshots.
