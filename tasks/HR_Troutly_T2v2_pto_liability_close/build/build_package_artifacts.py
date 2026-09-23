#!/usr/bin/env python3
"""The single source of truth for T2's graded content, at the prompt half: the PTO liability
schedule at 08/31/2026 recomputed from the world's bytes under the rules the world states, the
registered failing paths recomputed under the rules each path drops, the rubric plan that
scores them, and, from 09/20/2026, the rubric import that registers the plan. The five Gemini
runs of 09/20/2026 read 23.9% and the registered rule fired, so the plan's rows carry a criterion
type, a primary flag, an explanation in the house register and the picker's reference artifacts,
and 05_rubric_import.xlsx is generated from them in the HR 79 T1 shape, beside the golden page,
the verifier row files and the battery's expectations. Task round 2 of 09/20/2026 reshaped the
set to 43 rows: the form split from the reconciliation, an ID and a date row, one BambooHR row
per record the schedule moves with a guard over the records it leaves, and a Greenhouse guard.
Task round 3 the same day took the memo's out-of-scope block out and the Greenhouse guard with
it, added a policy row for each record the run creates, and reworded the two BambooHR guards
to the schedule's state: 44 rows. Task round 4 the same day split the precision row and the
column row three ways each, narrowed the population row to presence so the five exclusion rows
decide absence alone, and put the 44 policies and 33 balances the two BambooHR set rows read
into their criteria as stated values: 48 rows, 101 points. Task round 5 of 09/21/2026 removed
the five exclusion rows on the owner's decision and returned the population row to the 52 as the
only rows, and added a BambooHR balance row for each of the twelve moved balances the five
mirrored rules had left: 55 rows, 105 points.

Run from anywhere: python3 build/build_package_artifacts.py [--docs] [--table]
"""
import ast
import csv
import datetime as dt
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

# ---------------------------------------------------------------- the prompt and the deliverable
PAGE = "PTO Liability - 08/31/2026"
TASK_NAME = "PTO Liability at 08/31/2026"
# One sentence in the owner's register, the T1 shape: the ask, two named sources plus the open
# tail in a parenthetical, the request by subject, then the two deliverables. The two named
# sources are the ones the requester believes in and both carry the wrong numbers: the HRIS
# report prints uncapped balances at the loaded tiers and BambooHR carries the loaded rates.
# The cutover memo, the handbook, the archive, the signed pay changes, the schedule change and
# the offer letters are the response's work to find.
PROMPT = ("Complete the request (using the HRIS time off report and the rest of the Troutly "
          "files) about the August 2026 close by publishing the Wiki.js page "
          "PTO Liability - 08/31/2026.")
TASK_INPUTS = ["00_task_input_pto_liability_request.pdf"]
TASK_UPLOADS = ["pto_liability_request.pdf"]
ASOF = "08/31/2026"
SNAP = "snap_c6f6a0879f3d47a19048ee80d7529157"  # world_snapshot_id, unchanged across 14 exports
TASK_SNAP = "snap_31202a8918284a76a7c53582bfc550ec"  # v2's own task data id, read off its first export on 09/23/2026; T2's 09/21/2026 id was snap_1e12795ed0df4d489a36382afdb63279

# ---------------------------------------------------------------- world readers
def _csv(app, table):
    with open(os.path.join(APPS, app, table), newline="", encoding="utf8") as fh:
        return list(csv.DictReader(fh))


def _pdf_text(rel):
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
    return re.sub(r"\s+", " ", "\n".join(parts))


def _rows(rel, sheet=None, formulas=False):
    wb = load_workbook(os.path.join(WORLD, rel), data_only=not formulas)
    ws = wb[sheet] if sheet else wb.active
    return [r for r in ws.iter_rows(values_only=True)]


def _date(v):
    """A date from a date, a datetime, MM/DD/YYYY or ISO."""
    if isinstance(v, dt.datetime):
        return v.date()
    if isinstance(v, dt.date):
        return v
    s = str(v).strip()
    m = re.fullmatch(r"(\d{2})/(\d{2})/(\d{4})", s)
    if m:
        return dt.date(int(m.group(3)), int(m.group(1)), int(m.group(2)))
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", s)
    return dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))


def _d(v):
    return _date(v).strftime("%m/%d/%Y")


def md5(path):
    return hashlib.md5(open(path, "rb").read()).hexdigest()


# ---------------------------------------------------------------- the world files the package rests on
CUTOVER = "HR/Policies/2026-06-20_PTO_Policy_Cutover_Memo.docx"
HANDBOOK = "HR/Policies/Employee_Handbook_v3.pdf"
POLICY_2025 = "HR/Policies/PTO_Policy_2025.docx"
REPORT = "HR/Data/HRIS_Time_Off_Report_2026-08-31.xlsx"
ARCHIVE = "HR/Data/Migration/SplinterHR_Final_Archive_2026-07-28.xlsx"
ROSTER = "HR/Data/2026-08-31_Master_Employee_Roster.xlsx"
CROSSWALK = "HR/Data/2026-08-28_Employee_ID_Crosswalk.xlsx"
LOAD = "HR/Data/Migration/HRIS_Import_Load_2026-07-01.csv"
MAPPING = "HR/Data/Migration/2026-06-24_Field_Mapping_Workbook.xlsx"
CLOSEOUT = "HR/Data/Migration/2026-07-22_Migration_Closeout_Memo.docx"
PROCEDURES = "HR/Payroll/2026-06-25_Payroll_Procedures_Memo.docx"
PAY_HISTORY = "HR/Payroll/HRIS_Payroll_History_2026-07-01_to_2026-08-31.xlsx"
CLOSE_JULY = "Finance/Close/2026-07_Close_Package.xlsx"
PROMOTION_0088 = "HR/Comp/Promotions/2026-06-10_Promotion_Approval_TRT-0088.docx"
AMENDMENT_0117 = "HR/Comp/Amendments/2026-05-12_Comp_Amendment_TRT-0117.pdf"
REHIRE_0071 = "HR/People/Offer_Letters/2024-04-08_Rehire_Offer_TRT-0071.pdf"
OFFERS_HIST = "HR/People/Offer_Letters/Historical_Offer_Letters_2020-2026.pdf"
SCHEDULE_0141 = "HR/Benefits/2026-08-10_Schedule_Change_TRT-0141.pdf"
OFFER_0153 = "Recruiting/Offers/2026-07-02_Offer_TRT-0153_SIGNED.pdf"
WIKI_PTO = "Wiki/Paid_Time_Off.md"
WIKI_COMP = "Wiki/Compensation_Authority.md"
WIKI_ONBOARD = "Wiki/Onboarding_Data_Standards.md"

WORLD_FILES = [CUTOVER, HANDBOOK, POLICY_2025, REPORT, ARCHIVE, ROSTER, CROSSWALK, LOAD, MAPPING,
               CLOSEOUT, PROCEDURES, PAY_HISTORY, CLOSE_JULY, PROMOTION_0088, AMENDMENT_0117,
               REHIRE_0071, OFFERS_HIST, SCHEDULE_0141, OFFER_0153, WIKI_PTO, WIKI_COMP,
               WIKI_ONBOARD]
APP_TABLES = ["bamboohr/Employee.csv", "bamboohr/TimeOffBalance.csv", "bamboohr/TimeOffPolicy.csv",
              "bamboohr/TimeOffRequest.csv", "bamboohr/EmployeePolicy.csv",
              "bamboohr/TimeOffType.csv", "wiki_js/Page.csv"]

# ---------------------------------------------------------------- the rules, each read off its document
TIERS = [(2, 80), (5, 120), (999, 160)]  # completed years under, annual hours
PERIODS_PER_YEAR = 26
CAP = 40.0
CAP_DATE = _date("06/30/2026")
CUTOVER_DATE = _date("07/01/2026")
HOURS_PER_YEAR = 2080
PART_TIME_UNDER = 30
BRIDGE_UNDER_DAYS = 365
STEP = 3000.0
ASOF_DATE = _date(ASOF)


def _pay_periods():
    """(start, end, pay date) from the payroll procedures memo's own table."""
    text = _docx_text(PROCEDURES)
    out = []
    for m in re.finditer(r"(\d{2}/\d{2}/\d{4}) [-" + "\u2013" + r"] (\d{2}/\d{2}/\d{4}) \| (\d{2}/\d{2}/\d{4})", text):
        out.append((_date(m.group(1)), _date(m.group(2)), _date(m.group(3))))
    assert len(out) >= 14, "the procedures memo's pay period table did not parse"
    return out


PERIODS = _pay_periods()
POSTED = [p for p in PERIODS if p[2] <= ASOF_DATE]


def _roster():
    rows = _rows(ROSTER, "Employees")
    hdr = rows[4]
    out = []
    for r in rows[5:]:
        if not r or not r[0]:
            continue
        d = dict(zip(hdr, r))
        out.append(dict(id=d["Employee ID"], name=d["Legal Name"], dept=d["Department"],
                        title=d["Job Title"], hours=float(d["Weekly Scheduled Hours"]),
                        hire=_date(d["Original Hire Date"]), adj_roster=_date(d["Adjusted Service Date"]),
                        flsa=d["FLSA Status"], salary=float(d["Annual Base Salary"]),
                        status=d["Status"], type=d["Worker Type"]))
    return out


def _archive():
    rows = _rows(ARCHIVE, "Employees")
    hdr = rows[0]
    emp = {}
    for r in rows[1:]:
        if not r or not r[1]:
            continue
        d = dict(zip(hdr, r))
        term = None
        for tok in str(d["SalaryHistory"]).split(";"):
            if "TERMINATED" in tok:
                term = _date(tok.split(":")[0])
        emp[d["EmployeeID"]] = dict(hire=_date(d["OriginalHireDate"]),
                                     rehire=_date(d["RehireDate"]) if d["RehireDate"] else None,
                                     adj=_date(d["AdjustedServiceDate"]) if d["AdjustedServiceDate"] else None,
                                     term=_date(d["TerminationDate"]) if d["TerminationDate"] else None,
                                     break_from=term, salary=float(d["CurrentSalary"]),
                                     status=d["Status"], type=d["Type"])
    bal = {}
    for r in _rows(ARCHIVE, "Balances")[1:]:
        if r and r[0]:
            bal[r[0]] = dict(status=r[2], asof=_date(r[3]), hours=float(r[4]))
    return emp, bal


def _bamboo():
    emp = {e["employee_number"]: e for e in _csv("bamboohr", "Employee.csv")}
    policy = {e["employee_id"]: e["policy_id"] for e in _csv("bamboohr", "EmployeePolicy.csv")}
    balance = {e["employee_id"]: e for e in _csv("bamboohr", "TimeOffBalance.csv")}
    rates = {p["name"]: float(p["accrual_rate"]) for p in _csv("bamboohr", "TimeOffPolicy.csv")}
    used = {}
    for r in _csv("bamboohr", "TimeOffRequest.csv"):
        if r["status"] == "approved" and CUTOVER_DATE <= _date(r["start_date"]) <= ASOF_DATE:
            used[r["employee_id"]] = used.get(r["employee_id"], 0.0) + float(r["amount"])
    return emp, policy, balance, rates, used


def _report():
    rows = _rows(REPORT, "Balances")
    hdr = rows[0]
    out = {}
    for r in rows[1:]:
        if r and r[0] and r[0] != "TOTAL":
            d = dict(zip(hdr, r))
            out[d["EmployeeNumber"]] = dict(open=float(d["BalanceAt070126"]),
                                            accrued=float(d["AccruedSince070126"]),
                                            used=float(d["UsedSince070126"]))
    return out


ROSTER_ROWS = _roster()
ARCHIVE_EMP, ARCHIVE_BAL = _archive()
BAMBOO, BAMBOO_POLICY, BAMBOO_BALANCE, BAMBOO_RATES, USED = _bamboo()
REPORT_ROWS = _report()
POLICY_TIER = {"PTO Under 2 Years": 80, "PTO 2 to 5 Years": 120, "PTO 5 Plus Years": 160}
TIER_POLICY = {v: k for k, v in POLICY_TIER.items()}


def _signed_rates():
    """The two signed pay changes the load dropped, and the offer-letter step, each read off its
    own document rather than typed."""
    promo = _docx_text(PROMOTION_0088)
    m = re.search(r"\$(\d{3},\d{3}\.\d{2})", promo.split("To")[-1]) or re.search(r"new annual base salary of \$([\d,]+\.\d{2})", promo)
    p_new = float(re.search(r"new annual base salary of \$([\d,]+\.\d{2})", promo).group(1).replace(",", ""))
    p_eff = _date(re.search(r"effective (\d{2}/\d{2}/\d{4})", promo).group(1))
    amend = _pdf_text(AMENDMENT_0117)
    a_new = float(re.search(r"replacing it with USD \$([\d,]+\.\d{2})", amend).group(1).replace(",", ""))
    a_eff = dt.date(2026, 5, 16)
    assert "May 16, 2026" in amend
    offers = _pdf_text(OFFERS_HIST)
    assert "Automatic Anniversary Step Increase" in offers and "$3,000.00" in offers
    hb = _pdf_text(HANDBOOK)
    step = float(re.search(r"step increase of \$([\d,]+\.\d{2}) on each service anniversary", hb).group(1).replace(",", ""))
    return {"TRT-0088": (p_new, p_eff), "TRT-0117": (a_new, a_eff)}, step


