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
asks for - every employee beside the five lines, the seven columns T2 asked for, a line per
department beside the joined one, a second table - and each must score every point. Since review
round 1 of 09/22/2026 the lines are what the rows read, so the battery also proves that a line is
read where the page names it and nowhere else: not off an employee row, not off Sales alone.
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
LINE_ROWS = lambda n: {CELL_ROW[("line_hours", n)], CELL_ROW[("line_total", n)]}
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


def line_table(sched, split_sales=False):
    """The five lines as the golden prints them, or with Sales and Marketing as two lines."""
    f = B.line_figures(sched)
    out = ["| Line | PTO hours | PTO liability |", "|---|---|---|"]
    for name, ds in B.LINES:
        if split_sales and len(ds) > 1:
            for d in ds:
                rows = [r for r in sched if r["dept"] == d]
                out.append("| %s | %s | $%s |" % (d, f"{sum(r['balance'] for r in rows):,.2f}",
                                                   f"{sum(r['liability'] for r in rows):,.2f}"))
            continue
        out.append("| %s | %s | $%s |" % (name, f"{f[name][0]:,.2f}", f"{f[name][1]:,.2f}"))
    return out


def wide_page(sched=None):
    """The page a run writes when it prints the whole schedule beside the lines: a summary block,
    a line per department and the joined line, and every current employee in seven columns. It
    must score every point."""
    sched = sched or B.GOLDEN
    hours = round(sum(r["balance"] for r in sched), 2)
    total = round(sum(r["liability"] for r in sched), 2)
    lines = ["# %s" % PAGE, "", "## Summary", "",
             "- Employees on the schedule: %d" % len(sched),
             "- Total PTO hours: %s" % f"{hours:,.2f}",
             "- Total PTO liability: $%s" % f"{total:,.2f}", "", "## By department", ""]
    lines += line_table(sched, split_sales=True)
    f = B.line_figures(sched)
    lines += ["| Sales and Marketing | %s | $%s |" % (f"{f['Sales and Marketing'][0]:,.2f}", f"{f['Sales and Marketing'][1]:,.2f}"), "",
              "## Employees", "",
              "| Employee ID | Name | Department | Annual PTO tier | PTO balance | Hourly rate | Dollar liability |",
              "|---|---|---|---|---|---|---|"]
    for r in sched:
        lines.append("| %s | %s | %s | %d | %.2f | $%.4f | $%s |"
                     % (r["id"], r["name"], r["dept"], r["tier"], r["balance"], r["hourly"],
                        f"{r['liability']:,.2f}"))
    return "\n".join(lines) + "\n"


def prose_page(sched=None):
    """The lines written as prose, one bullet a line, each opening on the line's name."""
    sched = sched or B.GOLDEN
    f = B.line_figures(sched)
    hours = round(sum(r["balance"] for r in sched), 2)
    total = round(sum(r["liability"] for r in sched), 2)
    lines = ["# %s" % PAGE, "", "The total PTO liability is $%s on %s hours." % (f"{total:,.2f}", f"{hours:,.2f}"), ""]
    for name, ds in B.LINES:
        lines.append("- **%s**: %s hours, $%s" % (name.replace(" and ", " & ") if len(ds) > 1 else name,
                                                   f"{f[name][0]:,.2f}", f"{f[name][1]:,.2f}"))
    return "\n".join(lines) + "\n"


def employees_only_page(sched=None):
    """The v2 page as the first version asked for it: totals and every employee, no line."""
    sched = sched or B.GOLDEN
    hours = round(sum(r["balance"] for r in sched), 2)
    total = round(sum(r["liability"] for r in sched), 2)
    lines = ["# %s" % PAGE, "",
             "Total PTO liability at %s: $%s" % (B.ASOF, f"{total:,.2f}"), "",
             "Total PTO hours at %s: %s" % (B.ASOF, f"{hours:,.2f}"), "",
             "| Employee ID | Department | PTO balance in hours | Hourly rate |", "|---|---|---|---|"]
    for r in sched:
        lines.append("| %s | %s | %.2f | $%.4f |" % (r["id"], r["dept"], r["balance"], r["hourly"]))
    return "\n".join(lines) + "\n"


def set_line(page, name, hours=None, money=None):
    """One line's figures replaced, the rest of the page untouched."""
    out = []
    for line in page.split("\n"):
        if line.startswith("| %s |" % name):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if hours is not None:
                cells[1] = hours
            if money is not None:
                cells[2] = money
            line = "| " + " | ".join(cells) + " |"
        out.append(line)
    return "\n".join(out)


def drop_line(page, name):
    return "\n".join(l for l in page.split("\n") if not l.startswith("| %s |" % name))


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


