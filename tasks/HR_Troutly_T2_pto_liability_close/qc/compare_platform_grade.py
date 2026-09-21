#!/usr/bin/env python3
"""Read a platform grading back against the verifiers' own verdicts on the archived run.

    python3 qc/compare_platform_grade.py --set run_set_09-21-2026 G5

The platform grades the snapshot its own harness hands each verifier; this package grades the
bytes the export shows the apps returned. Where the two disagree, one of them is reading
something the other cannot see, and the disagreement is the measurement: which rows, which
target app, and whether the rows that agree are the ones that pass on inaction.

The transcribed grade is <run>_platform_grade.json under the set, typed from the grading pane
and nothing else: the passed rows, the weighted sum, the total and the metrics each row printed.
Every figure this script prints is recomputed here and the transcription's own arithmetic is
asserted against the plan's weights, so a mistyped grade fails rather than publishes.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
os.environ["T2_VERIFIER_QUIET"] = "1"
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(PKG, "build"))
import build_package_artifacts as B  # noqa: E402
import scenarios as S  # noqa: E402
import score_run_set as SC  # noqa: E402


def compare(set_name, run):
    folder = os.path.join(HERE, "findings", set_name)
    grade = json.load(open(os.path.join(folder, "%s_platform_grade.json" % run), encoding="utf8"))
    weights = {i + 1: r[1] for i, r in enumerate(B.PLAN)}
    targets = {i + 1: r[9]["target"] for i, r in enumerate(B.PLAN)}
    assert grade["verifier_count"] == len(B.PLAN), "the grade carries %d verifiers, the plan %d" % (
        grade["verifier_count"], len(B.PLAN))
    assert grade["total_weights"] == sum(weights.values()), "the grade totals %d, the plan %d" % (
        grade["total_weights"], sum(weights.values()))
    platform = {n: n in set(grade["passed_rows"]) for n in weights}
    assert sum(weights[n] for n in platform if platform[n]) == grade["weighted_sum"], \
        "the grade's weighted sum is not the weights of the rows it passed"
    assert grade["passes"] + grade["fails"] == len(weights), "passes and fails do not cover the set"

    text = open(os.path.join(folder, "%s_pto_liability.md" % run), encoding="utf8").read()
    pol, bal, _ = SC.bamboo_state(os.path.join(folder, "%s_bamboohr_writes.json" % run))
    hires = {h: S.HIRES[h] for h in S.HIRES if h in bal}
    runs = {r["run"]: r for r in json.load(open(os.path.join(folder, "runs.json"), encoding="utf8"))}
    published = bool((runs[run].get("page") or {}).get("published"))
    ctx = S.snap([(B.PAGE, text, 1 if published else 0)], S.bamboo_tables(pol, bal, hires))
    archive = SC.verdicts(ctx, SC.checks())

    print("| Row | Target | Weight | The platform | The archived bytes |")
    print("|---|---|---|---|---|")
    for n in sorted(weights):
        print("| %d | %s | %d | %s | %s |" % (n, targets[n], weights[n],
                                              "pass" if platform[n] else "fail",
                                              "pass" if archive[n] else "fail"))
    agree = [n for n in weights if platform[n] == archive[n]]
    differ = [n for n in weights if platform[n] != archive[n]]
    lost = sum(weights[n] for n in differ)
    by_target = {}
    for n in differ:
        by_target.setdefault(targets[n], []).append(n)
    print("")
    print("%s, %s: the platform scored %d of %d, %.1f%%; the archived bytes score %d of %d, %.1f%%"
          % (run, grade["graded_on"], grade["weighted_sum"], grade["total_weights"],
             100.0 * grade["weighted_sum"] / grade["total_weights"],
             sum(weights[n] for n in archive if archive[n]), sum(weights.values()),
             100.0 * sum(weights[n] for n in archive if archive[n]) / sum(weights.values())))
    print("%d rows agree, %d differ, %d points" % (len(agree), len(differ), lost))
    for target in sorted(by_target):
        rows = sorted(by_target[target])
        print("  %s: rows %s, every one of them read on the %s target"
              % (target, ", ".join(str(n) for n in rows), target))
    for target in sorted(set(targets.values())):
        rows = [n for n in weights if targets[n] == target]
        same = [n for n in rows if platform[n] == archive[n]]
        both_fail = [n for n in same if not archive[n]]
        print("  %s rows: %d of %d agree, %d of the agreements a fail on both readings"
              % (target, len(same), len(rows), len(both_fail)))
    return differ


def main():
    set_name = "run_set_09-21-2026"
    if "--set" in sys.argv:
        set_name = sys.argv[sys.argv.index("--set") + 1]
    runs = [a for a in sys.argv[1:] if not a.startswith("--") and a != set_name]
    for run in runs or ["G5"]:
        compare(set_name, run)
    return 0


if __name__ == "__main__":
    sys.exit(main())