SIGNED, STEP_READ = _signed_rates()
assert STEP_READ == STEP


def _schedule_change():
    t = _pdf_text(SCHEDULE_0141)
    old = float(re.search(r"Current Regular Hours per Week: (\d+)", t).group(1))
    new = float(re.search(r"New Regular Hours per Week: (\d+)", t).group(1))
    eff = _date(re.search(r"Effective Date: (\d{2}/\d{2}/\d{4})", t).group(1))
    return {"TRT-0141": (old, new, eff)}


SCHEDULE_CHANGES = _schedule_change()


# ---------------------------------------------------------------- the determination
def years_between(a, b):
    """Completed years of service from a to b."""
    y = b.year - a.year
    if (b.month, b.day) < (a.month, a.day):
        y -= 1
    return y


def tier_at(adj, at):
    y = years_between(adj, at)
    for under, hours in TIERS:
        if y < under:
            return hours
    return 160


def adjusted_service_date(emp, bridging=True):
    """The adjusted service date the handbook's rule gives: the archive's original hire date,
    bridged across a rehire when the break was under 365 days, else the rehire date; a record the
    archive does not carry keeps the roster's date."""
    a = ARCHIVE_EMP.get(emp["id"])
    if not a:
        return emp["adj_roster"]
    if a["rehire"]:
        gap = (a["rehire"] - a["break_from"]).days if a["break_from"] else 9999
        if bridging:
            return a["hire"] if gap < BRIDGE_UNDER_DAYS else a["rehire"]
        return a["rehire"]
    return a["adj"] or a["hire"]


def start_date(emp):
    """The day the person was first employed in the window: the archive's hire for a migrated
    record, the roster's for a hire after cutover."""
    a = ARCHIVE_EMP.get(emp["id"])
    if a and a["rehire"]:
        return a["rehire"]
    return a["hire"] if a else emp["hire"]


def hours_at(emp, at, part_time=True):
    if not part_time:
        return 40.0
    ch = SCHEDULE_CHANGES.get(emp["id"])
    if ch:
        old, new, eff = ch
        return new if at >= eff else old
    return emp["hours"]


def per_period(tier_hours, sched_hours):
    factor = sched_hours / 40.0 if sched_hours < PART_TIME_UNDER else 1.0
    return round(tier_hours * factor / PERIODS_PER_YEAR, 4)


DEFAULT_FLAGS = dict(population=True, cap=True, service_dates=True, bridging=True,
                     in_period=True, signed=True, step=True, part_time=True, periods=4,
                     hris_balances=False)


def schedule(**over):
    """The per-employee schedule under a set of rules; the golden is every rule on."""
    f = dict(DEFAULT_FLAGS)
    f.update(over)
    if f["population"]:
        people = [e for e in ROSTER_ROWS if e["status"] == "Active" and e["type"] == "Employee"]
    else:  # BambooHR's active rows taken whole, the two unloaded hires outside
        people = []
        for k, b in BAMBOO.items():
            if b["status"] != "Active":
                continue
            r = next((e for e in ROSTER_ROWS if e["id"] == k), None)
            people.append(r or dict(id=k, name=b["first_name"] + " " + b["last_name"],
                                    dept=b["department"], title=b["job_title"], hours=40.0,
                                    hire=_date(b["hire_date"]), adj_roster=_date(b["hire_date"]),
                                    flsa="", salary=float(b["salary"]), status="Active",
                                    type="Employee"))
    posted = POSTED[:f["periods"]] if f["periods"] <= len(POSTED) else POSTED + PERIODS[len(POSTED):f["periods"]]
    out = []
    for e in people:
        i = e["id"]
        adj = adjusted_service_date(e, bridging=f["bridging"]) if f["service_dates"] else e["adj_roster"]
        start = start_date(e)
        bal0 = ARCHIVE_BAL[i]["hours"] if i in ARCHIVE_BAL else 0.0
        if f["hris_balances"] and i in REPORT_ROWS:
            bal0 = REPORT_ROWS[i]["open"]
        opening = min(bal0, CAP) if f["cap"] else bal0
        accruals = []
        for (ps, pe, pay) in posted:
            if start > pe:
                accruals.append(0.0)
                continue
            if f["service_dates"]:
                t = tier_at(adj, pe if f["in_period"] else ASOF_DATE)
            else:
                t = POLICY_TIER.get(BAMBOO_POLICY.get(i, "PTO Under 2 Years"), 80)
            accruals.append(per_period(t, hours_at(e, pe, part_time=f["part_time"])))
        used = USED.get(i, 0.0)
        bal = round(opening + sum(accruals) - used, 2)
        run = opening
        for a in accruals:
            run = round(run + a, 2)
        bal_posted = round(run - used, 2)
        rate = e["salary"]
        if f["signed"] and i in SIGNED and SIGNED[i][1] <= ASOF_DATE:
            rate = SIGNED[i][0]
        if f["step"] and e["title"] == "Support Specialist":
            ann = adj.replace(year=ASOF_DATE.year)
            if CUTOVER_DATE <= ann <= ASOF_DATE:
                rate = rate + STEP
        hourly = round(rate / HOURS_PER_YEAR, 4)
        tier_now = tier_at(adj, ASOF_DATE) if f["service_dates"] else POLICY_TIER.get(BAMBOO_POLICY.get(i, "PTO Under 2 Years"), 80)
        out.append(dict(id=i, name=e["name"], dept=e["dept"], title=e["title"], adj=adj, start=start,
                        tier=tier_now, opening_raw=bal0, opening=opening, accruals=accruals,
                        accrued=round(sum(accruals), 4), used=used, balance=bal,
                        balance_posted=bal_posted, rate=rate, hourly=hourly,
                        liability=round(bal * hourly, 2),
                        liability_posted=round(bal_posted * hourly, 2)))
    return out


GOLDEN = schedule()
GOLDEN_BY_ID = {r["id"]: r for r in GOLDEN}
TOTAL_HOURS = round(sum(r["balance"] for r in GOLDEN), 2)
TOTAL = round(sum(r["liability"] for r in GOLDEN), 2)
TOTAL_POSTED = round(sum(r["liability_posted"] for r in GOLDEN), 2)
TOTAL_HOURS_POSTED = round(sum(r["balance_posted"] for r in GOLDEN), 2)
# The memo carries no Form section in v2, so nothing tells a response how many decimals to print.
# A stated total is graded at half a dollar and a stated hours total at a twentieth of an hour,
# which no rounding of a right answer fails and no registered path reaches, the nearest being
# P5 at $49.93 and 9.66 hours away. A cell keeps the cent and the hundredth of an hour.
TOL_TOTAL_MONEY = 0.5
TOL_TOTAL_HOURS = 0.05
CAPPED_IDS = sorted(r["id"] for r in GOLDEN if r["opening_raw"] > CAP)
MIGRATED_WRONG_TIER = sorted(r["id"] for r in GOLDEN if r["id"] in BAMBOO_POLICY
                             and POLICY_TIER[BAMBOO_POLICY[r["id"]]] != r["tier"])
UNLOADED_IDS = sorted(r["id"] for r in GOLDEN if r["id"] not in BAMBOO)
LOADED_IDS = sorted(r["id"] for r in GOLDEN if r["id"] in BAMBOO)
# Task round 2 split the two BambooHR set rows: one row per loaded record whose policy the schedule
# moves, one per rule mirrored into a balance, and a guard over every loaded record the schedule
# leaves as loaded, so a change to a record the request asks nothing of has a row that reads it.
POLICY_MOVED = MIGRATED_WRONG_TIER
POLICY_SAME = sorted(i for i in LOADED_IDS if i not in POLICY_MOVED)
BALANCE_MOVED = sorted(i for i in LOADED_IDS if not any(
    abs(float(BAMBOO_BALANCE[i]["balance"]) - GOLDEN_BY_ID[i][k]) <= 0.005 for k in ("balance", "balance_posted")))
BALANCE_SAME = sorted(i for i in LOADED_IDS if i not in BALANCE_MOVED)
# the five page rules that move a balance, each mirrored into BambooHR once: the cap, the archive's
# date, the bridge, the timed tier change and the part-time schedule; then, since task round 5,
# every other loaded balance the schedule moves, so the BambooHR ask is graded on all 52
MIRRORED_RULE_ROWS = ["TRT-0005", "TRT-0043", "TRT-0071", "TRT-0018", "TRT-0141"]
BAMBOO_BALANCE_ROWS = MIRRORED_RULE_ROWS + [i for i in BALANCE_MOVED if i not in MIRRORED_RULE_ROWS]


def _cap_only_ids():
    """The capped employees whose balance the cap alone moves. One tier across the window equal to
    the loaded policy, no time off, no schedule change, no signed rate. A row read on their balance
    cells fails on the cap and on nothing else."""
    out = []
    for i in CAPPED_IDS:
        r = GOLDEN_BY_ID[i]
        tiers = {tier_at(r["adj"], pe) for (ps, pe, pay) in POSTED}
        if len(tiers) == 1 and POLICY_TIER.get(BAMBOO_POLICY.get(i, "")) in tiers and r["used"] == 0 \
                and i not in SCHEDULE_CHANGES and i not in SIGNED:
            out.append(i)
    return out


CAP_ONLY_IDS = _cap_only_ids()
_WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve"]
CONTRACTOR_IDS = sorted(k for k, b in BAMBOO.items() if k.startswith("CTR-"))
ENDED_IN_BAMBOO = sorted(k for k, b in BAMBOO.items() if b["status"] == "Active"
                         and k not in GOLDEN_BY_ID and not k.startswith("CTR-"))

# the registered paths, each the golden with rules dropped
PATHS = [
    ("P0", "the July close method rolled forward: the HRIS report's rows and balances, the loaded tiers and rates, contractors and ended records inside, the two unloaded hires outside",
     dict(population=False, cap=False, service_dates=False, bridging=False, in_period=False, signed=False, step=False, part_time=False, hris_balances=True)),
    ("P1", "the HRIS report with the population fixed: 52 rows, balances uncapped, the loaded tiers and rates",
     dict(cap=False, service_dates=False, bridging=False, in_period=False, signed=False, step=False, part_time=False, hris_balances=True)),
    ("P2", "P1 with the 40.0-hour cap applied at 06/30/2026",
     dict(service_dates=False, bridging=False, in_period=False, signed=False, step=False, part_time=False)),
    ("P3", "P2 with tiers from the archive's service dates, the rehire unbridged, the tier change not timed, the rates as loaded",
     dict(bridging=False, in_period=False, signed=False, step=False, part_time=False)),
    ("P4", "P3 with the two signed pay changes applied",
     dict(bridging=False, in_period=False, step=False, part_time=False)),
    ("P5", "P4 with the rehire bridged and the tier change timed; the step and the part-time schedule still missed",
     dict(step=False, part_time=False)),
    ("P6", "the heal", dict()),
]


# ---------------------------------------------------------------- the rubric plan
# Each planned row is (family, weight, gate, criterion, predicate, criterion type, primary,
# explanation, references). The first five are the prompt half's plan, scored against the
# registered paths; the last four are the rubric half's, written 09/20/2026 after the five
# Gemini runs read 23.9%, and every value in them recomputes from the world on every build.
EA, OC = "Expert Assessment", "Objective Compliance"
# THE APP DB TYPE'S SPELLING IS THE PICKER'S, NOT THE GUIDE'S. RL Studio's Add-a-verifier control
# spells it "App DB Programatic", one "m"; the guide spells it "Programmatic". HR 32 lost the row
# to that letter twice and the importer skips an unknown type on a warning. check_import()
# refuses any type containing "Programmatic".
APPDB = "App DB Programatic"
# The guide's importance table by criterion type. A compliance row reads a stated value or a
# stated set and is at most Core, 1 to 5. A reasoning row applies a rule the record contradicts
# and runs 1 to 10; 9 and 10 are the gate's alone, rows on one cell that moves the total by under
# a third of a percent, the two hires, price at 2, and a BambooHR row that mirrors one page rule
# prices at 1, so the mirror never outweighs the rule it mirrors.
BANDS = {OC: set(range(1, 6)), EA: set(range(1, 11))}
IMPORT_DB_DROPDOWN = {"Objective Compliance", "Expert Assessment", "Process"}
FORM_TAG = "Style / formatting"
IMPORT_TAGS = {"Final Response", FORM_TAG}
# ---------------------------------------------------------------- what the load has wrong
# v2 grades the determination and nothing beside it. A cell is graded where the figure the world
# gives at 08/31/2026 is not the figure the load carries, because those are the cells a run that
# copies the HRIS report prints wrong and the cells a run that applies the rules prints right.
# Its weight is the dollars it moves, so a row's price is what the output loses when it is wrong.
MONEY_BANDS = [(2000.0, 7), (800.0, 6), (250.0, 5), (80.0, 4), (0.0, 3)]
TOL_CELL = 0.005


