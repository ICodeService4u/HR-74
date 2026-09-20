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
NINE_MD = os.path.join(PKG, "09_rubric_import.md")
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
# ---- the rubric mechanics: the guide's bands by criterion type, and the primary flag
ok.append(control("rubric: weight band", BLD,
    '("determination", 4, "-", "States, on the PTO liability page, no contractor row, CTR-2001 to CTR-2004.", no_contractor,\n         OC, "No",',
    '("determination", 7, "-", "States, on the PTO liability page, no contractor row, CTR-2001 to CTR-2004.", no_contractor,\n         OC, "No",',
    BLD, expect="outside its band"))
ok.append(control("rubric: a compliance row flagged primary", BLD,
    'no_contractor,\n         OC, "No",', 'no_contractor,\n         OC, "Yes",', BLD, expect="primary row is a reasoning row"))
ok.append(control("rubric: a stacked criterion", BLD,
    '"States, on the PTO liability page, no contractor row, CTR-2001 to CTR-2004."',
    '"States, on the PTO liability page, no contractor row, CTR-2001 to CTR-2004, and that no ended employee is on it."', BLD, expect="stacked"))
# ---- the register: every rule the explanations are held to, made to fail once
ok.append(control("register: punctuation", BLD,
    "as the handbook's 7.3 totals them.", "as the handbook (7.3) totals them.", BLD, expect="colon, semicolon or bracket"))
ok.append(control("register: a spaced dash", BLD,
    "as the handbook's 7.3 totals them.", "as the handbook's 7.3 - totals them.", BLD, expect="spaced dash"))
ok.append(control("register: a spelled month", BLD,
    'approved request of %.2f hours from %s to %s.', 'approved request of %.2f hours from %s to %s, filed July 6.', BLD, expect="spells a month"))
ok.append(control("register: an ISO date", BLD,
    'states the employee count, the total hours and the total dollar liability."',
    'states the employee count, the total hours and the total dollar liability at 2026-08-31."', BLD, expect="ISO date"))
ok.append(control("register: grading vocabulary", BLD,
    "so it exists with its published flag set.", "so it passes when it exists with its published flag set.", BLD, expect="describes grading"))
ok.append(control("register: self-reference", BLD,
    "The handbook bars contractors from paid time off.", "The handbook bars contractors from paid time off, as the other rows say.", BLD,
    expect="rubric's own construction"))
ok.append(control("register: no source named", BLD,
    '"The summary the request asks for states the employee count,', '"The summary states the employee count,', BLD, expect="names no source"))
ok.append(control("register: over 240 characters", BLD,
    "so it exists with its published flag set.",
    "so it exists with its published flag set, and it is the only page the analyst publishes for the August close, which is what the memo asks for and nothing else in the tree of files asks for.", BLD, expect="chars"))
ok.append(control("register: two rows carrying one explanation verbatim", BLD,
    '"Neither Okonkwo nor Ibarra has a BambooHR row and the crosswalk marks both Never Loaded. The request asks for the PTO balance in BambooHR for every employee on the schedule, so each has a balance row."',
    '"BambooHR carries CTR-2001 to CTR-2004 as active employees and the roster carries no contractor. The handbook bars contractors from paid time off."', BLD, expect="repeat verbatim"))
ok.append(control("register: two explanations opening alike", BLD,
    '"The summary the request asks for states the employee count,', '"The request sets out a summary that states the employee count,', BLD, expect="open alike"))
# ---- the import: the picker's spellings, the tags, the columns, the citations, the ids
ok.append(control("import: the guide's spelling of the App DB type", BLD,
    'APPDB = "App DB Programatic"', 'APPDB = "App DB Programmatic"', BLD, expect="the picker spells it Programatic"))
ok.append(control("import: a criterion type outside the code-verifier dropdown", BLD,
    'EA, OC = "Expert Assessment", "Objective Compliance"', 'EA, OC = "Expert Assessment", "Extraction"', BLD, expect="dropdown"))
