#!/usr/bin/env python3
"""The single source of truth for T2's graded content, at the prompt half: the PTO liability
schedule at 08/31/2026 recomputed from the world's bytes under the rules the world states, the
registered failing paths recomputed under the rules each path drops, and the rubric plan that
scores them. No rubric import, golden page, verifier code or battery exists yet: by the decision
of 09/20/2026 those are built only if the first run set fails, and this file is what they will
be generated from.

Run from anywhere: python3 build/build_package_artifacts.py [--docs] [--table]
"""
import csv
import datetime as dt
import hashlib
import os
import re
import sys

from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(PKG))
WORLD = os.path.join(REPO, "filesystem")
APPS = os.path.join(REPO, "apps_data")

# ---------------------------------------------------------------- the prompt and the deliverable
PAGE = "PTO Liability - 08/31/2026"
TASK_NAME = "PTO Liability Schedule and BambooHR PTO Records"
# One sentence in the owner's register, the T1 shape: the ask, two named sources plus the open
# tail in a parenthetical, the request by subject, then the two deliverables. The two named
# sources are the ones the requester believes in and both carry the wrong numbers: the HRIS
# report prints uncapped balances at the loaded tiers and BambooHR carries the loaded rates.
# The cutover memo, the handbook, the archive, the signed pay changes, the schedule change and
# the offer letters are the response's work to find.
PROMPT = ("Complete the request (using the HRIS time off report, the BambooHR records, and the "
          "rest of the Troutly files) about the August 2026 close by publishing the Wiki.js page "
          "%s and updating the BambooHR PTO records to match it." % PAGE)
TASK_INPUTS = ["00_task_input_pto_liability_request.pdf"]
TASK_UPLOADS = ["pto_liability_request.pdf"]
ASOF = "08/31/2026"
SNAP = "snap_c6f6a0879f3d47a19048ee80d7529157"  # world_snapshot_id, unchanged across 13 exports
TASK_SNAP = "SNAPSHOT_ID_NOT_YET_READ"  # task_data_id of the T2 upload, read off its first export

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
              "bamboohr/TimeOffType.csv", "greenhouse/applications.csv",
              "greenhouse/candidates.csv", "wiki_js/Page.csv"]

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
CAPPED_IDS = sorted(r["id"] for r in GOLDEN if r["opening_raw"] > CAP)
MIGRATED_WRONG_TIER = sorted(r["id"] for r in GOLDEN if r["id"] in BAMBOO_POLICY
                             and POLICY_TIER[BAMBOO_POLICY[r["id"]]] != r["tier"])
UNLOADED_IDS = sorted(r["id"] for r in GOLDEN if r["id"] not in BAMBOO)
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
def _same(a, b, tol=0.0):
    return abs(a - b) <= tol