def _band(dollars):
    return next(w for floor, w in MONEY_BANDS if dollars >= floor)


def _loaded():
    """(balance, hourly) as the load carries them for each current employee, zero where the load
    carries no record at all. The HRIS report's own three columns give the balance and BambooHR's
    salary over 2,080 the rate, which is what a run that trusts the load prints."""
    out = {}
    for r in GOLDEN:
        i = r["id"]
        rep = REPORT_ROWS.get(i)
        bal = round(rep["open"] + rep["accrued"] - rep["used"], 2) if rep else 0.0
        hourly = round(float(BAMBOO[i]["salary"]) / HOURS_PER_YEAR, 4) if i in BAMBOO else 0.0
        out[i] = (bal, hourly)
    return out


LOADED = _loaded()
LOADED_HOURS = round(sum(b for b, _ in LOADED.values()), 2)
LOADED_TOTAL = round(sum(round(b * h, 2) for b, h in LOADED.values()), 2)


# Review round 1 of 09/22/2026 narrowed the ask from a row per current employee, 156 values
# the 25-criterion limit could not cover, to five department lines. Sales and Marketing are
# one line in the request because Marketing alone is a line the load already carries right,
# and a line a copy of the load earns is a free point. Each line is stated twice, in hours and
# in dollars, and each figure is graded at the totals' bands.
LINES = [("Customer Success", ("Customer Success",)), ("Engineering", ("Engineering",)),
         ("Finance and Corporate", ("Finance and Corporate",)), ("Product", ("Product",)),
         ("Sales and Marketing", ("Sales", "Marketing"))]
LINE_OF = {d: name for name, ds in LINES for d in ds}
TOL_LINE_MONEY, TOL_LINE_HOURS = TOL_TOTAL_MONEY, TOL_TOTAL_HOURS


def line_figures(sched):
    """{line: (hours, dollars, hours posted, dollars posted)} for a schedule; a row whose
    department is on no line is on none, and the world asserts there is no such row."""
    out = {}
    for name, ds in LINES:
        rows = [r for r in sched if r["dept"] in ds]
        out[name] = (round(sum(r["balance"] for r in rows), 2), round(sum(r["liability"] for r in rows), 2),
                     round(sum(r["balance_posted"] for r in rows), 2),
                     round(sum(r["liability_posted"] for r in rows), 2))
    return out


LINE_GOLD = line_figures(GOLDEN)
LOADED_LINE = {name: (round(sum(LOADED[r["id"]][0] for r in GOLDEN if r["dept"] in ds), 2),
                      round(sum(round(LOADED[r["id"]][0] * LOADED[r["id"]][1], 2)
                                for r in GOLDEN if r["dept"] in ds), 2))
               for name, ds in LINES}


def _line_cells():
    """One entry per graded line figure, in the request's order, hours before dollars: the line,
    the field, what the world gives, what the load carries and the dollars between them. An
    hours figure moves the hours it is off by, each at its own employee's rate."""
    out = []
    for name, ds in LINES:
        rows = [r for r in GOLDEN if r["dept"] in ds]
        h, d = LINE_GOLD[name][0], LINE_GOLD[name][1]
        lh, ld = LOADED_LINE[name]
        out.append(dict(field="line_hours", line=name, want=h, loaded=lh,
                        moves=round(abs(sum((r["balance"] - LOADED[r["id"]][0]) * r["hourly"] for r in rows)), 2)))
        out.append(dict(field="line_total", line=name, want=d, loaded=ld, moves=round(abs(d - ld), 2)))
    return out


CELLS = _line_cells()
CELL_LINES = [name for name, ds in LINES]
assert CELLS and all(c["moves"] > 0 for c in CELLS)

HOURS_CRIT = "States, on the PTO liability page, hours to two decimals."
RATES_CRIT = "States, on the PTO liability page, hourly rates to four decimals."
DOLLARS_CRIT = "States, on the PTO liability page, dollars to the cent."
RECONCILE_CRIT = "States, on the PTO liability page, a total dollar liability equal to the sum of the rows."
ID_CRIT = "States, on the PTO liability page, an employee ID on every row."
DATES_CRIT = "States, on the PTO liability page, every date in MM/DD/YYYY form."
LAYOUT_CRIT = "States, on the PTO liability page, the summary above one table of employee rows."
# the request's Form section, tagged Style / formatting in the import; the reconciliation is content
FORM_ROWS = (HOURS_CRIT, RATES_CRIT, DOLLARS_CRIT, ID_CRIT, DATES_CRIT, LAYOUT_CRIT)
REQUEST = TASK_UPLOADS[0]


def _same(a, b, tol=0.0):
    return abs(a - b) <= tol


def _rate(x):
    """An hourly rate as the page prints it, four decimals behind a dollar sign."""
    return "$%.4f" % x


def _hrs(x):
    """An hours figure at the precision it carries, two decimals where that is exact."""
    t = ("%.4f" % x).rstrip("0")
    a, b = t.split(".")
    return "%s.%s" % (a, b.ljust(2, "0"))


def _money(x):
    return "$" + f"{x:,.2f}"


def _row_checks():
    """Each planned row as (family, weight, gate, criterion, predicate, criterion type, primary,
    explanation, references). v2 grades the determination and nothing beside it: the page under
    the title at 1, the two totals, and each department line's hours and dollars, priced by the
    dollars the figure moves off the load. Review round 1 of 09/22/2026 took the per-employee
    table out of the request, because 52 rows of three values is an ask no 25-criterion rubric
    covers, and put the five lines in its place.

    Nothing here grades the ABSENCE of content. A run that also prints every employee, or a
    line per department with Sales and Marketing joined beside them, passes every row it would
    otherwise pass, which is what keeps the golden valid when a response over-delivers."""
    g = GOLDEN_BY_ID
    by = lambda s: {r["id"]: r for r in s}

    def total_ok(s):
        t = round(sum(r["liability"] for r in s), 2)
        return _same(t, TOTAL, TOL_TOTAL_MONEY) or _same(t, TOTAL_POSTED, TOL_TOTAL_MONEY)

    def hours_ok(s):
        h = round(sum(r["balance"] for r in s), 2)
        hp = round(sum(r["balance_posted"] for r in s), 2)
        return _same(h, TOTAL_HOURS, TOL_TOTAL_HOURS) or _same(hp, TOTAL_HOURS, TOL_TOTAL_HOURS) \
            or _same(h, TOTAL_HOURS_POSTED, TOL_TOTAL_HOURS)

    def line_ok(field, name):
        def ok(s):
            f = line_figures(s)[name]
            gold = LINE_GOLD[name]
            if field == "line_hours":
                return any(_same(x, y, TOL_LINE_HOURS) for x in (f[0], f[2]) for y in (gold[0], gold[2]))
            return any(_same(x, y, TOL_LINE_MONEY) for x in (f[1], f[3]) for y in (gold[1], gold[3]))
        return ok

    always = lambda s: True
    cut, hb, arch, roster, xwalk = "/" + CUTOVER, "/" + HANDBOOK, "/" + ARCHIVE, "/" + ROSTER, "/" + CROSSWALK
    report, load, proc = "/" + REPORT, "/" + LOAD, "/" + PROCEDURES
    promo, amend, rehire, letters = "/" + PROMOTION_0088, "/" + AMENDMENT_0117, "/" + REHIRE_0071, "/" + OFFERS_HIST
    sched_form, offer153 = "/" + SCHEDULE_0141, "/" + OFFER_0153
    emp, bal_t, req_t = "bamboohr/Employee.csv", "bamboohr/TimeOffBalance.csv", "bamboohr/TimeOffRequest.csv"
    wiki = "wiki_js/Page.csv"

    def members(name):
        return {r["id"] for r in GOLDEN if r["dept"] in dict(LINES)[name]}

    def capped(name):
        return sorted(i for i in CAPPED_IDS if i in members(name))

    def retiered(name):
        return sorted(i for i in MIGRATED_WRONG_TIER if i in members(name) and i != "TRT-0071")

    def ids(xs):
        return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]

    def expl_refs(c):
        """The explanation and the references for one graded line figure, from the world's own
        bytes. Each names the rules that land in its line, and the build asserts that the rules
        named are the rules the schedule applies there, so a line that drifts stops the build."""
        n, f = c["line"], c["field"]
        h, d = LINE_GOLD[n][0], LINE_GOLD[n][1]
        lh, ld = LOADED_LINE[n]
        m = members(n)
        if n == "Customer Success":
            assert capped(n) == ["TRT-0021"] and retiered(n) == ["TRT-0083"] and {"TRT-0141", "TRT-0153", "TRT-0088", "TRT-0096"} <= m
            if f == "line_hours":
                return ("In Customer Success the cutover memo caps TRT-0021 at %.1f hours, the archive puts TRT-0083 at the %d-hour tier, "
                        "handbook 2.2 prorates TRT-0141 and TRT-0153 accrues from the start. The line holds %s hours, the HRIS report %s."
                        % (CAP, GOLDEN_BY_ID["TRT-0083"]["tier"], f"{h:,.2f}", f"{lh:,.2f}"),
                        [REQUEST, cut, arch, hb, sched_form, roster, xwalk, report])
            return ("Handbook 3.2 and 5.4 put TRT-0088 at %s and TRT-0096 at %s, and the roster puts TRT-0153 at %s. "
                    "On those rates and the capped balances Customer Success carries %s against the load's %s."
                    % (_money(GOLDEN_BY_ID["TRT-0088"]["rate"]), _money(GOLDEN_BY_ID["TRT-0096"]["rate"]),
                       _money(GOLDEN_BY_ID["TRT-0153"]["rate"]), _money(d), _money(ld)),
                    [REQUEST, promo, hb, letters, roster, offer153, cut, emp])
        if n == "Engineering":
            cp = capped(n)
            assert len(cp) == 5 and retiered(n) == ["TRT-0051"] and "TRT-0117" in m
            top = max(cp, key=lambda i: GOLDEN_BY_ID[i]["opening_raw"])
            if f == "line_hours":
                return ("Five Engineering balances sit over the cutover memo's %.1f-hour cap, %s at %.2f in the archive, and the archive puts "
                        "TRT-0051 at the %d-hour tier. Engineering holds %s hours against the HRIS report's %s."
                        % (CAP, top, GOLDEN_BY_ID[top]["opening_raw"], GOLDEN_BY_ID["TRT-0051"]["tier"], f"{h:,.2f}", f"{lh:,.2f}"),
                        [REQUEST, cut, arch, proc, report])
            return ("The signed amendment sets TRT-0117 at %s from %s over the loaded %s. With the capped balances "
                    "Engineering carries %s of liability against the load's %s."
                    % (_money(SIGNED["TRT-0117"][0]), _d(SIGNED["TRT-0117"][1]), _money(float(BAMBOO["TRT-0117"]["salary"])),
                       _money(d), _money(ld)),
                    [REQUEST, amend, arch, cut, emp])
        if n == "Finance and Corporate":
            assert capped(n) == ["TRT-0009"] and not retiered(n)
            if f == "line_hours":
                return ("Finance and Corporate has one balance over the cap, TRT-0009 at %.2f in the archive, which the cutover memo "
                        "holds to %.1f hours. The line holds %s hours against the HRIS report's %s."
                        % (GOLDEN_BY_ID["TRT-0009"]["opening_raw"], CAP, f"{h:,.2f}", f"{lh:,.2f}"),
                        [REQUEST, cut, arch, report])
            return ("Capping TRT-0009 under the cutover memo takes Finance and Corporate to %s at the rates on the roster. "
                    "The load values the same %s employees at %s."
                    % (_money(d), _WORDS[len(m)], _money(ld)),
                    [REQUEST, cut, arch, roster, emp])
        if n == "Product":
            assert capped(n) == ["TRT-0040"] and retiered(n) == ["TRT-0079"] and "TRT-0071" in m
            if f == "line_hours":
                return ("Product nets close to the load because the cutover memo caps TRT-0040 while handbook 7.6 bridges TRT-0071 and "
                        "the archive puts TRT-0079 at the %d-hour tier. It holds %s hours against the HRIS report's %s."
                        % (GOLDEN_BY_ID["TRT-0079"]["tier"], f"{h:,.2f}", f"{lh:,.2f}"),
                        [REQUEST, cut, hb, arch, rehire, report])
            return ("At the rates on the roster the Product line carries %s, the cap on TRT-0040 offset by the bridged TRT-0071 "
                    "and the retiered TRT-0079 under the cutover memo. The load carries %s."
                    % (_money(d), _money(ld)),
                    [REQUEST, cut, hb, arch, rehire, roster, emp])
        assert n == "Sales and Marketing"
        assert capped(n) == ["TRT-0018", "TRT-0029", "TRT-0043"] and "TRT-0155" in m
        if f == "line_hours":
            return ("The request joins Sales and Marketing. The cutover memo caps %s, times TRT-0018's tier change and accrues "
                    "TRT-0155 from the start, %s hours against the HRIS report's %s."
                    % (ids(capped(n)), f"{h:,.2f}", f"{lh:,.2f}"),
                    [REQUEST, cut, arch, proc, roster, xwalk, report])
        return ("Valued at the roster's rates, TRT-0155 at %s, the joined Sales and Marketing line carries %s under the "
                "cutover memo. The load's figures for the same %d employees come to %s."
                % (_money(GOLDEN_BY_ID["TRT-0155"]["rate"]), _money(d), len(m), _money(ld)),
                [REQUEST, cut, roster, xwalk, letters, emp])

    rows = [
        ("free", 1, "-", "States that a Wiki.js page titled %s is published." % PAGE, always,
         OC, "No",
         "One page under that title is what the request asks for in Wiki.js, so it exists with its published flag set.",
         [REQUEST, wiki]),
        ("determination", 10, "Critical value",
         "States, on the PTO liability page, a total dollar liability of %s." % _money(TOTAL), total_ok,
         EA, "Yes",
         "The cutover memo caps carryover at %.1f hours, accrues four posted periods at the tier over %d and values each balance at the rate on file over %s. The %d balances sum to %s, or %s rounding each posting."
         % (CAP, PERIODS_PER_YEAR, f"{HOURS_PER_YEAR:,}", len(GOLDEN), _money(TOTAL), _money(TOTAL_POSTED)),
         [cut, hb, arch, roster, proc, promo, amend, letters, sched_form]),
        ("determination", 8, "-",
         "States, on the PTO liability page, total PTO hours of %s." % f"{TOTAL_HOURS:,.2f}", hours_ok,
         EA, "Yes",
         "The %d current employees hold %s hours at %s once the cutover memo's cap runs and four posted periods accrue by adjusted service date. The HRIS report's columns add to %s."
         % (len(GOLDEN), f"{TOTAL_HOURS:,.2f}", ASOF, f"{LOADED_HOURS:,.2f}"),
         [cut, arch, roster, proc, report]),
    ]
    for c in CELLS:
        n = c["line"]
        expl, refs = expl_refs(c)
        if c["field"] == "line_hours":
            crit = "States, on the PTO liability page, PTO hours of %s for %s." % (f"{c['want']:,.2f}", n)
        else:
            crit = "States, on the PTO liability page, a PTO liability of %s for %s." % (_money(c["want"]), n)
        rows.append(("determination", _band(c["moves"]), "-", crit, line_ok(c["field"], n),
                     EA, "Yes", expl, refs))
    specs = _specs(g)
    assert len(rows) == len(specs), "%d rows, %d specs" % (len(rows), len(specs))
    return [r + (s,) for r, s in zip(rows, specs)]


