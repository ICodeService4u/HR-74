#!/usr/bin/env python3
"""The single source of truth for T1's graded content: the two golden pages, the rubric, the
verifier code, the show-your-work workbook, and the checks that hold all of them to the world's
bytes and to the house register.

HR 32's rule, carried through HR 79: edit this file, never the artifacts. `_rubric()` is the one
place a criterion, a weight, a gate, an explanation or a verifier spec is written; `pages()`
writes the golden pages from the same facts; `verifiers()` stamps each row's spec into the engine;
`syw()` writes the workbook; `check_world()` recomputes every graded value from the world files
before anything is written; `check_rubric()`, `check_register()`, `check_asks()` and
`check_import()` hold the mechanics, the register and the import; `check_docs()` holds
01_prompt.md, 02_task_metadata.md and README.md to the PROMPT constant and the built rubric.

Run from anywhere: python3 build/build_package_artifacts.py [--docs] [--table]
"""
import csv
import datetime
import hashlib
import io
import json
import os
import pprint
import re
import sys
import zipfile

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(PKG))
WORLD = os.path.join(REPO, "filesystem")
APPS = os.path.join(REPO, "apps_data")

BOLD = Font(bold=True)
WRAP = Alignment(vertical="top", wrap_text=True)

# ---------------------------------------------------------------- the prompt and the deliverable
PAGE_A = "Approved Hiring View - August 2026"
PAGE_B = "Staffed Role View - August 2026"
# The house convention names a task from its output, not from a description of the work. The
# output here is two wiki pages, so the name carries both page subjects.
TASK_NAME = "Approved Hiring and Staffed Role Views"
# One sentence in the owner's register, the T1 shape from HR 79: the ask, the named sources plus
# the open tail in a parenthetical, the request by subject and date, then the deliverable with
# both page titles named exactly. The two named sources carry no graded conclusion: the ATS
# export prints the eight open requisitions and their source-plan column, and the BambooHR
# records are the population the determination is made against. The Board plan, the org chart,
# the roster, the crosswalk and the archive are the response's work to find.
PROMPT = ("Complete the request (using the ATS requisition export, the BambooHR employee "
          "records, and the rest of the Troutly files) about the August 31, 2026 operating "
          "review by publishing the two Wiki.js pages %s and %s." % (PAGE_A, PAGE_B))
TASK_INPUTS = ["00_task_input_operating_review_request.pdf"]
ASOF = "08/31/2026"
ANCHOR = "08/31/2026"
TARGET_APP = "wiki_js"

# ---------------------------------------------------------------- world readers
def _csv(app, table):
    with open(os.path.join(APPS, app, table), newline="", encoding="utf8") as fh:
        return list(csv.DictReader(fh))


def _pdf_text(rel):
    """The PDF's text with whitespace collapsed, so a phrase can be asserted across a line break."""
    import pdfplumber
    with pdfplumber.open(os.path.join(WORLD, rel)) as pdf:
        return re.sub(r"\s+", " ", "\n".join((p.extract_text() or "") for p in pdf.pages))


def _docx_text(rel):
    import docx
    d = docx.Document(os.path.join(WORLD, rel))
    parts = [p.text for p in d.paragraphs]
    for t in d.tables:
        for r in t.rows:
            parts.append(" | ".join(c.text for c in r.cells))
    return "\n".join(parts)


def _rows(rel, sheet=None):
    wb = load_workbook(os.path.join(WORLD, rel), data_only=True)
    ws = wb[sheet] if sheet else wb.active
    return [r for r in ws.iter_rows(values_only=True)]


def _d(v):
    """MM/DD/YYYY from a date, a datetime or an ISO string."""
    if hasattr(v, "strftime"):
        return v.strftime("%m/%d/%Y")
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", str(v))
    return "%s/%s/%s" % (m.group(2), m.group(3), m.group(1)) if m else str(v)


# ---------------------------------------------------------------- the world facts the package rests on
ROSTER = "HR/Data/2026-08-31_Master_Employee_Roster.xlsx"
CROSSWALK = "HR/Data/2026-08-28_Employee_ID_Crosswalk.xlsx"
ARCHIVE = "HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx"
ORG_AUG = "HR/Org/2026-08-24_Org_Chart.pdf"
ORG_JAN = "HR/Org/2026-01-12_Org_Chart.pdf"
BOARD_PLAN = "Recruiting/2026-06-20_Hiring_Plan_Board_Approved.pdf"
MINUTES = "Executive/Board/2026-06-20_Board_Minutes.pdf"
PLAN_FINAL = "Recruiting/Hiring_Plan_2026_FINAL.xlsx"
ATS = "Recruiting/ATS_Requisition_Export_2026-08-31.xlsx"
OFFER_ADJEI = "Recruiting/Offers/2026-08-20_Offer_Acceptance_ATS-4471.pdf"
OFFER_OKONKWO = "Recruiting/Offers/2026-07-02_Offer_TRT-0153_SIGNED.pdf"
THREAD_OKONKWO = "Recruiting/Offers/2026-07-09_Start_Date_Thread_TRT-0153.eml"
IT_TICKET = "HR/People/Onboarding/2026-07-22_IT_Ticket_TRT-0153.pdf"
RESIGNATION_0064 = "HR/People/Separations/2026-05-29_Resignation_TRT-0064.eml"
COST_MEMO = "Finance/2026-08-06_Fully_Loaded_Cost_Memo.docx"
LEVELING = "HR/Comp/Leveling_Guide_v2.docx"
WIKI_METRICS = "Wiki/People_Metrics.md"
WIKI_PLAN = "Wiki/Hiring_Plan.md"
WIKI_DIRECTORY = "Wiki/Team_Directory.md"
REQUEST = "operating_review_request.pdf"

BOARD_BUDGET = "$612,000.00"
PLAN_BUDGET = "$868,000.00"
BOARD_ROLES = 5
PLAN_ROLES = 8
METRICS_HEADCOUNT = 57

# The requisitions the Board plan's page 2 table authorises, line by line, with the hiring
# manager each line names. Asserted against the PDF's text in check_world().
BOARD_LINES = [
    ("Senior Software Engineer", "IC4", "Engineering", "Jessica Ko", "$152,000.00"),
    ("Software Engineer II", "IC3", "Engineering", "Jessica Ko", "$128,000.00"),
    ("Account Executive", "AE", "Sales", "Michael Labeson", "$98,000.00"),
    ("Customer Success Manager", "CSM I", "Customer Success", "Edith Bustamante", "$96,000.00"),
    ("Product Designer", "IC3", "Product", "Sora Jackson", "$118,000.00"),
]
BACKFILL_LEVEL = "CSM I"
BACKFILL_DEADLINE = "09/30/2026"


def _population():
    """The 52 current employees, from the master roster, cross-checked against BambooHR, the
    crosswalk, the SplinterHR archive and the August org chart in check_world()."""
    rows = [r for r in _rows(ROSTER, "Employees")
            if isinstance(r[0], str) and r[0].startswith("TRT-")]
    names = {r[0]: r[1] for r in rows}
    return [dict(id=r[0], name=r[1], role=r[3], dept=r[4], mgr_id=r[5],
                 mgr=names.get(r[5], "None") if r[5] else "None", hire=_d(r[9]))
            for r in rows]


def _contractors():
    return [dict(id=r[0], name=r[1], role=r[3], dept=r[4], owner=r[5])
            for r in _rows(ROSTER, "Contractors")
            if isinstance(r[0], str) and r[0].startswith("CTR-")]


def _bamboo():
    return _csv("bamboohr", "Employee.csv")


def _archive_terminations():
    out = {}
    for r in _rows(ARCHIVE, "Employees"):
        if isinstance(r[1], str) and r[1].startswith("TRT-") and r[6] == "Terminated" and r[10]:
            out[r[1]] = _d(r[10])
    return out


def _jobs():
    jobs = _csv("greenhouse", "jobs.csv")
    users = {u["id"]: "%s %s" % (u["first_name"], u["last_name"])
             for u in _csv("greenhouse", "users.csv")}
    team = _csv("greenhouse", "hiring_team.csv")
    depts = {d["id"]: d["name"] for d in _csv("greenhouse", "departments.csv")}
    jd = {j["job_id"]: depts[j["department_id"]] for j in _csv("greenhouse", "job_departments.csv")}
    out = []
    for j in jobs:
        hm = [users[t["user_id"]] for t in team if t["job_id"] == j["id"] and t["role"] == "hiring_manager"]
        assert len(hm) == 1, j
        out.append(dict(id=j["id"], req=j["requisition_id"], role=j["name"], dept=jd[j["id"]],
                        owner=hm[0], status=j["status"], opened=_d(j["opened_at"]),
                        closed=_d(j["closed_at"]) if j["closed_at"] else "", notes=j["notes"]))
    return out


POP = _population()
CONTRACTORS = _contractors()
BAMBOO = _bamboo()
BAMBOO_ACTIVE = [e for e in BAMBOO if e["status"] == "Active"]
POP_IDS = {p["id"] for p in POP}
STALE_IDS = sorted({e["employee_number"] for e in BAMBOO_ACTIVE
                    if e["employee_number"].startswith("TRT-")} - POP_IDS)
UNLOADED_IDS = sorted(POP_IDS - {e["employee_number"] for e in BAMBOO_ACTIVE})
# Asserted here, where they are computed, so a population that has drifted fails on the fact
# rather than on whatever first indexes it.
assert len(POP) == 52, "the roster carries %d employees, the package rests on 52" % len(POP)
assert STALE_IDS == ["TRT-0037", "TRT-0049", "TRT-0064"], "STALE_IDS drifted: %r" % STALE_IDS
assert UNLOADED_IDS == ["TRT-0153", "TRT-0155"], "UNLOADED_IDS drifted: %r" % UNLOADED_IDS
ENDED = _archive_terminations()
STALE = [dict(id=i, name=next(e["first_name"] + " " + e["last_name"] for e in BAMBOO
                              if e["employee_number"] == i), ended=ENDED[i]) for i in STALE_IDS]
UNLOADED = [next(p for p in POP if p["id"] == i) for i in UNLOADED_IDS]
JOBS = _jobs()
OPEN_JOBS = [j for j in JOBS if j["status"] == "open"]
OPEN_TITLES = {j["role"]: j["req"] for j in OPEN_JOBS}
for p in POP:
    p["req"] = OPEN_TITLES.get(p["role"], "None")
WITH_REQ = [p for p in POP if p["req"] != "None"]
WITHOUT_REQ = [p for p in POP if p["req"] == "None"]
DEPT_ORDER = ["Engineering", "Product", "Sales", "Marketing", "Customer Success",
              "Finance and Corporate"]
DEPT_COUNT = {d: sum(1 for p in POP if p["dept"] == d) for d in DEPT_ORDER}
BAMBOO_DEPT = {d: sum(1 for e in BAMBOO_ACTIVE if e["department"] == d) for d in DEPT_ORDER}

