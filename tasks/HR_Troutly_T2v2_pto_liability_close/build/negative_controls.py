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
ENG = os.path.join(PKG, "build/verifier_engine.py")
SCN = os.path.join(PKG, "qc/scenarios.py")
VH = os.path.join(PKG, "qc/verifier_harness.py")
PROMPT_MD = os.path.join(PKG, "01_prompt.md")
META_MD = os.path.join(PKG, "02_task_metadata.md")
FA_MD = os.path.join(PKG, "06_failure_analysis.md")
README_MD = os.path.join(PKG, "README.md")
NINE_MD = os.path.join(PKG, "09_rubric_import.md")
GUIDE_MD = os.path.join(PKG, "07_paste_guide.md")
SELECT = os.path.join(REPO, "tasks", "check_selection_blocks.py")


def run(script, args=()):
    return subprocess.run([sys.executable, script, *args], cwd=PKG, capture_output=True, text=True)


def control(label, path, old, new, script, args=(), expect=None, pre=None):
    """Plant `new` for `old` in `path`, run `script` (after `pre`, which regenerates what the
    planted file feeds, the row files from the engine), expect red, revert. After the revert
    `pre` runs again, so the row files carry the clean engine and not the planted one."""
    original = open(path, encoding="utf8").read()
    assert old in original, "control %r: anchor not found" % label
    open(path, "w", encoding="utf8").write(original.replace(old, new, 1))
    try:
        if pre:
            run(pre)
        r = run(script, args)
        red = r.returncode != 0
        out = (r.stderr or r.stdout).strip()
        msg = out.splitlines()[-1] if out else ""
        if expect:
            red = red and expect in (r.stderr + r.stdout)
    finally:
        open(path, "w", encoding="utf8").write(original)
        if pre:
            run(pre)
    print("%-6s %-62s\t%s" % ("RED" if red else "GREEN!!", label, msg[:96]))
    return red


ASK = "The page states the total PTO liability in dollars and the total PTO hours, and the PTO hours"
CLOSE = "Troutly Analytics, Inc. - internal."
NEED = "### What I need\n"
DEFN = "A\ncurrent employee is anyone employed by Troutly on 08/31/2026."

ok = []
# ---- the memo's leak, shape, date, seat and content guards
ok.append(control("memo: the cap leaked", SRC, ASK, ASK + " Carryover was capped at 40.0 hours.", TIB))
ok.append(control("memo: the accrual period leaked", SRC, ASK, ASK + " PTO accrues each pay period.", TIB))
ok.append(control("memo: a tier value leaked", SRC, ASK, ASK + " The tiers are 80, 120 and 160 hours.", TIB))
ok.append(control("memo: a policy document named", SRC, "Grayson prepared the July detail",
    "The PTO policy cutover memo of 06/20/2026 governs. Grayson prepared the July detail", TIB))
ok.append(control("memo: the service-date basis leaked", SRC, ASK, ASK + " Tiers run by adjusted service date.", TIB))
ok.append(control("memo: the rehire rule leaked", SRC, ASK, ASK + " Prior service is bridged on a short break.", TIB))
ok.append(control("memo: the part-time rule leaked", SRC, ASK, ASK + " Part-time accrual is pro-rata.", TIB))
ok.append(control("memo: a signed change leaked", SRC, ASK, ASK + " Apply every signed promotion first.", TIB))
ok.append(control("memo: one of the eight names", SRC, ASK, ASK + " Featherstone is on the schedule.", TIB))
ok.append(control("memo: the total leaked", SRC, ASK, ASK + " It runs to about $92,739.", TIB))
ok.append(control("memo: a record called wrong", SRC, ASK, ASK + " The loaded balances are wrong.", TIB))
ok.append(control("memo: a word for checking", SRC, ASK, ASK + " Verify each balance before you publish.", TIB))
ok.append(control("memo: the shape of the answer", SRC, ASK, ASK + " Say whether the figures differ.", TIB))
ok.append(control("memo: the definition of a current employee dropped", SRC, DEFN, "", TIB))
ok.append(control("memo: the seat", SRC, "| **To** | Casey Ouk, People Operations Analyst |",
    "| **To** | Anjelina Brocollini, Head of People |", TIB))
