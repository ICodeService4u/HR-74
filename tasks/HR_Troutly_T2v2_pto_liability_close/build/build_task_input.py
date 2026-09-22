#!/usr/bin/env python3
"""Render the task input file, under machine-checked leak, answer-shape and seat guards.

One file ships through the task UI's 1.4) Additional task files:

  * ../00_task_input_operating_review_request.pdf - the recruiting lead's request to the agent's
    People Operations seat, the block between MEMO:BEGIN and MEMO:END in task_input_source.md.
    Target Filesystem, the one vehicle HR 79 measured delivering (7 of 7, then 5 of 5). It
    uploads as operating_review_request.pdf, the local name minus the sorting prefix.

The guards at the bottom are the machine-checkable half of the constraints in the source file's
header. The memo must not name any source record, page or chart, nor carry the current employee count,
a department count, the number of approved roles, either budget, any requisition level, any word
for a record being stale, ended, missing or reconciled, the word contractor, any of the six names
the determination turns on, any word for a document being superseded, any word for checking or
correcting, or the shape of the answer. T1's first run set measured what the pointers were worth:
nine of nine runs followed them. HR 32's T21 measured what one leaked sentence is worth: 97.9% with it, 30.6% without.
The seat assertions are the other half: the memo runs TO the People Operations Analyst and FROM
the Talent Acquisition Specialist.

The render is a pure function of its source: fixed in-world timestamps, a pinned trailer /ID and
office-software producer strings, so the published md5 reproduces on every build.
"""
import hashlib
import os
import re
import sys

from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (HRFlowable, Paragraph, SimpleDocTemplate, Spacer, Table,
                                TableStyle)

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)

COMPANY = "Troutly Analytics, Inc."
PREFIX = "00_task_input_"
UPLOAD_NAME = "pto_liability_request.pdf"

DOCS = {
    "memo": dict(
        src=os.path.join(HERE, "task_input_source.md"),
        markers=("<!-- MEMO:BEGIN -->", "<!-- MEMO:END -->"),
        final=os.path.join(PKG, PREFIX + UPLOAD_NAME),
        doc_id="MEMO-FIN-2026-0901-01",
        title="August close - PTO liability at 08/31/2026",
        author="Krystale Jumawan",
        subject="Internal memorandum - Finance",
        created="D:20260901083012-05'00'",
        modified="D:20260901084427-05'00'",
        pages=2,
        banner="INTERNAL MEMORANDUM",
    ),
}


# ---------------------------------------------------------------- source handling
def doc_text(key):
    """The document block, pulled from the markdown source so the two cannot drift."""
    d = DOCS[key]
    md = open(d["src"], encoding="utf8").read()
    begin, end = d["markers"]
    return md.split(begin)[1].split(end)[0]


def blocks(key):
    for raw in re.split(r"\n\s*\n", doc_text(key).strip()):
        raw = raw.strip()
        if raw:
            yield raw


def table_rows(block):
    rows = []
    for line in block.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if all(c and set(c) <= set("- ") for c in cells):
            continue
        rows.append(cells)
    return rows


def head_rows(block):
    return [(r[0].strip("*"), r[1]) for r in table_rows(block) if len(r) == 2 and r[0]]


def is_head_table(block):
    rows = table_rows(block)
    return bool(rows) and all(len(r) == 2 for r in rows) and rows[0] == ["", ""]


def esc(text):
    text = text.replace("&", "&amp;")
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)


