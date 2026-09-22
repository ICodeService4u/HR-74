"""The battery for T2 v2: wiki snapshots with the answer known, one planted defect per way a row
can be wrong, the registered failing paths and the archived runs as pages.

BATTERY is a list of (label, ctx_factory, failing_rows, why). `failing_rows` is the set of rubric
row numbers the scenario should FAIL, or "all". Every other row must pass. ROWS is the rubric row
count, read from the builder so the two cannot drift.

The fixture is the Wiki.js `pages` table in its documented 21-column order, seeded with the ten
world pages from apps_data/wiki_js/Page.csv, beside the BambooHR and Greenhouse seed tables that
no v2 row reads and every v2 row has to ignore. Column names are placeholders unless a scenario
asks for real ones, which is what a real grading snapshot has been measured to return.

What this battery exists to prove, beyond the verdicts: that NOTHING in the set grades the
absence of content. Half the correct-state scenarios are pages that carry more than the request
asks for - every employee rather than the ones the load has wrong, the columns v2 dropped, a
summary block, a second table - and each must score every point.
"""
import csv
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

# the row numbers, read off the plan so a reweighting cannot leave the battery behind
PAGE_ROW = 1
TOTAL_ROW = next(i for i, r in enumerate(B.PLAN, 1) if r[9]["kind"] == "total")
HOURS_ROW = next(i for i, r in enumerate(B.PLAN, 1) if r[9]["kind"] == "hours")
CELL_ROW = {(r[9]["kind"], r[9]["key"]): i for i, r in enumerate(B.PLAN, 1) if "key" in r[9]}
ALL_ROWS = set(range(1, ROWS + 1))
VALUE_ROWS = set(CELL_ROW.values())


def _csv(app, table):
    with open(os.path.join(REPO, "apps_data", app, table), newline="", encoding="utf8") as fh:
        return list(csv.DictReader(fh))


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


def other_tables():
    """The apps v2 reads and never writes, in the snapshot beside the wiki so a row that wandered
    into them fails here. The BambooHR seed keeps its own column names."""
    out = {}
    for app, table in (("bamboohr", "Employee.csv"), ("bamboohr", "TimeOffBalance.csv"),
                       ("bamboohr", "TimeOffPolicy.csv"), ("greenhouse", "candidates.csv")):
        rows = _csv(app, table)
        cols = list(rows[0].keys()) if rows else ["id"]
        name = "%s_%s" % (app, table[:-4].lower())
        out[name] = (cols, [[r[c] for c in cols] for r in rows])
    return out


def snap(pages=(), real_names=False, cols=PAGES_COLS, history=()):
    tables = dict(wiki_tables(pages, cols, history))
    tables.update(other_tables())
    return Ctx(tables, real_names=real_names)


# ---------------------------------------------------------------- pages a correct run might write
def to_html(md):
    out = ["<h1>%s</h1>" % PAGE]
    for line in md.split("\n")[1:]:
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if all(re.fullmatch(r":?-{2,}:?", c or "--") for c in cells):
                continue
            out.append("<tr>" + "".join("<td>%s</td>" % c for c in cells) + "</tr>")
        elif line.strip():
            out.append("<p>%s</p>" % line.strip())
    return "<table>".join(["\n".join(out[:3]), "\n".join(out[3:]) + "</table>"])


def wide_page(sched=None):
    """The page a run writes when it prints the whole schedule: seven columns, a summary block and
    every current employee, not only the ones the load has wrong. It must score every point."""
    sched = sched or B.GOLDEN
    hours = round(sum(r["balance"] for r in sched), 2)
    total = round(sum(r["liability"] for r in sched), 2)
    lines = ["# %s" % PAGE, "", "## Summary", "",
             "- Employees on the schedule: %d" % len(sched),
             "- Total PTO hours: %s" % f"{hours:,.2f}",
             "- Total PTO liability: $%s" % f"{total:,.2f}", "",
             "| Employee ID | Name | Department | Annual PTO tier | PTO balance | Hourly rate | Dollar liability |",
             "|---|---|---|---|---|---|---|"]
    for r in sched:
        lines.append("| %s | %s | %s | %d | %.2f | $%.4f | $%s |"
                     % (r["id"], r["name"], r["dept"], r["tier"], r["balance"], r["hourly"],
                        f"{r['liability']:,.2f}"))
    return "\n".join(lines) + "\n"


def exceptions_page(sched=None):
    """The page a run writes when it prints only the rows the load has wrong. Also every point."""
    sched = sched or B.GOLDEN
    by = {r["id"]: r for r in sched}
    hours = round(sum(r["balance"] for r in sched), 2)
    total = round(sum(r["liability"] for r in sched), 2)
    lines = ["# %s" % PAGE, "",
             "Total PTO liability at %s: $%s" % (B.ASOF, f"{total:,.2f}"), "",
             "Total PTO hours at %s: %s" % (B.ASOF, f"{hours:,.2f}"), "",
             "| Employee ID | PTO balance in hours | Hourly rate |", "|---|---|---|"]
    for i in B.CELL_IDS:
        if i in by:
            lines.append("| %s | %.2f | $%.4f |" % (i, by[i]["balance"], by[i]["hourly"]))
    return "\n".join(lines) + "\n"


