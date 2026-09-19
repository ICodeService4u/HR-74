"""Negative controls: plant a defect, confirm the guard goes red, revert the edit.

HR 32's section 8.6, carried through HR 79: a guard you have never seen fail is a guard you do
not have. Every guard this package relies on is made to fail here once, on a deliberate edit of
its own source, and the edit is reverted whether the control passes or not. Run it from the
package root:

    python3 build/negative_controls.py

It resolves the package from its own location, so it runs from any working directory. Every
control must go red or the run exits non-zero. The README's control table is this script's
output and nothing else.
"""
import os
import shutil
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
PROMPT_MD = os.path.join(PKG, "01_prompt.md")
META_MD = os.path.join(PKG, "02_task_metadata.md")
CATALOGUE = os.path.join(REPO, "tasks", "APP_TOOL_SURFACE.md")


def run(script, args=()):
    return subprocess.run([sys.executable, script, *args], cwd=PKG,
                          capture_output=True, text=True)


def control(label, path, old, new, script, args=(), expect=None, pre=None):
    """Plant `new` for `old` in `path`, run `script`, revert. `pre` names a script to run first
    with the defect in place, for a guard that reads a generated artifact: the verifier row
    files are generated from the engine, so an engine edit reaches the harness only through a
    rebuild, and a control that skipped the rebuild measured the old files and came back green
    seven times on 09/19/2026."""
    original = open(path, encoding="utf8").read()
    assert old in original, "control %r: anchor not found" % label
    open(path, "w", encoding="utf8").write(original.replace(old, new, 1))
    try:
        if pre:
            p = run(pre)
            assert p.returncode == 0, "control %r: the pre-step failed: %s" % (
                label, (p.stderr or p.stdout).strip().splitlines()[-1:])
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


def control_file(label, path, content, script, args=(), expect=None):
    """Plant a whole file that should not exist, run, remove it."""
    assert not os.path.exists(path), "control %r: %s already exists" % (label, path)
    open(path, "w", encoding="utf8").write(content)
    try:
        r = run(script, args)
        red = r.returncode != 0
        out = (r.stderr or r.stdout).strip()
        msg = out.splitlines()[-1] if out else ""
        if expect:
            red = red and expect in (r.stderr + r.stdout)
    finally:
        os.remove(path)
    print("%-6s %-60s %s" % ("RED" if red else "GREEN!!", label, msg[:100]))
    return red


TI = "build/build_task_input.py"
BP = "build/build_package_artifacts.py"
VH = "qc/verifier_harness.py"
ok = []
# ---- the memo's leak guards
ok.append(control("memo: the current employee count", SRC,
    "The People Metrics page has us at 57\npeople",
    "The People Metrics page has us at 57\npeople, 52 of them employees,", TI))
ok.append(control("memo: the Board's role count", SRC,
    "Board minutes of that meeting,\nand no other record.",
    "Board minutes of that meeting,\nand no other record. The plan has five roles.", TI))
ok.append(control("memo: the backfill level", SRC,
    "Board approval reads Approved or Not approved",
    "Board approval reads Approved or Not approved, the backfill line being CSM I", TI))
ok.append(control("memo: a record called stale", SRC,
    "Count people the way the People Metrics page describes.",
    "Count people the way the People Metrics page describes, dropping stale records.", TI))
ok.append(control("memo: the word contractor", SRC,
    "Count people the way the People Metrics page describes.",
    "Count people the way the People Metrics page describes, contractors out.", TI))
ok.append(control("memo: one of the five names", SRC,
    "reconciling items between that count and the BambooHR active record count.",
    "reconciling items between that count and the BambooHR active record count, Okonkwo first.", TI))
ok.append(control("memo: the workbook called superseded", SRC,
    "the Hiring Plan page carries the 8 roles at $868,000.00.",
    "the Hiring Plan page carries the 8 roles at $868,000.00, superseded or not.", TI))
ok.append(control("memo: a word for checking", SRC,
    "Two pages published in Wiki.js, each with",
    "Two pages published in Wiki.js, verified, each with", TI))
ok.append(control("memo: the shape of the answer", SRC,
    "employee ID, name, department, role, manager, and the\nopen",
    "employee ID, name, department, role, manager whether or not BambooHR has one, and the\nopen", TI,
    expect="sketches the shape"))