def _specs(g):
    """What each row's verifier reads, in the order of the rows above. Every value is the build's
    own, and check_rubric() holds each spec to the criterion beside it."""
    W = dict(target="wiki", page=PAGE)
    out = [dict(W, kind="exists"),
           dict(W, kind="total", expected=[TOTAL, TOTAL_POSTED]),
           dict(W, kind="hours", expected=[TOTAL_HOURS, TOTAL_HOURS_POSTED])]
    for c in CELLS:
        n = c["line"]
        if c["field"] == "line_hours":
            out.append(dict(W, kind="line_hours", key=n, expected=[LINE_GOLD[n][0], LINE_GOLD[n][2]]))
        else:
            out.append(dict(W, kind="line_total", key=n, expected=[LINE_GOLD[n][1], LINE_GOLD[n][3]]))
    return out


PLAN = _row_checks()
PLAN_TOTAL = sum(r[1] for r in PLAN)


def score_paths():
    out = []
    for key, desc, flags in PATHS:
        s = schedule(**flags)
        pts = sum(r[1] for r in PLAN if r[4](s))
        failed = [i + 1 for i, r in enumerate(PLAN) if not r[4](s)]
        tot = round(sum(r["liability"] for r in s), 2)
        out.append((key, desc, pts, failed, tot, len(s)))
    return out


# ---------------------------------------------------------------- the rubric (what registers)
def _rubric():
    """(verifier kind, criterion type, weight, gate kind, primary, criterion, explanation, refs),
    the HR 79 T1 tuple, read off the plan's rows. Every row is an App DB row: the deliverable is
    one wiki page and BambooHR state and no file, so the judge has nothing to open and the
    database is the only route."""
    return [(APPDB, typ, w, gate, primary, crit, expl, list(refs), spec)
            for fam, w, gate, crit, pred, typ, primary, expl, refs, spec in PLAN]


RUBRIC = _rubric()
UPLOAD_PREFIX = "00_task_input_"
assert TASK_UPLOADS == [n[len(UPLOAD_PREFIX):] for n in TASK_INPUTS]


def import_tag(crit):
    return FORM_TAG if crit in FORM_ROWS else "Final Response"


def artifact(ref):
    """(name, source) for one of the plan's reference strings in the picker's namespace, or
    None for an app seed table, which the picker's browser does not list."""
    if ref.startswith("/"):
        return "filesystem" + ref, "world"
    if ref in TASK_UPLOADS:
        return "filesystem/" + ref, "task"
    return None


# frozen timestamps, so the import's md5 is a property of its content and not of the build time
STAMP = dt.datetime(2026, 8, 31, 9, 0, 0)
ZIP_STAMP = (2026, 8, 31, 9, 0, 0)
ISO_STAMP = "2026-08-31T09:00:00Z"


def stamp(wb):
    wb.properties.creator = "Casey Ouk"
    wb.properties.lastModifiedBy = "Casey Ouk"
    wb.properties.created = STAMP
    wb.properties.modified = STAMP


def freeze(path):
    src_zip = zipfile.ZipFile(path)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as out:
        for info in src_zip.infolist():
            data = src_zip.read(info.filename)
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
    src_zip.close()
    open(path, "wb").write(buf.getvalue())


def check_rubric():
    """The weights sit in the guide's band for their criterion type, the gate is the only 10,
    reasoning carries at least half the points, and every criterion is one atomic States."""
    total = sum(c[2] for c in RUBRIC)
    assert total == PLAN_TOTAL
    gates = [c for c in RUBRIC if c[3] != "-"]
    assert all(c[1] in BANDS for c in RUBRIC), "a criterion type the guide's table does not price"
    assert all(c[2] in BANDS[c[1]] for c in RUBRIC), "a weight sits outside its band: %s" % [
        (c[1], c[2], c[5][:50]) for c in RUBRIC if c[2] not in BANDS[c[1]]]
    assert all((c[2] >= 9) == (c[3] != "-") for c in RUBRIC), "weight 9 or 10 and gate must coincide"
    assert len(gates) == 1 and gates[0][3] == "Critical value" and gates[0][1] == EA
    assert all(c[4] in ("Yes", "No") for c in RUBRIC)
    assert all((c[1] == EA) == (c[4] == "Yes") for c in RUBRIC), (
        "a primary row is a reasoning row and a reasoning row is primary")
    ea = sum(c[2] for c in RUBRIC if c[1] == EA)
    assert ea * 2 >= total, "Expert Assessment under half the weight"
    assert len(RUBRIC) >= 5
    assert all(c[0] == APPDB for c in RUBRIC)
    for c in RUBRIC:
        crit = c[5]
        assert crit.startswith("States"), "a row must open with States: " + crit
        assert not re.search(r"\b(and that|as well as|in addition)\b|;", crit), "stacked: " + crit
        assert "prompt" not in crit.lower() and ".docx" not in crit and ".pdf" not in crit, crit
        assert all(ord(ch) < 128 for ch in crit), crit
        assert c[7], "a row cites nothing: " + crit
        # the spec reads what the criterion states, and nothing else
        s = c[8]
        assert s["target"] in ("wiki", "bamboohr") and s.get("kind"), crit
        assert (s["target"] == "bamboohr") == crit.startswith("States, in BambooHR"), crit
        if "key" in s:
            assert s["key"] in crit, "spec keyed %s on a criterion that does not name it: %s" % (s["key"], crit)
        if s["kind"] in ("balance", "balance_row"):
            assert ("%.2f" % s["expected"][0]) in crit, "spec value %.2f is not the criterion's: %s" % (s["expected"][0], crit)
        if s["kind"] == "rate":
            assert ("%.4f" % s["expected"][0]) in crit, crit
        if s["kind"] == "tier":
            assert ("%d-hour" % s["expected"]) in crit, crit
        if s["kind"] == "absent":
            assert s["keys"][0] in crit, crit
        if s["kind"] in ("total", "line_total"):
            assert _money(s["expected"][0]) in crit, crit
        if s["kind"] == "line_hours":
            assert f"{s['expected'][0]:,.2f}" in crit and "hours" in crit, crit
        if s["kind"] == "policy":
            assert s["expected"] in crit, "spec expects a policy the criterion does not name: " + crit
        if s["kind"] == "format":
            assert {"balance": "hours to two decimals", "rate": "rates to four decimals", "liability": "dollars to the cent"}[s["field"]] in crit, crit
        if s["kind"] == "columns":
            assert {"name": "a name on", "department": "a department on", "tier": "PTO tier in hours on"}[s["field"]] in crit, crit
        if s["kind"] in ("policies", "balances"):
            # a set row reads the loaded records the schedule leaves as loaded, and no other, and
            # task round 4 has it state every record and value in terms, so the row resolves alone
            moved = POLICY_MOVED if s["kind"] == "policies" else BALANCE_MOVED
            assert str(len(s["expected"])) in crit and "change" not in crit, crit
            assert all(k not in s["expected"] for k in UNLOADED_IDS + moved), "a guard reads a record the schedule moves: " + crit
            for k, v in s["expected"].items():
                assert k in crit, "a set row omits %s from its criterion" % k
                assert (v if s["kind"] == "policies" else "%.2f" % v[0]) in crit, "a set row omits %s's value" % k
    kinds = [c[8]["kind"] for c in RUBRIC]
    # v2 after review round 1: the page, the two totals and each line's hours and dollars, and
    # nothing else. No row reads a second app, an employee row or the absence of anything.
    assert kinds.count("exists") == kinds.count("total") == kinds.count("hours") == 1
    assert kinds.count("line_hours") == kinds.count("line_total") == len(LINES)
    assert set(kinds) == {"exists", "total", "hours", "line_hours", "line_total"}, "a kind v2 does not ask for: %r" % sorted(set(kinds))
    assert all(c[8]["target"] == "wiki" for c in RUBRIC), "v2 writes one page and reads one app"
    assert len(RUBRIC) <= 25, "%d criteria, over the platform's 25" % len(RUBRIC)
    keyed = [(c[8]["kind"], c[8]["key"]) for c in RUBRIC if "key" in c[8]]
    assert sorted(keyed) == sorted((k, n) for n in CELL_LINES for k in ("line_hours", "line_total"))
    for c in RUBRIC:
        s_ = c[8]
        if s_["kind"] in ("line_hours", "line_total"):
            lh, ld = LOADED_LINE[s_["key"]]
            loaded, tol = (lh, TOL_LINE_HOURS) if s_["kind"] == "line_hours" else (ld, TOL_LINE_MONEY)
            assert all(abs(x - loaded) > tol for x in s_["expected"]), \
                "a graded line the load already carries right: " + c[5]
    print("rubric: %d verifiers, %d points, %d gate, EA %.1f%%, OC %.1f%%, %d primary"
          % (len(RUBRIC), total, len(gates), 100.0 * ea / total, 100.0 * (total - ea) / total,
             sum(1 for c in RUBRIC if c[4] == "Yes")))
    return total


