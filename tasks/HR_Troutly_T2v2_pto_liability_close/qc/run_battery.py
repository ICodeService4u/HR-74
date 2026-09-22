#!/usr/bin/env python3
"""Run a verifier's check(ctx) against a battery of scenarios.

    python3 kit/run_battery.py <check.py> <scenarios.py>

`scenarios.py` must define BATTERY: a list of (label, ctx_factory, expected_passed, why).
`why` is printed only when the check gets that scenario wrong, so write it as the reason the
scenario is in the battery at all.

A check that scores anything less than all of them is not ready to import, whatever the
per-verifier test-run says.
"""
import argparse, importlib.util, os, sys, traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("check")
    ap.add_argument("scenarios")
    ap.add_argument("--details", action="store_true",
                    help="print each run's details string - do this once before you ship, and "
                         "read it: a check whose details you cannot follow is one you cannot "
                         "debug from a grading run")
    args = ap.parse_args()

    check = _load(args.check, "check_under_test").check
    battery = _load(args.scenarios, "scenarios").BATTERY

    bad = 0
    print("%d scenarios against %s\n" % (len(battery), os.path.basename(args.check)))
    for label, factory, expected, why in battery:
        err = ""
        out = {}
        try:
            out = check(factory())
            got = bool(out.get("passed"))
        except Exception as exc:
            got = None
            err = "RAISED %s: %s" % (type(exc).__name__, exc)
        ok = got == expected
        bad += 0 if ok else 1
        print("%-7s %-52s expected %-5s got %-5s %s"
              % ("ok" if ok else ("FALSE PASS" if got else "WRONG"), label, expected, got, err))
        if not ok:
            print("        why it is in the battery: %s" % why)
            if err:
                print("        " + "\n        ".join(traceback.format_exc().splitlines()[-3:]))
            elif out.get("details"):
                print("        last line of details: "
                      + (out["details"].strip().splitlines() or [""])[-1][:150])
        if args.details and not err:
            print("        " + (out.get("details") or "").replace("\n", "\n        ")[:1200])
    print("\n%d of %d correct" % (len(battery) - bad, len(battery)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