def _row_checks():
    """Each planned row as (family, weight, gate, criterion, predicate over a schedule). The
    predicate is what the App DB verifier will read off the page and the BambooHR tables; here it
    reads the same values off a computed schedule so the paths score by the plan's own rule."""
    g = GOLDEN_BY_ID
    by = lambda s: {r["id"]: r for r in s}

    def total_ok(s):
        t = round(sum(r["liability"] for r in s), 2)
        return _same(t, TOTAL, 0.005) or _same(t, TOTAL_POSTED, 0.005)

    def rows_ok(s):
        return set(by(s)) == set(g)

    def capped_ok(s):
        b = by(s)
        return all(i in b and _same(b[i]["opening"], CAP) for i in CAPPED_IDS)

    def five_tiers_ok(s):
        b = by(s)
        ids = [i for i in MIGRATED_WRONG_TIER if i != "TRT-0071"]
        return all(i in b and b[i]["tier"] == g[i]["tier"] for i in ids)

    def bridge_ok(s):
        b = by(s)
        return "TRT-0071" in b and b["TRT-0071"]["tier"] == 160 and _same(b["TRT-0071"]["accrued"], g["TRT-0071"]["accrued"], 0.0001)

    def thornbury_ok(s):
        b = by(s)
        return "TRT-0018" in b and _same(b["TRT-0018"]["accrued"], g["TRT-0018"]["accrued"], 0.0001)

    def rate_ok(i):
        return lambda s: i in by(s) and _same(by(s)[i]["hourly"], g[i]["hourly"], 0.00005)

    def quint_ok(s):
        b = by(s)
        return "TRT-0141" in b and _same(b["TRT-0141"]["balance"], g["TRT-0141"]["balance"], 0.005)

    def no_contractor(s):
        return not any(i.startswith("CTR-") for i in by(s))

    def no_ended(s):
        return not any(i in by(s) for i in ENDED_IN_BAMBOO + ["TRT-0006"])

    def unloaded_ok(s):
        b = by(s)
        return all(i in b and b[i]["tier"] == 80 and b[i]["accrued"] > 0 for i in UNLOADED_IDS)

    def periods_ok(s):
        b = by(s)
        return "TRT-0002" in b and _same(b["TRT-0002"]["balance"], g["TRT-0002"]["balance"], 0.005)

    def usage_ok(s):
        b = by(s)
        return "TRT-0001" in b and _same(b["TRT-0001"]["balance"], g["TRT-0001"]["balance"], 0.005)

    def policies_ok(s):
        b = by(s)
        return all(i in b and b[i]["tier"] == g[i]["tier"] for i in MIGRATED_WRONG_TIER)

    def balances_ok(s):
        b = by(s)
        return set(b) == set(g) and all(_same(b[i]["balance"], g[i]["balance"], 0.005) or _same(b[i]["balance"], g[i]["balance_posted"], 0.005) for i in g)

    def unloaded_rows_ok(s):
        return all(i in by(s) for i in UNLOADED_IDS)

    always = lambda s: True
    return [
        ("free", 1, "-", "States that a Wiki.js page titled %s is published." % PAGE, always),
        ("free", 2, "-", "States, on the PTO liability page, the %d current employees at %s as the only employee rows." % (len(GOLDEN), ASOF), rows_ok),
        ("free", 1, "-", "States, on the PTO liability page, hours to two decimals, hourly rates to four decimals, dollars to the cent and a total equal to the sum of the rows.", always),
        ("free", 1, "-", "States, on the PTO liability page, a summary with the employee count, the total hours and the total dollar liability.", always),
        ("determination", 15, "Critical value", "States, on the PTO liability page, a total dollar liability of $%s." % f"{TOTAL:,.2f}", total_ok),
        ("determination", 5, "-", "States, on the PTO liability page, an opening balance of 40.00 hours for each of the %d employees whose 06/30/2026 balance exceeded 40.0 hours." % len(CAPPED_IDS), capped_ok),
        ("determination", 5, "-", "States, on the PTO liability page, the 120-hour tier for TRT-0043, TRT-0051, TRT-0058, TRT-0079 and TRT-0083.", five_tiers_ok),
        ("determination", 7, "-", "States, on the PTO liability page, the 160-hour tier for Samuel Burkenham, TRT-0071, with service bridged to 03/08/2021.", bridge_ok),
        ("determination", 6, "-", "States, on the PTO liability page, an accrual of %.4f hours for Marisela Thornbury, TRT-0018, three periods at the 120-hour tier and one at 160." % g["TRT-0018"]["accrued"], thornbury_ok),
        ("determination", 7, "-", "States, on the PTO liability page, an hourly rate of $%.4f for Yolanda Featherstone, TRT-0088." % g["TRT-0088"]["hourly"], rate_ok("TRT-0088")),
        ("determination", 6, "-", "States, on the PTO liability page, an hourly rate of $%.4f for Belaviv Luk, TRT-0117." % g["TRT-0117"]["hourly"], rate_ok("TRT-0117")),
        ("determination", 3, "-", "States, on the PTO liability page, an hourly rate of $%.4f for Delphine Marchetti, TRT-0096." % g["TRT-0096"]["hourly"], rate_ok("TRT-0096")),
        ("determination", 4, "-", "States, on the PTO liability page, a balance of %.2f hours for Beatriz Quintanilla, TRT-0141." % g["TRT-0141"]["balance"], quint_ok),
        ("determination", 4, "-", "States, on the PTO liability page, no contractor row, CTR-2001 to CTR-2004.", no_contractor),
        ("determination", 4, "-", "States, on the PTO liability page, no row for TRT-0037, TRT-0049, TRT-0064 or TRT-0006.", no_ended),
        ("determination", 4, "-", "States, on the PTO liability page, Simone Okonkwo, TRT-0153, and Rafael Ibarra, TRT-0155, at the 80-hour tier with accruals since their start dates.", unloaded_ok),
        ("determination", 3, "-", "States, on the PTO liability page, a balance of %.2f hours for Sora Jackson, TRT-0002, four posted periods at the 160-hour tier." % g["TRT-0002"]["balance"], periods_ok),
        ("determination", 2, "-", "States, on the PTO liability page, a balance of %.2f hours for Michael Labeson, TRT-0001, with 40.00 hours of approved time off deducted." % g["TRT-0001"]["balance"], usage_ok),
        ("bamboohr", 5, "-", "States, in BambooHR, the PTO policy the schedule's tier gives for each of the %d employees whose loaded policy differed." % len(MIGRATED_WRONG_TIER), policies_ok),
        ("bamboohr", 5, "-", "States, in BambooHR, a PTO balance equal to the schedule's %s balance for every employee on the schedule." % ASOF, balances_ok),
        ("bamboohr", 2, "-", "States, in BambooHR, a PTO balance row for TRT-0153 and TRT-0155.", unloaded_rows_ok),
    ]


