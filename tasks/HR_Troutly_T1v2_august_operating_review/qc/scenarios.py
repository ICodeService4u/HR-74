"""The battery for T1 v2: wiki snapshots with the answer known, one planted defect per way a
row can be wrong, the three registered failing paths as pages, plus the legitimate forms a
correct run might use.

BATTERY is a list of (label, ctx_factory, failing_rows, why). `failing_rows` is the set of rubric
row numbers the scenario should FAIL, or "all". Every other row must pass. ROWS is the rubric row
count, read from the builder so the two cannot drift.

The fixture is the Wiki.js `pages` table in its documented 21-column order, seeded with the ten
world pages from apps_data/wiki_js/Page.csv. A `pageHistory` table carries copies so a check
that reads history instead of pages is caught. Column names are placeholders unless a scenario
asks for real ones, which is what a real grading snapshot has been measured to return.
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
A, Bt = B.PAGE_A, B.PAGE_B
GOLD_A, GOLD_B = B.GOLDEN[A], B.GOLDEN[Bt]

PAGES_COLS = ["id", "path", "hash", "title", "description", "isPrivate", "isPublished",
              "privateNS", "publishStartDate", "publishEndDate", "content", "render", "toc",
              "contentType", "createdAt", "updatedAt", "editorKey", "localeCode", "authorId",
              "creatorId", "extra"]
HIST_COLS = ["id", "pageId", "path", "hash", "title", "description", "isPrivate", "isPublished",
             "publishStartDate", "publishEndDate", "action", "content", "contentType",
             "createdAt", "versionDate", "localeCode", "authorId"]


def _seed():
    with open(os.path.join(REPO, "apps_data", "wiki_js", "Page.csv"), newline="",
              encoding="utf8") as fh:
        return list(csv.DictReader(fh))


def _slug(title):
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def _row(i, title, content, published=1, path=None):
    return [i, path or _slug(title), "h%d" % i, title, "", 0, published, None, None, None,
            content, "<p>rendered</p>", "[]", "markdown", "2026-08-31 09:00:00",
            "2026-08-31 09:00:00", "markdown", "en", 5, 5, "{}"]


def snap(pages=(), real_names=False, cols=PAGES_COLS, history=()):
    """A snapshot: the seed pages plus `pages`, a list of (title, content[, published])."""
    rows = []
    for i, p in enumerate(_seed(), 1):
        rows.append(_row(i, p["title"], p["content"], 1 if p["isPublished"] == "true" else 0,
                         p["path"]))
    for n, spec in enumerate(pages, 11):
        title, content = spec[0], spec[1]
        pub = spec[2] if len(spec) > 2 else 1
        rows.append(_row(n, title, content, pub))
    rows = [r[:len(cols)] for r in rows]
    hist = [[n, 99, _slug(t), "h", t, "", 0, 1, None, None, "updated", c, "markdown",
             "2026-08-31 09:00:00", "2026-08-31 09:00:00", "en", 5]
            for n, (t, c) in enumerate(history, 1)]
    users = [[5, "casey@troutlyanalytics.com", "Casey Ouk"]]
    return Ctx({"pages": (cols, rows), "pageHistory": (HIST_COLS, hist),
                "users": (["id", "email", "name"], users)}, real_names=real_names)


# ---------------------------------------------------------------- markdown editing helpers
def set_cell(md, key, column, value):
    """Replace one cell: the row whose any cell equals `key`, in the column headed `column`."""
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
            if key in cells and any(column.lower() in h for h in header):
                i = next(i for i, h in enumerate(header) if column.lower() in h)
                cells[i] = value
                out.append("| " + " | ".join(cells) + " |")
                continue
        else:
            header = None
        out.append(line)
    assert out != md.split("\n"), "set_cell changed nothing for %r" % key
    return "\n".join(out)


def drop_row(md, key):
    out = [l for l in md.split("\n") if not (l.count("|") >= 2 and key in
                                             [c.strip() for c in l.strip().strip("|").split("|")])]
    assert len(out) < len(md.split("\n")), "drop_row removed nothing for %r" % key
    return "\n".join(out)


def add_row(md, heading, row):
    """Append a table row under the section whose heading contains `heading`."""
    lines = md.split("\n")
    start = next(i for i, l in enumerate(lines) if l.startswith("## ") and heading in l)
    end = start + 1
    while end < len(lines) and not lines[end].startswith("## "):
        end += 1
    last = max(i for i in range(start, end) if lines[i].count("|") >= 2)
    lines.insert(last + 1, "| " + " | ".join(row) + " |")
    return "\n".join(lines)


def replace(md, old, new):
    assert old in md, "replace found nothing for %r" % old[:50]
    return md.replace(old, new)


def to_html(md):
    out = []
    in_table = False
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


# ---------------------------------------------------------------- the failing paths, as pages
def bamboo_path(contractors_in=True, drop_ids=()):
    """The staffed page from BambooHR's active rows: whole (P1), less the contractors (P1b), or
    less the contractors and TRT-0064 (P1c), the two unloaded hires out on every path. The
    summary states what the tables carry, so the count rows read a page that agrees with itself."""
    names = {e["employee_number"]: (e["first_name"] + " " + e["last_name"], e)
             for e in B.BAMBOO}
    rows = []
    for e in B.BAMBOO_ACTIVE:
        if not contractors_in and e["employee_number"].startswith("CTR-"):
            continue
        if e["employee_number"] in drop_ids:
            continue
        mgr = names[e["supervisor_id"]][0] if e["supervisor_id"] else "None"
        req = B.OPEN_TITLES.get(e["job_title"], "None")
        rows.append((e["employee_number"], e["first_name"] + " " + e["last_name"],
                     e["department"], e["job_title"], mgr, req))
    with_req = [r for r in rows if r[5] != "None"]
    without = [r for r in rows if r[5] == "None"]
    by_dept = {d: sum(1 for r in rows if r[2] == d) for d in B.DEPT_ORDER}
    L = ["# %s" % Bt, "", "## Summary", "",
         "- %d current employees at 08/31/2026: %s." % (
             len(rows), ", ".join("%s %d" % (d, by_dept[d]) for d in B.DEPT_ORDER)),
         "- %d hold a role with an open requisition. %d do not." % (len(with_req), len(without)),
         ""]
    hdr = ["| Employee ID | Name | Department | Role | Manager | Open requisition |",
           "|---|---|---|---|---|---|"]
    for title, rs in (("Staffed roles with an open requisition", with_req),
                      ("Staffed roles with no open requisition", without)):
        L += ["## %s" % title, ""] + hdr + ["| " + " | ".join(r) + " |" for r in rs] + [""]
    return "\n".join(L)


def bamboo_whole():
    return bamboo_path(contractors_in=True)


def emptied(md):
    """The staffed page with its summary intact and every table row gone."""
    return "\n".join(l for l in md.split("\n")
                     if not (l.count("|") >= 2 and re.match(r"\|\s*[A-Z]{3}-\d{4}\s*\|", l)))


def thinned(md, keep=5):
    """The staffed page with its summary intact and only the first `keep` employee rows left, so
    the tables still parse as tables and every absence check has a populated table to read."""
    out, seen = [], 0
    for l in md.split("\n"):
        if l.count("|") >= 2 and re.match(r"\|\s*[A-Z]{3}-\d{4}\s*\|", l):
            seen += 1
            if seen > keep:
                continue
        out.append(l)
    return "\n".join(out)


CSM_TABLE = "Staffed roles with an open requisition"
NONE_TABLE = "Staffed roles with no open requisition"
A_ROWS = set(range(1, 10)) | {23}
B_ROWS = set(range(10, 23))
POP_ROWS = set(range(11, 23))

BATTERY = [
    ("the golden pages", lambda: snap([(A, GOLD_A), (Bt, GOLD_B)]), set(),
     "the graded end state - the golden must score 100"),
    ("the golden pages, real column names", lambda: snap([(A, GOLD_A), (Bt, GOLD_B)], real_names=True),
     set(), "the other branch - a check must work whether or not the snapshot carries names"),
    ("the golden pages, titles with an em dash",
     lambda: snap([(A.replace(" - ", " %s " % chr(0x2014)), GOLD_A),
                   (Bt.replace(" - ", " %s " % chr(0x2014)), GOLD_B)]),
     set(), "the prompt's dash is a hyphen; a run that types an em dash has still named the page"),
    ("the golden pages as HTML", lambda: snap([(A, to_html(GOLD_A)), (Bt, to_html(GOLD_B))]),
     set(), "a run on the visual editor stores HTML, and a table is still a table"),
    ("a wider header on the approval column",
     lambda: snap([(A, GOLD_A.replace("| Board approval |", "| Board Approval Status |")),
                   (Bt, GOLD_B)]),
     set(), "the memo's column name with a word added is the same column"),
    ("a requisition keyed with a note beside it",
     lambda: snap([(A, GOLD_A.replace("| REQ-2026-036 |", "| REQ-2026-036 (backfill) |")), (Bt, GOLD_B)]),
     set(), "a run that prints a note in parentheses beside the ID has still keyed the row on it; "
            "T1's G5 lost four rows to the same form on 09/19/2026"),
    ("the tables right, the summary in a bulleted list",
     lambda: snap([(A, GOLD_A), (Bt, replace(GOLD_B, "- 52 current employees at 08/31/2026: "
                                             "Engineering 19, Product 4, Sales 8, Marketing 5, "
                                             "Customer Success 11, Finance and Corporate 5.",
                                             "- 52 current employees at 08/31/2026.\n- Engineering: 19\n"
                                             "- Product: 4\n- Sales: 8\n- Marketing: 5\n"
                                             "- Customer Success: 11\n- Finance and Corporate: 5"))]),
     set(), "four of T1's nine runs put the count by department in a list or a table under the "
            "summary heading; a bulleted list is prose and states the figures"),
    ("nothing written, the golden only in page history",
     lambda: snap(history=[(A, GOLD_A), (Bt, GOLD_B)]), "all",
     "the seed state - a check that reads history instead of pages passes a run that did nothing"),
    ("only the hiring page published", lambda: snap([(A, GOLD_A)]),
     B_ROWS | {24}, "the second page missing fails every row on it and the two-page form row"),
    ("both pages saved unpublished", lambda: snap([(A, GOLD_A, 0), (Bt, GOLD_B, 0)]),
     {1, 10}, "a draft is not a published page; the content rows still read the content"),
    ("the hiring page under a different title",
     lambda: snap([("Approved Hiring View August 2026", GOLD_A), (Bt, GOLD_B)]),
     A_ROWS | {24}, "a title that drops the dash is a different page; the request fixes the title"),
    ("a snapshot with 20 columns", lambda: snap([(A, GOLD_A), (Bt, GOLD_B)], cols=PAGES_COLS[:-1]),
     {1, 10}, "a shape the documented layout does not validate reads the content but cannot show "
              "publication, and the exists rows take the false zero on purpose"),
    ("REQ-2026-036 marked Approved",
     lambda: snap([(A, set_cell(GOLD_A, "REQ-2026-036", "Board approval", "Approved")), (Bt, GOLD_B)]),
     {3}, "the determination the package exists for"),
    ("REQ-2026-036 marked Approved (conditional backfill)",
     lambda: snap([(A, set_cell(GOLD_A, "REQ-2026-036", "Board approval",
                                "Approved (conditional backfill)")), (Bt, GOLD_B)]),
     {3}, "Approved with a qualifier is still not Not approved"),
    ("the wiki page's eight roles read as the Board plan",
     lambda: snap([(A, replace(set_cell(set_cell(set_cell(GOLD_A, "REQ-2026-036", "Board approval", "Approved"),
                                                 "REQ-2026-037", "Board approval", "Approved"),
                                        "REQ-2026-038", "Board approval", "Approved"),
                               "annualized budget of $612,000.00", "annualized budget of $868,000.00")),
                   (Bt, GOLD_B)]),
     {3, 4, 5, 8}, "the second failing path: the Hiring Plan page says Board approved on 06/20/2026 "
                   "over eight roles at $868,000.00, and a run that reads no further marks all eight"),
    ("REQ-2026-031 marked Not approved",
     lambda: snap([(A, set_cell(GOLD_A, "REQ-2026-031", "Board approval", "Not approved")), (Bt, GOLD_B)]),
     {2}, "an approved line marked the other way, and Approved must not substring-match it"),
    ("Yes and No in the approval column",
     lambda: snap([(A, GOLD_A.replace("| Not approved |", "| No |").replace("| Approved |", "| Yes |")),
                   (Bt, GOLD_B)]),
     {2, 3, 4, 5, 23}, "a vocabulary the request does not allow"),
    ("REQ-2026-038 marked Open",
     lambda: snap([(A, set_cell(GOLD_A, "REQ-2026-038", "Hiring status", "Open")), (Bt, GOLD_B)]),
     {7}, "an accepted offer reported as open, which the memo's definition of Open rules out"),
    ("the plan workbook's budget stated as authorized",
     lambda: snap([(A, replace(GOLD_A, "annualized budget of $612,000.00",
                               "annualized budget of $868,000.00")), (Bt, GOLD_B)]),
     {8}, "the wiki page's figure carried into the summary"),
    ("three of five reported filled",
     lambda: snap([(A, replace(GOLD_A, "All 5 approved roles are open and unfilled at 08/31/2026. "
                               "0 of 5 are filled. No offer is out on any of them.",
                               "3 of the 5 approved roles are filled.")), (Bt, GOLD_B)]),
     {9}, "the summary contradicting the table"),
    ("P1: the staffed page from BambooHR taken whole",
     lambda: snap([(A, GOLD_A), (Bt, bamboo_whole())]),
     POP_ROWS, "the registered modal failing path - 57 rows, contractors and ended records in, "
               "the two unloaded hires out; every population row fails"),
    ("P1b: BambooHR less the contractors",
     lambda: snap([(A, GOLD_A), (Bt, bamboo_path(contractors_in=False))]),
     POP_ROWS - {17, 20}, "the visible class excluded and nothing else; the contractor row passes, and "
     "53 less the 22 matched titles is 31, so the no-requisition split passes by arithmetic"),
    ("P1c: BambooHR less the contractors and TRT-0064",
     lambda: snap([(A, GOLD_A), (Bt, bamboo_path(contractors_in=False, drop_ids=("TRT-0064",)))]),
     {11, 12, 13, 15, 16, 18, 21, 22}, "52 rows by arithmetic with three wrong people on them: the "
     "gate reads the set and fails, the two split rows pass on the coincidence, the invisible "
     "two stay on the tables"),
    ("the tables right, the summary saying 57",
     lambda: snap([(A, GOLD_A), (Bt, replace(GOLD_B, "- 52 current employees at 08/31/2026:",
                                             "- 57 current employees at 08/31/2026:"))]),
     {11}, "a count the summary contradicts is not stated; the department line stands on its own"),
    ("the staffed tables emptied",
     lambda: snap([(A, GOLD_A), (Bt, emptied(GOLD_B))]),
     POP_ROWS, "a page with the summary and no rows: a table with no rows is no table to the parser, "
               "so every population row fails on the missing table"),
    ("the staffed tables thinned to five rows",
     lambda: snap([(A, GOLD_A), (Bt, thinned(GOLD_B))]),
     POP_ROWS, "five rows are a table, and absence from five rows shows nothing: the absence rows "
               "fail on the populated-table floor, which is the guard the emptied page cannot reach"),
    ("the contractors added to the second table",
     lambda: snap([(A, GOLD_A), (Bt, add_row(add_row(GOLD_B, NONE_TABLE,
                   ["CTR-2001", "Henrike Sato", "Engineering", "Contract Data Engineer", "Jessica Ko", "None"]),
                   NONE_TABLE, ["CTR-2003", "Ines Farahani-Boyd", "Product", "Contract Product Designer",
                                "Sora Jackson", "None"]))]),
     {11, 17, 18, 20}, "contractors counted as employees, and every count that includes them"),
    ("TRT-0064 listed as a current employee",
     lambda: snap([(A, GOLD_A), (Bt, add_row(GOLD_B, CSM_TABLE,
                   ["TRT-0064", "Marguerite Delacroix-Hahn", "Customer Success",
                    "Customer Success Manager", "Edith Bustamante", "REQ-2026-034"]))]),
     {11, 14, 18, 19}, "an ended record still read as Active"),
    ("the tables right, the summary reduced to the total",
     lambda: snap([(A, GOLD_A), (Bt, replace(GOLD_B, GOLD_B.split("## Reconciliation summary")[1]
                                             .split("## Staffed roles")[0],
                                             "\n\n- 52 current employees at 08/31/2026.\n\n"))]),
     {18}, "the count by department is asked in the summary; nothing else on the page is"),
    ("the two staffed tables merged into one",
     lambda: snap([(A, GOLD_A), (Bt, replace(GOLD_B, "\n## %s\n\n| Employee ID | Name | Department | "
                                             "Role | Manager | Open requisition |\n|---|---|---|---|---|---|\n"
                                             % NONE_TABLE, ""))]),
     {20}, "the request asks for the no-requisition employees in a table of their own"),
    ("Okonkwo's manager as the Head of People",
     lambda: snap([(A, GOLD_A), (Bt, set_cell(GOLD_B, "TRT-0153", "Manager", "Anjelina Brocollini"))]),
     {21}, "the org chart hangs her under the Customer Success Lead"),
    ("Okonkwo placed in Sales",
     lambda: snap([(A, GOLD_A), (Bt, set_cell(GOLD_B, "TRT-0153", "Department", "Sales"))]),
     {12, 18}, "a department cell decides the presence row and the count by department"),
    ("an ISO date on the hiring page",
     lambda: snap([(A, replace(GOLD_A, "start 09/08/2026", "start 2026-09-08")), (Bt, GOLD_B)]),
     {24}, "the form the request sets"),
    ("another record's key mentioned in a cell's free text",
     lambda: snap([(A, set_cell(GOLD_A, "REQ-2026-036", "Basis",
                                "Opened at CSM II. The Board backfill line is CSM I, beside REQ-2026-034")),
                   (Bt, set_cell(GOLD_B, "TRT-0088", "Role",
                                 "Customer Success Manager, covering the TRT-0064 book"))]),
     set(), "a key is a whole cell, never a substring: the mention must neither resolve the "
     "other requisition to this row nor put the ended employee back on the table"),
    ("a subtotal row naming an ID range",
     lambda: snap([(A, GOLD_A), (Bt, add_row(GOLD_B, NONE_TABLE,
                   ["Engineering subtotal, TRT-0002 to TRT-0128", "19", "Engineering", "", "", "None"]))]),
     set(), "a row keyed on no whole ID is not an employee, and a count that searches for an ID "
     "inside a cell counts it"),
    ("a second page with the same title carrying the wrong reading",
     lambda: snap([(A, GOLD_A), (A, set_cell(GOLD_A, "REQ-2026-036", "Board approval", "Approved")),
                   (Bt, GOLD_B)]),
     {3}, "a wrong duplicate leaves the wiki wrong; every row under the title has to satisfy"),
]