def check_register():
    """The judge-facing strings, held to the house register HR 32 settled and HR 79 carries.
    ASCII only, no colons, semicolons or brackets, no spaced dash, months never spelled, no ISO
    dates, no grading vocabulary, no self-reference, a source named, at most three sentences and
    240 characters, no two rows opening alike or carrying one explanation."""
    SOURCES = ("request", "cutover memo", "handbook", "archive", "roster", "crosswalk", "BambooHR",
               "procedures memo", "promotion approval", "amendment", "offer letter",
               "schedule change form", "HRIS report", "field mapping", "load file", "Greenhouse",
               "Wiki.js", "org chart")
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
        assert e.endswith("."), "v%d explanation is not a full sentence" % i
        assert all(ord(ch) < 128 for ch in e), "v%d explanation is not ASCII" % i
        assert not any(ch in e for ch in ":;()[]"), "v%d explanation carries a colon, semicolon or bracket: %s" % (i, e)
        assert not re.search(r"(?<![A-Za-z0-9])-|-(?![A-Za-z0-9])", e), "v%d explanation carries a spaced dash" % i
        hit = GRADING.search(e)
        assert hit is None, "v%d explanation describes grading (%r)" % (i, hit.group(0) if hit else "")
        ref = SELF_REFERENCE.search(e)
        assert ref is None, "v%d explanation refers to the rubric's own construction (%r)" % (i, ref.group(0) if ref else "")
        assert any(t in e for t in SOURCES), "v%d names no source: %s" % (i, e)
        assert len(e) <= 240, "v%d explanation runs to %d chars" % (i, len(e))
        sentences = len(re.findall(r"\.(?:\s|$)", e))
        assert sentences <= 3, "v%d explanation runs to %d sentences" % (i, sentences)
        lengths.append(len(e))
        firsts.append(" ".join(e.split()[:3]))
    seen = [c[6] for c in RUBRIC]
    dupes = sorted({e for e in seen if seen.count(e) > 1})
    assert not dupes, "explanations repeat verbatim across rows: %r" % dupes[:1]
    assert len(set(firsts)) == len(firsts), "two explanations open alike: %r" % [
        f for f in firsts if firsts.count(f) > 1][:1]
    avg = sum(lengths) / len(lengths)
    assert avg <= 200, "explanations average %.0f chars" % avg
    print("register: %d explanations, %d-%d chars, %.0f average"
          % (len(lengths), min(lengths), max(lengths), avg))


IMPORT = os.path.join(PKG, "05_rubric_import.xlsx")
IMPORT_STATS = {}  # filled by check_import(), read by check_docs()
IMPORT_HEADER = ["Index", "Verifier Type", "Criteria", "Criteria Explanation",
                 "Tags", "Criterion Type", "Severity Level", "Numerical Weight",
                 "Is this a primary criterion?", "Reference Artifacts",
                 "Grading Target", "Output Dependencies", "Depends on"]


def rubric_import():
    """05_rubric_import.xlsx in the HR 79 T1 shape: one sheet named Rubric, thirteen columns, one
    row per verifier, every reference artifact the picker's own resolved object."""
    wb = Workbook()
    ws = wb.active
    ws.title = "Rubric"
    ws.append(IMPORT_HEADER)
    for c in ws[1]:
        c.font = Font(bold=True)
    for i, (kind, typ, wt, gate, primary, crit, expl, refs, spec) in enumerate(RUBRIC, 1):
        arts = json.dumps([
            {"name": name, "index": None, "source": source,
             "snapshotId": TASK_SNAP if source == "task" else SNAP,
             "transformations": []}
            for name, source in filter(None, (artifact(r) for r in refs))])
        ws.append([i, kind, crit, expl, import_tag(crit), typ,
                   "Critical" if primary == "Yes" else "Major", wt, primary, arts, None, "", "None"])
    for col, wd in {"A": 7, "B": 20, "C": 80, "D": 80, "E": 16, "F": 20, "G": 14,
                    "H": 9, "I": 12, "J": 60, "K": 30, "L": 38, "M": 11}.items():
        ws.column_dimensions[col].width = wd
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(vertical="top", wrap_text=True)
    stamp(wb)
    wb.save(IMPORT)
    freeze(IMPORT)
    return IMPORT


def check_import():
    """The file on disk is the plan, row for row, in the form the picker parses."""
    rows = list(load_workbook(IMPORT)["Rubric"].iter_rows(values_only=True))
    hdr, body = list(rows[0]), rows[1:]
    assert hdr == IMPORT_HEADER, "the import's columns are not the HR 79 T1 shape: %s" % hdr
    assert len(body) == len(RUBRIC), "the import carries %d rows, the rubric %d" % (len(body), len(RUBRIC))
    col = {name: n for n, name in enumerate(hdr)}
    with open(os.path.join(HERE, "rubric_plan.csv"), encoding="utf-8") as f:
        csv_rows = list(csv.DictReader(f))
    assert len(csv_rows) == len(RUBRIC)
    for sid in (SNAP, TASK_SNAP):
        assert re.fullmatch(r"snap_[0-9a-f]{32}", sid), (
            "a snapshot id is not one read off an export, do not load this file: %r" % sid)
    cited_task, world_files, citations = set(), set(), 0
    selection = {"filesystem/" + f for f in WORLD_FILES}
    for n, (r, c, v) in enumerate(zip(body, csv_rows, RUBRIC), 1):
        kind, typ, wt, _gate, primary, crit, expl, refs, spec = v
        assert r[col["Index"]] == n == int(c["Index"]), "v%d is out of order" % n
        assert r[col["Criteria"]] == c["Criterion"] == crit, "v%d criteria differ" % n
        assert r[col["Criteria Explanation"]] == c["Criteria Explanation"] == expl, "v%d explanation differs" % n
        assert str(r[col["Numerical Weight"]]) == c["Weight"] == str(wt), "v%d weight differs" % n
        assert r[col["Is this a primary criterion?"]] == c["Is Primary Objective"] == primary, n
        assert r[col["Verifier Type"]] == c["Verifier Type"] == kind, n
        assert "Programmatic" not in str(r[col["Verifier Type"]]), (
            "v%d carries the guide's spelling of the App DB type; the picker spells it Programatic" % n)
        want_tag = FORM_TAG if any(p in crit for p in ("to two decimals", "to four decimals", "to the cent", "summary above one table",
                                                        "an employee ID on every row", "MM/DD/YYYY")) else "Final Response"
        assert r[col["Tags"]] == want_tag, "v%d tags %r, wanted %r" % (n, r[col["Tags"]], want_tag)
        assert r[col["Tags"]] in IMPORT_TAGS, n
        assert r[col["Criterion Type"]] in IMPORT_DB_DROPDOWN, (
            "v%d Criterion Type %r is not in the dropdown the code-verifier form offers" % (n, r[col["Criterion Type"]]))
        assert r[col["Criterion Type"]] == typ == c["Criterion Type"], "v%d criterion type is not the record's" % n
        assert r[col["Severity Level"]] == ("Critical" if primary == "Yes" else "Major"), n
        assert r[col["Grading Target"]] is None, "v%d carries a grading target on an App DB row" % n
        assert (r[col["Output Dependencies"]] or "") == "", (
            "v%d carries an output dependency, and no row here grades a file" % n)
        assert r[col["Depends on"]] == "None", n
        arts = json.loads(r[col["Reference Artifacts"]])
        assert arts, "v%d cites no reference artifact" % n
        citations += len(arts)
        for a in arts:
            assert set(a) == {"name", "index", "source", "snapshotId", "transformations"}, (
                "v%d cites an artifact that is not the picker's resolved object" % n)
            assert a["source"] in ("world", "task"), n
            assert a["snapshotId"] == (TASK_SNAP if a["source"] == "task" else SNAP), n
            if a["source"] == "task":
                assert a["name"].split("/")[-1] in TASK_UPLOADS, n
                cited_task.add(a["name"].split("/")[-1])
            else:
                assert a["name"] in selection, (
                    "v%d cites %s, which the selection block does not carry" % (n, a["name"]))
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
            else:
                assert ref in APP_TABLES, "v%d cites an app table outside the selection: %r" % (n, ref)
    for name in world_files:
        assert os.path.exists(os.path.join(WORLD, name[len("filesystem/"):])), \
            "the import cites %s, which is not in the world archive" % name
    assert set(cited_task) == set(TASK_UPLOADS), "the 1.4 upload is cited by no row"
    print("import: %d rows, %d columns, %d citations over %d world files and %d upload"
          % (len(body), len(hdr), citations, len(world_files), len(cited_task)))
    IMPORT_STATS.update(citations=citations, world_files=len(world_files))
    return citations, len(world_files)


def rubric_table():
    """The rubric as 02_task_metadata.md publishes it; check_docs() holds 02 to every cell."""
    lines = ["| # | Family | Type | Wt | Gate | Primary | Criterion | Explanation |",
             "|---|---|---|---|---|---|---|---|"]
    for i, (fam, w, gate, crit, pred, typ, primary, expl, refs, spec) in enumerate(PLAN, 1):
        lines.append("| %d | %s | %s | %d | %s | %s | %s | %s |"
                     % (i, fam, "EA" if typ == EA else "OC", w, gate, primary, crit, expl))
    return "\n".join(lines)


# ---------------------------------------------------------------- the golden page
PAGE_HEADERS = ["Line", "PTO hours at %s" % ASOF, "PTO liability at %s" % ASOF]
GOLDEN_FILE = "04_golden_output_PTO_Liability.md"


def render_page(sched, title=None, headers=None):
    """A page in the request's shape from a schedule: the two totals it asks for, then one table
    of the five lines it asks for, each line's hours and dollars. The request carries no Form
    section, so the golden prints the precision the world's own records print."""
    hours = round(sum(r["balance"] for r in sched), 2)
    total = round(sum(r["liability"] for r in sched), 2)
    lines_ = line_figures(sched)
    hdr = headers or PAGE_HEADERS
    lines = ["# %s" % (title or PAGE), "",
             "Total PTO liability at %s: $%s" % (ASOF, f"{total:,.2f}"), "",
             "Total PTO hours at %s: %s" % (ASOF, f"{hours:,.2f}"), "",
             "| " + " | ".join(hdr) + " |", "|" + "---|" * len(hdr)]
    for name, ds in LINES:
        h, d = lines_[name][0], lines_[name][1]
        lines.append("| %s | %s | $%s |" % (name, f"{h:,.2f}", f"{d:,.2f}"))
    return "\n".join(lines) + "\n"


GOLDEN_PAGE = render_page(GOLDEN)


def golden():
    path = os.path.join(PKG, GOLDEN_FILE)
    open(path, "w", encoding="utf8", newline="\n").write(GOLDEN_PAGE)
    return path


def check_golden():
    text = GOLDEN_PAGE
    assert text.startswith("# %s\n" % PAGE), "the golden page is not the schedule"
    assert _money(TOTAL) in text and f"{TOTAL_HOURS:,.2f}" in text
    assert all(ord(ch) < 128 for ch in text), "the golden page is not ASCII"
    # the page carries the five lines the request asks for and nothing the rubric does not read
    for name, ds in LINES:
        assert "| %s | %s | %s |" % (name, f"{LINE_GOLD[name][0]:,.2f}", _money(LINE_GOLD[name][1])) in text
    assert _same(sum(v[1] for v in LINE_GOLD.values()), TOTAL, 0.005), "the lines do not add to the total"
    assert _same(sum(v[0] for v in LINE_GOLD.values()), TOTAL_HOURS, 0.005), "the lines do not add to the hours"
    assert "TRT-" not in text, "the golden page carries an employee row, which the request no longer asks for"
    for word in ("Tier", "Summary", "Employees on the schedule"):
        assert word not in text, "the golden page carries %r, which v2's request does not ask for" % word


FORM_CHECK_TYPE = {"exists": "Existence Check", "hours": "Content Match", "idset": "Count Check", "present": "Count Check", "format": "Content Match",
                   "reconcile": "Content Match", "summary": "Content Match", "columns": "Content Match",
                   "id_rows": "Content Match", "dates": "Content Match", "layout": "Content Match",
                   "total": "Content Match", "balance": "Content Match", "tier": "Content Match",
                   "rate": "Content Match", "line_hours": "Content Match", "line_total": "Content Match", "no_contractor": "Guard (Negative Check)",
                   "absent": "Guard (Negative Check)", "policy": "Content Match",
                   "policies": "Content Match", "balances": "Content Match",
                   "balance_row": "Existence Check"}
# the service each row's code is grounded on, as the run's own tool names spell it: every wiki tool
# the archived runs called carries the prefix wiki_js_mcp, every BambooHR tool the prefix bamboohr
TARGET_APP = {"wiki": "wiki_js_mcp", "bamboohr": "bamboohr"}


def form_check_type(spec):
    # a balance row on a record the run creates checks existence; on a loaded record it matches content
    if spec["kind"] == "balance_row" and spec["key"] not in UNLOADED_IDS:
        return "Content Match"
    return FORM_CHECK_TYPE[spec["kind"]]


def slug(crit):
    s = re.sub(r"[^a-z0-9]+", "_", crit.lower()).strip("_")
    return s[:48].rstrip("_")


