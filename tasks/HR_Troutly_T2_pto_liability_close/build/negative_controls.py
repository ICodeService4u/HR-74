"""Negative controls: plant a defect, confirm the guard goes red, revert the edit.

HR 32's section 8.6, carried through HR 79 and T1: a guard you have never seen fail is a guard
you do not have. Every guard this prompt-half package relies on is made to fail here once, on a
deliberate edit of its own source, and the edit is reverted whether the control passes or not.

    python3 build/negative_controls.py

It resolves the package from its own location, so it runs from any working directory. Every
control must go red or the run exits non-zero. The README's control table is this script's
output and nothing else.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(PKG))
SRC = os.path.join(PKG, "build/task_input_source.md")
BLD = os.path.join(PKG, "build/build_package_artifacts.py")
TIB = os.path.join(PKG, "build/build_task_input.py")
PROMPT_MD = os.path.join(PKG, "01_prompt.md")
META_MD = os.path.join(PKG, "02_task_metadata.md")
FA_MD = os.path.join(PKG, "06_failure_analysis.md")
README_MD = os.path.join(PKG, "README.md")
SELECT = os.path.join(REPO, "tasks", "check_selection_blocks.py")


def run(script, args=()):
    return subprocess.run([sys.executable, script, *args], cwd=PKG, capture_output=True, text=True)


def control(label, path, old, new, script, args=(), expect=None):
    original = open(path, encoding="utf8").read()
    assert old in original, "control %r: anchor not found" % label
    open(path, "w", encoding="utf8").write(original.replace(old, new, 1))
    try:
        r = run(script, args)
        red = r.returncode != 0
        out = (r.stderr or r.stdout).strip()
        msg = out.splitlines()[-1] if out else ""
        if expect:
            red = red and expect in (r.stderr + r.stdout)
    finally:
        open(path, "w", encoding="utf8").write(original)
    print("%-6s %-60s %s" % ("RED" if red else "GREEN!!", label, msg[:100]))
    return red


ok = []
# ---- the memo's leak, shape, date, seat and content guards
ok.append(control("memo: the cap leaked", SRC, "with a short summary above one table.",
                  "with a short summary above one table, the opening balance capped at 40.0 hours.", TIB))
ok.append(control("memo: the accrual period leaked", SRC, "Use 08/31/2026 as the measurement date.",
                  "Use 08/31/2026 as the measurement date, biweekly.", TIB))
ok.append(control("memo: a tier value leaked", SRC, "annual PTO tier\nin hours,", "annual PTO tier\nin hours (80 hours, 120 hours or 160 hours),", TIB))
ok.append(control("memo: a policy document named", SRC, "Grayson prepared the July detail",
                  "The cutover memo sets the rules. Grayson prepared the July detail", TIB))
ok.append(control("memo: the service-date basis leaked", SRC, "PTO balance in hours at 08/31/2026,",
                  "PTO balance in hours at 08/31/2026 by adjusted service date,", TIB))
ok.append(control("memo: the rehire rule leaked", SRC, "and dollar liability.", "and dollar liability, prior service bridged.", TIB))
ok.append(control("memo: the part-time rule leaked", SRC, "and dollar liability.", "and dollar liability, part-time pro-rata.", TIB))
ok.append(control("memo: a signed change leaked", SRC, "Once the page is published,", "Apply every signed promotion first. Once the page is published,", TIB))
ok.append(control("memo: one of the eight names", SRC, "Once the page is published,", "Featherstone is on the schedule. Once the page is published,", TIB))
ok.append(control("memo: the total leaked", SRC, "the total\ndollar liability.", "the total\ndollar liability, about $92,739.", TIB))
ok.append(control("memo: a record called wrong", SRC, "bring BambooHR to it:", "bring BambooHR to it, since its balances are wrong:", TIB))
ok.append(control("memo: a word for checking", SRC, "bring BambooHR to it:", "verify BambooHR against it:", TIB))
ok.append(control("memo: the shape of the answer", SRC, "for every employee on the schedule,", "for every employee on the schedule, whether or not BambooHR agrees,", TIB))
ok.append(control("memo: the definition of a current employee dropped", SRC,
                  "A current\nemployee is anyone employed by Troutly on 08/31/2026.", "", TIB))
ok.append(control("memo: the seat", SRC, "| **To** | Casey Ouk, People Operations Analyst |", "| **To** | Anjelina Brocollini, Head of People |", TIB))
ok.append(control("memo: an unlicensed date", SRC, "Retain with the August 2026 close package.", "Retain with the August 2026 close package dated 09/05/2026.", TIB))
ok.append(control("names: the upload name the record publishes", TIB, 'UPLOAD_NAME = "pto_liability_request.pdf"', 'UPLOAD_NAME = "pto_liability_request_v2.pdf"', TIB))
# ---- the world guards: every rule the schedule applies is read off its document
ok.append(control("world: the cap", BLD, "CAP = 40.0", "CAP = 45.0", BLD))
ok.append(control("world: the posted periods", BLD, 'ASOF = "08/31/2026"', 'ASOF = "09/05/2026"', BLD))
ok.append(control("world: the rehire bridging rule", BLD, "BRIDGE_UNDER_DAYS = 365", "BRIDGE_UNDER_DAYS = 200", BLD))
ok.append(control("world: the step", BLD, "STEP = 3000.0", "STEP = 2000.0", BLD))
ok.append(control("world: the tier boundaries", BLD, "TIERS = [(2, 80), (5, 120), (999, 160)]", "TIERS = [(3, 80), (5, 120), (999, 160)]", BLD))
ok.append(control("world: a signed rate dropped", BLD, 'if f["signed"] and i in SIGNED and SIGNED[i][1] <= ASOF_DATE:', 'if False:', BLD))
ok.append(control("world: the part-time schedule", BLD, "PART_TIME_UNDER = 30", "PART_TIME_UNDER = 20", BLD))
ok.append(control("world: a phrase the cutover memo must carry", BLD, '"capped at 40.0 hours as of 06/30/2026"', '"capped at 40.0 hours as of 07/31/2026"', BLD))
ok.append(control("world: the population", BLD, 'if f["population"]:\n        people = [e for e in ROSTER_ROWS if e["status"] == "Active" and e["type"] == "Employee"]',
                  'if f["population"]:\n        people = [e for e in ROSTER_ROWS if e["status"] == "Active" and e["id"] in BAMBOO]', BLD))
# ---- the plan guards
ok.append(control("plan: weight band", BLD, '("determination", 10, "Critical value"', '("determination", 15, "Critical value"', BLD))
ok.append(control("plan: the gate demoted off the total", BLD, '("determination", 10, "Critical value"', '("determination", 9, "Critical value"', BLD))
ok.append(control("plan: a row not opening on States", BLD, '"States that a Wiki.js page titled %s is published." % PAGE', '"A Wiki.js page titled %s is published." % PAGE', BLD))
ok.append(control("plan: the free base over a tenth", BLD, '("free", 2, "-", "States, on the PTO liability page, the %d current employees', '("free", 9, "-", "States, on the PTO liability page, the %d current employees', BLD))
ok.append(control("plan: the golden not scoring every point", BLD, 'return bal_ok("TRT-0018", s)',
                  'return "TRT-0018" in by(s) and _same(by(s)["TRT-0018"]["balance"], 24.6154, 0.005)', BLD))
ok.append(control("plan: a hours row read off a column the page does not carry", BLD, 'return bal_ok("TRT-0141", s)',
                  'return "TRT-0141" in by(s) and _same(by(s)["TRT-0141"]["accrued"], 8.8462, 0.0001) and False', BLD))
ok.append(control("plan: P0 scoring over a fifth", BLD, "return _same(t, TOTAL, 0.005) or _same(t, TOTAL_POSTED, 0.005)", "return True", BLD))
# ---- the show-your-work guard
ok.append(control("syw: a total the build did not write", BLD, 'total_cell = _money(TOTAL)', 'total_cell = _money(TOTAL + 1)', BLD, ["--docs"]))
ok.append(control("syw: a semicolon joining two clauses", BLD, 'Ended employees out. Wiki pages do not set policy.', 'Ended employees out; wiki pages do not set policy.', BLD, ["--docs"]))
# ---- the docs guards
ok.append(control("docs: the prompt blockquote", PROMPT_MD, "about the August 2026 close", "about the August close", BLD, ["--docs"]))
ok.append(control("docs: a stale figure in the record", META_MD, "$92,739.54", "$92,739.45", BLD, ["--docs"]))
ok.append(control("docs: a stale path score in the predictions", FA_MD, "| P3 | ", "| P3x | ", BLD, ["--docs"]))
ok.append(control("docs: a planned row missing from the record", META_MD, "States, on the PTO liability page, no contractor row, CTR-2001 to CTR-2004.", "States, on the PTO liability page, no contractor row.", BLD, ["--docs"]))
ok.append(control("docs: a selection dropped from the block", META_MD, "\nHR/Benefits/2026-08-10_Schedule_Change_TRT-0141.pdf\n", "\n", BLD, ["--docs"]))
ok.append(control("docs: a file missing from the README", README_MD, "`build/task_input_source.md`", "`build/task_input_sources.md`", BLD, ["--docs"]))
ok.append(control("docs: a non-ASCII character in a package document", META_MD, "## Fences", "## Fences " + "\u2014", BLD, ["--docs"]))
ok.append(control("selection: a wildcard in the block", META_MD, "\nbamboohr/Employee.csv\n", "\nbamboohr/*.csv\n", SELECT))

print("\n%d of %d controls went red" % (sum(ok), len(ok)))
if not all(ok):
    sys.exit(1)
