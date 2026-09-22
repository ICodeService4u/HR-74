"""The battery for T2: wiki and BambooHR snapshots with the answer known, one planted defect per
way a row can be wrong, the registered failing paths and the archived runs as pages, plus the
legitimate forms a correct run might use.

BATTERY is a list of (label, ctx_factory, failing_rows, why). `failing_rows` is the set of rubric
row numbers the scenario should FAIL, or "all". Every other row must pass. ROWS is the rubric row
count, read from the builder so the two cannot drift.

The fixture is the Wiki.js `pages` table in its documented 21-column order, seeded with the ten
world pages from apps_data/wiki_js/Page.csv, beside six BambooHR tables built from the seed CSVs
under apps_data/bamboohr. The BambooHR shape a grading snapshot carries is UNMEASURED, so the
fixture follows the seed CSV columns and gives every employee and policy the app's own integer
id as the run set observed them, ids 1 to 58 in the seed's row order and 59 and 60 for the two
rows the run creates; a second form keys the tables on the seed's strings and a third renames
every table, and the engine has to read all three. Column names are placeholders unless a
scenario asks for real ones, which is what a real grading snapshot has been measured to return.
"""
import csv
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(PKG))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(PKG, "build"))
from ctx import Ctx  # noqa: E402
import build_package_artifacts as B  # noqa: E402

ROWS = len(B.RUBRIC)
PAGE = B.PAGE
GOLD = B.GOLDEN_PAGE
G = B.GOLDEN_BY_ID

PAGES_COLS = ["id", "path", "hash", "title", "description", "isPrivate", "isPublished",
              "privateNS", "publishStartDate", "publishEndDate", "content", "render", "toc",
              "contentType", "createdAt", "updatedAt", "editorKey", "localeCode", "authorId",
              "creatorId", "extra"]
HIST_COLS = ["id", "pageId", "path", "hash", "title", "description", "isPrivate", "isPublished",
             "publishStartDate", "publishEndDate", "action", "content", "contentType",
             "createdAt", "versionDate", "localeCode", "authorId"]
EMP_COLS = ["id", "employee_number", "first_name", "last_name", "work_email", "department", "job_title",
            "location", "status", "hire_date", "termination_date", "supervisor_id", "salary", "pay_type", "pay_schedule"]
POL_COLS = ["id", "name", "type_id", "accrual_type", "accrual_rate", "max_balance", "carry_over", "carry_over_max"]
ASSIGN_COLS = ["id", "employee_id", "policy_id", "effective_date", "end_date"]
BAL_COLS = ["id", "employee_id", "policy_id", "year", "balance", "used", "scheduled"]
REQ_COLS = ["id", "employee_id", "type_id", "policy_id", "start_date", "end_date", "amount", "status", "notes", "approver_id"]
TYPE_COLS = ["id", "name", "color", "paid", "units"]
NAMES = dict(emp="employees", pol="time_off_policies", assign="employee_time_off_policies",
             bal="time_off_balances", req="time_off_requests", typ="time_off_types")
OTHER_NAMES = dict(emp="bamboo_staff", pol="bamboo_pto_plans", assign="bamboo_plan_membership",
                   bal="bamboo_pto_ledger", req="bamboo_pto_requests", typ="bamboo_pto_kinds")


def _csv(app, table):
    with open(os.path.join(REPO, "apps_data", app, table), newline="", encoding="utf8") as fh:
        return list(csv.DictReader(fh))


# ---------------------------------------------------------------- the wiki side
def _slug(title):
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def _page_row(i, title, content, published=1, path=None, desc=""):
    return [i, path or _slug(title), "h%d" % i, title, desc, 0, published, None, None, None,
            content, "<p>rendered</p>", "[]", "markdown", "2026-08-31 09:00:00",
            "2026-08-31 09:00:00", "markdown", "en", 5, 5, "{}"]


def wiki_tables(pages=(), cols=PAGES_COLS, history=()):
    rows = []
    for i, p in enumerate(_csv("wiki_js", "Page.csv"), 1):
        rows.append(_page_row(i, p["title"], p["content"], 1 if p["isPublished"] == "true" else 0, p["path"]))
    for n, spec in enumerate(pages, 11):
        title, content = spec[0], spec[1]
        pub = spec[2] if len(spec) > 2 else 1
        desc = spec[3] if len(spec) > 3 else ""
        rows.append(_page_row(n, title, content, pub, desc=desc))
    rows = [r[:len(cols)] for r in rows]
    hist = [[n, 99, _slug(t), "h", t, "", 0, 1, None, None, "updated", c, "markdown",
             "2026-08-31 09:00:00", "2026-08-31 09:00:00", "en", 5] for n, (t, c) in enumerate(history, 1)]
    return {"pages": (cols, rows), "pageHistory": (HIST_COLS, hist),
            "users": (["id", "email", "name"], [[5, "casey@troutlyanalytics.com", "Casey Ouk"]])}