# ---------------------------------------------------------------- rendering
def build(key):
    d = DOCS[key]
    out = d["final"] + ".building"
    base = getSampleStyleSheet()["BodyText"]
    body = ParagraphStyle("body", parent=base, fontName="Times-Roman",
                          fontSize=10, leading=12.1, spaceAfter=5)
    org = ParagraphStyle("org", parent=body, fontName="Times-Bold", fontSize=13,
                         leading=16, alignment=TA_CENTER, spaceAfter=2)
    unit = ParagraphStyle("unit", parent=body, fontSize=10, alignment=TA_CENTER,
                          spaceAfter=10)
    title = ParagraphStyle("title", parent=body, fontName="Times-Bold",
                           fontSize=11, alignment=TA_CENTER, spaceAfter=10)
    head = ParagraphStyle("head", parent=body, fontName="Times-Bold",
                          fontSize=10, spaceBefore=3, spaceAfter=4)

    flow = []
    for block in blocks(key):
        if block.startswith("## "):
            flow.append(Paragraph(esc(block[3:]), org))
        elif block.startswith("### "):
            flow.append(Paragraph(esc(block[4:]), unit if len(flow) == 1 else head))
        elif block.startswith("**%s**" % d["banner"]):
            flow.append(Paragraph(d["banner"], title))
        elif block.startswith("|") and is_head_table(block):
            rows = [[Paragraph("<b>%s:</b>" % esc(k), body), Paragraph(esc(v), body)]
                    for k, v in head_rows(block)]
            tbl = Table(rows, colWidths=[0.85 * inch, 5.75 * inch])
            tbl.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                                     ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                                     ("TOPPADDING", (0, 0), (-1, -1), 3),
                                     ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
            flow += [tbl, Spacer(1, 6)]
        elif set(block) <= set("- "):
            flow.append(HRFlowable(width="100%", thickness=0.5, spaceAfter=12))
        else:
            flow.append(Paragraph(esc(" ".join(block.split())), body))

    SimpleDocTemplate(out, pagesize=LETTER,
                      topMargin=0.55 * inch, bottomMargin=0.55 * inch,
                      leftMargin=0.9 * inch, rightMargin=0.9 * inch,
                      title=d["title"], author=COMPANY).build(flow)
    stamp_metadata(key, out)
    return out


def stamp_metadata(key, out):
    """Replace the library-default document metadata with in-world values, so the file reads as
    a document exported from office software on the day it is dated rather than a pipeline
    render. The title carries the subject line's words and nothing the body withholds."""
    d = DOCS[key]
    try:
        import pikepdf
        with pikepdf.open(out, allow_overwriting_input=True) as pdf:
            assert len(pdf.pages) <= d["pages"], \
                "%s runs to %d pages, over its %d" % (key, len(pdf.pages), d["pages"])
            info = pdf.docinfo
            info["/Title"] = d["title"]
            info["/Author"] = d["author"]
            info["/Subject"] = d["subject"]
            info["/Creator"] = "Microsoft(R) Word for Microsoft 365"
            info["/Producer"] = "Microsoft(R) Word for Microsoft 365"
            info["/CreationDate"] = d["created"]
            info["/ModDate"] = d["modified"]
            pdf.save(out, deterministic_id=True)
    except ImportError:
        from pypdf import PdfReader, PdfWriter
        reader = PdfReader(out)
        assert len(reader.pages) <= d["pages"], \
            "%s runs to %d pages, over its %d" % (key, len(reader.pages), d["pages"])
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        writer.add_metadata({
            "/Title": d["title"], "/Author": d["author"], "/Subject": d["subject"],
            "/Creator": "Microsoft(R) Word for Microsoft 365",
            "/Producer": "Microsoft(R) Word for Microsoft 365",
            "/CreationDate": d["created"], "/ModDate": d["modified"],
        })
        with open(out, "wb") as fh:
            writer.write(fh)
    fix_trailer_id(key, out)
    raw = open(out, "rb").read()
    assert b"ReportLab" not in raw, "library producer string survived in %s" % key
    assert b"pypdf" not in raw and b"pikepdf" not in raw, "library name survived in %s" % key
    for stamp in (d["created"], d["modified"]):
        assert stamp.split("-")[0].encode() in raw, "in-world timestamp missing in %s" % key


def fix_trailer_id(key, out):
    """Pin the trailer /ID so each render is a pure function of its source."""
    ids = (hashlib.md5(DOCS[key]["doc_id"].encode()).hexdigest(),
           hashlib.md5(COMPANY.encode()).hexdigest())
    raw = open(out, "rb").read()
    fixed = ("/ID [<%s><%s>]" % ids).encode()
    raw, n = re.subn(rb"/ID ?\[ ?<[0-9a-fA-F]{32}> ?<[0-9a-fA-F]{32}> ?\]", fixed, raw)
    assert n == 1, "expected exactly one trailer /ID in %s, found %d" % (key, n)
    open(out, "wb").write(raw)
    assert fixed in open(out, "rb").read(), "trailer /ID not pinned in %s" % key


# ---------------------------------------------------------------- guards
MONTHS = ("january", "february", "march", "april", "may", "june", "july",
          "august", "september", "october", "november", "december")