ok.append(control("import: the form row losing its Style / formatting tag", BLD,
    '    return FORM_TAG if crit == FORM_CRIT else "Final Response"', '    return "Final Response"', BLD, expect="tags"))
ok.append(control("import: a grading target on an App DB row", BLD,
    '"Critical" if primary == "Yes" else "Major", wt, primary, arts, None, "", "None"])',
    '"Critical" if primary == "Yes" else "Major", wt, primary, arts, "All Output", "", "None"])', BLD, expect="grading target"))
ok.append(control("import: a reference artifact as a bare path", BLD,
    '            {"name": name, "index": None, "source": source,\n             "snapshotId": TASK_SNAP if source == "task" else SNAP,\n             "transformations": []}',
    '            name', BLD, expect="not the picker's resolved object"))
ok.append(control("import: a world reference dropped", BLD,
    '    if ref.startswith("/"):\n        return "filesystem" + ref, "world"',
    '    if ref.startswith("/HR/Data/2026-08-31"):\n        return None\n    if ref.startswith("/"):\n        return "filesystem" + ref, "world"',
    BLD, expect="drops the world reference"))
ok.append(control("import: the 1.4 upload dropped from every row", BLD,
    '    if ref in TASK_UPLOADS:\n        return "filesystem/" + ref, "task"', '    if ref in TASK_UPLOADS:\n        return None', BLD, expect="reference"))
ok.append(control("import: a citation outside the selection block", BLD,
    '[REQUEST, wiki]),', '[REQUEST, wiki, "/HR/Data/Nonexistent_Report.xlsx"]),', BLD, expect="selection block does not carry"))
ok.append(control("import: a snapshot id not read off an export", BLD,
    'TASK_SNAP = "snap_45e68b376f2547dca61408b65d8ba774"', 'TASK_SNAP = "SNAPSHOT_ID_NOT_YET_READ"', BLD, expect="do not load this file"))
ok.append(control("import: the sheet not named Rubric", BLD, '    ws.title = "Rubric"', '    ws.title = "Sheet1"', BLD))
ok.append(control("import: a column out of the HR 79 T1 order", BLD,
    'IMPORT_HEADER = ["Index", "Verifier Type", "Criteria", "Criteria Explanation",',
    'IMPORT_HEADER = ["Index", "Criteria", "Verifier Type", "Criteria Explanation",', BLD))
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
ok.append(control("docs: a stale explanation in the record's rubric table", BLD,
    "The handbook bars contractors from paid time off.", "The handbook bars contractors from paid leave.", BLD, ["--docs"], expect="stale explanation"))
ok.append(control("docs: a stale import md5 in the record", META_MD, "d018e720530d412bd593cfd0c0251d85", "d018e720530d412bd593cfd0c0251d86", BLD, ["--docs"], expect="stale md5 for the import"))
ok.append(control("docs: a stale import md5 in the mappings document", NINE_MD, "d018e720530d412bd593cfd0c0251d85", "d018e720530d412bd593cfd0c0251d86", BLD, ["--docs"], expect="09 lacks the figure"))
ok.append(control("docs: a stale citation count in the mappings document", NINE_MD, "71 citations over 17 of the", "70 citations over 17 of the", BLD, ["--docs"], expect="09 lacks the figure"))
ok.append(control("selection: a wildcard in the block", META_MD, "\nbamboohr/Employee.csv\n", "\nbamboohr/*.csv\n", SELECT))

print("\n%d of %d controls went red" % (sum(ok), len(ok)))

# Restore the artifacts. A control plants its defect, runs the builder and reverts the source, but
# a builder run that fails LATE has already written its output from the planted defect, the
# import among them. The rebuild below is the guard.
print("\nrebuilding the artifacts the controls dirtied")
failed = False
for script, args in ((TIB, ()), (BLD, ("--docs",))):
    rebuild = run(script, args)
    out = (rebuild.stderr if rebuild.returncode else rebuild.stdout).strip()
    print(out.splitlines()[-1] if out else "")
    failed = failed or rebuild.returncode != 0
if failed or not all(ok):
    sys.exit(1)