ok.append(control("memo: the premise dropped", SRC,
    "The People Metrics page has us at 57\npeople and 8 open requisitions, and the Hiring Plan page "
    "carries the 8 roles at $868,000.00. That\nis what Anjelina and I have been working from.",
    "We have the pages.", TI, expect="lost required content"))
ok.append(control("memo: a Board reading asserted", SRC,
    "That\nis what Anjelina and I have been working from.",
    "The Board approved them all. That\nis what Anjelina and I have been working from.", TI,
    expect="asserts a Board reading"))
ok.append(control("memo: the seat", SRC,
    "| **To** | Casey Ouk, People Operations Analyst |",
    "| **To** | Luka Odum, Talent Acquisition Specialist |", TI))
ok.append(control("memo: an unlicensed date", SRC,
    "Use\n08/31/2026 as the last date",
    "Use\n08/31/2026, not 08/24/2026, as the last date", TI, expect="unlicensed date"))
ok.append(control("names: the upload name the record publishes", TIB,
    'UPLOAD_NAME = "operating_review_request.pdf"',
    'UPLOAD_NAME = "operating_review_request_v2.pdf"', TI, expect="but the record publishes"))
# ---- the world facts
ok.append(control("world: the population", BLD,
    "assert len(POP) == 52 and len(CONTRACTORS) == 4",
    "assert len(POP) == 53 and len(CONTRACTORS) == 4", BP))
ok.append(control("world: a stale record read as current", BLD,
    '    rows = [r for r in _rows(ROSTER, "Employees")\n            if isinstance(r[0], str) and r[0].startswith("TRT-")]',
    '    rows = [r for r in _rows(ROSTER, "Employees")\n            if isinstance(r[0], str) and r[0].startswith("TRT-")]\n'
    '    rows.append(("TRT-0064", "Marguerite Delacroix-Hahn", "Marguerite", "Customer Success Manager", "Customer Success", "TRT-0021", "Employee", "TX", 40, None, None, "Exempt", 0, "Biweekly", None, "", "", "Active"))', BP,
    expect="the package rests on 52"))
ok.append(control("world: the Board reading of 036", BLD,
    '        elif j["req"] == "REQ-2026-036":\n            approval = "Not approved"',
    '        elif j["req"] == "REQ-2026-036":\n            approval = "Approved"', BP))
ok.append(control("world: the backfill line moved to CSM II", BLD,
    'assert ats[5][2] == "CSM II" and "TRT-0064" in ats[5][6]',
    'assert ats[5][2] == "CSM I" and "TRT-0064" in ats[5][6]', BP))
ok.append(control("world: Okonkwo's start date", BLD,
    'assert [u["hire"] for u in UNLOADED] == ["07/22/2026", "08/03/2026"], UNLOADED',
    'assert [u["hire"] for u in UNLOADED] == ["07/13/2026", "08/03/2026"], UNLOADED', BP))
ok.append(control("world: the department counts", BLD,
    '"Customer Success": 11, "Finance and Corporate": 5}, DEPT_COUNT',
    '"Customer Success": 12, "Finance and Corporate": 5}, DEPT_COUNT', BP))
# ---- the golden pages
ok.append(control("golden: a contractor on the staffed page", BLD,
    'for title, rows in (("Staffed roles with an open requisition", WITH_REQ),\n                        ("Staffed roles with no open requisition", WITHOUT_REQ)):',
    'for title, rows in (("Staffed roles with an open requisition", WITH_REQ),\n                        ("Staffed roles with no open requisition", WITHOUT_REQ + [dict(id="CTR-2001", name="Henrike Sato", dept="Engineering", role="Contract Data Engineer", mgr="Jessica Ko", req="None")])):',
    BP))
ok.append(control("golden: an ISO date", BLD,
    '"- 1 offer is accepted against a requisition the Board did not authorize: Kwame Adjei, "\n         "REQ-2026-038, start 09/08/2026.",',
    '"- 1 offer is accepted against a requisition the Board did not authorize: Kwame Adjei, "\n         "REQ-2026-038, start 2026-09-08.",', BP, expect="ISO date"))
# ---- the rubric mechanics and the register
ok.append(control("rubric: weight band", BLD,
    'R.append((APPDB, EA, 9, "-", "Yes",\n              A_ + "that REQ-2026-036',
    'R.append((APPDB, EA, 8, "-", "Yes",\n              A_ + "that REQ-2026-036', BP))