DATE_RE = re.compile(r"\b(?:%s)\s+\d{1,2}(?!\d)(?:,\s*\d{4})?|\b\d{1,2}/\d{1,2}/\d{2,4}" % "|".join(MONTHS))
META_WORDS = ("rubric", "verifier", "golden", "trajectory", "autoqc", "spec 1", "spec 2",
              "task input", "world file", "canonical", "trap")


def flat(key):
    return " ".join(doc_text(key).split()).lower()


def banned_in(low, terms, label):
    for term in terms:
        assert term not in low, "%s leaks withheld material: %r" % (label, term)


def shape_in(low, terms, label):
    for term in terms:
        assert not re.search(r"\b%s\b" % re.escape(term), low), \
            "%s sketches the shape of the answer: %r" % (label, term)


def dates_in(low, allowed, label):
    dates = set(DATE_RE.findall(low))
    assert dates <= allowed, "%s carries an unlicensed date-shaped token: %r" % (label, dates - allowed)


def required_in(low, terms, label):
    for term in terms:
        assert term in low, "%s lost required content: %r" % (label, term)


def check_memo():
    """The request supplies the ask, the page title, the two totals, the five department lines and
    what a current employee is. Review round 1 of 09/22/2026 took the row per current employee and
    the measurement-date sentence out: 156 values no 25-criterion rubric covers, and an ask the
    title already carries. It carries no summary count, no name, department,
    tier or liability column, no BambooHR instruction and no Form section: v2 of 09/22/2026 took
    each of them out because each was an explicit ask that drew a rubric row the failing tier
    earned in full, and the builder bars every one from returning. It carries no fence either:
    task round 3 of 09/20/2026 took the out-of-scope block out, HR 79 T1's round 9 remedy, because
    a fence graded is a fence argued every round and a fence unguarded is a finding every round.
    Task round 4 took the deadline heading and the retention line out the same way. It
    names the July detail it replaces and no rule: the cutover memo, the cap, the accrual period,
    the tiers, the service dates, the rehire rule, the part-time rule, the signed changes and the
    step are the world's to state and the response's to find."""
    low = flat("memo")
    banned_in(low, (
        # every policy document, page and record the determination turns on
        "cutover", "policy memo", "2025 policy", "policy document", "time off policy", "handbook", "paid time off page",
        "time off page", "wiki page", "archive", "roster", "crosswalk", "field mapping", "load file",
        "migration", "migrated", "snapshot", "system of record", "hris report",
        "time off report", "offer letter", "promotion", "amendment", "schedule change",
        "compensation authority", "onboarding data", "procedures memo", "register",
        # the rules
        "carryover", "carry over", "forfeit", "biweekly", "bi-weekly", "semi-monthly",
        "monthly", "per pay period", "pay period", "divided by", "2,080", "2080", "accru",
        "anniversar", "service date", "adjusted service", "years of service", "tenure", "rehire",
        "re-hire", "bridg", "part-time", "part time", "pro-rata", "pro rata", "prorat",
        "scheduled hours", "hours per week", "step increase", "signed", "countersign",
        "effective date", "supersed", "govern", "prevail", "outrank", "80 hours", "120 hours",
        "160 hours", "two years", "five years", "2 years", "5 years", "under 2", "5 plus",
        "2 to 5",
        # every word for a record being stale, wrong, loaded, ended or missing
        "wrong", "incorrect", "error", "defect", "mistake", "loaded", "terminat",
        "ended", "departed", "departure", "resign", "left the company", "missing", "unloaded",
        "never loaded", "not loaded", "no record", "not in bamboohr", "no matching",
        "contractor", "ctr-", "active record", "bamboohr active", "still active",
        # the eight names the determination turns on, and the ended employees
        "featherstone", "luk", "burkenham", "thornbury", "quintanilla", "marchetti", "okonkwo",
        "ibarra", "athanasoulis", "perevalov", "delacroix", "trt-0",
        # every figure a run could print
        "92,739", "92,772", "1,522", "1522", "90,862", "119,758", "111,455", "$", "hours/year",
        # every word for checking, confirming, correcting, resolving or governing
        "check", "verif", "confirm", "audit", "double", "correct", "adjust", "modif", "amend",
        "revise", "recompute", "true up", "true-up", "resolve", "settle", "decide", "determine",
        "which one", "which is right", "control", "authoritative", "yield", "trust", "reliable",
        "up to date", "out of date", "behind", "drift", "reconcil", "tie out", "tie-out",
        # a fence: work put out of scope asks for nothing and draws a finding every round
        "no part of this request", "not part of this request", "out of scope", "out-of-scope",
        "change nothing", "do not change", "do not touch", "leave alone", "greenhouse",
        # a deadline or a filing instruction: neither is a property of app state, and each drew a finding
        "need by", "needed by", "deadline", "no later than", "due by", "due on", "retain", "file with",
        "keep with", "attach to the close",
    ) + META_WORDS, "the memo")
    shape_in(low, (
        "whether", "if any", "if either", "if neither", "only", "except", "unless", "instead",
        "rather than", "either", "neither", "whichever", "differ", "different", "discrepan",
        "disagree", "conflict", "contradict", "override", "overrides", "at all",
        "does not", "do not", "may not", "cannot", "must not", "should not", "actually",
        "really", "properly", "in fact", "the right", "the true", "the real", "assume",
        "assumption", "presum", "in case", "just in case", "one way or the other",
        "no longer", "any more", "as loaded", "as recorded", "on file", "stale", "26", "cap", "capped", "step", "import",
    ), "the memo")
    dates_in(low, {"08/31/2026", "09/01/2026", "09/04/2026"}, "the memo")
    header = next(b for b in blocks("memo") if b.startswith("|"))
    rows = head_rows(header)
    assert ("To", "Casey Ouk, People Operations Analyst") in rows, \
        "To row must address the agent's People Operations seat"
    assert ("From", "Krystale Jumawan, Finance Manager") in rows, \
        "From row must be the Finance Manager, not the agent"
    assert ("Cc", "Anjelina Brocollini, Head of People") in rows, "Cc row drifted"
    required_in(low, (
        "casey ouk, people operations analyst", "krystale jumawan, finance manager",
        DOCS["memo"]["doc_id"].lower(), "08/31/2026",
        "one page published in wiki.js, pto liability - 08/31/2026",
        "the page states the total pto liability in dollars and the total pto hours, and the pto "
        "hours and the pto liability in dollars for each of five lines, customer success, "
        "engineering, finance and corporate, product, and sales and marketing",
        "the figures cover every current employee",
        "a current employee is anyone employed by troutly on 08/31/2026",
    ), "the memo")
    # v2 asks for the determination and nothing beside it: every line T2 carried that drew a
    # rubric row the failing tier earned in full is barred from returning, as the fence, the
    # deadline and the retention line are.
    banned_in(low, (
        "name, department", "annual pto tier", "dollar liability,", "a short summary",
        "the summary states", "bamboohr", "dates mm/dd/yyyy", "two decimals", "four decimals",
        "to the cent", "the total is the sum of the rows", "an employee id on every row",
        # review round 1 of 09/22/2026: the per-employee table and the measurement-date sentence,
        # 156 values no 25-criterion rubric covers and an ask the title already carries
        "a row for every", "row for each", "employee id", "hourly rate", "balance in hours",
        "measurement date", "per employee", "each employee", "every employee",
    ), "the memo")