# The eight open requisitions with the Board reading of each. The basis strings are the golden's
# own words; the graded value is the Approved / Not approved cell.
def _requisitions():
    board = {(l[0], l[2]): l for l in BOARD_LINES}
    out = []
    for j in sorted(OPEN_JOBS, key=lambda j: j["req"]):
        line = board.get((j["role"], j["dept"]))
        if line:
            n = BOARD_LINES.index(line) + 1
            approval, basis = "Approved", "Board plan line %d, %s" % (n, line[1])
        elif j["req"] == "REQ-2026-036":
            approval = "Not approved"
            basis = "Opened at CSM II. The Board backfill line is CSM I"
        else:
            approval = "Not approved"
            basis = "Not on the Board plan. Opened from Hiring_Plan_2026_FINAL"
        if j["req"] == "REQ-2026-038":
            status, date = "Offer accepted", "08/20/2026"
        else:
            status, date = "Open", ASOF
        out.append(dict(req=j["req"], role=j["role"], dept=j["dept"], owner=j["owner"],
                        approval=approval, basis=basis, status=status, date=date))
    return out


REQS = _requisitions()
APPROVED = [r for r in REQS if r["approval"] == "Approved"]
NOT_APPROVED = [r for r in REQS if r["approval"] != "Approved"]
OPEN_NO_OFFER = [r for r in REQS if r["status"] == "Open"]

# The three recruiting records with no BambooHR employee record: the accepted offer and the two
# hires the HRIS never loaded. Start dates are asserted against the world in check_world().
RECRUITING = [
    dict(name="Kwame Adjei", req="REQ-2026-038", role="Data Analyst II", status="Offer accepted",
         start="09/08/2026", working="No", bamboo="No"),
    dict(name="Simone Okonkwo", req="REQ-2026-029", role="Customer Success Manager",
         status="Hired", start="07/22/2026", working="Yes", bamboo="No"),
    dict(name="Rafael Ibarra", req="REQ-2026-030", role="Sales Development Representative",
         status="Hired", start="08/03/2026", working="Yes", bamboo="No"),
]
OKONKWO_OFFER_START = "07/13/2026"

WORDS = {0: "zero", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six",
         7: "seven", 8: "eight"}


# ---------------------------------------------------------------- the golden pages
def page_approved():
    L = ["# %s" % PAGE_A, "",
         "Prepared %s for the workforce planning and recruiting operating review. Employee and "
         "recruiting activity through %s. Board approval is read from the Board-approved "
         "Second-Half 2026 Hiring Plan of 06/20/2026 and the Board minutes of 06/20/2026."
         % (ASOF, ASOF), "",
         "## Reconciliation summary", "",
         "- The Board approved %d roles on 06/20/2026 at an annualized budget of %s, plus one "
         "conditional Customer Success backfill at the %s midpoint that lapses without a Customer "
         "Success departure before %s." % (BOARD_ROLES, BOARD_BUDGET, BACKFILL_LEVEL,
                                           BACKFILL_DEADLINE),
         "- All %d approved roles are open and unfilled at %s. 0 of %d are filled. No offer is "
         "out on any of them." % (BOARD_ROLES, ASOF, BOARD_ROLES),
         "- %d requisitions are open in Greenhouse. %d trace to the Board plan. %d do not: "
         "REQ-2026-036 was opened at CSM II against the CSM I backfill line, and REQ-2026-037 "
         "and REQ-2026-038 were opened from the Hiring_Plan_2026_FINAL workbook, which the "
         "Board plan supersedes." % (len(REQS), len(APPROVED), len(NOT_APPROVED)),
         "- 1 offer is accepted against a requisition the Board did not authorize: Kwame Adjei, "
         "REQ-2026-038, start 09/08/2026.",
         "- The Hiring Plan wiki page and the Hiring_Plan_2026_FINAL workbook carry %d roles at "
         "%s on 2025 midpoints. The Board plan supersedes both." % (PLAN_ROLES, PLAN_BUDGET),
         "- 2 hires from second-quarter requisitions are working at %s and have no BambooHR "
         "record: Simone Okonkwo, TRT-0153, and Rafael Ibarra, TRT-0155." % ASOF, "",
         "## Open requisitions at %s" % ASOF, "",
         "| Requisition | Role | Department | Owner | Board approval | Basis | Hiring status | "
         "Status source date |",
         "|---|---|---|---|---|---|---|---|"]
    for r in REQS:
        L.append("| %s | %s | %s | %s | %s | %s | %s | %s |" % (
            r["req"], r["role"], r["dept"], r["owner"], r["approval"], r["basis"],
            r["status"], r["date"]))
    L += ["", "## Recruiting records with no matching BambooHR employee record", "",
          "| Candidate | Requisition | Role | Recruiting status | Start date | Working at %s | "
          "BambooHR record |" % ASOF,
          "|---|---|---|---|---|---|---|"]
    for r in RECRUITING:
        L.append("| %s | %s | %s | %s | %s | %s | %s |" % (
            r["name"], r["req"], r["role"], r["status"], r["start"], r["working"], r["bamboo"]))
    return "\n".join(L) + "\n"


def page_staffed():
    stale = ", ".join("%s %s (ended %s)" % (s["name"], s["id"], s["ended"]) for s in STALE)
    unl = " and ".join("%s %s (started %s)" % (u["name"], u["id"], u["hire"]) for u in UNLOADED)
    ctr = ", ".join(c["id"] for c in CONTRACTORS)
    L = ["# %s" % PAGE_B, "",
         "Prepared %s for the workforce planning and recruiting operating review. A current "
         "employee is anyone working for Troutly as an employee at %s, counted the way the "
         "People Metrics page describes: contractors, ended employment and future-dated hires "
         "left out. Managers and reporting lines are from the org chart of 08/24/2026."
         % (ASOF, ASOF), "",
         "## Reconciliation summary", "",
         "- %d current employees at %s: %s." % (
             len(POP), ASOF, ", ".join("%s %d" % (d, DEPT_COUNT[d]) for d in DEPT_ORDER)),
         "- BambooHR carries %d active records. %d are contractors (%s). %d are employees whose "
         "employment ended and whose records still read Active: %s. %d current employees have "
         "no BambooHR record: %s. %d - %d - %d + %d = %d."
         % (len(BAMBOO_ACTIVE), len(CONTRACTORS), ctr, len(STALE), stale, len(UNLOADED), unl,
            len(BAMBOO_ACTIVE), len(CONTRACTORS), len(STALE), len(UNLOADED), len(POP)),
         "- %d current employees hold a role with an open requisition. %d do not."
         % (len(WITH_REQ), len(WITHOUT_REQ)),
         "- The People Metrics page's %d is the BambooHR active record count, contractors and "
         "ended records included and the two unloaded hires left out." % METRICS_HEADCOUNT, ""]
    hdr = ["| Employee ID | Name | Department | Role | Manager | Open requisition |",
           "|---|---|---|---|---|---|"]
    order = {d: i for i, d in enumerate(DEPT_ORDER)}
    for title, rows in (("Staffed roles with an open requisition", WITH_REQ),
                        ("Staffed roles with no open requisition", WITHOUT_REQ)):
        L += ["## %s" % title, ""] + hdr
        for p in sorted(rows, key=lambda p: (order[p["dept"]], p["id"])):
            L.append("| %s | %s | %s | %s | %s | %s |" % (
                p["id"], p["name"], p["dept"], p["role"], p["mgr"], p["req"]))
        L.append("")
    return "\n".join(L)


GOLDEN = {PAGE_A: page_approved(), PAGE_B: page_staffed()}
GOLDEN_FILES = {PAGE_A: "04_golden_output_Approved_Hiring_View.md",
                PAGE_B: "04_golden_output_Staffed_Role_View.md"}

# ---------------------------------------------------------------- the rubric
EA, OC = "Expert Assessment", "Objective Compliance"
# THE APP DB TYPE'S SPELLING IS THE PICKER'S, NOT THE GUIDE'S. RL Studio's Add-a-verifier control
# spells it "App DB Programatic", one "m"; the guide spells it "Programmatic". HR 32 lost the row
# to that letter twice and the importer skips an unknown type on a warning. check_import()
# refuses any type containing "Programmatic".
APPDB = "App DB Programatic"
BANDS = {OC: {1, 2, 3, 7, 10}, EA: {5, 7, 9, 10}, "Process": {2, 4, 6}}
FORM_VOCAB_CRIT = ("States, on the approved hiring page, every Board approval cell as Approved "
                   "or Not approved.")
FORM_DATES_CRIT = "States, on both pages, every date in MM/DD/YYYY form."
FORM_ROWS = (FORM_VOCAB_CRIT, FORM_DATES_CRIT)

A_ = "States, on the approved hiring page, "
B_ = "States, on the staffed role page, "