ok.append(control("rubric: the gate demoted off weight 10", BLD,
    'R.append((APPDB, EA, 10, "Critical value", "Yes",',
    'R.append((APPDB, EA, 9, "Critical value", "Yes",', BP, expect="weight 10 and gate must coincide"))
ok.append(control("rubric: atomicity", BLD,
    'A_ + "that REQ-2026-036 carries a Board approval of Not approved.",',
    'A_ + "that REQ-2026-036 carries a Board approval of Not approved and that its level is CSM II.",',
    BP, expect="stacked"))
ok.append(control("rubric: a row not opening on States", BLD,
    '"States that a Wiki.js page titled %s is published." % PAGE_A,',
    '"A Wiki.js page titled %s is published." % PAGE_A,', BP, expect="must open with States"))
ok.append(control("register: punctuation", BLD,
    '"The request fixes the Board approval vocabulary to those two values so the "',
    '"The request fixes the Board approval vocabulary (two values) so the "', BP))
ok.append(control("register: a spelled month", BLD,
    '"His offer on REQ-2026-038 was accepted 08/20/2026 with a start date of "',
    '"His offer on REQ-2026-038 was accepted August 20, 2026 with a start date of "', BP,
    expect="spells a month"))
ok.append(control("register: grading vocabulary", BLD,
    '"The request names the page and asks for it published in Wiki.js, so the page "',
    '"The request names the page and passes when it is published in Wiki.js, so the page "', BP,
    expect="describes grading"))
ok.append(control("register: self-reference", BLD,
    '"Kwame Adjei signed the offer on REQ-2026-038 on 08/20/2026 with a start date of "',
    '"Kwame Adjei signed the offer on REQ-2026-038 on 08/20/2026, as the other rows say, with a start date of "', BP,
    expect="rubric's own construction"))
ok.append(control("register: two rows carrying one explanation verbatim", BLD,
    '"No Data Analyst II is on the Board plan and the ATS export sources the "\n              "requisition to Hiring_Plan_2026_FINAL. An accepted offer on it does not change "\n              "what the Board authorized.",',
    '"No Marketing Manager is on the Board plan, the ATS export sources the "\n              "requisition to Hiring_Plan_2026_FINAL, and the plan treats a requisition opened "\n              "from a working spreadsheet as unauthorized.",', BP,
    expect="repeat verbatim"))
# ---- the asks guard, both directions
ok.append(control("asks: a row hung on the request's scope fence", BLD,
    '        return "Board approval reads Approved or Not approved" if "Board approval" in crit \\\n            else "Dates MM/DD/YYYY"',
    '        return "Change nothing in BambooHR or Greenhouse" if "Board approval" in crit \\\n            else "Dates MM/DD/YYYY"',
    BP, expect="fences work out of scope"))
ok.append(control("asks: a form the request sets left ungraded", BLD,
    '        return "Board approval reads Approved or Not approved" if "Board approval" in crit \\\n            else "Dates MM/DD/YYYY"',
    '        return "Board approval reads Approved or Not approved" if "Board approval" in crit \\\n            else "Two pages published in Wiki.js"',
    BP, expect="carries no row"))
ok.append(control("asks: the request reworded out from under a row", SRC,
    "The summary on this page states the Board-authorized annualized budget,",
    "The summary on this page states the annualized budget the Board set,", BP,
    expect="does not ask it any more"))
ok.append(control("asks: a row with no clause to hang on", BLD,
    '    ("the Board-authorized annualized budget", 1, DELIVERABLE),',
    '    ("the Board-authorized annualized budget", 2, DELIVERABLE),', BP, expect="carries 1 rows"))
# ---- the tool catalogue guard, once a catalogue exists
ok.append(control_file("tools: a catalogue with no wiki page writer", CATALOGUE,
    "# stub\n\n- `wiki_js_pages_get`\n- `wiki_js_pages_list`\n- `bamboohr_get_employee`\n",
    BP, expect="no Wiki.js page-writing tool"))
# ---- the import
ok.append(control("import: the guide's spelling of the App DB type", BLD,
    'APPDB = "App DB Programatic"', 'APPDB = "App DB Programmatic"', BP,
    expect="the picker spells it Programatic"))
ok.append(control("import: a form row losing its Style / formatting tag", BLD,
    '    return FORM_TAG if crit in FORM_ROWS else "Final Response"',
    '    return "Final Response"', BP, expect="tags"))
