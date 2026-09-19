#!/usr/bin/env python3
"""Score an archived run set against the rubric, the way 06_failure_analysis.md reports it.

    python3 qc/score_run_set.py                       # the set archived on 09/19/2026
    python3 qc/score_run_set.py --set run_set_09-19-2026 --details 8

Each run's two published pages are read from qc/findings/<set>/<run>_<page>.md, exactly as the
trajectory export carries them, and dropped into the harness fixture beside the ten seed pages,
under placeholder column names. The verifier files under qc/verifiers/ then grade them, so the
numbers in the record recompute from the archived bytes on every run of this script and never
live in a cell. runs.json in the same folder carries each run's model, trajectory id and step
count, read off the export by the archiving step and never typed.
"""
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(PKG, "build"))
from scenarios import snap, A, Bt  # noqa: E402
import build_package_artifacts as B  # noqa: E402

PAGE_FILES = {A: "approved_hiring_view", Bt: "staffed_role_view"}


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def score(set_name, details=None):
    folder = os.path.join(HERE, "findings", set_name)
    runs = json.load(open(os.path.join(folder, "runs.json"), encoding="utf8"))
    vdir = os.path.join(HERE, "verifiers")
    files = sorted(f for f in os.listdir(vdir) if f.startswith("row") and f.endswith(".py"))
    checks = {int(f[3:5]): _load(os.path.join(vdir, f), f[:-3]).check for f in files}
    weights = {i + 1: c[2] for i, c in enumerate(B.RUBRIC)}
    total = sum(weights.values())
    out = []
    for r in runs:
        pages = []
        for title, short in PAGE_FILES.items():
            p = os.path.join(folder, "%s_%s.md" % (r["run"], short))
            if os.path.exists(p):
                pages.append((title, open(p, encoding="utf8").read()))
        ctx = snap(pages)
        verdicts = {}
        for n in sorted(checks):
            try:
                res = checks[n](ctx)
                verdicts[n] = bool(res.get("passed"))
                if details == n:
                    print("---- %s row %02d\n%s\n" % (r["run"], n, res.get("details", "")[-900:]))
            except Exception as exc:  # a raise is a zero, and it is printed
                verdicts[n] = False
                print("%s row %02d RAISED %s: %s" % (r["run"], n, type(exc).__name__, exc))
        points = sum(weights[n] for n in verdicts if verdicts[n])
        out.append((r, points, verdicts))
    return out, weights, total


def main():
    set_name = "run_set_09-19-2026"
    details = None
    if "--set" in sys.argv:
        set_name = sys.argv[sys.argv.index("--set") + 1]
    if "--details" in sys.argv:
        details = int(sys.argv[sys.argv.index("--details") + 1])
    out, weights, total = score(set_name, details)
    print("| Run | Model | Steps | Score | Rows failed |")
    print("|---|---|---|---|---|")
    by_model = {}
    for r, points, v in out:
        failed = [n for n in sorted(v) if not v[n]]
        print("| %s | %s | %d | %d of %d, %.1f%% | %s |" % (
            r["run"], r["model"], r["tool_calls"], points, total, 100.0 * points / total,
            ", ".join(str(n) for n in failed) or "none"))
        by_model.setdefault(r["model"], []).append(100.0 * points / total)
    print()
    for m, xs in by_model.items():
        print("%s: %d run%s, mean %.1f%%, low %.1f%%, high %.1f%%" % (
            m, len(xs), "" if len(xs) == 1 else "s", sum(xs) / len(xs), min(xs), max(xs)))
    print()
    print("rows failed by run (X fails):")
    tags = [r["run"] for r, _, _ in out]
    print("         " + " ".join("%-4s" % t[:4] for t in tags))
    for n in sorted(weights):
        marks = ["X" if not v[n] else "." for _, _, v in out]
        if "X" in marks:
            print("row %02d w%-2d %s" % (n, weights[n], "    ".join(marks)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