def _rubric():
    """(verifier kind, criterion type, weight, gate kind, primary, criterion, explanation, refs,
    spec). Every row is an App DB row on the Wiki.js pages table: the deliverable is two wiki
    pages and no file, so the judge has nothing to open and the database is the only route.

    Weights are the guide's importance table crossed with the difficulty this package predicts
    and registers in 02_task_metadata.md before any run; a run set replaces the prediction with
    a measurement, which is HR 79 T1's rule. The spine is the population reconciliation on the
    staffed page and the Board reading of REQ-2026-036 on the hiring page."""
    board = "/" + BOARD_PLAN
    minutes = "/" + MINUTES
    ats = "/" + ATS
    roster = "/" + ROSTER
    xwalk = "/" + CROSSWALK
    arch = "/" + ARCHIVE
    org = "/" + ORG_AUG
    metrics = "/" + WIKI_METRICS
    plan = "/" + PLAN_FINAL
    wplan = "/" + WIKI_PLAN
    offer = "/" + OFFER_ADJEI
    thread = "/" + THREAD_OKONKWO
    ticket = "/" + IT_TICKET
    cost = "/" + COST_MEMO
    resig = "/" + RESIGNATION_0064
    jobs, apps, team = ("greenhouse/jobs.csv", "greenhouse/applications.csv",
                        "greenhouse/hiring_team.csv")
    emp, wiki = "bamboohr/Employee.csv", "wiki_js/Page.csv"
    ok_keys = {"Simone Okonkwo": ["Okonkwo, Simone"], "Rafael Ibarra": ["Ibarra, Rafael"],
               "Kwame Adjei": ["Adjei, Kwame"]}
    R = []
    # ---- the approved hiring page
    R.append((APPDB, OC, 2, "-", "No",
              "States that a Wiki.js page titled %s is published." % PAGE_A,
              "The request names the page and asks for it published in Wiki.js, so the page "
              "exists under that title with its published flag set.",
              [REQUEST, wiki], dict(kind="exists", pages=[PAGE_A])))
    R.append((APPDB, OC, 3, "-", "No",
              A_ + "that %s each carry a Board approval of Approved."
              % (", ".join(r["req"] for r in APPROVED[:-1]) + " and " + APPROVED[-1]["req"]),
              "The Board plan's page 2 table authorises these five roles by title, level and "
              "department, and each requisition traces to its line on the ATS export.",
              [board, ats, jobs],
              dict(kind="cells", pages=[PAGE_A], keys=[r["req"] for r in APPROVED],
                   column="board approval", expected=["Approved"])))
    R.append((APPDB, EA, 9, "-", "Yes",
              A_ + "that REQ-2026-036 carries a Board approval of Not approved.",
              "The Board's backfill line is CSM I and the requisition was opened as Customer "
              "Success Manager II at CSM II, so it does not trace line-for-line to a Board "
              "authorization and the plan holds it pending Board action.",
              [board, minutes, ats, jobs],
              dict(kind="cell", pages=[PAGE_A], keys=["REQ-2026-036"],
                   column="board approval", expected=["Not approved"])))
    R.append((APPDB, EA, 5, "-", "Yes",
              A_ + "that REQ-2026-037 carries a Board approval of Not approved.",
              "No Marketing Manager is on the Board plan, the ATS export sources the "
              "requisition to Hiring_Plan_2026_FINAL, and the plan treats a requisition opened "
              "from a working spreadsheet as unauthorized.",
              [board, ats, plan, jobs],
              dict(kind="cell", pages=[PAGE_A], keys=["REQ-2026-037"],
                   column="board approval", expected=["Not approved"])))
    R.append((APPDB, EA, 5, "-", "Yes",
              A_ + "that REQ-2026-038 carries a Board approval of Not approved.",
              "No Data Analyst II is on the Board plan and the ATS export sources the "
              "requisition to Hiring_Plan_2026_FINAL. An accepted offer on it does not change "
              "what the Board authorized.",
              [board, ats, plan, offer],
              dict(kind="cell", pages=[PAGE_A], keys=["REQ-2026-038"],
                   column="board approval", expected=["Not approved"])))
    R.append((APPDB, OC, 2, "-", "No",
              A_ + "a hiring status of Open on each of %s."
              % (", ".join(r["req"] for r in APPROVED[:-1]) + " and " + APPROVED[-1]["req"]),
              "The ATS export of %s carries no offer on any of the five approved requisitions "
              "and Greenhouse holds no application on them, so each is open and unfilled."
              % ASOF,
              [ats, jobs, apps],
              dict(kind="cells", pages=[PAGE_A], keys=[r["req"] for r in APPROVED],
                   column="hiring status", expected=["Open"])))
    R.append((APPDB, OC, 2, "-", "No",
              A_ + "that REQ-2026-038 carries a hiring status of Offer accepted.",
              "Kwame Adjei signed the offer on REQ-2026-038 on 08/20/2026 with a start date of "
              "09/08/2026, so at %s the requisition holds an accepted offer and no hire." % ASOF,
              [offer, ats, apps],
              dict(kind="cell", pages=[PAGE_A], keys=["REQ-2026-038"],
                   column="hiring status", expected=["Offer accepted"])))
    R.append((APPDB, OC, 1, "-", "No",
              A_ + "a status source date of 08/20/2026 on REQ-2026-038.",
              "The signed offer letter is dated 08/20/2026 on the acceptance line and the ATS "
              "export carries the same date, which is the latest record behind the status.",
              [offer, ats],
              dict(kind="cell", pages=[PAGE_A], keys=["REQ-2026-038"],
                   column="source date", date="08/20/2026")))
    R.append((APPDB, OC, 1, "-", "No",
              A_ + "a status source date of %s on each of %s." % (
                  ASOF, ", ".join(r["req"] for r in OPEN_NO_OFFER[:-1]) + " and "
                  + OPEN_NO_OFFER[-1]["req"]),
              "Seven requisitions stand open with no offer on the ATS export of %s, which is the "
              "latest record showing each, and the request sets that date as the last day of "
              "recruiting activity." % ASOF,
              [ats, jobs],
              dict(kind="cells", pages=[PAGE_A], keys=[r["req"] for r in OPEN_NO_OFFER],
                   column="source date", date=ASOF)))
    R.append((APPDB, OC, 1, "-", "No",
              A_ + "Jessica Ko as owner of REQ-2026-031 and REQ-2026-032, Michael Labeson of "
              "REQ-2026-033, Edith Bustamante of REQ-2026-034 and Sora Jackson of REQ-2026-035.",
              "The Board plan names the hiring manager on each approved line and the Greenhouse "
              "hiring team carries the same person as hiring manager on each requisition.",
              [board, team, ats],
              dict(kind="cells", pages=[PAGE_A], keys=[r["req"] for r in APPROVED],
                   column="owner", contains_by_key={r["req"]: [r["owner"].split()[-1]]
                                                    for r in APPROVED})))
    R.append((APPDB, EA, 5, "-", "Yes",
              A_ + "that Kwame Adjei is not working at %s." % ASOF,
              "His offer on REQ-2026-038 was accepted 08/20/2026 with a start date of "
              "09/08/2026, so at %s he is a recruiting record and not an employee, and the "
              "Finance cost memo leaves accepted offers with future start dates out." % ASOF,
              [offer, apps, cost],
              dict(kind="cell", pages=[PAGE_A], keys=["Kwame Adjei"], aliases=ok_keys,
                   column="working at", expected=["No"])))
    R.append((APPDB, OC, 2, "-", "No",
              A_ + "that Simone Okonkwo, hired on REQ-2026-029, has no BambooHR employee record.",
              "Greenhouse carries her application as hired and the crosswalk carries TRT-0153 "
              "as Never Loaded, and no BambooHR employee row carries her number.",
              [apps, xwalk, emp],
              dict(kind="cell", pages=[PAGE_A], keys=["Simone Okonkwo"], aliases=ok_keys,
                   column="bamboohr record", expected=["No"])))
    R.append((APPDB, OC, 2, "-", "No",
              A_ + "that Rafael Ibarra, hired on REQ-2026-030, has no BambooHR employee record.",
              "Greenhouse carries his application as hired with a start of 08/03/2026 and the "
              "crosswalk carries TRT-0155 as Never Loaded, and no BambooHR row carries his number.",
              [apps, xwalk, emp],
              dict(kind="cell", pages=[PAGE_A], keys=["Rafael Ibarra"], aliases=ok_keys,
                   column="bamboohr record", expected=["No"])))
    R.append((APPDB, OC, 2, "-", "No",
              A_ + "a start date of 07/22/2026 for Simone Okonkwo.",
              "The 07/09/2026 email thread moves the start from %s on the signed offer letter "
              "to 07/22/2026, which the IT ticket, the Greenhouse note and the master roster "
              "all carry." % OKONKWO_OFFER_START,
              [thread, ticket, roster],
              dict(kind="cell", pages=[PAGE_A], keys=["Simone Okonkwo"], aliases=ok_keys,
                   column="start date", date="07/22/2026")))
    R.append((APPDB, OC, 2, "-", "No",
              A_ + "that the Board-authorized annualized budget is %s." % BOARD_BUDGET,
              "Both the Board plan and the minutes resolve the second-half plan at %s, and the "
              "%s on the plan workbook is a superseded working figure." % (BOARD_BUDGET, PLAN_BUDGET),
              [board, minutes, plan],
              dict(kind="summary", pages=[PAGE_A],
                   regex=r"612,000\.00[^.\n]{0,120}(board|authoriz|budget|approved)|"
                         r"(board|authoriz|budget|approved)[^.\n]{0,120}612,000\.00")))
    R.append((APPDB, OC, 1, "-", "No",
              A_ + "that none of the five Board-approved roles is filled at %s." % ASOF,
              "The request asks the summary to say how many approved roles are filled, and the "
              "ATS export shows all five still open with no offer.",
              [ats, board],
              dict(kind="summary", pages=[PAGE_A], prose_only=True,
                   regex=r"\b(0|zero|none|no)\b[^.\n]{0,80}\bfilled\b|\bunfilled\b|"
                         r"\bfilled\b[^.\n]{0,40}\b(0|zero|none)\b")))
    # ---- the staffed role page
    R.append((APPDB, OC, 2, "-", "No",
              "States that a Wiki.js page titled %s is published." % PAGE_B,
              "A second page is named by the request and asked for in Wiki.js, so it exists "
              "under that title with its published flag set.",
              [REQUEST, wiki], dict(kind="exists", pages=[PAGE_B])))
    R.append((APPDB, EA, 10, "Critical value", "Yes",
              B_ + "%d current employees at %s." % (len(POP), ASOF),
              "Fifty-two employees sit on the master roster and the August org chart. BambooHR's "
              "%d active records hold four contractors and three ended employees and lack two "
              "working hires, and the People Metrics method leaves all three classes out."
              % len(BAMBOO_ACTIVE),
              [roster, org, emp, xwalk, metrics],
              dict(kind="count", pages=[PAGE_B], key_re=r"[a-z]{3}-\d{4}", expected=len(POP),
                   summary_re=r"\b52\b[^.\n]{0,80}(current employee|employees|headcount|people)|"
                              r"(current employee|employees|headcount|people)[^.\n]{0,80}\b52\b")))
    for u, refs in ((UNLOADED[0], [roster, org, ticket, xwalk]),
                    (UNLOADED[1], [roster, org, apps, xwalk])):
        R.append((APPDB, EA, 7, "-", "Yes",
                  B_ + "%s, %s, as a current employee in %s." % (u["name"], u["id"], u["dept"]),
                  "%s started %s on the master roster and sits on the August org chart under "
                  "%s. The crosswalk carries the number as Never Loaded, so BambooHR alone "
                  "misses the person." % (u["name"].split()[-1], u["hire"], u["mgr"]),
                  refs,
                  dict(kind="cell", pages=[PAGE_B], keys=[u["id"]], column="department",
                       expected=[u["dept"]])))
    for s, refs in ((STALE[2], [resig, xwalk, org, emp]), (STALE[0], [arch, xwalk, org, emp]),
                    (STALE[1], [arch, xwalk, org, emp])):
        R.append((APPDB, EA, 5, "-", "Yes",
                  B_ + "that %s, %s, is a BambooHR active record left out of the current "
                  "employee count." % (s["name"], s["id"]),
                  "%s ended employment %s on the SplinterHR archive and the crosswalk, and is on "
                  "neither the August org chart nor the master roster, while the BambooHR "
                  "record still reads Active." % (s["name"].split()[-1], s["ended"]),
                  refs,
                  dict(kind="absent", pages=[PAGE_B], keys=[s["id"]],
                       mentions=[s["id"], s["name"].split()[-1]])))
    R.append((APPDB, EA, 5, "-", "Yes",
              B_ + "that the four contractor records %s are left out of the current employee "
              "count." % ", ".join(c["id"] for c in CONTRACTORS),
              "BambooHR carries the four contractors as active employee rows, and the People "
              "Metrics method and the Finance cost memo both leave contractors out of headcount.",
              [emp, roster, metrics, cost],
              dict(kind="no_rows", pages=[PAGE_B], key_re=r"ctr-\d{4}",
                   mention_re=r"ctr-20\d\d|\b(4|four) contractors?\b")))
    DEPT_EXPL = {
        "Engineering": "The master roster and the August org chart carry %d in Engineering, "
                       "where BambooHR's active records carry %d with three contractors inside.",
        "Sales": "Sales carries %d on the master roster and the August org chart, where "
                 "BambooHR's active records carry %d with two ended employees inside.",
        "Product": "Product carries %d on the master roster and the August org chart, where "
                   "BambooHR's active records carry %d with a contractor inside.",
    }
    for d, w in (("Engineering", 2), ("Sales", 2), ("Product", 2)):
        R.append((APPDB, OC, w, "-", "No",
                  B_ + "%d current employees in %s." % (DEPT_COUNT[d], d),
                  DEPT_EXPL[d] % (DEPT_COUNT[d], BAMBOO_DEPT[d]),
                  [roster, org, emp],
                  dict(kind="count", pages=[PAGE_B], key_re=r"[a-z]{3}-\d{4}", expected=DEPT_COUNT[d],
                       filter_column="department", filter_value=d,
                       summary_re=r"%s[^.\n]{0,25}\b%d\b|\b%d\b[^.\n]{0,25}%s"
                                  % (d.lower(), DEPT_COUNT[d], DEPT_COUNT[d], d.lower()),
                       summary_figure_re=r"%s\s+(?P<n>\d{1,2})\b" % d.lower())))
    R.append((APPDB, OC, 1, "-", "No",
              B_ + "%d current employees in Customer Success, %d in Marketing and %d in Finance "
              "and Corporate." % (DEPT_COUNT["Customer Success"], DEPT_COUNT["Marketing"],
                                  DEPT_COUNT["Finance and Corporate"]),
              "Customer Success 11, Marketing 5 and Finance and Corporate 5 are the counts on "
              "the master roster and the August org chart. The Customer Success count holds "
              "because one ended record leaves and one unloaded hire enters.",
              [roster, org],
              dict(kind="count_multi", pages=[PAGE_B], key_re=r"[a-z]{3}-\d{4}",
                   filter_column="department",
                   expected_by_value={d: DEPT_COUNT[d] for d in
                                      ("Customer Success", "Marketing", "Finance and Corporate")},
                   summary_by_value={d: r"%s[^.\n]{0,25}\b%d\b|\b%d\b[^.\n]{0,25}%s"
                                     % (d.lower(), DEPT_COUNT[d], DEPT_COUNT[d], d.lower())
                                     for d in ("Customer Success", "Marketing",
                                               "Finance and Corporate")})))
    R.append((APPDB, EA, 5, "-", "Yes",
              B_ + "%d current employees in a role that carries an open requisition."
              % len(WITH_REQ),
              "Five open titles on the ATS export match a roster title, Senior Software "
              "Engineer, Software Engineer II, Account Executive, Customer Success Manager and "
              "Product Designer. %d of the %d current employees hold one of them."
              % (len(WITH_REQ), len(POP)),
              [roster, ats, jobs],
              dict(kind="count", pages=[PAGE_B], key_re=r"[a-z]{3}-\d{4}", expected=len(WITH_REQ),
                   filter_column="open requisition", filter_re=r"req-\d{4}-\d{3}")))
    R.append((APPDB, OC, 2, "-", "No",
              B_ + "%d current employees in a role with no open requisition, in a table of "
              "their own." % len(WITHOUT_REQ),
              "No open title on the ATS export matches the other %d roster titles, and the "
              "request puts those employees in a second table of the same shape."
              % len(WITHOUT_REQ),
              [roster, ats],
              dict(kind="count", pages=[PAGE_B], key_re=r"[a-z]{3}-\d{4}", expected=len(WITHOUT_REQ),
                   filter_column="open requisition", filter_none=True, own_table=True)))
    MGR_EXPL = ("The August org chart hangs %s under %s and the master roster carries %s as "
                "the manager, and BambooHR has no row to say otherwise.",
                "%s sits under %s on the August org chart and the master roster carries %s as "
                "the manager, and BambooHR has no row to say otherwise.")
    for u, mgr_key, expl in ((UNLOADED[0], "TRT-0021", MGR_EXPL[0]),
                             (UNLOADED[1], "TRT-0018", MGR_EXPL[1])):
        R.append((APPDB, OC, 2, "-", "No",
                  B_ + "%s as %s's manager." % (u["mgr"], u["name"]),
                  expl % (u["name"].split()[-1], u["mgr"], mgr_key),
                  [org, roster],
                  dict(kind="cell", pages=[PAGE_B], keys=[u["id"]], column="manager",
                       contains=[u["mgr"].split()[-1], mgr_key])))
    R.append((APPDB, OC, 2, "-", "No",
              B_ + "that BambooHR carries %d active records." % len(BAMBOO_ACTIVE),
              "How the current employee count reconciles to the BambooHR active record count is "
              "what the request asks the summary for, and that count is %d on the employee "
              "table and on the People Metrics page." % len(BAMBOO_ACTIVE),
              [emp, metrics],
              dict(kind="summary", pages=[PAGE_B], prose_only=True,
                   regex=r"\b57\b[^.\n]{0,80}(bamboohr|active record|hris)|"
                         r"(bamboohr|active record|hris)[^.\n]{0,80}\b57\b")))
    # ---- the request's two FORM instructions, graded because the 09/15/2026 EPM direction
    # requires every explicit ask to be evaluated and names formatting as one
    R.append((APPDB, OC, 1, "-", "No", FORM_VOCAB_CRIT,
              "The request fixes the Board approval vocabulary to those two values so the "
              "operating review reads one word per requisition.",
              [REQUEST],
              dict(kind="vocab", pages=[PAGE_A], column="board approval",
                   allowed=["Approved", "Not approved"])))
    R.append((APPDB, OC, 1, "-", "No", FORM_DATES_CRIT,
              "MM/DD/YYYY is the form the request sets and the form every Troutly record in "
              "the packet already uses, from the ATS export to the master roster.",
              [REQUEST, ats, roster],
              dict(kind="dates", pages=[PAGE_A, PAGE_B])))
    return R