# ---------------------------------------------------------------- the BambooHR side
SEED_EMP = _csv("bamboohr", "Employee.csv")
SEED_POL = _csv("bamboohr", "TimeOffPolicy.csv")
SEED_ASSIGN = _csv("bamboohr", "EmployeePolicy.csv")
SEED_BAL = _csv("bamboohr", "TimeOffBalance.csv")
SEED_REQ = _csv("bamboohr", "TimeOffRequest.csv")
SEED_TYPE = _csv("bamboohr", "TimeOffType.csv")
EMP_ID = {e["employee_number"]: str(i) for i, e in enumerate(SEED_EMP, 1)}
POL_ID = {p["name"]: str(i) for i, p in enumerate(SEED_POL, 1)}
_observed = json.load(open(os.path.join(HERE, "findings", "run_set_09-20-2026", "G1_bamboohr_writes.json")))["id_to_employee_number"]
assert all(_observed[k] == num for num, k in EMP_ID.items()), "the fixture's ids are not the ids G1 observed"
HIRES = {"TRT-0153": dict(first="Simone", last="Okonkwo", dept="Customer Success", title="Customer Success Manager",
                          hire="2026-07-22", salary="92000.00", sup="15"),
         "TRT-0155": dict(first="Rafael", last="Ibarra", dept="Engineering", title="Software Engineer II",
                          hire="2026-08-03", salary="56300.00", sup="5")}


def seed_state():
    """(policies, balances) as the seed loads them: {number: policy name}, {number: balance}."""
    return ({a["employee_id"]: a["policy_id"] for a in SEED_ASSIGN},
            {b["employee_id"]: float(b["balance"]) for b in SEED_BAL})


def correct_state(sched=None):
    """BambooHR brought to a schedule: the schedule's policy and balance on every row, the two hires
    created. The golden schedule by default."""
    sched = sched or B.GOLDEN
    pol, bal = seed_state()
    hires = {}
    for r in sched:
        pol[r["id"]] = B.TIER_POLICY[r["tier"]]
        bal[r["id"]] = r["balance"]
        if r["id"] in HIRES:
            hires[r["id"]] = HIRES[r["id"]]
    return pol, bal, hires


def bamboo_tables(pol=None, bal=None, hires=None, names=NAMES, string_keys=False, keep_old=None,
                  extra_balance=None, balance_as_text=False, drop=(), extra_assign=None):
    """The six BambooHR tables from the seed plus a state. `keep_old` = "ended" or "open" keeps
    each reassigned employee's old assignment row beside the new one; `extra_balance` adds a
    second 2026 balance row (number, policy, balance); `extra_assign` adds an assignment row
    (number, policy) for an employee the seed left without one; `drop` removes tables."""
    seed_pol, seed_bal = seed_state()
    pol = pol if pol is not None else seed_pol
    bal = bal if bal is not None else seed_bal
    hires = hires or {}
    emp_rows, ids = [], dict(EMP_ID)
    for i, e in enumerate(SEED_EMP, 1):
        emp_rows.append([i, e["employee_number"], e["first_name"], e["last_name"], e["work_email"], e["department"],
                         e["job_title"], e["location"], e["status"], e["hire_date"], e["termination_date"] or None,
                         EMP_ID.get(e["supervisor_id"]) if e["supervisor_id"] else None, e["salary"], e["pay_type"], e["pay_schedule"]])
    for n, (num, h) in enumerate(sorted(hires.items()), 59):
        ids[num] = str(n)
        emp_rows.append([n, num, h["first"], h["last"], "%s@troutlyanalytics.com" % h["first"].lower(), h["dept"], h["title"],
                         "TX", "Active", h["hire"], None, h["sup"], h["salary"], "salary", "Biweekly"])
    pol_rows = [[i, p["name"], p["type_id"] if string_keys else 1, p["accrual_type"], p["accrual_rate"],
                 p["max_balance"] or None, p["carry_over"], p["carry_over_max"] or None] for i, p in enumerate(SEED_POL, 1)]

    def eref(num):
        return num if string_keys else int(ids[num])

    def pref(name):
        return name if string_keys else int(POL_ID[name])

    assign_rows, n = [], 1
    for num in list(seed_pol) + [h for h in hires if h not in seed_pol]:
        if num not in ids or num not in pol:
            continue
        old = seed_pol.get(num)
        new = pol[num]
        eff = next((a["effective_date"] for a in SEED_ASSIGN if a["employee_id"] == num), None) or hires.get(num, {}).get("hire", "2026-07-01")
        if old and old != new and keep_old:
            assign_rows.append([n, eref(num), pref(old), eff, "2026-09-20" if keep_old == "ended" else None]); n += 1
            assign_rows.append([n, eref(num), pref(new), "2026-09-20", None]); n += 1
        else:
            assign_rows.append([n, eref(num), pref(new), eff, None]); n += 1
    if extra_assign:
        assign_rows.append([n, eref(extra_assign[0]), pref(extra_assign[1]), "2026-07-01", None]); n += 1
    bal_rows, n = [], 1
    for num in list(seed_bal) + [h for h in hires if h not in seed_bal]:
        if num not in ids or num not in bal:
            continue
        v = bal[num]
        v = ("%.4f" % v) if balance_as_text else v
        bal_rows.append([n, eref(num), pref(pol.get(num, seed_pol.get(num, "PTO Under 2 Years"))), 2026, v,
                         next((b["used"] for b in SEED_BAL if b["employee_id"] == num), "0"), 0]); n += 1
    if extra_balance:
        num, pname, v = extra_balance
        bal_rows.append([n, eref(num), pref(pname), 2026, v, 0, 0])
    req_rows = [[i, eref(r["employee_id"]), 1, pref(r["policy_id"]), r["start_date"], r["end_date"], r["amount"],
                 r["status"], r["notes"], eref(r["approver_id"]) if r["approver_id"] else None]
                for i, r in enumerate(SEED_REQ, 1) if r["employee_id"] in ids]
    type_rows = [[i, t["name"], t["color"], t["paid"], t["units"]] for i, t in enumerate(SEED_TYPE, 1)]
    out = {names["emp"]: (EMP_COLS, emp_rows), names["pol"]: (POL_COLS, pol_rows), names["assign"]: (ASSIGN_COLS, assign_rows),
           names["bal"]: (BAL_COLS, bal_rows), names["req"]: (REQ_COLS, req_rows), names["typ"]: (TYPE_COLS, type_rows)}
    for d in drop:
        out.pop(names[d], None)
    return out