def verifiers():
    """One standalone check(ctx) per rubric row: the row's SPEC stamped onto the engine. Every file
    is built and held to the skill before any old file is removed, so a refused build leaves the
    row files on disk as they were."""
    engine = open(os.path.join(HERE, "verifier_engine.py"), encoding="utf8").read()
    vdir = os.path.join(PKG, "qc", "verifiers")
    files = []
    for i, c in enumerate(RUBRIC, 1):
        spec = dict(c[8])
        spec["criterion"] = c[5]
        name = "row%02d_%s.py" % (i, slug(c[5]))
        head = ("# Row %d of the %s rubric - generated by build/build_package_artifacts.py, never "
                "edited here.\n# Criterion: %s\n# Target app: %s, check kind %s\n"
                "SPEC = %s\n\n" % (i, TASK_NAME, c[5], spec["target"], spec["kind"],
                                   pprint.pformat(spec, width=96, sort_dicts=True)))
        # the app-db-verifier skill's section 6 sets 200 lines. Raised to 240 on 09/23/2026 for the one
        # route the graded dump forced: it carries no Wiki.js table, so the page is read off the
        # run's own Wiki.js calls, which is the drift toward a judge that section 6 warns of
        assert (head + engine).count("\n") < 240, "row file %s runs to %d lines, over 240" % (name, (head + engine).count("\n"))
        assert (head + engine).isascii(), "row file %s is not ASCII" % name
        # the platform's AST gate rejected `import os` on 09/23/2026 as a permanently banned import,
        # so the row files import from an allow-list: re, and json for the run's tool-call record
        tree = ast.walk(ast.parse(head + engine))
        imports = {a.name for n in tree if isinstance(n, ast.Import) for a in n.names}
        imports |= {n.module or "" for n in ast.walk(ast.parse(head + engine)) if isinstance(n, ast.ImportFrom)}
        assert imports <= {"json", "re"}, "row file %s imports %r; the allow-list is json and re" % (name, sorted(imports))
        files.append((name, head + engine))
    os.makedirs(vdir, exist_ok=True)
    for old in os.listdir(vdir):
        if re.match(r"row\d\d_.*\.py$", old):
            os.remove(os.path.join(vdir, old))
    for name, text in files:
        open(os.path.join(vdir, name), "w", encoding="utf8").write(text)
    return [name for name, text in files]


# ---------------------------------------------------------------- guards
def check_world():
    """Every rule the schedule applies is read off the document that states it."""
    cut = _docx_text(CUTOVER)
    # every rule constant is spelled into the phrase it is read from, so a constant that drifts
    # from the document stops the build instead of quietly repricing the schedule
    for phrase in ("replaces the 2025 PTO policy effective 07/01/2026",
                   "PTO accrues per BIWEEKLY PAY PERIOD at the annual tier divided by %d" % PERIODS_PER_YEAR,
                   "posts to each employee's balance on the pay date",
                   "capped at %.1f hours as of %s" % (CAP, _d(CAP_DATE)),
                   "pay period that contains the employee's service anniversary",
                   "divided by %s" % f"{HOURS_PER_YEAR:,}",
                   "employees whose employment ended on or before the measurement date are excluded",
                   "Under %d years | %d hours/year" % (TIERS[0][0], TIERS[0][1]),
                   "%d years to under %d years | %d hours/year" % (TIERS[0][0], TIERS[1][0], TIERS[1][1]),
                   "%d years and over | %d hours/year" % (TIERS[1][0], TIERS[2][1]),
                   "14 calendar days written notice"):
        assert phrase in cut, "the cutover memo does not say %r" % phrase
    hb = _pdf_text(HANDBOOK)
    for phrase in ("fewer than %d hours per week" % PART_TIME_UNDER,
                   "accrue paid time off pro-rata to scheduled hours",
                   "less than %d days" % BRIDGE_UNDER_DAYS, "%s on each service anniversary" % _money(STEP),
                   "signed document governs until the record is corrected",
                   "totals are the sum of the rounded rows",
                   "A dated policy memo governs the handbook section it replaces",
                   "Contractors are not eligible for employee benefits, paid time off"):
        assert phrase in hb, "the handbook does not say %r" % phrase
    p25 = _docx_text(POLICY_2025)
    assert "PTO accrues monthly on the 1st of each month" in p25 and "carry over without limit" in p25
    wiki = open(os.path.join(WORLD, WIKI_PTO), encoding="utf8").read()
    assert "accrue PTO **monthly**" in wiki and "carry over without limit" in wiki
    # the lines: every current employee's department is on exactly one line
    assert {r["dept"] for r in GOLDEN} == set(LINE_OF), sorted({r["dept"] for r in GOLDEN})
    assert sum(len([r for r in GOLDEN if r["dept"] in ds]) for n, ds in LINES) == len(GOLDEN)
    # Marketing alone is the line the load carries right, which is why the request joins it to Sales
    mk = [r for r in GOLDEN if r["dept"] == "Marketing"]
    assert _same(round(sum(r["balance"] for r in mk), 2), round(sum(LOADED[r["id"]][0] for r in mk), 2), 0.005)
    # the periods
    assert [p[2].strftime("%m/%d/%Y") for p in POSTED] == ["07/10/2026", "07/24/2026", "08/07/2026", "08/21/2026"], POSTED
    assert PERIODS[4][2].strftime("%m/%d/%Y") == "09/04/2026"
    # BambooHR's own per-period rates are the tiers over 26
    for name, hours in POLICY_TIER.items():
        assert _same(BAMBOO_RATES[name], round(hours / 26, 4), 0.00005), (name, BAMBOO_RATES[name])
    # the population
    assert len(GOLDEN) == 52, len(GOLDEN)
    assert UNLOADED_IDS == ["TRT-0153", "TRT-0155"], UNLOADED_IDS
    assert ENDED_IN_BAMBOO == ["TRT-0037", "TRT-0049", "TRT-0064"], ENDED_IN_BAMBOO
    assert CONTRACTOR_IDS == ["CTR-2001", "CTR-2002", "CTR-2003", "CTR-2004"]
    assert BAMBOO["TRT-0006"]["status"] == "Terminated"
    # the cap, the load and the report
    assert len(CAPPED_IDS) == 11, CAPPED_IDS
    mapping = " ".join(str(v) for ws in load_workbook(os.path.join(WORLD, MAPPING), read_only=True)
                       for r in ws.iter_rows(values_only=True) for v in r if v is not None)
    assert "no cap" in mapping and "07/01/2026" in mapping, "the field mapping does not say no cap"
    load = list(csv.DictReader(open(os.path.join(WORLD, LOAD), encoding="utf8")))
    assert len(load) == 56
    moved = sorted(r["EmployeeNumber"] for r in load if r["HireDate"] == "07/01/2026" and r["EmployeeNumber"] in ARCHIVE_EMP)
    assert moved == ["TRT-0043", "TRT-0051", "TRT-0058", "TRT-0071", "TRT-0079", "TRT-0083", "TRT-0096", "TRT-0102", "TRT-0110"], moved
    for i in ARCHIVE_BAL:
        if i in REPORT_ROWS and i != "TRT-0021":
            assert _same(REPORT_ROWS[i]["open"], ARCHIVE_BAL[i]["hours"]), i
    assert REPORT_ROWS["TRT-0021"]["open"] == 74.0 and ARCHIVE_BAL["TRT-0021"]["hours"] == 58.5
    assert all(i in REPORT_ROWS for i in CONTRACTOR_IDS + ENDED_IN_BAMBOO)
    assert not any(i in REPORT_ROWS for i in UNLOADED_IDS)
    # the tiers
    assert MIGRATED_WRONG_TIER == ["TRT-0043", "TRT-0051", "TRT-0058", "TRT-0071", "TRT-0079", "TRT-0083"], MIGRATED_WRONG_TIER
    assert len(LOADED_IDS) == 50 and set(LOADED_IDS) | set(UNLOADED_IDS) == set(GOLDEN_BY_ID)
    # task round 2's split: the records the schedule moves and the records it leaves
    assert POLICY_MOVED == MIGRATED_WRONG_TIER and len(POLICY_SAME) == 44, len(POLICY_SAME)
    assert len(BALANCE_MOVED) == 17 and len(BALANCE_SAME) == 33, (len(BALANCE_MOVED), len(BALANCE_SAME))
    assert all(i in BALANCE_MOVED for i in BAMBOO_BALANCE_ROWS), "a mirrored balance the schedule does not move"
    assert set(BAMBOO_BALANCE_ROWS) == set(BALANCE_MOVED) and len(BAMBOO_BALANCE_ROWS) == 17
    assert set(BAMBOO_BALANCE_ROWS) | set(POLICY_MOVED) | set(BALANCE_SAME) <= set(LOADED_IDS)
    assert GOLDEN_BY_ID["TRT-0005"]["opening_raw"] == 92.5 and GOLDEN_BY_ID["TRT-0005"]["balance"] == 64.62
    assert "TRT-0005" in CAP_ONLY_IDS and GOLDEN_BY_ID["TRT-0005"]["tier"] == 160
    assert GOLDEN_BY_ID["TRT-0043"]["adj"].strftime("%m/%d/%Y") == "10/15/2021" and GOLDEN_BY_ID["TRT-0043"]["tier"] == 120
    assert [_d(ARCHIVE_EMP[i]["term"]) for i in ENDED_IN_BAMBOO + ["TRT-0006"]] == ["03/20/2026", "05/08/2026", "06/15/2026", "07/25/2026"]
    assert _d(BAMBOO["TRT-0006"]["termination_date"]) == "07/25/2026"
    a71 = ARCHIVE_EMP["TRT-0071"]
    assert (a71["rehire"] - a71["break_from"]).days == 241 and GOLDEN_BY_ID["TRT-0071"]["adj"] == a71["hire"]
    assert GOLDEN_BY_ID["TRT-0071"]["adj"].strftime("%m/%d/%Y") == "03/08/2021"
    assert GOLDEN_BY_ID["TRT-0018"]["accruals"] == [4.6154, 4.6154, 4.6154, 6.1538], GOLDEN_BY_ID["TRT-0018"]["accruals"]
    assert BAMBOO_POLICY["TRT-0018"] == "PTO 5 Plus Years" and REPORT_ROWS["TRT-0018"]["accrued"] == 24.6154
    # the rates
    assert SIGNED["TRT-0088"] == (118000.0, _date("06/16/2026")) and SIGNED["TRT-0117"] == (148200.0, _date("05/16/2026"))
    assert float(BAMBOO["TRT-0088"]["salary"]) == 104000.0 and float(BAMBOO["TRT-0117"]["salary"]) == 138000.0
    assert ARCHIVE_EMP["TRT-0088"]["salary"] == 118000.0 and ARCHIVE_EMP["TRT-0117"]["salary"] == 148200.0
    assert GOLDEN_BY_ID["TRT-0096"]["rate"] == 61000.0 and float(BAMBOO["TRT-0096"]["salary"]) == 58000.0
    assert GOLDEN_BY_ID["TRT-0113"]["rate"] == 61900.0  # anniversary 04/07, before the window
    assert GOLDEN_BY_ID["TRT-0141"]["rate"] == 47840.0  # anniversary 11/03, after the window
    # the part-time schedule
    assert SCHEDULE_CHANGES["TRT-0141"] == (25.0, 32.0, _date("08/10/2026"))
    assert GOLDEN_BY_ID["TRT-0141"]["accruals"] == [1.9231, 1.9231, 1.9231, 3.0769], GOLDEN_BY_ID["TRT-0141"]["accruals"]
    # the new hires
    assert GOLDEN_BY_ID["TRT-0153"]["accruals"] == [0.0, 0.0, 3.0769, 3.0769]
    assert GOLDEN_BY_ID["TRT-0155"]["accruals"] == [0.0, 0.0, 0.0, 3.0769]
    assert GOLDEN_BY_ID["TRT-0156"]["accruals"] == [0.0, 0.0, 0.0, 0.0]
    assert GOLDEN_BY_ID["TRT-0150"]["accruals"] == [3.0769] * 4
    assert BAMBOO_BALANCE["TRT-0154"]["balance"] == "3.0769" and BAMBOO_BALANCE["TRT-0150"]["balance"] == "12.3076"
    # usage
    assert round(sum(USED.values()), 2) == 560.0 and USED["TRT-0001"] == 40.0
    # the July close's method, the requester's own premise
    close = _rows(CLOSE_JULY, "PTOLiability", formulas=True)
    flat = " ".join(str(v) for r in close for v in r if v is not None)
    assert "=ROUND(G5/2080,4)" in flat and "Total = 90862.13" in flat
    assert "TRT-0037" in flat and "TRT-0064" in flat and "TRT-0153" not in flat
    assert " 92.5 " in " " + flat + " ", "the July close carried Hosana's balance uncapped"
    print("world: %d employees, %d capped, %d loaded tiers wrong, 2 signed rates dropped, 1 step, 1 schedule change; "
          "total hours %.2f, total liability $%s (posted-rounding $%s); the July close booked $90,862.13"
          % (len(GOLDEN), len(CAPPED_IDS), len(MIGRATED_WRONG_TIER), TOTAL_HOURS, f"{TOTAL:,.2f}", f"{TOTAL_POSTED:,.2f}"))