RUBRIC = _rubric()

# ---------------------------------------------------------------- the import (what registers)
# Both snapshot ids are read off an export, never invented. They were read off the nine trajectory
# exports of 09/19/2026, every one carrying the same pair; check_import() refuses to call the file
# loadable while either is the sentinel.
SNAP = "snap_c6f6a0879f3d47a19048ee80d7529157"  # world_snapshot_id, nine exports of 09/19/2026
TASK_SNAP = "snap_dc228e8bba9d423fbe9f3dd35862f658"  # task_data_id, the same exports
UPLOAD_PREFIX = "00_task_input_"
TASK_UPLOADS = tuple(n[len(UPLOAD_PREFIX):] for n in TASK_INPUTS)
IMPORT_DB_DROPDOWN = {"Objective Compliance", "Expert Assessment", "Process"}
IMPORT_TAGS = {"Final Response", "Style / formatting"}
FORM_TAG = "Style / formatting"


def import_tag(kind, crit):
    return FORM_TAG if crit in FORM_ROWS else "Final Response"


def artifact(ref):
    """(name, source) for one of _rubric()'s reference strings in the picker's namespace, or
    None for an app seed table, which the picker's browser does not list."""
    if ref.startswith("/"):
        return "filesystem" + ref, "world"
    if ref in TASK_UPLOADS:
        return "filesystem/" + ref, "task"
    return None


# ---------------------------------------------------------------- frozen archives
STAMP = datetime.datetime(2026, 8, 31, 9, 0, 0)
ZIP_STAMP = (2026, 8, 31, 9, 0, 0)
ISO_STAMP = "2026-08-31T09:00:00Z"


def stamp(wb):
    wb.properties.creator = "Casey Ouk"
    wb.properties.lastModifiedBy = "Casey Ouk"
    wb.properties.created = STAMP
    wb.properties.modified = STAMP


def freeze(path):
    src = zipfile.ZipFile(path)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as out:
        for info in src.infolist():
            data = src.read(info.filename)
            if info.filename == "docProps/core.xml":
                text = data.decode("utf8")
                text, n = re.subn(r"(<dcterms:modified[^>]*>)[^<]+(</dcterms:modified>)",
                                  r"\g<1>%s\g<2>" % ISO_STAMP, text)
                assert n == 1, "expected one dcterms:modified in core.xml, found %d" % n
                data = text.encode("utf8")
            zi = zipfile.ZipInfo(info.filename, date_time=ZIP_STAMP)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = info.external_attr
            out.writestr(zi, data)
    src.close()
    open(path, "wb").write(buf.getvalue())


def sheet(wb, title, widths, headers, rows, first=False):
    ws = wb.active if first else wb.create_sheet()
    ws.title = title
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[chr(64 + i)].width = w
    ws.append(headers)
    for c in ws[1]:
        c.font = BOLD
    for r in rows:
        ws.append(list(r))
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.alignment = WRAP
    return ws


def md5(path):
    return hashlib.md5(open(path, "rb").read()).hexdigest()


