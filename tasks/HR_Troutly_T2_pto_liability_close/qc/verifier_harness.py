#!/usr/bin/env python3
"""Run every generated verifier against a battery of snapshots with the answer known.

    python3 qc/verifier_harness.py            # every row against every scenario
    python3 qc/verifier_harness.py --row 8    # one row, with its details printed

Studio's per-verifier test-run reports whether the code RAN. This reports whether its verdict is
RIGHT, which the platform cannot ask because nothing on it knows the right answer. The fixture is
a Wiki.js `pages` table in the documented column order, seeded with the ten world pages from
apps_data/wiki_js/Page.csv plus whatever the scenario publishes, beside the BambooHR tables built
from the six seed CSVs under apps_data/bamboohr with the app's integer ids as the run set observed
them, under placeholder column names by default and real names on demand. The correct state is
the golden page and BambooHR brought to the schedule, so this is also the proof that the golden
scores 100 on the rubric.

Every scenario names the rows it expects to FAIL. A row that fails a scenario it should pass is a
false zero; a row that passes a scenario it should fail is a FALSE PASS, which is the defect class
that silently credits a run that did nothing, and the one this battery exists to catch.
"""
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(PKG, "build"))
from ctx import Ctx  # noqa: E402
from scenarios import BATTERY, ROWS  # noqa: E402


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    only = None
    details = "--details" in sys.argv
    if "--row" in sys.argv:
        only = int(sys.argv[sys.argv.index("--row") + 1])
        details = True
    vdir = os.path.join(HERE, "verifiers")
    files = sorted(f for f in os.listdir(vdir) if f.startswith("row") and f.endswith(".py"))
    assert len(files) == ROWS, "%d verifier files against %d rubric rows" % (len(files), ROWS)
    checks = {int(f[3:5]): _load(os.path.join(vdir, f), f[:-3]).check for f in files}
    bad, total = 0, 0
    for label, factory, failing, why in BATTERY:
        ctx = factory()
        for n in sorted(checks):
            if only and n != only:
                continue
            expected = not (failing == "all" or n in failing)
            try:
                out = checks[n](ctx)
                got = bool(out.get("passed"))
                err = ""
            except Exception as exc:
                got, out, err = None, {}, "RAISED %s: %s" % (type(exc).__name__, exc)
            total += 1
            ok = got == expected
            if not ok:
                bad += 1
                print("%-10s row %02d  %-46s expected %-5s got %-5s %s"
                      % ("FALSE PASS" if got else "WRONG", n, label, expected, got, err))
                print("           why it is in the battery: %s" % why)
                if out.get("details"):
                    print("           last line: %s" % (out["details"].strip().splitlines() or [""])[-1][:160])
            if details and out.get("details"):
                print("---- row %02d on %r\n%s\n" % (n, label, out["details"][:2500]))
    print("\n%d of %d verdicts correct across %d scenarios and %d rows"
          % (total - bad, total, len(BATTERY), len([n for n in checks if not only or n == only])))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