LG = B.LINE_GOLD
ENG_H, ENG_D = CELL_ROW[("line_hours", "Engineering")], CELL_ROW[("line_total", "Engineering")]
SM = LINE_ROWS("Sales and Marketing")
NOT_TOTALS = ALL_ROWS - {PAGE_ROW, TOTAL_ROW, HOURS_ROW}
LOADED_SCHED = [dict(r, balance=B.LOADED[r["id"]][0], hourly=B.LOADED[r["id"]][1],
                     liability=round(B.LOADED[r["id"]][0] * B.LOADED[r["id"]][1], 2),
                     balance_posted=B.LOADED[r["id"]][0],
                     liability_posted=round(B.LOADED[r["id"]][0] * B.LOADED[r["id"]][1], 2))
                for r in B.GOLDEN]

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
    ("every employee, a line per department and a summary block", lambda: snap([(PAGE, wide_page())]), set(),
     "NOTHING grades absence: a run that prints the whole schedule, Sales and Marketing apart and joined, loses not one point"),
    ("the lines as prose bullets, an ampersand for and", lambda: snap([(PAGE, prose_page())]), set(),
     "a line is read where the page names it, in a table or on a line of its own"),
    ("a header with other words",
     lambda: snap([(PAGE, B.render_page(B.GOLDEN, headers=["Department", "Hours", "Dollars"]))]), set(),
     "the lines are found by their names, not by the header's words"),
    ("line labels with a subtotal word",
     lambda: snap([(PAGE, "\n".join(l.replace("| %s |" % n, "| %s subtotal |" % n) if l.startswith("| %s |" % n) else l
                                     for l in GOLD.split("\n") for n in [next((x for x, _ in B.LINES if l.startswith("| %s |" % x)), "")]))]), set(),
     "Engineering subtotal is the Engineering line"),
    ("the totals and lines without a dollar sign or a comma",
     lambda: snap([(PAGE, set_total(GOLD, money="%.2f" % B.TOTAL, hours="%.2f" % B.TOTAL_HOURS).replace("$", "").replace(",", ""))]), set(),
     "the request carries no Form section, so a figure is a figure however it is punctuated"),
    ("the totals and lines rounded to the dollar and the tenth of an hour",
     lambda: snap([(PAGE, "\n".join([l for l in set_total(GOLD, money="$%s" % f"{round(B.TOTAL):,}", hours="%.1f" % B.TOTAL_HOURS).rstrip("\n").split("\n") if not any(l.startswith("| %s |" % n) for n, _ in B.LINES)]
                                     + ["| %s | %.1f | $%s |" % (n, LG[n][0], f"{round(LG[n][1]):,}") for n, _ in B.LINES]))]), set(),
     "with no Form section a response may round what it states, and the bands are wider than any rounding of a right answer"),
    ("the lines under posted rounding",
     lambda: snap([(PAGE, "\n".join([l for l in GOLD.rstrip("\n").split("\n") if not any(l.startswith("| %s |" % n) for n, _ in B.LINES)]
                                     + ["| %s | %s | $%s |" % (n, f"{LG[n][2]:,.2f}", f"{LG[n][3]:,.2f}") for n, _ in B.LINES]))]), set(),
     "each posting rounded is the other reading the totals already accept"),
    ("a second table that carries no line",
     lambda: snap([(PAGE, GOLD + "\n| Source | Read |\n|---|---|\n| Archive | 06/30/2026 |\n")]), set(),
     "v2 grades no layout, so a working table beside the lines costs nothing"),
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
    # ---- where a line is and is not read
    ("Sales and Marketing given only as two lines",
     lambda: snap([(PAGE, "\n".join(B.render_page(B.GOLDEN).split("\n")[:8] + line_table(B.GOLDEN, split_sales=True)[2:]) + "\n")]), SM,
     "the request joins the two departments; Sales alone is not the joined line and neither is a sum the reader does"),
    ("the joined figures labelled Sales alone, in the table",
     lambda: snap([(PAGE, GOLD.replace("| Sales and Marketing |", "| Sales |"))]), SM,
     "a line labelled Sales tells the reader it is Sales without Marketing, whatever figure it carries"),
    ("the joined figures labelled Sales alone, in prose",
     lambda: snap([(PAGE, drop_line(GOLD, "Sales and Marketing") + "\n- Sales: %s hours, $%s\n" % (f"{LG['Sales and Marketing'][0]:,.2f}", f"{LG['Sales and Marketing'][1]:,.2f}"))]), SM,
     "a prose line opens on the line it states, and Sales is not Sales and Marketing"),
    ("the lines left for the reader to add up from the employees",
     lambda: snap([(PAGE, employees_only_page())]), NOT_TOTALS,
     "a department on each employee row is not a stated line"),
    ("an employee row carrying a line's figures",
     lambda: snap([(PAGE, drop_line(GOLD, "Engineering") + "| TRT-0005 | Engineering | %s | $%s |\n" % (f"{LG['Engineering'][0]:,.2f}", f"{LG['Engineering'][1]:,.2f}"))]),
     {ENG_H, ENG_D},
     "a figure inside an employee row is that employee's, whatever else the row names"),
    ("a prose sentence that mentions Sales before the joined figure",
     lambda: snap([(PAGE, drop_line(GOLD, "Sales and Marketing") + "\nSales carried most of the change. Marketing did not move.\n")]), SM,
     "a line is named where the page states it, not wherever a word appears"),
    ("the totals written into the line table as a Total row",
     lambda: snap([(PAGE, "\n".join(l for l in GOLD.split("\n") if not l.startswith("Total PTO")) + "| Total | %s | $%s |\n" % (f"{B.TOTAL_HOURS:,.2f}", f"{B.TOTAL:,.2f}"))]), set(),
     "a total row in a table keyed on no employee is a stated total"),
    ("the totals written into an employee's own row",
     lambda: snap([(PAGE, "\n".join(l for l in GOLD.split("\n") if not l.startswith("Total PTO")) + "\n| Employee ID | Balance | Rate |\n|---|---|---|\n| TRT-0001 | %s | $%s |\n" % (f"{B.TOTAL_HOURS:,.2f}", f"{B.TOTAL:,.2f}"))]),
     {TOTAL_ROW, HOURS_ROW},
     "a figure inside an employee row is that employee's figure; the request asks the page to state the totals"),
    # ---- the skill's menu for a value in text: the asked figure in the asked unit, not a number
    ("the total dollars written as hours, the hours total as a bare number",
     lambda: snap([(PAGE, set_total(GOLD, money="%s hours" % f"{B.TOTAL_HOURS:,.2f}", hours=f"{B.TOTAL:,.2f}"))]), {TOTAL_ROW},
     "a dollar figure in hours is the right number in the wrong unit, and a bare number on an hours line is hours"),
    ("Engineering's hours and dollars swapped between the columns",
     lambda: snap([(PAGE, set_line(GOLD, "Engineering", hours=f"{LG['Engineering'][1]:,.2f}", money="$%s" % f"{LG['Engineering'][0]:,.2f}"))]), {ENG_H, ENG_D},
     "a cell's unit is its own sign or its column's header, so each figure is read in the column it sits in"),
    ("Engineering's dollars written as hours in prose",
     lambda: snap([(PAGE, drop_line(GOLD, "Engineering") + "\nEngineering: %s hours\n" % f"{LG['Engineering'][1]:,.2f}")]), {ENG_H, ENG_D},
     "the number is on the page and is not the asked figure"),
    ("the total struck through beside another figure",
     lambda: snap([(PAGE, set_total(GOLD, money="~~$%s~~ $95,000.00" % f"{B.TOTAL:,.2f}"))]), {TOTAL_ROW},
     "strikethrough is markup, the one retraction a database check reads"),
    ("Engineering's dollars struck through beside another figure",
     lambda: snap([(PAGE, set_line(GOLD, "Engineering", money="~~$%s~~ $40,000.00" % f"{LG['Engineering'][1]:,.2f}"))]), {ENG_D},
     "a struck figure is not stated"),
    ("the total shown with its arithmetic",
     lambda: snap([(PAGE, set_total(GOLD, money="$%s, the load's %s less %s" % (f"{B.TOTAL:,.2f}", B._money(B.LOADED_TOTAL), B._money(round(B.LOADED_TOTAL - B.TOTAL, 2)))))]), set(),
     "a correct run showing its working must not be failed by the other numbers it shows"),
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
    # ---- one figure wrong
    ("Engineering's hours a tenth out",
     lambda: snap([(PAGE, set_line(GOLD, "Engineering", hours="%.2f" % (LG["Engineering"][0] + 0.1)))]), {ENG_H},
     "a twentieth of an hour is the band"),
    ("Engineering's hours two hundredths out",
     lambda: snap([(PAGE, set_line(GOLD, "Engineering", hours="%.2f" % (LG["Engineering"][0] + 0.02)))]), set(),
     "inside the band is the same figure"),
    ("Engineering's dollars a dollar out",
     lambda: snap([(PAGE, set_line(GOLD, "Engineering", money="$%s" % f"{LG['Engineering'][1] + 1.0:,.2f}"))]), {ENG_D},
     "half a dollar is the band; a dollar out is a different figure"),
    ("the Engineering line dropped",
     lambda: snap([(PAGE, drop_line(GOLD, "Engineering"))]), {ENG_H, ENG_D},
     "a missing line is a missing value; the totals are graded as stated, so they stand"),
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
     lambda: snap([(PAGE, B.render_page(LOADED_SCHED))]), ALL_ROWS - {PAGE_ROW},
     "the failure this ask measures: every graded figure is one the load carries wrong, so copying it earns the page and nothing else"),
]