# ---------------------------------------------------------------- the show-your-work upload
def syw():
    wb = Workbook()
    stale = ". ".join("%s %s ended %s" % (s["name"], s["id"], s["ended"]) for s in STALE)
    sheet(wb, "Sources", [30, 46, 74], ["Fact", "Source", "Value"], [
        ("The Board authorized five roles",
         "Board-approved hiring plan of 06/20/2026, page 2, /" + BOARD_PLAN,
         "Senior Software Engineer IC4, Software Engineer II IC3, Account Executive AE, Customer "
         "Success Manager CSM I and Product Designer IC3, priced at 2026 draft midpoints, "
         "total annualized budget %s with a %s reserve inside it." % (BOARD_BUDGET, "$20,000.00")),
        ("The conditional backfill",
         "Same plan, page 2, and the minutes, item 7",
         "One Customer Success backfill at the CSM I midpoint, authorized to fill on a Customer "
         "Success departure before %s. It is outside the %s." % (BACKFILL_DEADLINE, BOARD_BUDGET)),
        ("Requisition discipline",
         "Same plan, appendix B, and the minutes, item 7, fourth resolution",
         "A requisition must trace line for line to a Board authorization. One opened from a "
         "working spreadsheet or a draft plan is unauthorized and is closed or held. No offer may "
         "be written at a level other than the level listed."),
        ("The plan supersedes the workbook",
         "Same plan, page 1, approval reference",
         "The document supersedes any prior draft, working spreadsheet or informal circulation "
         "on the same subject."),
        ("Who reports to the Board",
         "Minutes of 06/20/2026, item 7, fifth resolution, /" + MINUTES,
         "The Head of People and the Chief Executive Officer report requisitions opened, offers "
         "extended and accepted, start dates and the annualized commitment against %s at each "
         "regular meeting." % BOARD_BUDGET),
        ("The eight open requisitions",
         "ATS requisition export of %s, /%s" % (ASOF, ATS),
         "REQ-2026-031 to 035 sourced to the Board plan. REQ-2026-036 sourced to a backfill for "
         "TRT-0064 at CSM II. REQ-2026-037 and 038 sourced to Hiring_Plan_2026_FINAL. Offer "
         "accepted 08/20/2026 on 038 for Kwame Adjei, start 09/08/2026."),
        ("The same requisitions in Greenhouse",
         "Greenhouse jobs, hiring team, users and applications tables",
         "Ten jobs. Eight open with the requisition IDs above and one hiring manager each. Two "
         "closed from the second-quarter plan, REQ-2026-029 filled by Simone Okonkwo and "
         "REQ-2026-030 filled by Rafael Ibarra. Three applications, all hired."),
        ("The working spreadsheet and its wiki page",
         "Hiring_Plan_2026_FINAL, /%s, and the Hiring Plan wiki page" % PLAN_FINAL,
         "Eight roles at 2025 midpoints totalling %s, footed Board approved 06/20/2026 on the "
         "sheet and on the page. The three extra lines are Marketing Manager, Data Analyst II "
         "and a second Account Executive." % PLAN_BUDGET),
        ("The accepted offer",
         "Offer of employment ATS-4471, /" + OFFER_ADJEI,
         "Kwame Adjei, Data Analyst II, Product, %s base, issued 08/18/2026 against REQ-2026-038, "
         "accepted 08/20/2026, start 09/08/2026." % "$89,500.00"),
        ("Simone Okonkwo's start date",
         "Offer of 07/02/2026, the email thread of 07/09/2026 and the IT ticket of 07/22/2026",
         "The signed offer names %s. The thread moves the start to 07/22/2026 at her request "
         "and Luka confirms it. The IT ticket, the Greenhouse note and the master roster carry "
         "07/22/2026." % OKONKWO_OFFER_START),
        ("The current employees",
         "Master employee roster as of %s, /%s" % (ASOF, ROSTER),
         "%d active employees with employee ID, title, department and manager ID. Four "
         "contractors on their own tab. %s." % (len(POP), ", ".join(
             "%s %d" % (d, DEPT_COUNT[d]) for d in DEPT_ORDER))),
        ("The same people on the org chart",
         "Organization chart of 08/24/2026, /" + ORG_AUG,
         "Every roster employee is a solid box with its employee ID, hung under its manager. The "
         "four contractors are dotted boxes hung from engagement owners. TRT-0037, TRT-0049 and "
         "TRT-0064 are not on it. TRT-0153 and TRT-0155 are."),
        ("What BambooHR carries",
         "BambooHR employee table",
         "%d rows, %d Active. The four contractors are Active employee rows. TRT-0037, TRT-0049 "
         "and TRT-0064 are Active. TRT-0153 and TRT-0155 are not in the table."
         % (len(BAMBOO), len(BAMBOO_ACTIVE))),
        ("The crosswalk",
         "Employee ID crosswalk of 08/28/2026, /" + CROSSWALK,
         "TRT-0037, TRT-0049 and TRT-0064 carry a BambooHR number and read Terminated. TRT-0153 "
         "and TRT-0155 carry no BambooHR number and read Never Loaded."),
        ("When the three ended",
         "SplinterHR final archive of 07/28/2026, Employees tab, /" + ARCHIVE,
         stale + ". Each with an approver on the record."),
        ("The resignation behind TRT-0064",
         "Email thread of 05/29/2026, /" + RESIGNATION_0064,
         "Marguerite Delacroix-Hahn resigns with last day 06/15/2026 and Edith Bustamante "
         "accepts it. The Board minutes report the departure at item 6."),
        ("How people are counted",
         "People Metrics wiki page and the Finance cost memo of 08/06/2026, /" + COST_MEMO,
         "Active employees as of the date. Contractors out. Accepted offers with future start "
         "dates out. Ended employment out. The page carries %d, which is the BambooHR active "
         "row count taken whole." % METRICS_HEADCOUNT),
        ("Role titles and levels",
         "Leveling guide v2.1 of 07/15/2026, /" + LEVELING,
         "Customer Success Manager is CSM I. Customer Success Manager II is CSM II and Senior "
         "Customer Success Manager resolves to it. Data Analyst is Analytics IC2 and Data "
         "Analyst II is Analytics IC3, so the two are different roles."),
        ("The pages the request names",
         "Wiki.js pages table and the request memo, the task input file " + REQUEST,
         "Ten seeded pages. The request asks for two more with exact titles, the tables and "
         "columns each carries, the fixed vocabulary of the status cells and the summaries."),
    ], first=True)

    sheet(wb, "Verifiers", [5, 96, 6, 8, 13],
          ["#", "Verifier", "Type", "Weight", "Gate"],
          [(i, c[5], "EA" if c[1] == EA else "OC", c[2], c[3])
           for i, c in enumerate(RUBRIC, 1)] + [
        (),
        ("Note", "The heavy rows are the current employee count, the two hires BambooHR never "
         "loaded, the three ended records it still calls Active and the Board reading of "
         "REQ-2026-036.", "", "", ""),
        ("Note", "The light rows are the fields the request asks for that a run reading the "
         "ATS export and the Board plan prints correctly on the way.", "", "", ""),
    ])

    sheet(wb, "Row assembly", [56, 60], ["Step", "Result"], [
        ("The Board lines",
         "Five roles on page 2 of the Board plan, each with a level, a department and a hiring "
         "manager, at %s. One conditional CSM I backfill outside it." % BOARD_BUDGET),
        ("The open requisitions",
         "Eight on the ATS export and in Greenhouse. Each matched to a Board line by title, "
         "level and department."),
        ("The five that trace",
         "REQ-2026-031 to 035. Approved. Open with no offer at %s." % ASOF),
        ("The backfill requisition",
         "REQ-2026-036 was opened at CSM II. The Board line is CSM I. Not approved as opened."),
        ("The two from the workbook",
         "REQ-2026-037 and 038 were opened from Hiring_Plan_2026_FINAL, which the plan "
         "supersedes. Not approved. 038 holds an accepted offer dated 08/20/2026."),
        ("The recruiting records with no employee match",
         "Kwame Adjei, offer accepted, start 09/08/2026, not working at %s. Simone Okonkwo and "
         "Rafael Ibarra, hired on second-quarter requisitions, working, no BambooHR row." % ASOF),
        ("The population",
         "%d on the master roster and the August org chart. BambooHR's %d active rows less 4 "
         "contractors less 3 ended plus 2 unloaded." % (len(POP), len(BAMBOO_ACTIVE))),
        ("The count by department",
         ", ".join("%s %d" % (d, DEPT_COUNT[d]) for d in DEPT_ORDER) + "."),
        ("The managers",
         "From the August org chart and the roster's manager ID. Okonkwo under Edith Bustamante. "
         "Ibarra under Marisela Thornbury. The CEO has none."),
        ("Roles with an open requisition",
         "%d employees hold a title that an open requisition carries. %d do not and sit in the "
         "second table." % (len(WITH_REQ), len(WITHOUT_REQ))),
        ("The pages",
         "Two Wiki.js pages with the exact titles, each with its summary above its tables, "
         "Approved or Not approved in every Board approval cell, every date MM/DD/YYYY."),
    ])
    out = os.path.join(PKG, "03_show_your_work.xlsx")
    stamp(wb)
    wb.save(out)
    freeze(out)
    return out


