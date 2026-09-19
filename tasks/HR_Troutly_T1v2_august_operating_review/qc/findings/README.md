# findings

Each AutoQC round is archived here verbatim before it is triaged, and the register beside this
folder, `../README.md`, carries the verdicts. A run set is archived as `run_set_MM-DD-YYYY/`, each
run's two published pages as the export carries them plus a `runs.json` with the model, trajectory
id and step count read off the export, and `python3 qc/score_run_set.py --set <folder>` grades it.
No round and no run set has landed on v2.