GH_TABLES = sorted(f[:-4] for f in os.listdir(os.path.join(REPO, "apps_data", "greenhouse")) if f.endswith(".csv"))


def greenhouse_tables():
    """The fourteen Greenhouse seed tables as the CSVs carry them, in every snapshot as the third
    app's tables. No row reads them since task round 3 took the memo's fence out; they are here so
    the BambooHR and pages discovery has to pass over another app's tables to find its own."""
    out = {}
    for t in GH_TABLES:
        rows = _csv("greenhouse", t + ".csv")
        cols = list(rows[0].keys()) if rows else ["id"]
        out[t] = (cols, [[r.get(c, "") for c in cols] for r in rows])
    return out


def snap(pages=(), bamboo=None, real_names=False, cols=PAGES_COLS, history=()):
    tables = dict(wiki_tables(pages, cols, history))
    tables.update(bamboo if bamboo is not None else bamboo_tables())
    tables.update(greenhouse_tables())
    return Ctx(tables, real_names=real_names)


def correct_bamboo(**kw):
    pol, bal, hires = correct_state()
    return bamboo_tables(pol, bal, hires, **kw)


# ---------------------------------------------------------------- page editing helpers
def set_cell(md, key, column, value):
    """Replace one cell: the row whose first cell equals `key`, in the column headed `column`."""
    out, header = [], None
    for line in md.split("\n"):
        if line.count("|") >= 2:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if all(re.fullmatch(r":?-{2,}:?", c or "--") for c in cells):
                out.append(line)
                continue
            if header is None:
                header = [c.lower() for c in cells]
                out.append(line)
                continue
            if cells[0] == key:
                i = next(i for i, h in enumerate(header) if column.lower() in h)
                cells[i] = value
                out.append("| " + " | ".join(cells) + " |")
                continue
        else:
            header = None
        out.append(line)
    assert out != md.split("\n"), "set_cell changed nothing for %r" % key
    return "\n".join(out)


def set_balance(md, key, value):
    """One balance cell changed and the summary's total hours recomputed from the cells, so the
    page stays consistent with itself and only the value row reads the defect."""
    md = set_cell(md, key, "balance", value)
    hours = 0.0
    for line in md.split("\n"):
        if re.match(r"\|\s*TRT-", line):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            hours += float(cells[4].replace(",", ""))
    return re.sub(r"- Total hours: [\d,]+\.\d+", "- Total hours: %s" % f"{round(hours, 2):,.2f}", md)


def replace(md, old, new):
    assert old in md, "replace found nothing for %r" % old[:50]
    return md.replace(old, new)