# ---------------------------------------------------------------- checks
def check_world():
    """Every graded value recomputed from the world's own bytes, before anything is written."""
    # the population, four ways
    assert len(POP) == 52 and len(CONTRACTORS) == 4, (len(POP), len(CONTRACTORS))
    assert len(BAMBOO_ACTIVE) == 57 and sum(1 for e in BAMBOO_ACTIVE
                                           if e["employee_number"].startswith("CTR-")) == 4
    assert STALE_IDS == ["TRT-0037", "TRT-0049", "TRT-0064"], STALE_IDS
    assert UNLOADED_IDS == ["TRT-0153", "TRT-0155"], UNLOADED_IDS
    assert [s["ended"] for s in STALE] == ["03/20/2026", "05/08/2026", "06/15/2026"], STALE
    assert [u["hire"] for u in UNLOADED] == ["07/22/2026", "08/03/2026"], UNLOADED
    assert DEPT_COUNT == {"Engineering": 19, "Product": 4, "Sales": 8, "Marketing": 5,
                          "Customer Success": 11, "Finance and Corporate": 5}, DEPT_COUNT
    assert BAMBOO_DEPT == {"Engineering": 22, "Product": 5, "Sales": 9, "Marketing": 5,
                           "Customer Success": 11, "Finance and Corporate": 5}, BAMBOO_DEPT
    xwalk = {r[0]: r[6] for r in _rows(CROSSWALK) if isinstance(r[0], str)}
    assert all(xwalk[i] == "Terminated" for i in STALE_IDS), xwalk
    assert all(xwalk[i] == "Never Loaded" for i in UNLOADED_IDS), xwalk
    org = _pdf_text(ORG_AUG)
    for p in POP:
        assert p["id"] in org, "%s is not on the August org chart" % p["id"]
    for i in STALE_IDS:
        assert i not in org, "%s is on the August org chart" % i
    for c in CONTRACTORS:
        assert "%s Contractor" % c["id"] in org, c
    assert "As of 08/24/2026" in org and "Anjelina Brocollini, Head of People" in org
    jan = _pdf_text(ORG_JAN)
    assert "TRT-0037" in jan and "TRT-0064" in jan and "Grayson Oshimoto" in jan
    # managers agree between BambooHR and the roster wherever both carry the person
    bam = {e["employee_number"]: e for e in BAMBOO}
    for p in POP:
        if p["id"] in bam:
            assert (bam[p["id"]]["supervisor_id"] or None) == p["mgr_id"], p
            assert bam[p["id"]]["job_title"] == p["role"] and bam[p["id"]]["department"] == p["dept"]
    assert next(p for p in POP if p["id"] == "TRT-0153")["mgr"] == "Edith Bustamante"
    assert next(p for p in POP if p["id"] == "TRT-0155")["mgr"] == "Marisela Thornbury"
    assert next(p for p in POP if p["id"] == "TRT-0001")["mgr"] == "None"
    ticket = _pdf_text(IT_TICKET)
    assert "TRT-0153" in ticket and "Edith Bustamante" in ticket and "07/22/2026" in ticket
    # the Board plan and the minutes
    board = _pdf_text(BOARD_PLAN)
    for role, level, dept, mgr, mid in BOARD_LINES:
        assert re.search(r"%s %s %s %s %s" % tuple(re.escape(x) for x in (role, level, dept, mgr, mid)),
                         board), (role, board[:200])
    for phrase in ("TOTAL ANNUALIZED BUDGET $612,000.00", "CSM I Customer Success $96,000.00",
                   "traceable line-for-line", "shall be closed or held pending a further Board",
                   "supersedes any prior draft, working spreadsheet",
                   "No offer may be written at a level other than the level listed above"):
        assert phrase in board, phrase
    minutes = _pdf_text(MINUTES)
    for phrase in ("total annualized budget of $612,000.00",
                   "priced at the CSM I", "shall be treated as unauthorized",
                   "Head of People, upon her arrival on or about August 3, 2026"):
        assert phrase in minutes, phrase
    assert "tendered on May 29, 2026" in minutes and "last day of June 15, 2026" in minutes
    # the requisitions
    assert [r["req"] for r in REQS] == ["REQ-2026-03%d" % n for n in range(1, 9)], REQS
    assert [r["approval"] for r in REQS] == ["Approved"] * 5 + ["Not approved"] * 3
    assert len(OPEN_NO_OFFER) == 7 and REQS[7]["status"] == "Offer accepted"
    ats = [r for r in _rows(ATS) if isinstance(r[0], str) and r[0].startswith("REQ-")]
    assert len(ats) == 8 and ats[7][8] == "Offer accepted 08/20/2026" and "09/08/2026" in ats[7][9]
    assert ats[5][2] == "CSM II" and "TRT-0064" in ats[5][6]
    assert ats[6][6] == "Hiring_Plan_2026_FINAL" == ats[7][6]
    assert all(a[6] == "Board plan 06/20/2026" for a in ats[:5])
    assert all(a[4] == r["owner"] for a, r in zip(ats, REQS))
    for r in REQS:
        assert r["role"] == next(a[1] for a in ats if a[0] == r["req"])
    j36 = next(j for j in JOBS if j["req"] == "REQ-2026-036")
    assert j36["role"] == "Customer Success Manager II" and "TRT-0064" in j36["notes"]
    closed = {j["req"]: j for j in JOBS if j["status"] == "closed"}
    assert set(closed) == {"REQ-2026-029", "REQ-2026-030"}
    apps = _csv("greenhouse", "applications.csv")
    assert [a["status"] for a in apps] == ["hired"] * 3 and {a["job_id"] for a in apps} == {"8", "9", "10"}
    notes = " ".join(n["body"] for n in _csv("greenhouse", "notes.csv"))
    for phrase in ("Start date moved from 07/13 to 07/22", "Offer accepted and signed 08/20/2026. "
                   "Start date 09/08/2026", "Start date 08/03/2026. Employee ID TRT-0155"):
        assert phrase in notes, phrase
    offer = _pdf_text(OFFER_ADJEI)
    assert "September 8, 2026" in offer and "REQ-2026-038" in offer and "Date: 08/20/2026" in offer
    okoffer = _pdf_text(OFFER_OKONKWO)
    assert "July 13, 2026 (07/13/2026)" in okoffer
    thread = open(os.path.join(WORLD, THREAD_OKONKWO), encoding="utf8").read()
    assert "new start date is 07/22/2026" in re.sub(r"\s+(?:>\s*)*", " ", thread)
    resig = open(os.path.join(WORLD, RESIGNATION_0064), encoding="utf8").read()
    assert "last day 06/15/2026" in resig
    # the workbook, the wiki pages and the cost memo
    plan = _rows(PLAN_FINAL)
    assert any(r[0] == "TOTAL" and str(r[5]) == "868000" for r in plan) and \
        any(r[0] == "Board approved 06/20/2026" for r in plan)
    assert sum(1 for r in plan if isinstance(r[1], str) and r[1].endswith("2026")
               and isinstance(r[4], (int, float))) == 8
    wiki = open(os.path.join(WORLD, WIKI_PLAN), encoding="utf8").read()
    assert "Board approved on 06/20/2026" in wiki and "$868,000.00" in wiki and "8 roles" in wiki
    metrics = open(os.path.join(WORLD, WIKI_METRICS), encoding="utf8").read()
    assert "Headcount 57" in metrics and "Open reqs: 8" in metrics and "contractors handled separately" in metrics
    pages = {r["title"]: r for r in _csv("wiki_js", "Page.csv")}
    assert set(pages) >= {"Hiring Plan", "People Metrics", "Team Directory"} and len(pages) == 10
    assert PAGE_A not in pages and PAGE_B not in pages
    assert "$868,000.00" in pages["Hiring Plan"]["content"] and "Headcount 57" in pages["People Metrics"]["content"]
    cost = _docx_text(COST_MEMO)
    assert "excludes contractors, excludes accepted offers with future start dates" in cost
    lev = _docx_text(LEVELING)
    assert "Customer Success Manager II | Customer Success | CSM II" in lev and \
        "Data Analyst II | Analytics | Analytics IC3" in lev
    assert _csv("bamboohr", "DefaultUser.csv")[0]["employee_id"] == "TRT-0156"
    assert any(u["email"] == "casey@troutlyanalytics.com" for u in _csv("wiki_js", "User.csv"))
    # the arithmetic
    assert len(WITH_REQ) == 21 and len(WITHOUT_REQ) == 31
    assert len(BAMBOO_ACTIVE) - len(CONTRACTORS) - len(STALE) + len(UNLOADED) == len(POP)
    assert {p["req"] for p in WITH_REQ} == {"REQ-2026-03%d" % n for n in range(1, 6)}
    print("world: %d current employees, %d BambooHR active, %d approved of %d open requisitions"
          % (len(POP), len(BAMBOO_ACTIVE), len(APPROVED), len(REQS)))


def check_rubric():
    total = sum(c[2] for c in RUBRIC)
    gates = [c for c in RUBRIC if c[3] != "-"]
    assert all(c[2] in BANDS[c[1]] for c in RUBRIC), "a weight sits outside its band"
    assert all((c[2] == 10) == (c[3] != "-") for c in RUBRIC), "weight 10 and gate must coincide"
    assert 1 <= len(gates) <= 8 and sum(c[3] == "Critical value" for c in gates) <= 5
    assert all(c[1] == EA or c[3] == "Critical value" for c in gates)
    ea = sum(c[2] for c in RUBRIC if c[1] == EA)
    assert ea * 2 >= total, "Expert Assessment under half the weight"
    assert len(RUBRIC) >= 5
    assert all(c[0] == APPDB for c in RUBRIC)
    kinds = set()
    for c in RUBRIC:
        crit = c[5]
        assert crit.startswith("States"), "a row must open with States: " + crit
        assert not re.search(r"\b(and that|as well as|in addition)\b|;", crit), "stacked: " + crit
        assert "prompt" not in crit.lower() and ".docx" not in crit and ".pdf" not in crit, crit
        assert all(ord(ch) < 128 for ch in crit), crit
        assert isinstance(c[8], dict) and c[8].get("kind") and c[8].get("pages"), crit
        kinds.add(c[8]["kind"])
    print("rubric: %d verifiers, %d points, %d gates, EA %.1f%%, OC %.1f%%, %d check kinds"
          % (len(RUBRIC), total, len(gates), 100.0 * ea / total, 100.0 * (total - ea) / total,
             len(kinds)))
    return total


def check_register():
    """The judge-facing strings, held to the house register HR 32 settled and HR 79 carries.
    ASCII only, no colons or brackets, no spaced dash outside the two page titles, months never
    spelled, no ISO dates, no grading vocabulary, no self-reference, a source named, at most
    three sentences and 240 characters."""
    SOURCES = ("Board", "ATS", "Greenhouse", "BambooHR", "roster", "org chart", "crosswalk",
               "archive", "offer", "email", "IT ticket", "People Metrics", "cost memo",
               "request", "Hiring_Plan_2026_FINAL", "resig", "Wiki.js")
    MONTHS = re.compile(r"\b(January|February|March|April|May|June|July|August|September|"
                        r"October|November|December)\s+\d{1,2}(?!\d)")
    ISO_DATE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
    SELF_REFERENCE = re.compile(
        r"\b(this row|that row|these rows|the row|rows? above|rows? below|own rows?|above it|"
        r"the other rows?|the other (two|three|four)|as the rest|a response|a run|elsewhere)\b",
        re.I)
    GRADING = re.compile(
        r"\b(pass|passes|passing|passed|fail|fails|failing|failed|satisf(y|ies|ied)|"
        r"penalis\w*|penaliz\w*|scores?|scored|grade[sd]?|grading|grader|"
        r"verifier|rubric|criterion|criteria)\b", re.I)
    lengths, firsts = [], []
    for i, c in enumerate(RUBRIC, 1):
        crit, e = c[5], c[6]
        for label, text in (("criteria", crit), ("explanation", e)):
            assert not MONTHS.search(text), "v%d %s spells a month" % (i, label)
            assert not ISO_DATE.search(text), "v%d %s carries an ISO date" % (i, label)
        assert crit.endswith("."), "v%d criteria is not a full sentence" % i
        assert all(ord(ch) < 128 for ch in e), e
        assert not any(ch in e for ch in ":;()[]"), e
        assert not re.search(r"(?<![A-Za-z0-9])-|-(?![A-Za-z0-9])", e), e
        hit = GRADING.search(e)
        assert hit is None, "v%d explanation describes grading (%r)" % (i, hit.group(0) if hit else "")
        ref = SELF_REFERENCE.search(e)
        assert ref is None, "v%d explanation refers to the rubric's own construction" % i
        assert any(t in e for t in SOURCES), "no source named: " + e
        assert len(e) <= 240, "%d chars: %s" % (len(e), e)
        sentences = len(re.findall(r"\.(?:\s|$)", e))
        assert sentences <= 3, "v%d explanation runs to %d sentences" % (i, sentences)
        lengths.append(len(e))
        firsts.append(" ".join(e.split()[:3]))
    seen = [c[6] for c in RUBRIC]
    dupes = sorted({e for e in seen if seen.count(e) > 1})
    assert not dupes, "explanations repeat verbatim across rows: %r" % dupes[:1]
    assert len(set(firsts)) == len(firsts), "two explanations open alike"
    avg = sum(lengths) / len(lengths)
    assert avg <= 200, "explanations average %.0f chars" % avg
    print("register: %d explanations, %d-%d chars, %.0f average"
          % (len(lengths), min(lengths), max(lengths), avg))