def check_names():
    """The crossing between the repo and the 1.4 uploader. A shipped input's uploaded name is
    its local name minus the sorting prefix, and the memo cites no file by name, so the only
    thing to hold is that the local name strips to the name the record publishes."""
    local = os.path.basename(DOCS["memo"]["final"])
    assert local.startswith(PREFIX), "%s does not carry the repo sorting prefix" % local
    # The record is the source file's own header table, which names the shipped file. A guard
    # that compared the name to the constant it was built from compared a thing to itself.
    header = open(DOCS["memo"]["src"], encoding="utf8").read().split("<!-- MEMO:BEGIN -->")[0]
    assert "`%s`" % local in header, \
        "the built file is %r, but the record publishes a different name" % local
    assert UPLOAD_NAME.lower() not in flat("memo"), \
        "the memo cites its own file by name, which nothing measured says lands under it"


def check():
    check_memo()
    check_names()


# ---------------------------------------------------------------- promotion
def promote(key, built):
    final = DOCS[key]["final"]
    os.replace(built, final)
    print("md5 %s  %s  (%d bytes)" % (hashlib.md5(open(final, "rb").read()).hexdigest(),
                                      os.path.basename(final), os.path.getsize(final)))


def discard():
    for d in DOCS.values():
        tmp = d["final"] + ".building"
        if os.path.exists(tmp):
            os.remove(tmp)


if __name__ == "__main__":
    try:
        check()
        built = {k: build(k) for k in DOCS}
    except Exception:
        discard()
        raise
    for k, b in built.items():
        promote(k, b)