def rows_of(sched_ids):
    return [G[i] for i in sched_ids]


def with_rows(extra):
    """The golden schedule plus the given extra rows, rendered so the summary agrees with the table."""
    return B.render_page(B.GOLDEN + list(extra))


def without(ids):
    return B.render_page([r for r in B.GOLDEN if r["id"] not in ids])


def to_html(md):
    out, in_table = [], False
    for line in md.split("\n"):
        if line.count("|") >= 2:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if all(re.fullmatch(r":?-{2,}:?", c or "--") for c in cells):
                continue
            if not in_table:
                out.append("<table>")
                in_table = True
            out.append("<tr>" + "".join("<td>%s</td>" % c for c in cells) + "</tr>")
            continue
        if in_table:
            out.append("</table>")
            in_table = False
        if line.startswith("# "):
            out.append("<h1>%s</h1>" % line[2:])
        elif line.startswith("## "):
            out.append("<h2>%s</h2>" % line[3:])
        elif line.startswith("- "):
            out.append("<li>%s</li>" % line[2:])
        elif line.strip():
            out.append("<p>%s</p>" % line)
    if in_table:
        out.append("</table>")
    return "\n".join(out)


def split_tables(md, at=26):
    lines = md.split("\n")
    idx = [i for i, l in enumerate(lines) if re.match(r"\|\s*TRT-", l)]
    hdr = lines[idx[0] - 2:idx[0]]
    cut = idx[at]
    return "\n".join(lines[:cut] + ["", "## Second half", ""] + hdr + lines[cut:])


def summary_below(md):
    lines = md.split("\n")
    s = lines.index("## Summary")
    e = next(i for i in range(s + 1, len(lines)) if lines[i].startswith("|"))
    summary = lines[s:e]
    rest = lines[:s] + lines[e:]
    return "\n".join(rest + [""] + summary)


def archived(run):
    """An archived run's page and its BambooHR end state, from qc/findings."""
    sys.path.insert(0, HERE)
    import score_run_set as S
    folder = os.path.join(HERE, "findings", "run_set_09-20-2026")
    text = open(os.path.join(folder, "%s_pto_liability.md" % run), encoding="utf8").read()
    pol, bal, _ = S.bamboo_state(os.path.join(folder, "%s_bamboohr_writes.json" % run))
    hires = {h: HIRES[h] for h in HIRES if h in bal}
    return text, bamboo_tables(pol, bal, hires)


def path_page(key):
    sched = next(B.schedule(**flags) for k, d, flags in B.PATHS if k == key)
    pol, bal, hires = correct_state(sched)
    return B.render_page(sched), bamboo_tables(pol, bal, hires)


def path_fails(key):
    return set(next(fl for k, d, pts, fl, tot, n in B.score_paths() if k == key))


P0 = [r for r in B.schedule(population=False)]
CTR_ROWS = [r for r in P0 if r["id"].startswith("CTR-")]
ENDED_ROWS = {r["id"]: r for r in P0 if r["id"] in B.ENDED_IN_BAMBOO}
PAGE_ROWS = set(range(1, 27))
POL_ROWS = set(range(27, 33))        # one policy per record the schedule moves
POL_GUARD = 33                       # the 44 loaded policies the schedule leaves, stated in terms
BAL_ROWS = set(range(34, 51))        # one balance per loaded balance the schedule moves, 17
BAL_GUARD = 51                       # the 33 loaded balances the schedule leaves, stated in terms
HIRE_ROWS = {52, 53, 54, 55}         # a balance and a policy for each record the run creates
BAM_ROWS = POL_ROWS | {POL_GUARD} | BAL_ROWS | {BAL_GUARD} | HIRE_ROWS
DET = set(range(14, 23))             # the gate and the eight page rules
h05 = G["TRT-0005"]