# The request's clauses, typed, and the rows that grade each. Every clause is a VERBATIM
# substring of the memo block in task_input_source.md, so a reworded request breaks the build.
# DELIVERABLE and FORM clauses must carry a row; a FENCE may host none.
DELIVERABLE, FORM, FENCE = "deliverable", "form", "fence"
ASKS = [
    ("Two pages published in Wiki.js", 2, DELIVERABLE),
    ("requisition ID, role, department, owner, Board approval, hiring status, and the source "
     "date for the status", 9, DELIVERABLE),
    ("a second table for recruiting records with no matching BambooHR employee record", 4,
     DELIVERABLE),
    ("the Board-authorized annualized budget", 1, DELIVERABLE),
    ("how many of the approved roles are filled", 1, DELIVERABLE),
    ("employee ID, name, department, role, manager, and the open requisition that carries the "
     "same title as the role", 5, DELIVERABLE),
    ("Employees whose role has no open requisition go in a second table of the same shape", 1,
     DELIVERABLE),
    ("the current employee count, the count by department", 5, DELIVERABLE),
    ("the reconciling items between that count and the BambooHR active record count", 5,
     DELIVERABLE),
    ("Board approval reads Approved or Not approved", 1, FORM),
    ("Dates MM/DD/YYYY", 1, FORM),
    ("Compensation, the September cycle and PTO are no part of this request", 0, FENCE),
    ("Change nothing in BambooHR or Greenhouse", 0, FENCE),
]
ASK_OF = {
    "exists": "Two pages published in Wiki.js",
}


def _ask_for(c):
    """Which clause a row hangs on, from the criterion and the spec."""
    crit, spec = c[5], c[8]
    if crit in FORM_ROWS:
        return "Board approval reads Approved or Not approved" if "Board approval" in crit \
            else "Dates MM/DD/YYYY"
    if spec["kind"] == "exists":
        return "Two pages published in Wiki.js"
    if spec["pages"] == [PAGE_A]:
        if spec["kind"] == "summary":
            return "the Board-authorized annualized budget" if "budget" in crit \
                else "how many of the approved roles are filled"
        if spec.get("column") in ("working at", "bamboohr record", "start date"):
            return "a second table for recruiting records with no matching BambooHR employee record"
        return ("requisition ID, role, department, owner, Board approval, hiring status, and the "
                "source date for the status")
    if spec["kind"] in ("absent", "no_rows") or (spec["kind"] == "summary" and "57" in crit):
        return "the reconciling items between that count and the BambooHR active record count"
    if spec["kind"] == "count" and spec.get("own_table"):
        return "Employees whose role has no open requisition go in a second table of the same shape"
    if spec["kind"] in ("count", "count_multi") and not spec.get("filter_column") == "open requisition":
        return "the current employee count, the count by department"
    return ("employee ID, name, department, role, manager, and the open requisition that carries "
            "the same title as the role")


def check_asks():
    src = open(os.path.join(HERE, "task_input_source.md"), encoding="utf8").read()
    memo = " ".join(src.split("<!-- MEMO:BEGIN -->")[1].split("<!-- MEMO:END -->")[0].split())
    counts = {a[0]: 0 for a in ASKS}
    for c in RUBRIC:
        ask = _ask_for(c)
        assert ask in counts, "row hangs on an unlisted clause: %r" % ask
        counts[ask] += 1
    for clause, want, kind in ASKS:
        assert clause in memo, "the request does not ask it any more: %r" % clause
    for clause, want, kind in ASKS:
        if kind == FENCE:
            assert counts[clause] == 0, "a row hangs on a clause that fences work out of scope: %r" % clause
    for clause, want, kind in ASKS:
        if kind != FENCE:
            assert counts[clause] >= 1, ("an asking clause carries no row, and the rubric set "
                                         "has to evaluate it: %r" % clause)
    for clause, want, kind in ASKS:
        if kind != FENCE:
            assert counts[clause] == want, "%r carries %d rows, the record says %d" % (
                clause, counts[clause], want)
    print("asks: %d clauses, %d graded, %d fences carrying nothing"
          % (len(ASKS), sum(1 for a in ASKS if a[2] != FENCE), sum(1 for a in ASKS if a[2] == FENCE)))


def check_tools():
    """Every App DB row grades a Wiki.js page, so the platform has to offer a page-create tool
    and a route to read the pages table back. HR 79 learned to parse the platform's own tool
    catalogue rather than assume it. This world has no exported trajectory yet, so there is no
    catalogue to parse: the guard reports UNMEASURED and does not pass. Once
    tasks/APP_TOOL_SURFACE.md exists it fails the build unless a wiki write tool is listed."""
    cat = os.path.join(REPO, "tasks", "APP_TOOL_SURFACE.md")
    if not os.path.exists(cat):
        print("tools: UNMEASURED - no tasks/APP_TOOL_SURFACE.md yet; capture it from the first "
              "trajectory's toolbelt before the run set")
        return
    text = open(cat, encoding="utf8").read()
    tools = re.findall(r"^- `([a-z0-9_]+)`(.*)$", text, flags=re.M)
    assert len(tools) >= 100, "the tool catalogue is a stub, %d tools" % len(tools)
    writes = {n for n, tail in tools if "(write)" in tail}
    wiki_writes = [t for t in writes if "wiki" in t and "page" in t
                   and any(k in t for k in ("create", "update", "write", "publish"))]
    assert wiki_writes, "the tool catalogue lists no Wiki.js page-writing tool, so no App DB row here is reachable"
    print("tools: %d catalogued, wiki writers %r" % (len(tools), sorted(wiki_writes)))


def check_syw(path):
    EMPHASIS = re.compile(r"^[A-Z]{2,}[.,]?$")
    IDENTIFIER = re.compile(r"[/_0-9]")
    SECOND_PERSON = re.compile(r"\b(you|your|yours|yourself)\b", re.I)
    MONTHS = re.compile(r"\b(January|February|March|April|May|June|July|August|September|"
                        r"October|November|December)\s+\d{1,2}(?!\d)")
    ALLOWED_CAPS = {"VP", "HR", "MEMO", "PTO", "CEO", "CSM", "AE", "ATS", "IC2", "IC3", "IC4",
                    "II", "TX", "ID", "IT"}
    ROMAN = re.compile(r"^[IVXL]+$")
    CITED_SECTION = re.compile(r"\bSections?\b")

    def check_string(sh, text):
        where = "%s %r" % (sh, text[:60])
        assert all(ord(ch) < 128 for ch in text), "%s carries a non-ASCII character" % where
        shout = [w for w in text.split() if EMPHASIS.match(w) and not IDENTIFIER.search(w)
                 and w.strip(".,") not in ALLOWED_CAPS and not ROMAN.match(w.strip(".,"))]
        assert not shout, "%s shouts %r" % (where, shout[0])
        assert not SECOND_PERSON.search(text), "%s addresses the reader" % where
        assert not MONTHS.search(text), "%s spells a month" % where
        bad = [ch for ch in ";:()[]" if ch in text]
        assert not bad, "%s uses %r" % (where, bad[0])
        stripped = text.replace(PAGE_A, "").replace(PAGE_B, "")
        assert not re.search(r"(?<![A-Za-z0-9])-|-(?![A-Za-z0-9])", stripped), "%s uses a dash" % where

    wb = load_workbook(path)
    assert [ws.title for ws in wb] == ["Sources", "Verifiers", "Row assembly"], wb.sheetnames
    cells, sentences = 0, 0
    for ws in wb:
        if ws.title == "Verifiers":
            rows = list(ws.iter_rows(min_row=2, values_only=True))
            crits = [r[1] for r in rows if isinstance(r[0], int)]
            assert crits == [c[5] for c in RUBRIC], "Verifiers tab drifted from the rubric"
            for row in rows:
                if row[0] == "Note":
                    for text in row:
                        if isinstance(text, str) and text.strip():
                            check_string(ws.title, text)
            continue
        header = next(ws.iter_rows(max_row=1, values_only=True))
        source_col = next((i for i, h in enumerate(header) if h == "Source"), None)
        value_col = next(i for i, h in enumerate(header) if h in ("Value", "Result"))
        for row in ws.iter_rows(min_row=2, values_only=True):
            for col, text in enumerate(row):
                if not isinstance(text, str) or not text.strip():
                    continue
                check_string(ws.title, text)
                if col == source_col:
                    assert CITED_SECTION.search(text) is None, "capital Section in a Source cell"
                if col == value_col:
                    cells += 1
                    sentences += len(re.findall(r"\.(?:\s|$)", text))
    density = sentences / cells
    assert density <= 3.5, "value cells average %.1f sentences" % density
    print("show your work: %d value cells, %d sentences, %.1f a cell" % (cells, sentences, density))


def check_golden():
    """The golden pages are what the verifiers grade against in the battery, so hold them to the
    house register and to the facts before they are written."""
    for title, text in GOLDEN.items():
        # a person's name is a world fact and keeps the world's spelling; everything else is ASCII
        plain = text
        for p in POP:
            plain = plain.replace(p["name"], "")
        assert all(ord(ch) < 128 for ch in plain), "%s carries a non-ASCII character" % title
        assert text.startswith("# %s\n" % title)
        assert "## Reconciliation summary" in text
        assert not re.search(r"\b\d{4}-\d{2}-\d{2}\b", text), "ISO date on " + title
    a, b = GOLDEN[PAGE_A], GOLDEN[PAGE_B]
    assert a.count("\n| REQ-2026-0") == 8 and a.count("| REQ-2026-0") == 8 + 3
    assert a.count("| Not approved |") == 3 and a.count("| Approved |") == 5
    assert b.count("\n| TRT-") == 52 and "CTR-" not in b.split("## Staffed roles", 1)[1]
    for i in STALE_IDS:
        assert i not in b.split("## Staffed roles")[1] and i in b
    print("golden: two pages, %d and %d chars" % (len(a), len(b)))


def blockquotes(path):
    text = open(path, encoding="utf8").read()
    out = []
    for block in re.split(r"\n\s*\n", text):
        lines = block.strip().splitlines()
        if lines and all(l.startswith(">") for l in lines):
            out.append(" ".join(l.lstrip("> ").strip() for l in lines))
    return out


def check_hashes(meta):
    for name in ["03_show_your_work.xlsx", "05_rubric_import.xlsx"] + TASK_INPUTS + \
            list(GOLDEN_FILES.values()):
        path = os.path.join(PKG, name)
        if not os.path.exists(path):
            continue
        digest = md5(path)
        assert digest in meta, "02 publishes a stale md5 for %s, this build wrote %s" % (name, digest)