ok.append(control("import: a grading target on an App DB row", BLD,
    '"Critical" if primary == "Yes" else "Major", wt, primary, arts, None, "", "None"])',
    '"Critical" if primary == "Yes" else "Major", wt, primary, arts, "All Output", "", "None"])',
    BP, expect="grading target"))
ok.append(control("import: a reference artifact as a bare path", BLD,
    '            {"name": name, "index": None, "source": source,\n             "snapshotId": TASK_SNAP if source == "task" else SNAP,\n             "transformations": []}',
    '            name', BP, expect="not the picker's resolved object"))
ok.append(control("import: a world reference dropped", BLD,
    '    if ref.startswith("/"):\n        return "filesystem" + ref, "world"',
    '    if ref.startswith("/HR/Data/2026-08-31"):\n        return None\n    if ref.startswith("/"):\n        return "filesystem" + ref, "world"',
    BP, expect="drops the world reference"))
# ---- the verifiers, through the harness: a defect in the engine must fail the battery
ok.append(control("verifier: a substring match on the status cell", ENG,
    '    return c == w or (c.startswith(w) and c[len(w):len(w) + 1] in SEPS)',
    '    return w in c', VH, expect="FALSE PASS", pre=BP))
ok.append(control("verifier: the key matched as a substring", ENG,
    '    return any(c == _norm(k) for k in keys)',
    '    return any(_norm(k) in c for k in keys)', VH, pre=BP))
ok.append(control("verifier: page history read as pages", ENG,
    '    if ctx.has_table("pages"):\n        return "pages"',
    '    if ctx.has_table("pageHistory"):\n        return "pageHistory"', VH, pre=BP))
ok.append(control("verifier: the published flag assumed", ENG,
    '        if page.published is None:\n            return False, "the published flag could not be read, so publication is not shown"',
    '        if page.published is None:\n            return True, "assumed published"', VH, expect="FALSE PASS", pre=BP))
ok.append(control("verifier: a count that tallies substrings", ENG,
    '                key = next((c for c in r if re.fullmatch(S["key_re"], _norm(c))), None)\n                if key is None:\n                    continue\n                if fi is not None:',
    '                key = next((c for c in r if re.search(S["key_re"], _norm(c))), None)\n                if key is None:\n                    continue\n                if fi is not None:', VH, pre=BP))
ok.append(control("verifier: absence passing without the item named", ENG,
    '        if not named:\n            return False, "absent from the tables but never named as a reconciling item"',
    '        if not named:\n            return True, "absent"', VH, expect="FALSE PASS", pre=BP))
ok.append(control("verifier: a duplicate page passing on its better copy", ENG,
    '        if verdicts and all(verdicts):',
    '        if verdicts and any(verdicts):', VH, expect="FALSE PASS", pre=BP))
ok.append(control("battery: a scenario expecting the wrong verdict", SCN,
    '     {3}, "the determination the package exists for"),',
    '     set(), "the determination the package exists for"),', VH))
# ---- the docs
ok.append(control("docs: the prompt blockquote", PROMPT_MD,
    "> Complete the request (using the ATS requisition export",
    "> Please complete the request (using the ATS requisition export", BP, ("--docs",)))
ok.append(control("docs: a stale explanation in the record's rubric table", BLD,
    '"The request fixes the Board approval vocabulary to those two values so the "\n              "operating review reads one word per requisition.",',
    '"The request fixes the Board approval vocabulary to those two values so the "\n              "operating review reads one word per line.",', BP, ("--docs",),
    expect="stale explanation"))
ok.append(control("docs: a non-ASCII character in a package document", META_MD,
    "# Task metadata - ", "# Task metadata %s " % chr(0x2014), BP, ("--docs",), expect="is not ASCII"))
print("\n%d of %d controls went red" % (sum(ok), len(ok)))

# Restore the artifacts. A control plants its defect, runs the builder and reverts the source, but
# a builder run that fails LATE has already written its output, and a control on the engine or the
# scenarios has rebuilt the verifier files from the planted defect. The rebuild below is the guard.
print("\nrebuilding the artifacts the controls dirtied")
failed = False
for script, args in ((TI, ()), (BP, ("--docs",)), (VH, ())):
    rebuild = run(script, args)
    out = (rebuild.stderr if rebuild.returncode else rebuild.stdout).strip()
    print(out.splitlines()[-1] if out else "")
    failed = failed or rebuild.returncode != 0
if failed:
    print("REBUILD FAILED - the tree is dirty, do not commit")
    sys.exit(1)
sys.exit(0 if all(ok) else 1)