def set_cell(page, key, field, value):
    """One cell of one keyed row replaced, the rest of the page untouched."""
    out = []
    for line in page.split("\n"):
        if line.startswith("| %s " % key):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            cells[1 if field == "balance" else 2] = value
            line = "| " + " | ".join(cells) + " |"
        out.append(line)
    return "\n".join(out)


def drop_row(page, key):
    return "\n".join(l for l in page.split("\n") if not l.startswith("| %s " % key))


def set_total(page, money=None, hours=None):
    out = []
    for line in page.split("\n"):
        if money is not None and line.startswith("Total PTO liability"):
            line = "Total PTO liability at %s: %s" % (B.ASOF, money)
        if hours is not None and line.startswith("Total PTO hours"):
            line = "Total PTO hours at %s: %s" % (B.ASOF, hours)
        out.append(line)
    return "\n".join(out)


def path_page(key):
    return B.render_page(next(B.schedule(**flags) for k, d, flags in B.PATHS if k == key))


def path_fails(key):
    return set(next(fl for k, d, pts, fl, tot, n in B.score_paths() if k == key))


h05 = G["TRT-0005"]
BAL5, RATE88 = CELL_ROW[("balance", "TRT-0005")], CELL_ROW[("rate", "TRT-0088")]

BATTERY = [
    # ---- the correct state, in every shape a right answer can take
    ("the golden page", lambda: snap([(PAGE, GOLD)]), set(),
     "the graded end state - the golden must score 100"),
    ("the golden, real column names", lambda: snap([(PAGE, GOLD)], real_names=True), set(),
     "the other branch - a check must work whether or not the snapshot carries names"),
    ("the golden, the title with an em dash",
     lambda: snap([(PAGE.replace(" - ", " %s " % chr(0x2014)), GOLD)]), set(),
     "the request's dash is a hyphen; a run that types an em dash has still named the page"),
    ("the golden as HTML", lambda: snap([(PAGE, to_html(GOLD))]), set(),
     "a run on the visual editor stores HTML, and a table is still a table"),
    ("every employee, seven columns and a summary block", lambda: snap([(PAGE, wide_page())]), set(),
     "NOTHING grades absence: a run that prints the whole schedule and more columns than the request asks for loses not one point"),
    ("only the rows the load has wrong", lambda: snap([(PAGE, exceptions_page())]), set(),
     "the other end of the same rule: a run that prints only the exceptions carries every graded cell"),
    ("a header with other words",
     lambda: snap([(PAGE, B.render_page(B.GOLDEN, headers=["ID", "Balance 08/31/2026", "Rate ($/hr)"]))]), set(),
     "the request's column names in other words are the same columns"),
    ("a header with no usable words",
     lambda: snap([(PAGE, B.render_page(B.GOLDEN, headers=["A", "B", "C"]))]), set(),
     "three columns keyed on an ID in the first cell read in the request's order"),
    ("the totals without a dollar sign or a comma",
     lambda: snap([(PAGE, set_total(GOLD, money="%.2f" % B.TOTAL, hours="%.2f" % B.TOTAL_HOURS))]), set(),
     "the request carries no Form section, so a total is a total however it is punctuated"),
    ("the totals rounded to the dollar and the tenth of an hour",
     lambda: snap([(PAGE, set_total(GOLD, money="$%s" % f"{round(B.TOTAL):,}", hours="%.1f" % B.TOTAL_HOURS))]), set(),
     "with no Form section a response may round what it states, and the bands are wider than any rounding of a right answer"),
    ("a second table that carries no employee row",
     lambda: snap([(PAGE, GOLD + "\n| Source | Read |\n|---|---|\n| Archive | 06/30/2026 |\n")]), set(),
     "v2 grades no layout, so a working table beside the schedule costs nothing"),
    # ---- nothing, or the wrong page
    ("the seed: no page", lambda: snap(history=[(PAGE, GOLD)]), "all",
     "a check that reads history instead of pages passes a run that did nothing"),
    ("the page saved unpublished", lambda: snap([(PAGE, GOLD, 0)]), {PAGE_ROW},
     "a draft is not a published page; the content rows still read the content"),
    ("the page under a different title", lambda: snap([("PTO Liability August 2026", GOLD)]), "all",
     "a title that drops the date is a different page; the request fixes the title"),
    ("a snapshot with 20 page columns", lambda: snap([(PAGE, GOLD)], cols=PAGES_COLS[:-1]), {PAGE_ROW},
     "a shape the documented layout does not validate reads the content but cannot show publication"),
    ("a second page with the same title, both correct",
     lambda: snap([(PAGE, GOLD), (PAGE, GOLD)]), "all",
     "the request asks for one page published under the title; two correct copies are two pages"),
    ("a note page carrying the title in its description, real column names",
     lambda: snap([(PAGE, GOLD), ("PTO Liability Notes", "# Notes\n\nThe schedule is the other page.", 1, PAGE)],
                  real_names=True), set(),
     "a description is not a title, so the one page under the title is the schedule"),
    ("a note row naming an employee, above the rows it notes",
     lambda: snap([(PAGE, GOLD.replace("|---|---|---|\n",
                                       "|---|---|---|\n| Subtotal before TRT-0005 was capped, TRT-0001 to TRT-0155 | 500.00 | $40.0000 |\n", 1))]),
     set(),
     "a key is a whole cell: a note that names an employee, and sits before that employee's own row, must not be read as it"),
    ("an employee row keyed with a note beside the ID",
     lambda: snap([(PAGE, set_cell(GOLD, "TRT-0005", "balance", "%.2f" % h05["balance"]).replace(
         "| TRT-0005 |", "| TRT-0005 (capped) |"))]), set(),
     "the ID with a parenthetical beside it is still that employee's row, and the engine says so"),
    ("the totals written into an employee's own row",
     lambda: snap([(PAGE, "\n".join(l for l in GOLD.split("\n") if not l.startswith("Total PTO")).replace(
         "| TRT-0001 | 22.87 | $103.3654 |",
         "| TRT-0001 | %s | $%s |" % (f"{B.TOTAL_HOURS:,.2f}", f"{B.TOTAL:,.2f}")))]),
     {TOTAL_ROW, HOURS_ROW, CELL_ROW[("balance", "TRT-0005")]} - {CELL_ROW[("balance", "TRT-0005")]},
     "a figure inside an employee row is that employee's figure; the request asks the page to state the totals"),
    # ---- the registered paths
    ("P0 as a page: the July method rolled forward", lambda: snap([(PAGE, path_page("P0"))]), path_fails("P0"),
     "the July close's own method, every rule missed"),
    ("P1 as a page: the report copied, the population fixed", lambda: snap([(PAGE, path_page("P1"))]), path_fails("P1"),
     "the modal failure measured on 09/20/2026 and 09/21/2026"),
    ("P2 as a page: the cap applied and nothing else", lambda: snap([(PAGE, path_page("P2"))]), path_fails("P2"),
     "the cap alone"),
    ("P3 as a page", lambda: snap([(PAGE, path_page("P3"))]), path_fails("P3"),
     "the archive's dates unbridged and untimed, the rates as loaded"),
    ("P4 as a page", lambda: snap([(PAGE, path_page("P4"))]), path_fails("P4"),
     "the signed rates found, the bridge and the timing missed"),
    ("P5 as a page", lambda: snap([(PAGE, path_page("P5"))]), path_fails("P5"),
     "everything but the step and the part-time schedule"),
    # ---- one cell wrong
    ("Hosana's balance one hundredth under",
     lambda: snap([(PAGE, set_cell(GOLD, "TRT-0005", "balance", "%.2f" % (h05["balance"] - 0.01)))]), {BAL5},
     "a stated balance is graded to the hundredth; the totals are graded as stated, so they stand"),
    ("Hosana's balance a thousandth under",
     lambda: snap([(PAGE, set_cell(GOLD, "TRT-0005", "balance", "%.3f" % (h05["balance"] - 0.001)))]), set(),
     "the band is half a hundredth, so a third decimal inside it is the same number"),
    ("Hosana's row dropped",
     lambda: snap([(PAGE, drop_row(GOLD, "TRT-0005"))]), {BAL5},
     "a missing row is a missing value; the request asks for the totals to be stated, not reconciled"),
    ("Featherstone at the loaded rate",
     lambda: snap([(PAGE, set_cell(GOLD, "TRT-0088", "rate", "$%.4f" % B.LOADED["TRT-0088"][1]))]), {RATE88},
     "the rate the load carries is the one the signed approval replaced"),
    ("the total stated a dollar out",
     lambda: snap([(PAGE, set_total(GOLD, money="$%s" % f"{B.TOTAL + 1.0:,.2f}"))]), {TOTAL_ROW},
     "half a dollar is the band; a dollar out is a different total"),
    ("the hours total stated a tenth out",
     lambda: snap([(PAGE, set_total(GOLD, hours="%.2f" % (B.TOTAL_HOURS + 0.1)))]), {HOURS_ROW},
     "a twentieth of an hour is the band"),
    ("neither total stated",
     lambda: snap([(PAGE, "\n".join(l for l in GOLD.split("\n") if not l.startswith("Total PTO")))]),
     {TOTAL_ROW, HOURS_ROW},
     "the request asks the page to state both totals, and a sum the reader has to do is not a stated total"),
    ("the load copied whole: the report's balances and the loaded rates",
     lambda: snap([(PAGE, B.render_page([dict(r, balance=B.LOADED[r["id"]][0], hourly=B.LOADED[r["id"]][1],
                                              liability=round(B.LOADED[r["id"]][0] * B.LOADED[r["id"]][1], 2))
                                         for r in B.GOLDEN]))]),
     ALL_ROWS - {PAGE_ROW},
     "the failure this ask measures: every graded cell is a cell the load carries wrong, so copying it earns the page and nothing else"),
]