def check_import():
    rows = list(load_workbook(os.path.join(PKG, "05_rubric_import.xlsx"))["Rubric"]
                .iter_rows(values_only=True))
    hdr, body = rows[0], rows[1:]
    assert len(body) == len(RUBRIC), "the import carries %d rows, the rubric %d" % (len(body), len(RUBRIC))
    col = {name: n for n, name in enumerate(hdr)}
    with open(os.path.join(HERE, "rubric_preview.csv"), encoding="utf-8") as f:
        csv_rows = list(csv.DictReader(f))
    assert len(csv_rows) == len(RUBRIC)
    cited_task, world_files = set(), set()
    for n, (r, c, v) in enumerate(zip(body, csv_rows, RUBRIC), 1):
        kind, typ, wt, _gate, primary, crit, expl, refs, spec = v
        assert r[col["Index"]] == n == int(c["Index"]), "v%d is out of order" % n
        assert r[col["Criteria"]] == c["Criteria"] == crit, "v%d criteria differ" % n
        assert r[col["Criteria Explanation"]] == c["Criteria Explanation"] == expl, "v%d explanation differs" % n
        assert str(r[col["Numerical Weight"]]) == c["Numerical Weight"] == str(wt), "v%d weight differs" % n
        assert r[col["Is this a primary criterion?"]] == c["Is Primary Objective"] == primary, n
        assert r[col["Verifier Type"]] == c["Verifier Type"] == kind, n
        assert "Programmatic" not in str(r[col["Verifier Type"]]), (
            "v%d carries the guide's spelling of the App DB type; the picker spells it Programatic" % n)
        grades_a_form = "in MM/DD/YYYY form" in crit or "as Approved or Not approved" in crit
        want_tag = FORM_TAG if grades_a_form else "Final Response"
        assert r[col["Tags"]] == want_tag, "v%d tags %r, wanted %r" % (n, r[col["Tags"]], want_tag)
        assert r[col["Criterion Type"]] in IMPORT_DB_DROPDOWN, (
            "v%d Criterion Type %r is not in the dropdown the code-verifier form offers" % (n, r[col["Criterion Type"]]))
        assert r[col["Criterion Type"]] == typ, "v%d criterion type is not the record's" % n
        assert r[col["Severity Level"]] == ("Critical" if primary == "Yes" else "Major"), n
        assert r[col["Grading Target"]] is None, "v%d carries a grading target on an App DB row" % n
        assert (r[col["Output Dependencies"]] or "") == "", (
            "v%d carries an output dependency, and no row here grades a file" % n)
        assert r[col["Depends on"]] == "None", n
        arts = json.loads(r[col["Reference Artifacts"]])
        assert arts, "v%d cites no reference artifact" % n
        for a in arts:
            assert set(a) == {"name", "index", "source", "snapshotId", "transformations"}, (
                "v%d cites an artifact that is not the picker's resolved object" % n)
            assert a["source"] in ("world", "task"), n
            assert a["snapshotId"] == (TASK_SNAP if a["source"] == "task" else SNAP), n
            if a["source"] == "task":
                assert a["name"].split("/")[-1] in TASK_UPLOADS, n
                cited_task.add(a["name"].split("/")[-1])
            else:
                assert a["name"].startswith("filesystem/"), n
                world_files.add(a["name"])
            assert not a["name"].startswith(("filesystem/greenhouse/", "filesystem/bamboohr/",
                                             "filesystem/wiki_js/")), (
                "v%d cites an app seed table as a world file" % n)
        names = [a["name"] for a in arts]
        for ref in refs:
            if ref.startswith("/"):
                assert "filesystem" + ref in names, "v%d drops the world reference %r" % (n, ref)
            elif ref in TASK_UPLOADS:
                assert "filesystem/" + ref in names, "v%d drops the task reference %r" % (n, ref)
    for name in world_files:
        assert os.path.exists(os.path.join(WORLD, name[len("filesystem/"):])), \
            "the import cites %s, which is not in the world archive" % name
    assert set(cited_task) == set(TASK_UPLOADS), "the 1.4 upload is cited by no row"
    real = re.fullmatch(r"snap_[0-9a-f]{32}", SNAP) and re.fullmatch(r"snap_[0-9a-f]{32}", TASK_SNAP)
    print("import: %d rows, %d columns, %d citations over %d world files and %d upload%s"
          % (len(body), len(hdr), sum(len(json.loads(r[col["Reference Artifacts"]])) for r in body),
             len(world_files), len(cited_task),
             "" if real else " - SNAPSHOT IDS NOT YET READ OFF AN EXPORT, do not load this file"))


def check_docs():
    assert PAGE_A in PROMPT and PAGE_B in PROMPT, "the prompt must name both pages"
    assert all(ord(ch) < 128 for ch in PROMPT), "the prompt is not ASCII"
    for name in ("01_prompt.md", "02_task_metadata.md"):
        quotes = blockquotes(os.path.join(PKG, name))
        assert PROMPT in quotes, "%s does not blockquote the PROMPT constant verbatim" % name
    meta = open(os.path.join(PKG, "02_task_metadata.md"), encoding="utf8").read()
    for i, c in enumerate(RUBRIC, 1):
        assert c[5] in meta, "02 lacks the criterion: " + c[5][:70]
        assert c[6] in meta, "02 publishes a stale explanation for v%d: %s" % (i, c[6][:70])
    total = sum(c[2] for c in RUBRIC)
    for fig in ("%d verifiers" % len(RUBRIC), "%d-point" % total, TASK_NAME, PAGE_A, PAGE_B):
        assert fig in meta, "02 lacks the figure %r" % fig
    for name in ("01_prompt.md", "02_task_metadata.md", "06_failure_analysis.md",
                 "08_section_1_3_step_plan.md", "09_rubric_import.md", "README.md",
                 "qc/README.md"):
        text = open(os.path.join(PKG, name), encoding="utf8").read()
        bad = [ch for ch in text if ord(ch) > 127]
        assert not bad, "%s is not ASCII: %r" % (name, bad[:3])
    check_hashes(meta)
    readme = open(os.path.join(PKG, "README.md"), encoding="utf8").read()
    shipped = [f for f in sorted(os.listdir(PKG)) if f[0].isdigit()]
    shipped += ["build/" + f for f in sorted(os.listdir(HERE)) if not f.startswith("__")]
    shipped += ["qc/" + f for f in sorted(os.listdir(os.path.join(PKG, "qc")))
                if not f.startswith("__") and f != "verifiers"]
    shipped.append("qc/verifiers/")
    for f in shipped:
        assert f in readme, "README does not list %s" % f
    inputs = sorted(f for f in os.listdir(PKG) if f.startswith("00_"))
    assert inputs == TASK_INPUTS, "the task inputs on disk are %s" % inputs
    for f in inputs:
        assert os.path.splitext(f)[1] in (".pdf", ".csv", ".png", ".jpg"), f
    print("docs: prompt %d chars, %d words, md5 %s"
          % (len(PROMPT), len(PROMPT.split()), hashlib.md5(PROMPT.encode()).hexdigest()))


# ---------------------------------------------------------------- outputs
def rubric_table():
    lines = ["| # | Type | Wt | Gate | Criterion | Explanation |", "|---|---|---|---|---|---|"]
    for i, c in enumerate(RUBRIC, 1):
        lines.append("| %d | %s | %d | %s | %s | %s |"
                     % (i, "EA" if c[1] == EA else "OC", c[2], c[3], c[5], c[6]))
    return "\n".join(lines)


def rubric_csv():
    out = os.path.join(HERE, "rubric_preview.csv")
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Index", "Verifier Type", "Criteria", "Criterion Type", "Numerical Weight",
                    "Gate Kind", "Is Primary Objective", "Check Kind", "Criteria Explanation",
                    "Reference Artifacts"])
        for i, c in enumerate(RUBRIC, 1):
            w.writerow([i, c[0], c[5], c[1], c[2], c[3], c[4], c[8]["kind"], c[6], "; ".join(c[7])])
    return out


def rubric_import():
    out = os.path.join(PKG, "05_rubric_import.xlsx")
    wb = Workbook()
    ws = wb.active
    ws.title = "Rubric"
    hdr = ["Index", "Verifier Type", "Criteria", "Criteria Explanation",
           "Tags", "Criterion Type", "Severity Level", "Numerical Weight",
           "Is this a primary criterion?", "Reference Artifacts",
           "Grading Target", "Output Dependencies", "Depends on"]
    ws.append(hdr)
    for c in ws[1]:
        c.font = BOLD
    for i, (kind, typ, wt, _gate, primary, crit, expl, refs, spec) in enumerate(RUBRIC, 1):
        arts = json.dumps([
            {"name": name, "index": None, "source": source,
             "snapshotId": TASK_SNAP if source == "task" else SNAP,
             "transformations": []}
            for name, source in filter(None, (artifact(r) for r in refs))])
        ws.append([i, kind, crit, expl, import_tag(kind, crit), typ,
                   "Critical" if primary == "Yes" else "Major", wt, primary, arts, None, "", "None"])
    for col, wd in {"A": 7, "B": 20, "C": 80, "D": 80, "E": 16, "F": 20, "G": 14,
                    "H": 9, "I": 12, "J": 60, "K": 30, "L": 38, "M": 11}.items():
        ws.column_dimensions[col].width = wd
    stamp(wb)
    wb.save(out)
    freeze(out)
    return out


def slug(crit):
    s = re.sub(r"[^a-z0-9]+", "_", crit.lower()).strip("_")
    return s[:48].rstrip("_")


def verifiers():
    """One standalone check(ctx) per rubric row: the row's SPEC stamped onto the engine."""
    engine = open(os.path.join(HERE, "verifier_engine.py"), encoding="utf8").read()
    vdir = os.path.join(PKG, "qc", "verifiers")
    os.makedirs(vdir, exist_ok=True)
    for old in os.listdir(vdir):
        if re.match(r"row\d\d_.*\.py$", old):
            os.remove(os.path.join(vdir, old))
    names = []
    for i, c in enumerate(RUBRIC, 1):
        spec = dict(c[8])
        spec["criterion"] = c[5]
        name = "row%02d_%s.py" % (i, slug(c[5]))
        head = ("# Row %d of the %s rubric - generated by build/build_package_artifacts.py, never "
                "edited here.\n# Criterion: %s\n# Target app: %s, table pages, check kind %s\n"
                "SPEC = %s\n\n" % (i, TASK_NAME, c[5], TARGET_APP, spec["kind"],
                                   pprint.pformat(spec, width=96, sort_dicts=True)))
        open(os.path.join(vdir, name), "w", encoding="utf8").write(head + engine)
        names.append(name)
    return names


def golden():
    out = []
    for title, name in GOLDEN_FILES.items():
        path = os.path.join(PKG, name)
        open(path, "w", encoding="utf8", newline="\n").write(GOLDEN[title])
        out.append(path)
    return out


def main():
    check_world()
    check_golden()
    total = check_rubric()
    check_register()
    check_asks()
    check_tools()
    for p in golden():
        print("md5 %s  %s" % (md5(p), os.path.basename(p)))
    wb = syw()
    check_syw(wb)
    print("md5 %s  %s" % (md5(wb), os.path.basename(wb)))
    rubric_csv()
    imp = rubric_import()
    check_import()
    print("md5 %s  %s" % (md5(imp), os.path.basename(imp)))
    names = verifiers()
    print("verifiers: %d row files under qc/verifiers/" % len(names))
    if "--docs" in sys.argv:
        check_docs()
    if "--table" in sys.argv:
        print(rubric_table())
    print("%d verifiers, %d points, %d gate" % (len(RUBRIC), total,
                                                 sum(1 for c in RUBRIC if c[3] != "-")))


if __name__ == "__main__":
    main()