PLAN = _row_checks()
PLAN_TOTAL = sum(r[1] for r in PLAN)


def score_paths():
    out = []
    for key, desc, flags in PATHS:
        s = schedule(**flags)
        pts = sum(w for fam, w, gate, crit, pred in PLAN if pred(s))
        failed = [i + 1 for i, (fam, w, gate, crit, pred) in enumerate(PLAN) if not pred(s)]
        tot = round(sum(r["liability"] for r in s), 2)
        out.append((key, desc, pts, failed, tot, len(s)))
    return out


# ---------------------------------------------------------------- guards
def check_world():
    """Every rule the schedule applies is read off the document that states it."""
    cut = _docx_text(CUTOVER)
    for phrase in ("replaces the 2025 PTO policy effective 07/01/2026",
                   "PTO accrues per BIWEEKLY PAY PERIOD at the annual tier divided by 26",
                   "posts to each employee's balance on the pay date",
                   "capped at 40.0 hours as of 06/30/2026",
                   "pay period that contains the employee's service anniversary",
                   "divided by 2,080",
                   "employees whose employment ended on or before the measurement date are excluded",
                   "Under 2 years | 80 hours/year", "2 years to under 5 years | 120 hours/year",
                   "5 years and over | 160 hours/year",
                   "14 calendar days written notice"):
        assert phrase in cut, "the cutover memo does not say %r" % phrase
    hb = _pdf_text(HANDBOOK)
    for phrase in ("fewer than 30 hours per week", "accrue paid time off pro-rata to scheduled hours",
                   "less than 365 days", "$3,000.00 on each service anniversary",
                   "signed document governs until the record is corrected",
                   "totals are the sum of the rounded rows",
                   "A dated policy memo governs the handbook section it replaces",
                   "Contractors are not eligible for employee benefits, paid time off"):
        assert phrase in hb, "the handbook does not say %r" % phrase
    p25 = _docx_text(POLICY_2025)
    assert "PTO accrues monthly on the 1st of each month" in p25 and "carry over without limit" in p25
    wiki = open(os.path.join(WORLD, WIKI_PTO), encoding="utf8").read()
    assert "accrue PTO **monthly**" in wiki and "carry over without limit" in wiki
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
    assert all(1 <= w <= 15 for w in weights), "a weight sits outside its band"
    gates = [r for r in PLAN if r[2] != "-"]
    assert len(gates) == 1 and gates[0][1] == 15, "the gate is the total and carries 15"
    for r in PLAN:
        assert r[3].startswith("States"), "a row must open with States: " + r[3][:60]
        assert all(ord(ch) < 128 for ch in r[3]), "a criterion is not ASCII"
    fam = {}
    for f, w, *_ in PLAN:
        fam[f] = fam.get(f, 0) + w
    assert fam["free"] * 10 <= PLAN_TOTAL, "the free base is over a tenth of the points"
    scores = score_paths()
    assert scores[-1][2] == PLAN_TOTAL, "the golden must score every point"
    assert scores[0][2] * 5 < PLAN_TOTAL, "P0 must score under a fifth"
    return fam, scores