def check_plan():
    weights = [r[1] for r in PLAN]
    assert all(1 <= w <= 10 for w in weights), "a weight sits outside the platform's 1 to 10"
    gates = [r for r in PLAN if r[2] != "-"]
    assert len(gates) == 1 and gates[0][1] == 10, "the gate is the total and carries 10, the top of the scale"
    for r in PLAN:
        assert r[3].startswith("States"), "a row must open with States: " + r[3][:60]
        assert all(ord(ch) < 128 for ch in r[3]), "a criterion is not ASCII"
    fam = {}
    for f, w, *_ in PLAN:
        fam[f] = fam.get(f, 0) + w
    # the free base: the page's existence and its shape, every point of which the failing tier
    # earns. Task round 2 added three form rows and task round 4 split two of them three ways each,
    # so the ceiling is a seventh, and the two BambooHR set rows that pass on inaction stay under a
    # twentieth.
    assert fam["free"] * 7 <= PLAN_TOTAL, "the free base is over a seventh of the points"
    inaction = sum(r[1] for r in PLAN if r[9]["kind"] in ("policies", "balances"))
    assert inaction * 20 <= PLAN_TOTAL, "the guards that pass on inaction carry over a twentieth"
    # The two BambooHR set rows read the loaded records the schedule leaves as loaded and nothing
    # the created rows read, so on a schedule that is the golden less the two hires the set rows
    # pass and every row naming TRT-0153 or TRT-0155 fails. Task round 1 asked for exactly this
    # carve-out. It runs before the path scores so a planted row fails on its own message.
    loaded_only = [r for r in GOLDEN if r["id"] in LOADED_IDS]
    for fam_, w, gate, crit, pred, typ, primary, expl, refs, spec in PLAN:
        if spec["kind"] in ("policies", "balances"):
            assert pred(loaded_only), "a set row reads a created row too: " + crit[:70]
        elif "TRT-0153" in crit or "TRT-0155" in crit:
            assert not pred(loaded_only), "a created-row row passes with the row absent: " + crit[:70]
    scores = score_paths()
    assert scores[-1][2] == PLAN_TOTAL, "the golden must score every point"
    assert scores[0][2] * 5 < PLAN_TOTAL, "P0 must score under a fifth"
    return fam, scores


def check_documents_ascii():
    """Every package document is ASCII; the house register's dashes and quotes."""
    for name in ("01_prompt.md", "02_task_metadata.md", "06_failure_analysis.md", "07_paste_guide.md",
                 "08_section_1_3_step_plan.md", "09_rubric_import.md", "README.md", "qc/README.md",
                 "build/task_input_source.md"):
        path = os.path.join(PKG, name)
        if not os.path.exists(path):
            continue
        text = open(path, encoding="utf8").read()
        bad = [ch for ch in text if ord(ch) > 127]
        assert not bad, "%s is not ASCII: %r" % (name, bad[:3])


def check_docs():
    """01, 02 and README quote PROMPT verbatim, carry the live figures and list what ships."""
    for name in ("01_prompt.md", "02_task_metadata.md"):
        text = open(os.path.join(PKG, name), encoding="utf8").read()
        quoted = " ".join(l[2:] for l in text.splitlines() if l.startswith("> "))
        assert PROMPT in " ".join(quoted.split()), "%s does not blockquote the PROMPT constant verbatim" % name
    meta = open(os.path.join(PKG, "02_task_metadata.md"), encoding="utf8").read()
    for fig in (f"${TOTAL:,.2f}", f"{TOTAL_HOURS:,.2f}", "52 ", TASK_NAME, PAGE, TASK_SNAP, SNAP,
                md5(os.path.join(PKG, TASK_INPUTS[0])),
                "%d rows" % len(RUBRIC), "%d points" % PLAN_TOTAL):
        assert fig in meta, "02 lacks the figure %r" % fig
    allowed = {f"${TOTAL:,.2f}", f"${TOTAL_POSTED:,.2f}", "$90,862.13", "$118,000.00", "$148,200.00",
               "$104,000.00", "$138,000.00", "$61,000.00", "$58,000.00", "$92,000.00", "$3,000.00",
               "$56,300.00", _money(LOADED_TOTAL), _money(sum(c["moves"] for c in CELLS))}
    allowed |= {_money(f) for f, w in MONEY_BANDS}
    # every dollar figure the graded-cell table carries is the build's own arithmetic
    allowed |= {_money(c["moves"]) for c in CELLS}
    allowed |= {_money(SIGNED[i][0]) for i in SIGNED}
    allowed |= {_money(v[k]) for v in LINE_GOLD.values() for k in (1, 3)}
    allowed |= {_money(v[1]) for v in LOADED_LINE.values()}
    allowed |= {f"${t:,.2f}" for k, d, pts, fl, t, n in score_paths()}
    for fig in re.findall(r"\$\d{1,3},\d{3}\.\d{2}", meta):
        assert fig in allowed, "02 carries a dollar figure the build did not write: %s" % fig
    for f in WORLD_FILES + APP_TABLES:
        assert "\n%s\n" % f in meta, "02's selection block lacks %s" % f
    for i, (fam, w, gate, crit, pred, typ, primary, expl, refs, spec) in enumerate(PLAN, 1):
        assert crit in meta, "02 lacks planned row %d: %s" % (i, crit[:60])
        assert expl in meta, "02 publishes a stale explanation for row %d: %s" % (i, expl[:60])
    assert md5(IMPORT) in meta, "02 publishes a stale md5 for the import, this build wrote %s" % md5(IMPORT)
    nine = open(os.path.join(PKG, "09_rubric_import.md"), encoding="utf8").read()
    if not IMPORT_STATS:
        check_import()
    for fig in ("%d rows" % len(RUBRIC), "%d points" % PLAN_TOTAL, SNAP, TASK_SNAP, md5(IMPORT),
                "%d primary" % sum(1 for c in RUBRIC if c[4] == "Yes"), APPDB, FORM_TAG,
                "%d citations over %d of the" % (IMPORT_STATS["citations"], IMPORT_STATS["world_files"])):
        assert fig in nine, "09 lacks the figure %r" % fig
    fa = open(os.path.join(PKG, "06_failure_analysis.md"), encoding="utf8").read()
    for key, desc, pts, failed, tot, n in score_paths():
        assert "%s | " % key in fa and "%d of %d" % (pts, PLAN_TOTAL) in fa, "06 lacks %s at %d of %d" % (key, pts, PLAN_TOTAL)
    assert md5(os.path.join(PKG, GOLDEN_FILE)) in meta, "02 publishes a stale md5 for the golden page, this build wrote %s" % md5(os.path.join(PKG, GOLDEN_FILE))
    # 07 is written by qc/write_paste_guide.py from these rows; it has to carry every row as built
    guide = open(os.path.join(PKG, "07_paste_guide.md"), encoding="utf8").read()
    for i, (fam, w, gate, crit, pred, typ, primary, expl, refs, spec) in enumerate(PLAN, 1):
        assert crit in guide, "07 lacks row %d: %s" % (i, crit[:60])
        assert "qc/verifiers/row%02d_%s.py" % (i, slug(crit)) in guide, "07 lacks the row file for row %d" % i
        assert "| Target app | `%s` |" % TARGET_APP[spec["target"]] in guide, "07 lacks the target app of row %d" % i
    for fig in (md5(IMPORT), "%d rows" % len(RUBRIC), "%d points" % PLAN_TOTAL, "**DB only**"):
        assert fig in guide, "07 lacks the figure %r" % fig
    assert guide.count("### Row ") == len(RUBRIC), "07 carries %d row blocks for %d rows" % (guide.count("### Row "), len(RUBRIC))
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
    check_documents_ascii()
    print("docs: prompt %d chars, %d words, md5 %s" % (len(PROMPT), len(PROMPT.split()),
                                                        hashlib.md5(PROMPT.encode()).hexdigest()))


# ---------------------------------------------------------------- outputs
def write_previews():
    p = os.path.join(HERE, "schedule_preview.csv")
    with open(p, "w", newline="", encoding="utf8") as fh:
        w = csv.writer(fh)
        w.writerow(["Employee ID", "Name", "Department", "Adjusted service date", "Tier", "Opening 06/30/2026",
                    "Opening capped", "Accrual p1", "Accrual p2", "Accrual p3", "Accrual p4", "Used",
                    "Balance 08/31/2026", "Balance, posted rounding", "Annual rate", "Hourly rate", "Liability"])
        for r in GOLDEN:
            w.writerow([r["id"], r["name"], r["dept"], _d(r["adj"]), r["tier"], "%.2f" % r["opening_raw"],
                        "%.2f" % r["opening"]] + ["%.4f" % a for a in r["accruals"]] +
                       ["%.2f" % r["used"], "%.2f" % r["balance"], "%.2f" % r["balance_posted"],
                        "%.2f" % r["rate"], "%.4f" % r["hourly"], "%.2f" % r["liability"]])
        w.writerow(["TOTAL", "", "", "", "", "", "", "", "", "", "", "", "%.2f" % TOTAL_HOURS, "", "", "", "%.2f" % TOTAL])
    q = os.path.join(HERE, "rubric_plan.csv")
    with open(q, "w", newline="", encoding="utf8") as fh:
        w = csv.writer(fh)
        w.writerow(["Index", "Family", "Weight", "Gate", "Criterion", "Verifier Type", "Criterion Type",
                    "Is Primary Objective", "Tags", "Criteria Explanation", "Reference Artifacts",
                    "Target App", "Check Type", "Target Record ID", "Fallback Strategy", "Verifier File"])
        for i, (fam, wt, gate, crit, pred, typ, primary, expl, refs, spec) in enumerate(PLAN, 1):
            if "key" in spec:
                record = spec["key"]
            elif "keys" in spec:
                record = ", ".join(spec["keys"])
            elif spec["target"] == "wiki":
                record = PAGE
            else:
                record = "%d loaded records" % len(spec["expected"])
            w.writerow([i, fam, wt, gate, crit, APPDB, typ, primary, import_tag(crit), expl, "; ".join(refs),
                        TARGET_APP[spec["target"]], form_check_type(spec), record,
                        "DB only", "row%02d_%s.py" % (i, slug(crit))])
    return p, q


SYW = os.path.join(PKG, "03_show_your_work.xlsx")


def _w(n):
    """A small count in words, as the package documents write it."""
    return _WORDS[n] if 0 <= n < len(_WORDS) else str(n)


def _rows_of(pred):
    return [i for i, r in enumerate(PLAN, 1) if pred(r)]


def _row_list(ns):
    """Row numbers as the documents write them, runs of consecutive numbers joined with to."""
    runs, start = [], None
    for a, b in zip(ns, ns[1:] + [None]):
        start = a if start is None else start
        if b != a + 1:
            runs.append("%d" % a if start == a else "%d to %d" % (start, a))
            start = None
    return ", ".join(runs[:-1]) + " and " + runs[-1] if len(runs) > 1 else runs[0]