ok.append(control("memo: an unlicensed date", SRC, CLOSE, CLOSE[:-1] + ", dated 09/05/2026.", TIB))
ok.append(control("memo: a fence returning, the Greenhouse line", SRC, CLOSE, "Change nothing in Greenhouse. " + CLOSE, TIB))
ok.append(control("memo: a fence returning, the scope line", SRC, CLOSE, "Payroll changes are no part of this request. " + CLOSE, TIB))
ok.append(control("memo: a deadline returning", SRC, NEED, "### What I need by 09/03/2026\n", TIB))
ok.append(control("memo: a retention line returning", SRC, CLOSE, CLOSE + " Retain with the August 2026 close package.", TIB))
# ---- the lines v2 took out, each of which drew a rubric row the failing tier earned in full
ok.append(control("memo: the Form section returning", SRC, CLOSE,
    "### Form\n\nDates MM/DD/YYYY. Hours to two decimals.\n\n" + CLOSE, TIB))
ok.append(control("memo: the BambooHR ask returning", SRC, CLOSE,
    "### BambooHR\n\nOnce the page is published, bring BambooHR to it.\n\n" + CLOSE, TIB))
ok.append(control("memo: the summary count returning", SRC, ASK,
    ASK.replace("and the PTO hours", "and the number of employees on the schedule, and the PTO hours"), TIB))
ok.append(control("memo: a dropped column returning", SRC, "The figures cover every current employee.",
    "The figures cover every current employee, with the name, department and tier of each.", TIB))
# ---- review round 1 of 09/22/2026: the two lines it took out, each an ask no row could cover
ok.append(control("memo: the per-employee table returning", SRC, "The figures cover every current employee.",
    "The page carries a row for every current employee with the employee ID, the PTO balance in hours and the hourly rate.", TIB))
ok.append(control("memo: the measurement-date line returning", SRC, "One page published in Wiki.js, PTO Liability - 08/31/2026.",
    "One page published in Wiki.js, PTO Liability - 08/31/2026. Use 08/31/2026 as the measurement date.", TIB))
ok.append(control("memo: a line dropped from the ask", SRC, "Engineering, Finance\nand Corporate, Product,", "Engineering, Product,", TIB))
ok.append(control("memo: the one-table shape returning", SRC, "One page published in Wiki.js, PTO Liability - 08/31/2026.",
    "One page published in Wiki.js, PTO Liability - 08/31/2026, with a short summary above one table.", TIB))
# ---- the world's own bytes: a rule read wrong is a schedule read wrong
ok.append(control("world: the cap", BLD, "CAP = 40.0", "CAP = 60.0", BLD))
ok.append(control("world: the posted periods", BLD, "PERIODS_PER_YEAR = 26", "PERIODS_PER_YEAR = 24", BLD))
ok.append(control("world: the rehire bridging rule", BLD, "BRIDGE_UNDER_DAYS = 365", "BRIDGE_UNDER_DAYS = 30", BLD))
ok.append(control("world: the step", BLD, "STEP = 3000.0", "STEP = 0.0", BLD))
ok.append(control("world: the tier boundaries", BLD, "TIERS = [(2, 80), (5, 120), (999, 160)]",
    "TIERS = [(3, 80), (6, 120), (999, 160)]", BLD))
ok.append(control("world: the part-time rule", BLD, "PART_TIME_UNDER = 30", "PART_TIME_UNDER = 20", BLD))
ok.append(control("world: the valuation basis", BLD, "HOURS_PER_YEAR = 2080", "HOURS_PER_YEAR = 2000", BLD))
# ---- the plan: what the weights and the graded cells are held to
ok.append(control("plan: the gate demoted off the total", BLD,
    '("determination", 10, "Critical value",', '("determination", 8, "-",', BLD))
ok.append(control("plan: a row not opening on States", BLD,
    '"States that a Wiki.js page titled %s is published." % PAGE',
    '"A Wiki.js page titled %s is published." % PAGE', BLD))
ok.append(control("plan: the free base over a seventh", BLD, '("free", 1, "-",', '("free", 30, "-",', BLD))
ok.append(control("plan: a cell priced outside its band", BLD,
    "MONEY_BANDS = [(2000.0, 7), (800.0, 6), (250.0, 5), (80.0, 4), (0.0, 3)]",
    "MONEY_BANDS = [(2000.0, 9), (800.0, 6), (250.0, 5), (80.0, 4), (0.0, 3)]", BLD))