def check_register():
    """Every package document is ASCII; the house register's dashes and quotes."""
    for name in ("01_prompt.md", "02_task_metadata.md", "06_failure_analysis.md",
                 "08_section_1_3_step_plan.md", "README.md", "qc/README.md",
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
    for fig in (f"${TOTAL:,.2f}", f"{TOTAL_HOURS:,.2f}", "52 ", TASK_NAME, PAGE, TASK_SNAP, md5(os.path.join(PKG, TASK_INPUTS[0]))):
        assert fig in meta, "02 lacks the figure %r" % fig
    allowed = {f"${TOTAL:,.2f}", f"${TOTAL_POSTED:,.2f}", "$90,862.13", "$118,000.00", "$148,200.00",
               "$104,000.00", "$138,000.00", "$61,000.00", "$58,000.00", "$92,000.00", "$3,000.00"}
    allowed |= {f"${t:,.2f}" for k, d, pts, fl, t, n in score_paths()}
    for fig in re.findall(r"\$\d{1,3},\d{3}\.\d{2}", meta):
        assert fig in allowed, "02 carries a dollar figure the build did not write: %s" % fig
    for f in WORLD_FILES + APP_TABLES:
        assert "\n%s\n" % f in meta, "02's selection block lacks %s" % f
    for i, (fam, w, gate, crit, pred) in enumerate(PLAN, 1):
        assert crit in meta, "02 lacks planned row %d: %s" % (i, crit[:60])
    fa = open(os.path.join(PKG, "06_failure_analysis.md"), encoding="utf8").read()
    for key, desc, pts, failed, tot, n in score_paths():
        assert "%s | " % key in fa and "%d of %d" % (pts, PLAN_TOTAL) in fa, "06 lacks %s at %d of %d" % (key, pts, PLAN_TOTAL)
    readme = open(os.path.join(PKG, "README.md"), encoding="utf8").read()
    shipped = [f for f in sorted(os.listdir(PKG)) if f[0].isdigit()]
    shipped += ["build/" + f for f in sorted(os.listdir(HERE)) if not f.startswith("__")]
    shipped += ["qc/" + f for f in sorted(os.listdir(os.path.join(PKG, "qc"))) if not f.startswith("__")]
    for f in shipped:
        assert f in readme, "README does not list %s" % f
    inputs = sorted(f for f in os.listdir(PKG) if f.startswith("00_"))
    assert inputs == TASK_INPUTS, "the task inputs on disk are %s" % inputs
    for f in inputs:
        assert os.path.splitext(f)[1] in (".pdf", ".csv", ".png", ".jpg"), f
    check_register()
    print("docs: prompt %d chars, %d words, md5 %s" % (len(PROMPT), len(PROMPT.split()),
                                                        hashlib.md5(PROMPT.encode()).hexdigest()))


# ---------------------------------------------------------------- outputs
def write_previews():
    p = os.path.join(HERE, "schedule_preview.csv")
    with open(p, "w", newline="", encoding="utf8") as fh:
        w = csv.writer(fh)
        w.writerow(["Employee ID", "Name", "Department", "Adjusted service date", "Tier", "Opening 06/30/2026",
                    "Opening capped", "Accrual p1", "Accrual p2", "Accrual p3", "Accrual p4", "Used",
                    "Balance 08/31/2026", "Balance (posted rounding)", "Annual rate", "Hourly rate", "Liability"])
        for r in GOLDEN:
            w.writerow([r["id"], r["name"], r["dept"], _d(r["adj"]), r["tier"], "%.2f" % r["opening_raw"],
                        "%.2f" % r["opening"]] + ["%.4f" % a for a in r["accruals"]] +
                       ["%.2f" % r["used"], "%.2f" % r["balance"], "%.2f" % r["balance_posted"],
                        "%.2f" % r["rate"], "%.4f" % r["hourly"], "%.2f" % r["liability"]])
        w.writerow(["TOTAL", "", "", "", "", "", "", "", "", "", "", "", "%.2f" % TOTAL_HOURS, "", "", "", "%.2f" % TOTAL])
    q = os.path.join(HERE, "rubric_plan.csv")
    with open(q, "w", newline="", encoding="utf8") as fh:
        w = csv.writer(fh)
        w.writerow(["Index", "Family", "Weight", "Gate", "Criterion"])
        for i, (fam, wt, gate, crit, pred) in enumerate(PLAN, 1):
            w.writerow([i, fam, wt, gate, crit])
    return p, q


def path_table():
    lines = ["| Path | What the run does | Rows | Total it prints | Score |", "|---|---|---|---|---|"]
    for key, desc, pts, failed, tot, n in score_paths():
        lines.append("| %s | %s | %d | $%s | %d of %d, %.1f%% |" % (key, desc, n, f"{tot:,.2f}", pts, PLAN_TOTAL, 100.0 * pts / PLAN_TOTAL))
    return "\n".join(lines)


def main():
    check_world()
    fam, scores = check_plan()
    p, q = write_previews()
    print("plan: %d rows, %d points, families %s" % (len(PLAN), PLAN_TOTAL, fam))
    for key, desc, pts, failed, tot, n in scores:
        print("  %s %3d of %d, %5.1f%%  rows %2d  total $%12s  fails %s" % (key, pts, PLAN_TOTAL, 100.0 * pts / PLAN_TOTAL, n, f"{tot:,.2f}", failed))
    print("md5 %s  %s" % (md5(p), os.path.basename(p)))
    print("md5 %s  %s" % (md5(q), os.path.basename(q)))
    if "--docs" in sys.argv:
        check_docs()
    if "--table" in sys.argv:
        print(path_table())


if __name__ == "__main__":
    main()