BATTERY = [
    ("the golden page and BambooHR brought to the schedule", lambda: snap([(PAGE, GOLD)], correct_bamboo()), set(),
     "the graded end state - the golden must score 100"),
    ("the golden, real column names", lambda: snap([(PAGE, GOLD)], correct_bamboo(), real_names=True), set(),
     "the other branch - a check must work whether or not the snapshot carries names"),
    ("the golden, the title with an em dash",
     lambda: snap([(PAGE.replace(" - ", " %s " % chr(0x2014)), GOLD)], correct_bamboo()), set(),
     "the prompt's dash is a hyphen; a run that types an em dash has still named the page"),
    ("the golden as HTML", lambda: snap([(PAGE, to_html(GOLD))], correct_bamboo()), set(),
     "a run on the visual editor stores HTML, and a table is still a table"),
    ("the golden, BambooHR keyed on the seed's strings", lambda: snap([(PAGE, GOLD)], correct_bamboo(string_keys=True)), set(),
     "a loader that keeps the seed's employee numbers and policy names as keys"),
    ("the golden, BambooHR tables under other names", lambda: snap([(PAGE, GOLD)], correct_bamboo(names=OTHER_NAMES)), set(),
     "the live app's table names are unmeasured; the tables are found by content"),
    ("the golden, string keys and an assignment row for every employee",
     lambda: snap([(PAGE, GOLD)], correct_bamboo(string_keys=True, extra_assign=("TRT-0006", "PTO 5 Plus Years"))), set(),
     "the assignment table carries as many distinct employee numbers as the employee table; the count alone cannot tell them apart"),
    ("the golden, balances stored as text", lambda: snap([(PAGE, GOLD)], correct_bamboo(balance_as_text=True)), set(),
     "the column renders as 64.6200; cast before comparing"),
    ("the golden, old assignments kept with an end date", lambda: snap([(PAGE, GOLD)], correct_bamboo(keep_old="ended")), set(),
     "a reassignment that end-dates the old row is a reassignment"),
    ("the golden, old assignments kept open beside the new", lambda: snap([(PAGE, GOLD)], correct_bamboo(keep_old="open")), set(),
     "two open rows; the later effective date is the current policy"),
    ("the golden, rates without a dollar sign and tiers as policy names",
     lambda: snap([(PAGE, re.sub(r"\| \$(\d+\.\d{4}) \|", r"| \1 |", GOLD.replace("| 160 |", "| PTO 5 Plus Years |")))], correct_bamboo()),
     set(), "the request fixes precision, not the sign or the tier's spelling; the reviewer rule accepts a policy name"),
    ("the golden, a header with other words",
     lambda: snap([(PAGE, B.render_page(B.GOLDEN, headers=["ID", "Employee Name", "Dept", "PTO Tier (hrs/yr)", "Balance 08/31/2026", "Hourly Rate ($)", "Liability ($)"]))], correct_bamboo()),
     set(), "the memo's column names with other words are the same columns"),
    ("the golden, a header with no usable words",
     lambda: snap([(PAGE, B.render_page(B.GOLDEN, headers=["A", "B", "C", "D", "E", "F", "G"]))], correct_bamboo()),
     set(), "seven columns keyed on an ID in the first cell read in the request's order"),
    ("the golden with a total row in the table",
     lambda: snap([(PAGE, GOLD + "| Total | | | | %s | | $%s |\n" % (f"{B.TOTAL_HOURS:,.2f}", f"{B.TOTAL:,.2f}"))], correct_bamboo()),
     set(), "a row keyed on no ID and carrying no name is not an employee row, and its total is a stated total"),
    ("a subtotal row naming an ended employee in its first cell",
     lambda: snap([(PAGE, GOLD + "| Subtotal after TRT-0037 left, TRT-0002 to TRT-0128 | | | | 500.00 | | $40,000.00 |\n")], correct_bamboo()),
     set(), "a key is a whole cell: a note naming an ended employee must not put him on the table or into the set"),
    ("Ibarra's row replaced by a note naming him",
     lambda: snap([(PAGE, without(["TRT-0155"]) + "| TRT-0155 not loaded, see BambooHR | Rafael Ibarra | Engineering | | | | |\n")], correct_bamboo()),
     {2, 11, 14, 24}, "a mention in a cell is not a row: the set, the ID-on-every-row form, the total and his balance fail, and a substring key would pass the set"),
    # ---- nothing, or the wrong page
    ("the seed: no page, BambooHR untouched", lambda: snap(history=[(PAGE, GOLD)]), set(range(1, 56)) - {POL_GUARD, BAL_GUARD},
     "a check that reads history instead of pages passes a run that did nothing; the two guards pass on inaction by design"),
    ("the page saved unpublished", lambda: snap([(PAGE, GOLD, 0)], correct_bamboo()), {1},
     "a draft is not a published page; the content rows still read the content"),
    ("the page under a different title", lambda: snap([("PTO Liability August 2026", GOLD)], correct_bamboo()), PAGE_ROWS,
     "a title that drops the date is a different page; the request fixes the title"),
    ("a snapshot with 20 page columns", lambda: snap([(PAGE, GOLD)], correct_bamboo(), cols=PAGES_COLS[:-1]), {1},
     "a shape the documented layout does not validate reads the content but cannot show publication"),
    ("a second page with the same title carrying the uncapped balance",
     lambda: snap([(PAGE, GOLD), (PAGE, B.render_page([dict(r, balance=r["opening_raw"] + round(sum(r["accruals"]), 2),
                                                         liability=round((r["opening_raw"] + round(sum(r["accruals"]), 2)) * r["hourly"], 2))
                                                    if r["id"] == "TRT-0005" else r for r in B.GOLDEN]))], correct_bamboo()),
     PAGE_ROWS, "a wrong duplicate leaves the wiki wrong, and the request asks for one page under the title"),
    ("a second page with the same title carrying the same schedule",
     lambda: snap([(PAGE, GOLD), (PAGE, GOLD)], correct_bamboo()), PAGE_ROWS,
     "the memo asks for one page published under the title; two correct copies are two pages, and a check that reads them row by row passes them"),
    ("a note page carrying the title in its description, real column names",
     lambda: snap([(PAGE, GOLD), ("PTO Liability Notes", "# PTO Liability Notes\n\nThe schedule is the other page.", 1, PAGE)],
                  correct_bamboo(), real_names=True), set(),
     "a description is not a title: the one page under the title is the schedule, and a title read off any cell would call this a duplicate"),
    # ---- the archived runs and the registered paths
    ("G1 as archived: P1 row for row, BambooHR as G1 left it", lambda: snap([(PAGE, archived("G1")[0])], archived("G1")[1]),
     {12} | DET | POL_ROWS | BAL_ROWS, "the modal path measured on 09/20/2026, three of five runs; the two guards pass on an untouched BambooHR, and G1 wrote August 31, 2026 in its prose against the request's MM/DD/YYYY"),
    ("G2 as archived: P1 less the two hires, BambooHR untouched", lambda: snap([(PAGE, archived("G2")[0])], archived("G2")[1]),
     {2, 23, 24} | DET | POL_ROWS | BAL_ROWS | HIRE_ROWS, "two of five runs read Never Loaded as no liability"),
    ("P2 as a page, BambooHR brought to it", lambda: snap([(PAGE, path_page("P2")[0])], path_page("P2")[1]), path_fails("P2"),
     "the cap applied and nothing else"),
    ("P3 as a page, BambooHR brought to it", lambda: snap([(PAGE, path_page("P3")[0])], path_page("P3")[1]), path_fails("P3"),
     "the archive's dates unbridged and untimed, the rates as loaded"),
    ("P4 as a page, BambooHR brought to it", lambda: snap([(PAGE, path_page("P4")[0])], path_page("P4")[1]), path_fails("P4"),
     "the signed rates found, the bridge and the timing missed"),
    ("P5 as a page, BambooHR brought to it", lambda: snap([(PAGE, path_page("P5")[0])], path_page("P5")[1]), path_fails("P5"),
     "everything but the step and the part-time schedule"),
    # ---- one cell wrong
    ("Hosana's balance one hundredth under", lambda: snap([(PAGE, set_balance(GOLD, "TRT-0005", "%.2f" % (h05["balance"] - 0.01)))], correct_bamboo()),
     {15}, "a stated two-decimal value is graded to the cent; its neighbour is not it"),
    ("Hosana's balance one hundredth over", lambda: snap([(PAGE, set_balance(GOLD, "TRT-0005", "%.2f" % (h05["balance"] + 0.01)))], correct_bamboo()),
     {15}, "the other neighbour"),
    ("Hosana's balance at four decimals", lambda: snap([(PAGE, set_cell(GOLD, "TRT-0005", "balance", "64.6152"))], correct_bamboo()),
     {3}, "the same quantity at more precision passes the value row and fails the hours form row alone"),
    ("Hosana's balance uncapped", lambda: snap([(PAGE, set_balance(GOLD, "TRT-0005", "117.12"))], correct_bamboo()),
     {15}, "the HRIS report's figure on one row; the liability cell left alone keeps the total"),
    ("Kastellanos at the 80-hour tier", lambda: snap([(PAGE, set_cell(GOLD, "TRT-0043", "tier", "80"))], correct_bamboo()),
     {16}, "the loaded date's tier"),
    ("Kastellanos's tier as the loaded policy name", lambda: snap([(PAGE, set_cell(GOLD, "TRT-0043", "tier", "PTO Under 2 Years"))], correct_bamboo()),
     {16}, "the policy name for the wrong tier is still the wrong tier"),
    ("Burkenham at the 120-hour tier", lambda: snap([(PAGE, set_cell(GOLD, "TRT-0071", "tier", "120"))], correct_bamboo()),
     {17}, "the rehire date without the bridge"),
    ("Featherstone at the loaded rate", lambda: snap([(PAGE, set_cell(GOLD, "TRT-0088", "rate", "$50.0000"))], correct_bamboo()),
     {19}, "the record's rate over the signed document"),
    ("Featherstone's rate one ten-thousandth under", lambda: snap([(PAGE, set_cell(GOLD, "TRT-0088", "rate", "$56.7307"))], correct_bamboo()),
     {19}, "a four-decimal rate is graded to the fourth decimal"),
    ("Featherstone's rate at two decimals", lambda: snap([(PAGE, set_cell(GOLD, "TRT-0088", "rate", "$56.73"))], correct_bamboo()),
     {4, 19}, "not the stated value and not the rates form row"),
    ("Luk at the loaded rate", lambda: snap([(PAGE, set_cell(GOLD, "TRT-0117", "rate", "$66.3462"))], correct_bamboo()),
     {20}, "the amendment missed"),
    ("Marchetti without the step", lambda: snap([(PAGE, set_cell(GOLD, "TRT-0096", "rate", "$27.8846"))], correct_bamboo()),
     {21}, "the step missed"),
    ("Quintanilla at 40 hours a week", lambda: snap([(PAGE, set_balance(GOLD, "TRT-0141", "33.06"))], correct_bamboo()),
     {22}, "the part-time rule missed"),
    ("Thornbury at 160 all four periods", lambda: snap([(PAGE, set_balance(GOLD, "TRT-0018", "64.62"))], correct_bamboo()),
     {18}, "the anniversary untimed"),
    # ---- the population
    ("the four contractors on the table", lambda: snap([(PAGE, with_rows(CTR_ROWS))], correct_bamboo()),
     {2, 14}, "contractors as employees; the summary agrees with the table, so the set and the total fail"),
    ("Athanasoulis on the table", lambda: snap([(PAGE, with_rows([ENDED_ROWS["TRT-0037"]]))], correct_bamboo()),
     {2, 14}, "an ended record still read as Active; the set and the total fail"),
    ("Delacroix-Hahn on the table", lambda: snap([(PAGE, with_rows([ENDED_ROWS["TRT-0064"]]))], correct_bamboo()),
     {2, 14}, "the third ended record"),
    ("the two hires off the page", lambda: snap([(PAGE, without(B.UNLOADED_IDS))], correct_bamboo()),
     {2, 14, 23, 24}, "Never Loaded read as no liability, the page side; the total moves with the rows"),
    ("the page thinned to its first five rows", lambda: snap([(PAGE, B.render_page(B.GOLDEN[:5]))], correct_bamboo()),
     {2, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24},
     "five rows are a table; every row keyed on an employee outside the five fails, and the set fails on the missing 47"),
    # ---- the form and the layout
    ("the table split in two", lambda: snap([(PAGE, split_tables(GOLD))], correct_bamboo()), {13},
     "the request asks for one table; every value row still reads its cell"),
    ("the summary below the table", lambda: snap([(PAGE, summary_below(GOLD))], correct_bamboo()), {13},
     "the request puts the summary above the table"),
    ("the summary without the total hours",
     lambda: snap([(PAGE, replace(GOLD, "- Total hours: %s\n" % f"{B.TOTAL_HOURS:,.2f}", ""))], correct_bamboo()), {7},
     "the summary's three figures are asked; the layout row reads the count and a dollar figure"),
    ("the summary without the count",
     lambda: snap([(PAGE, replace(GOLD, "- Employees on the schedule: %d\n" % len(B.GOLDEN), ""))], correct_bamboo()), {7, 13},
     "the count is asked in the summary and above the table"),
    ("the summary's total not the sum of the rows",
     lambda: snap([(PAGE, replace(GOLD, "- Total dollar liability: $%s" % f"{B.TOTAL:,.2f}", "- Total dollar liability: $92,739.99"))], correct_bamboo()),
     {6, 14}, "a stated total that is not the rows' sum fails the reconciliation and the gate; the summary still states a figure"),
    ("a name cell blank", lambda: snap([(PAGE, set_cell(GOLD, "TRT-0005", "Name", ""))], correct_bamboo()), {8},
     "a name on every row is asked"),
    ("a department cell carrying the ID again", lambda: snap([(PAGE, set_cell(GOLD, "TRT-0005", "Department", "TRT-0005"))], correct_bamboo()), {9},
     "a department on every row is asked, and an ID is not one"),
    ("a tier cell blank", lambda: snap([(PAGE, set_cell(GOLD, "TRT-0012", "tier", ""))], correct_bamboo()), {10},
     "an annual PTO tier on every row is asked"),
    ("an employee row with the ID blank", lambda: snap([(PAGE, B.render_page([dict(r, id="") if r["id"] == "TRT-0012" else r for r in B.GOLDEN]))], correct_bamboo()),
     {2, 11}, "an employee ID on every row is the request's form line; the set misses the row too, and the row still counts and sums as an employee row, so the summary, the reconciliation and the layout stand"),
    ("a total line with the name column reading Total", lambda: snap([(PAGE, GOLD + "| | Total | | | %s | | $%s |\n" % (f"{B.TOTAL_HOURS:,.2f}", f"{B.TOTAL:,.2f}"))], correct_bamboo()),
     set(), "a total word where the name would be is not a name; the line neither counts nor sums as an employee row"),
    ("an ISO date in the summary", lambda: snap([(PAGE, replace(GOLD, "## Summary\n\n", "## Summary\n\n- Measurement date: 2026-08-31\n"))], correct_bamboo()),
     {12}, "Dates MM/DD/YYYY is the request's form line"),
    # ---- BambooHR
    ("the golden page, BambooHR untouched", lambda: snap([(PAGE, GOLD)]), POL_ROWS | BAL_ROWS | HIRE_ROWS,
     "the seed state on the BambooHR side: six policies wrong, seventeen balances wrong, no rows for the hires; the two guards pass by design"),
    ("policies fixed, balances untouched, hires created", lambda: snap([(PAGE, GOLD)], bamboo_tables(correct_state()[0], dict(seed_state()[1], **{"TRT-0153": 6.15, "TRT-0155": 3.08}), correct_state()[2])),
     BAL_ROWS, "the policy half of the ask without the balance half"),
    ("balances fixed, policies untouched", lambda: snap([(PAGE, GOLD)], bamboo_tables(seed_state()[0], correct_state()[1], correct_state()[2])),
     POL_ROWS | {54, 55}, "the balance half without the policy half, the created records' policies included"),
    ("everything but the two rows created", lambda: snap([(PAGE, GOLD)], bamboo_tables(correct_state()[0], correct_state()[1], {})),
     HIRE_ROWS, "the Never Loaded rows never created"),
    ("Okonkwo's row created at zero hours", lambda: snap([(PAGE, GOLD)], bamboo_tables(correct_state()[0], dict(correct_state()[1], **{"TRT-0153": 0.0}), correct_state()[2])),
     {52}, "a row created with the wrong balance"),
    ("Raghunath's policy left as loaded", lambda: snap([(PAGE, GOLD)], bamboo_tables(dict(correct_state()[0], **{"TRT-0051": "PTO Under 2 Years"}), correct_state()[1], correct_state()[2])),
     {28}, "one of the six policies not moved; the other five and the guard stand"),
    ("Labeson's policy moved for no reason", lambda: snap([(PAGE, GOLD)], bamboo_tables(dict(correct_state()[0], **{"TRT-0001": "PTO Under 2 Years"}), correct_state()[1], correct_state()[2])),
     {POL_GUARD}, "a policy the schedule leaves as loaded, changed: the guard fails and nothing else does"),
    ("Kastellanos's BambooHR balance left as loaded", lambda: snap([(PAGE, GOLD)], bamboo_tables(correct_state()[0], dict(correct_state()[1], **{"TRT-0043": 31.8076}), correct_state()[2])),
     {35}, "one of the five mirrored balances not moved"),
    ("Jackson's BambooHR balance zeroed", lambda: snap([(PAGE, GOLD)], bamboo_tables(correct_state()[0], dict(correct_state()[1], **{"TRT-0002": 0.0}), correct_state()[2])),
     {BAL_GUARD}, "a balance the schedule leaves as loaded, changed: the guard fails and nothing else does"),
    ("Hosana's BambooHR balance one hundredth under", lambda: snap([(PAGE, GOLD)], bamboo_tables(correct_state()[0], dict(correct_state()[1], **{"TRT-0005": h05["balance"] - 0.01}), correct_state()[2])),
     {34}, "the neighbour planted on the BambooHR side"),
    ("Hosana's BambooHR balance as the golden's four decimals", lambda: snap([(PAGE, GOLD)], bamboo_tables(correct_state()[0], dict(correct_state()[1], **{"TRT-0005": 64.6152}), correct_state()[2])),
     set(), "the app's own precision, within 0.005 of the stated value"),
    ("a second 2026 balance row for Hosana", lambda: snap([(PAGE, GOLD)], correct_bamboo(extra_balance=("TRT-0005", "PTO 5 Plus Years", 117.12))),
     {34}, "two balances for one employee in one year leave the record wrong; the false zero is taken"),
    ("the balance table missing", lambda: snap([(PAGE, GOLD)], correct_bamboo(drop=("bal",))), BAL_ROWS | {BAL_GUARD, 52, 53},
     "a snapshot without a balance table shows no balance; the created records' policies still read"),
    ("the policy table missing", lambda: snap([(PAGE, GOLD)], correct_bamboo(drop=("pol",))), BAM_ROWS,
     "without the policy table no reference resolves, and the rows say so rather than guess"),
]