ok.append(control("plan: a line the load already carries right, Marketing alone", BLD,
    '("Sales and Marketing", ("Sales", "Marketing"))]', '("Sales", ("Sales",)), ("Marketing", ("Marketing",))]', BLD))
ok.append(control("plan: the golden not scoring every point", BLD,
    "    def line_ok(field, name):", "    def line_ok(field, name):\n        if name == \"Product\":\n            return lambda s: False", BLD))
ok.append(control("plan: over 25 criteria", BLD,
    "    for c in CELLS:\n        n = c[\"line\"]\n        expl, refs = expl_refs(c)",
    "    for c in CELLS * 3:\n        n = c[\"line\"]\n        expl, refs = expl_refs(c)", BLD))
# ---- the rubric and the register
ok.append(control("rubric: a compliance row flagged primary", BLD, '         OC, "No",\n         "One page under that title',
    '         OC, "Yes",\n         "One page under that title', BLD))
ok.append(control("register: punctuation", BLD, '"One page under that title is what the request asks for in Wiki.js, so it exists with its published flag set."',
    '"One page under that title is what the request asks for in Wiki.js; it exists with its published flag set."', BLD))
ok.append(control("register: a spelled month", BLD, '"One page under that title is what the request asks for in Wiki.js, so it exists with its published flag set."',
    '"One page under that title is what the request asks for in Wiki.js on August 31, so it exists with its flag set."', BLD))
ok.append(control("register: grading vocabulary", BLD, '"One page under that title is what the request asks for in Wiki.js, so it exists with its published flag set."',
    '"One page under that title is what the request asks for in Wiki.js, so this criterion passes when the flag is set."', BLD))
ok.append(control("register: no source named", BLD, '"One page under that title is what the request asks for in Wiki.js, so it exists with its published flag set."',
    '"One page under that title is what is wanted, so it exists with its published flag set."', BLD))
ok.append(control("register: over 240 characters", BLD, '         "The %d current employees hold %s hours at %s',
    '         "The page is the one the close package links and the number on it is the one the balance sheet carries, which is why the hours behind it are read the same way and stated the same way and carried the same way. The %d current employees hold %s hours at %s', BLD))
# ---- the import file
ok.append(control("import: the sheet not named Rubric", BLD, 'ws.title = "Rubric"', 'ws.title = "Verifiers"', BLD))
ok.append(control("import: a column out of the HR 79 T1 order", BLD,
    'IMPORT_HEADER = ["Index", "Verifier Type", "Criteria", "Criteria Explanation",',
    'IMPORT_HEADER = ["Index", "Criteria", "Verifier Type", "Criteria Explanation",', BLD))
ok.append(control("import: a criterion type outside the code-verifier dropdown", BLD,
    'EA, OC = "Expert Assessment", "Objective Compliance"', 'EA, OC = "Extraction", "Objective Compliance"', BLD))
ok.append(control("import: the 1.4 upload dropped from every row", BLD, "REQUEST = TASK_UPLOADS[0]", 'REQUEST = ""', BLD))
# ---- the verifiers, through the harness: a defect in the engine must fail the battery
ok.append(control("verifier: a line matched as a substring", ENG,
            "            hit = [i for i, c in enumerate(r) if _line_name(c) == want]",
            "            hit = [i for i, c in enumerate(r) if want in _line_name(c) or _line_name(c) in want]",
            VH, expect="FALSE PASS", pre=BLD))
ok.append(control("verifier: a line read off a prose word", ENG,
    "        if n.startswith(want) and", "        if want.split()[0] in n and", VH, expect="FALSE PASS", pre=BLD))
ok.append(control("verifier: a line read off an employee row", ENG,
    "            if _key_of(r):\n                continue\n            hit =", "            hit =", VH, expect="FALSE PASS", pre=BLD))
ok.append(control("verifier: a band around a stated line", ENG,
    "TOL_LINE_MONEY, TOL_LINE_HOURS = TOL_TOTAL_MONEY, TOL_TOTAL_HOURS", "TOL_LINE_MONEY, TOL_LINE_HOURS = 2.0, 0.2", VH, expect="FALSE PASS", pre=BLD))