def _syw_sources():
    g = GOLDEN_BY_ID
    top = max(CAPPED_IDS, key=lambda i: g[i]["opening_raw"])
    used = sum(USED.values())
    return [
        ("The rules from 07/01/2026", "PTO policy cutover memo of 06/20/2026, /" + CUTOVER,
         "Biweekly accrual at the annual tier over 26, posted on the pay date. Carryover capped at %.1f hours at 06/30/2026. Tiers by adjusted service date, the change in the period containing the anniversary. Valued at the rate on file over %s. Ended employees out. Wiki pages do not set policy." % (CAP, f"{HOURS_PER_YEAR:,}")),
        ("What the handbook adds", "Employee Handbook v3, /" + HANDBOOK,
         "Section 7 incorporates the memo. 2.2 accrues part-time pro-rata under %d hours. 7.6 bridges service on a break under %d days. 5.4 carries the $%s Support Specialist step. 3.2 puts the signed document over the record. 7.3 totals the rounded rows." % (PART_TIME_UNDER, BRIDGE_UNDER_DAYS, f"{STEP:,.2f}")),
        ("The superseded rules", "PTO Policy 2025, /" + POLICY_2025 + ", and the Paid Time Off wiki page, /" + WIKI_PTO,
         "Monthly accrual on the 1st and unlimited carryover, replaced 07/01/2026. The wiki page was last edited 01/2025."),
        ("The current employees", "Master employee roster of 08/31/2026, /" + ROSTER + ", and the crosswalk of 08/28/2026, /" + CROSSWALK,
         "%d active employees. BambooHR carries 57 active rows. Four are contractors, three are employees whose employment ended 03/20, 05/08 and 06/15/2026, and TRT-0153 and TRT-0155 have no row, Never Loaded on the crosswalk." % len(GOLDEN)),
        ("The opening balances", "SplinterHR final archive of 07/28/2026, Balances tab, /" + ARCHIVE,
         "%d balances at 06/30/2026. %s are above %.1f hours, %s at %.2f the highest. The HRIS report, the load file and the July close carry them uncapped." % (len(ARCHIVE_BAL), _w(len(CAPPED_IDS)).capitalize(), CAP, top, g[top]["opening_raw"])),
        ("The posted periods", "Payroll procedures memo of 06/25/2026, /" + PROCEDURES,
         "Pay dates %s and %s, posted by %s. The fifth pays %s and is not posted." % (", ".join(_d(p[2]) for p in POSTED[:-1]), _d(POSTED[-1][2]), ASOF, _d(PERIODS[len(POSTED)][2]))),
        ("The service dates", "The archive's Employees tab and the historical offer letters, /" + OFFERS_HIST,
         "%s migrated records read 07/01/2026 in BambooHR and on the roster and carry their true dates in the archive and the letters. TRT-0071 was hired %s, ended 08/25/2023 and was rehired 04/22/2024, a break under %d days, bridged under handbook 7.6." % (_w(sum(1 for e in ROSTER_ROWS if e["adj_roster"] == CUTOVER_DATE and e["id"] in ARCHIVE_EMP)).capitalize(), _d(g["TRT-0071"]["adj"]), BRIDGE_UNDER_DAYS)),
        ("The tier change in the window", "The archive's dates and the memo's timing rule",
         "TRT-0018 reaches five years inside the fourth period. Three periods at 120 and one at 160, %.4f hours accrued." % g["TRT-0018"]["accrued"]),
        ("The signed pay changes", "Promotion approval TRT-0088 of 06/10/2026, /" + PROMOTION_0088 + ", and comp amendment TRT-0117 of 05/12/2026, /" + AMENDMENT_0117,
         "$%s from %s and $%s from %s, signed. BambooHR, the roster and payroll carry the loaded rates." % (f"{SIGNED['TRT-0088'][0]:,.2f}", _d(SIGNED['TRT-0088'][1]), f"{SIGNED['TRT-0117'][0]:,.2f}", _d(SIGNED['TRT-0117'][1]))),
        ("The step", "Marchetti's offer letter in the historical letters and handbook 5.4",
         "TRT-0096 steps $%s on her 08/17/2026 anniversary to $%s on file at %s." % (f"{STEP:,.2f}", f"{g['TRT-0096']['rate']:,.2f}", ASOF)),
        ("The part-time schedule", "Schedule change form TRT-0141 of 08/10/2026, /" + SCHEDULE_0141,
         "%d hours to %d hours effective %s. Pro-rata under %d hours, so three periods at %d and one at %d." % (SCHEDULE_CHANGES["TRT-0141"][0], SCHEDULE_CHANGES["TRT-0141"][1], _d(SCHEDULE_CHANGES["TRT-0141"][2]), PART_TIME_UNDER, SCHEDULE_CHANGES["TRT-0141"][0], SCHEDULE_CHANGES["TRT-0141"][1])),
        ("The two unloaded hires", "The roster, the signed offer /" + OFFER_0153 + ", letter 13 of the historical letters and Greenhouse",
         "Okonkwo started %s at $%s, moved from 07/13/2026 by the thread of 07/09/2026. Ibarra started %s at $%s. Both accrue at 80 from the period containing the start, as BambooHR credited TRT-0150, %.2f and %.2f hours." % (_d(g["TRT-0153"]["start"]), f"{g['TRT-0153']['rate']:,.2f}", _d(g["TRT-0155"]["start"]), f"{g['TRT-0155']['rate']:,.2f}", g["TRT-0153"]["balance"], g["TRT-0155"]["balance"])),
        ("Approved time off", "BambooHR TimeOffRequest",
         "%d approved requests, %.2f hours, all in July. TRT-0001 used %.2f hours." % (sum(1 for r in _csv("bamboohr", "TimeOffRequest.csv") if r["status"] == "approved" and CUTOVER_DATE <= _date(r["start_date"]) <= ASOF_DATE), used, USED["TRT-0001"])),
        ("The July close", "/" + CLOSE_JULY,
         "The requester's method. The HRIS balance, tier and rate per row, three ended employees inside, $90,862.13 booked."),
        ("The BambooHR tables", "Employee, EmployeePolicy, TimeOffBalance, TimeOffPolicy",
         "57 active rows, the loaded policies, %s of them wrong, and the loaded balances. Read, never written." % _w(len(MIGRATED_WRONG_TIER))),
    ]


def _syw_assembly():
    return [
        ("The population", "%d from the roster and the org chart. BambooHR's 57 active less four contractors less three ended plus the two unloaded hires." % len(GOLDEN)),
        ("The rules", "The cutover memo over the 2025 policy and the wiki page. The handbook's bridging, part-time, step and signed-document rules."),
        ("The opening balances", "The archive's 06/30/2026 balance capped at %.2f. %s capped. The two hires at 0.00." % (CAP, _w(len(CAPPED_IDS)).capitalize())),
        ("The service dates and tiers", "The archive's and the letters' dates over the loaded 07/01/2026. TRT-0071 bridged to %s at 160. Five migrated records at 120. TRT-0018 to 160 in the fourth period." % _d(GOLDEN_BY_ID["TRT-0071"]["adj"])),
        ("The accruals", "Four posted periods at the tier over %d to four decimals, the period containing a start credited in full. TRT-0141 pro-rata at 25 then 32 hours." % PERIODS_PER_YEAR),
        ("The usage", "%.2f approved hours deducted, %.2f on TRT-0001." % (sum(USED.values()), USED["TRT-0001"])),
        ("The rates", "The rate on file over %s to four decimals. TRT-0088 at %s, TRT-0117 at %s and TRT-0096 at %s by the signed documents and the step." % (f"{HOURS_PER_YEAR:,}", _money(GOLDEN_BY_ID['TRT-0088']['rate']), _money(GOLDEN_BY_ID['TRT-0117']['rate']), _money(GOLDEN_BY_ID['TRT-0096']['rate']))),
        ("The rows and the totals", "Balance to two decimals, liability to the cent, the total the sum of the rounded rows. %s hours and %s, %s under posted rounding." % (f"{TOTAL_HOURS:,.2f}", _money(TOTAL), _money(TOTAL_POSTED))),
        ("The lines", "The %d employees summed by department onto the request's five lines, Sales and Marketing together. %s." % (len(GOLDEN), ". ".join("%s %s hours and %s" % (n, f"{LINE_GOLD[n][0]:,.2f}", _money(LINE_GOLD[n][1])) for n in CELL_LINES))),
        ("The page", "%s. The two totals, then one table of the five lines, published." % PAGE),
    ]


def write_show_your_work():
    """03_show_your_work.xlsx: the sources, the planned rows, the assembly and the schedule, every
    value from the build, every cell ASCII."""
    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Sources"
    ws.append(["Fact", "Source", "Value"])
    for row in _syw_sources():
        ws.append(list(row))
    ws = wb.create_sheet("Verifiers")
    ws.append(["#", "Verifier", "Weight", "Gate"])
    for i, (fam, w, gate, crit, pred, typ, primary, expl, refs, spec) in enumerate(PLAN, 1):
        ws.append([i, crit, w, gate])
    ws.append([])
    ws.append(["Note", "Row 2 reads the total of all %d liabilities, the one number every rule feeds, and it matches the schedule's only if every entry is right. Row 3 reads the same population on the hours axis." % len(GOLDEN)])
    ws.append(["Note", "Rows %s read the five lines the request asks for, each line's hours and dollars. Every line figure is one the load carries wrong, so a response that copies the report earns none of them and a response that applies the rules earns them all." % (
        _row_list(_rows_of(lambda r: r[9]["kind"] in ("line_hours", "line_total"))))])
    ws.append(["Note", "Each line figure carries the dollars it moves off the load, banded %s. Sales and Marketing are one line because Marketing alone is a figure the load already carries right." % (
        ", ".join("%d where the figure moves %s or more" % (w, _money(f)) for f, w in MONEY_BANDS[:-1]) + " and 3 below that")])
    ws.append(["Note", "Row 1 is the only row that is not a determination. It carries 1 point of %d, which is the whole of what a response earns for publishing a page with the wrong numbers on it." % PLAN_TOTAL])
    ws = wb.create_sheet("Row assembly")
    ws.append(["Step", "Result"])
    for row in _syw_assembly():
        ws.append(list(row))
    ws = wb.create_sheet("Schedule")
    ws.append(["Employee ID", "Name", "Department", "Adjusted service date", "Tier", "Opening 06/30/2026",
               "Opening capped", "Accrual p1", "Accrual p2", "Accrual p3", "Accrual p4", "Used",
               "Balance 08/31/2026", "Balance, posted rounding", "Annual rate", "Hourly rate", "Liability"])
    for r in GOLDEN:
        ws.append([r["id"], r["name"], r["dept"], _d(r["adj"]), r["tier"], "%.2f" % r["opening_raw"], "%.2f" % r["opening"]]
                  + ["%.4f" % a for a in r["accruals"]]
                  + ["%.2f" % r["used"], "%.2f" % r["balance"], "%.2f" % r["balance_posted"], _money(r["rate"]), "$%.4f" % r["hourly"], _money(r["liability"])])
    total_cell = _money(TOTAL)
    ws.append(["TOTAL", "", "", "", "", "", "", "", "", "", "", "", f"{TOTAL_HOURS:,.2f}", "", "", "", total_cell])
    names = {e["name"] for e in ROSTER_ROWS}  # a person's name is a world fact and keeps the world's spelling
    from openpyxl.styles import Alignment, Font
    from openpyxl.utils import get_column_letter
    widths = {"Sources": [30, 60, 110], "Verifiers": [6, 110, 8, 14], "Row assembly": [30, 120],
              "Schedule": [12, 22, 22, 20, 6, 16, 14, 11, 11, 11, 11, 8, 16, 22, 14, 12, 12]}
    for sheet in wb:
        for i, w in enumerate(widths[sheet.title], 1):
            sheet.column_dimensions[get_column_letter(i)].width = w
        sheet.freeze_panes = "A2"
        for row in sheet.iter_rows():
            for c in row:
                if isinstance(c.value, str) and c.value not in names:
                    assert all(ord(ch) < 128 for ch in c.value), "show-your-work is not ASCII: %r" % c.value[:60]
                    assert ";" not in c.value and ":" not in c.value, "show-your-work joins clauses with ; or : where the register writes a new sentence: %r" % c.value[:60]
                c.alignment = Alignment(wrap_text=sheet.title != "Schedule", vertical="top")
                if c.row == 1:
                    c.font = Font(bold=True)
    wb.save(SYW)
    return SYW


def check_show_your_work():
    """The show-your-work on disk carries the plan's rows and the schedule's totals."""
    wb = load_workbook(SYW)
    assert wb.sheetnames == ["Sources", "Verifiers", "Row assembly", "Schedule"], wb.sheetnames
    rows = [r for r in wb["Verifiers"].iter_rows(values_only=True) if r and isinstance(r[0], int)]
    assert [r[1] for r in rows] == [p[3] for p in PLAN], "the show-your-work's verifier rows are not the plan's"
    last = [r for r in wb["Schedule"].iter_rows(values_only=True) if r and r[0] == "TOTAL"][-1]
    assert last[16] == _money(TOTAL) and last[12] == f"{TOTAL_HOURS:,.2f}", "the show-your-work's totals are not the build's: %s" % (last,)
    n = sum(1 for r in wb["Schedule"].iter_rows(values_only=True) if r and str(r[0]).startswith("TRT-"))
    assert n == len(GOLDEN), n


def path_table():
    lines = ["| Path | What the run does | Rows | Total it prints | Score |", "|---|---|---|---|---|"]
    for key, desc, pts, failed, tot, n in score_paths():
        lines.append("| %s | %s | %d | $%s | %d of %d, %.1f%% |" % (key, desc, n, f"{tot:,.2f}", pts, PLAN_TOTAL, 100.0 * pts / PLAN_TOTAL))
    return "\n".join(lines)


def main():
    check_world()
    fam, scores = check_plan()
    check_rubric()
    check_register()
    p, q = write_previews()
    s = write_show_your_work()
    imp = rubric_import()
    check_import()
    check_golden()
    gp = golden()
    names = verifiers()
    print("golden: %s, %d rows; verifiers: %d row files under qc/verifiers/" % (os.path.basename(gp), len(GOLDEN), len(names)))
    print("plan: %d rows, %d points, families %s" % (len(PLAN), PLAN_TOTAL, fam))
    for key, desc, pts, failed, tot, n in scores:
        print("  %s %3d of %d, %5.1f%%  rows %2d  total $%12s  fails %s" % (key, pts, PLAN_TOTAL, 100.0 * pts / PLAN_TOTAL, n, f"{tot:,.2f}", failed))
    print("md5 %s  %s" % (md5(p), os.path.basename(p)))
    print("md5 %s  %s" % (md5(q), os.path.basename(q)))
    print("md5 %s  %s" % (md5(s), os.path.basename(s)))
    print("md5 %s  %s" % (md5(imp), os.path.basename(imp)))
    print("md5 %s  %s" % (md5(gp), os.path.basename(gp)))
    if "--docs" in sys.argv:
        check_show_your_work()
        check_docs()
    if "--table" in sys.argv:
        print(path_table())
        print()
        print(rubric_table())


if __name__ == "__main__":
    main()