ok.append(control("verifier: the band around a stated total", ENG,
    "TOL_TOTAL_MONEY, TOL_TOTAL_HOURS = 0.5, 0.05", "TOL_TOTAL_MONEY, TOL_TOTAL_HOURS = 5.0, 0.5",
    VH, expect="FALSE PASS", pre=BLD))
ok.append(control("verifier: a total read off an employee row", ENG,
    "                if not _key_of(r):\n                    figures += [x for c in r for x in read(c)]",
    "                figures += [x for c in r for x in read(c)]", VH, expect="FALSE PASS", pre=BLD))
ok.append(control("verifier: two pages under the title graded one by one", ENG,
    '        if len(pages) > 1:\n            return out(False, "%d page rows carry the title %r; the request asks for one"\n                       % (len(pages), SPEC["page"]))\n', "", VH, expect="FALSE PASS", pre=BLD))
ok.append(control("verifier: the title read off any cell of a page row", ENG,
    '            if cols.index("title") not in hits:\n                notes.append("page row %d carries %r outside its title column, in %r; not this page"\n                             % (n, title, [cols[i] for i in hits]))\n                continue\n', "", VH, expect="WRONG", pre=BLD))
ok.append(control("verifier: a page row reading a ctx primitive the measured surface does not carry", ENG,
    "    names = list(ctx.list_tables())", '    names = ["pages"] if ctx.has_table("pages") else list(ctx.list_tables())', VH, expect="WRONG", pre=BLD))
ok.append(control("verifier: a run's narration read instead of the database", ENG,
    '        pages = _load_pages(ctx, SPEC["page"], notes)',
    '        pages = _load_pages(ctx, SPEC["page"], notes) or [_Page(SPEC["page"], _clean(ctx.final_answer), True, "final answer")]', VH, pre=BLD))
ok.append(control("battery: an expectation planted wrong", SCN,
    '("the golden page", lambda: snap([(PAGE, GOLD)]), set(),', '("the golden page", lambda: snap([(PAGE, GOLD)]), {1},', VH, expect="FALSE PASS"))
ok.append(control("battery: a page that over-delivers expected to fail", SCN,
    '("every employee, a line per department and a summary block", lambda: snap([(PAGE, wide_page())]), set(),',
    '("every employee, a line per department and a summary block", lambda: snap([(PAGE, wide_page())]), {1},', VH, expect="FALSE PASS"))
# ---- the golden, the show-your-work and the documents
ok.append(control("golden: a total the schedule did not give", BLD,
    'lines = ["# %s" % (title or PAGE), "",\n             "Total PTO liability at %s: $%s" % (ASOF, f"{total:,.2f}")',
    'lines = ["# %s" % (title or PAGE), "",\n             "Total PTO liability at %s: $%s" % (ASOF, f"{total + 1:,.2f}")', BLD))
ok.append(control("docs: a stale figure in the record", META_MD, "$92,739.54", "$92,739.45", BLD, ["--docs"]))
ok.append(control("docs: a planned row missing from the record", META_MD,
    "States, on the PTO liability page, PTO hours of 558.31 for Engineering.",
    "States, on the PTO liability page, PTO hours of 558.13 for Engineering.", BLD, ["--docs"]))
ok.append(control("docs: a file missing from the README", README_MD, "`build/task_input_source.md`", "`build/task_input_sources.md`", BLD, ["--docs"]))
ok.append(control("docs: a non-ASCII character in a package document", META_MD, "## Fences", "## Fences " + "\u2014", BLD, ["--docs"]))
ok.append(control("selection: a wildcard in the block", META_MD, "\nbamboohr/Employee.csv\n", "\nbamboohr/*.csv\n", SELECT))

print("\n%d of %d controls went red" % (sum(1 for x in ok if x), len(ok)))
print("\nrebuilding the artifacts the controls dirtied")
failed = False
for script, args in ((TIB, ()), (BLD, ("--docs",)), (VH, ())):
    rebuild = run(script, args)
    out = (rebuild.stderr if rebuild.returncode else rebuild.stdout).strip()
    print(out.splitlines()[-1] if out else "")
    failed = failed or rebuild.returncode != 0
if failed or not all(ok):
    sys.exit(1)
