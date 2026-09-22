#!/usr/bin/env python3
"""Write 07_paste_guide.md: the paste, row by row, from the same rows that wrote the import.

    python3 qc/write_paste_guide.py            # writes ../07_paste_guide.md
    python3 qc/write_paste_guide.py --table    # prints the one-line-per-row table as well

Every field the code-verifier form carries, per row, in the HR 79 playbook's order: Target app,
Check type, Expected Content, Target Table, Target Record ID, Target Record Label, Fallback
Strategy, Additional Notes, then the Tags and Reference Artifacts the import does not populate,
the row file to paste, and the verdict and last details line the per-verifier test-run should
report on the untouched task, measured here by running the row file against the seed fixture.
The builder's check_docs() holds the file on disk to the plan; nothing in it is typed by hand.
"""
import importlib.util
import os
import sys

# the engine prints its notes so a graded run on the platform shows them; here the verdicts
# are what is read, and every row over every snapshot would bury them
os.environ["T2_VERIFIER_QUIET"] = "1"

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(PKG, "build"))
import build_package_artifacts as B  # noqa: E402
import scenarios as S  # noqa: E402

GUIDE = os.path.join(PKG, "07_paste_guide.md")
# the two rows to paste first: the page row, which proves the route, and the gate, which proves
# the reader that every other row leans on
FIRST = [1, next(i for i, r in enumerate(B.PLAN, 1) if r[9]["kind"] == "total")]


def _name(i):
    if i in B.GOLDEN_BY_ID:
        return B.GOLDEN_BY_ID[i]["name"]
    b = B.BAMBOO[i]
    return b["first_name"] + " " + b["last_name"]


def expected_content(spec):
    """The Expected Content field per row, from the spec the builder wrote. A kind the builder
    does not write is a defect and raises here."""
    k = spec["kind"]
    if k == "exists":
        return "one pages row titled %s with isPublished true" % B.PAGE
    if k == "total":
        return "%s, or %s under posted rounding, within %s" % (
            B._money(spec["expected"][0]), B._money(spec["expected"][1]), B.TOL_TOTAL_MONEY)
    if k == "hours":
        return "%s hours, or %s under posted rounding, within %s" % (
            f"{spec['expected'][0]:,.2f}", f"{spec['expected'][1]:,.2f}", B.TOL_TOTAL_HOURS)
    if k == "balance":
        a, b = spec["expected"]
        if abs(a - b) < B.TOL_CELL:
            return "%.2f hours under either rounding, within %s" % (a, B.TOL_CELL)
        return "%.2f hours, or %.2f under posted rounding, within %s" % (a, b, B.TOL_CELL)
    if k == "rate":
        return "%s within %s" % (B._rate(spec["expected"][0]), B.TOL_CELL)
    if k == "line_hours":
        return "%s hours on the %s line, or %s under posted rounding, within %s" % (
            f"{spec['expected'][0]:,.2f}", spec["key"], f"{spec['expected'][1]:,.2f}", B.TOL_LINE_HOURS)
    if k == "line_total":
        return "%s on the %s line, or %s under posted rounding, within %s" % (
            B._money(spec["expected"][0]), spec["key"], B._money(spec["expected"][1]), B.TOL_LINE_MONEY)
    raise KeyError(k)


def target_table(spec):
    if spec["target"] == "wiki":
        return "pages, the documented Wiki.js table"
    if spec["kind"] in ("policy", "policies"):
        return "the employee policy assignment table, found by its references into the employee and policy tables"
    return "the time-off balance table, found by its references into the employee and policy tables"


def record_label(spec):
    k = spec["kind"]
    if spec["target"] == "wiki" and k in ("line_hours", "line_total"):
        return "the %s line on %s" % (spec["key"], B.PAGE)
    if spec["target"] == "wiki" and "key" in spec:
        return "%s, %s" % (_name(spec["key"]), spec["key"])
    if spec["target"] == "wiki" and k == "absent":
        return "%s, %s, ended" % (_name(spec["keys"][0]), spec["keys"][0])
    if spec["target"] == "wiki" and k == "no_contractor":
        return "CTR-2001 to CTR-2004"
    if spec["target"] == "wiki":
        return B.PAGE
    if "key" in spec:
        return "%s, %s" % (_name(spec["key"]), spec["key"])
    return "%d loaded records the schedule leaves as loaded" % len(spec["expected"])


def record_id(spec):
    if spec["kind"] in ("line_hours", "line_total"):
        return B.PAGE
    if "key" in spec:
        return spec["key"]
    if "keys" in spec:
        return ", ".join(spec["keys"])
    if spec["target"] == "wiki":
        return B.PAGE
    return ", ".join(sorted(spec["expected"]))


def picker_refs(refs):
    out = []
    for r in refs:
        a = B.artifact(r)
        out.append("%s (%s)" % (a[0], a[1]) if a else "%s (app table, not in the picker)" % r)
    return out


def seed_verdicts():
    """Every row file against the untouched task: the seed pages and BambooHR tables, with the
    Greenhouse seed tables beside them as the third app's, which no row reads."""
    ctx = S.snap(history=[(S.PAGE, S.GOLD)])
    vdir = os.path.join(HERE, "verifiers")
    out = {}
    for f in sorted(os.listdir(vdir)):
        if f.startswith("row") and f.endswith(".py"):
            spec = importlib.util.spec_from_file_location(f[:-3], os.path.join(vdir, f))
            m = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(m)
            r = m.check(ctx)
            out[int(f[3:5])] = (bool(r["passed"]), r["details"].strip().splitlines()[-1], f)
    return out


def rows():
    verdicts = seed_verdicts()
    out = []
    for i, (fam, wt, gate, crit, pred, typ, primary, expl, refs, spec) in enumerate(B.PLAN, 1):
        passed, last, fname = verdicts[i]
        out.append(dict(i=i, crit=crit, weight=wt, typ=typ, primary=primary, app=B.TARGET_APP[spec["target"]],
                        check=B.form_check_type(spec), content=expected_content(spec), table=target_table(spec),
                        record=record_id(spec), label=record_label(spec), tag=B.import_tag(crit),
                        refs=picker_refs(refs), file="qc/verifiers/" + fname,
                        verdict="PASSED" if passed else "FAILED", last=last))
    return out


def table(rs):
    lines = ["| # | Wt | Target app | Check type | Target Record ID | Expected Content | Test-run on the untouched task |",
             "|---|---|---|---|---|---|---|"]
    for r in rs:
        rec = r["record"] if len(r["record"]) <= 40 else r["record"][:37] + "..."
        lines.append("| %d | %d | %s | %s | %s | %s | %s |" % (r["i"], r["weight"], r["app"], r["check"], rec, r["content"], r["verdict"]))
    return "\n".join(lines)


def guide(rs):
    md5 = B.md5(B.IMPORT)
    head = """# 07 - the paste, row by row (T2 v2, 09/22/2026)

The rubric import registers criteria, explanations, weights and criterion types and nothing else,
measured by task round 1. Everything below is what the interface still needs per row, generated
from the same rows that wrote `05_rubric_import.xlsx` (md5 `%s`, %d rows, %d points) by
`qc/write_paste_guide.py`, so a rebuild rewrites it and `check_docs()` holds it to the plan.

## The procedure

1. **Load the import** and count the rows Studio holds against %d. Read the import toast: a value
   outside a control's list is dropped with a warning, not an error.
2. **Structured view, per row**: set Tags and Reference Artifacts from the row's block below. The
   picker lists world files under `filesystem/` and the upload as `filesystem/pto_liability_request.pdf`;
   the app tables a block names are for the record and are not in the picker.
3. **Code verifier form, per row**: set Target app, Check type, Expected Content, Target Table,
   Target Record ID, Target Record Label and Fallback Strategy **DB only** from the block, leave
   Additional Notes empty, and paste the row file whole into the code box. Every row file is the
   engine with the row's SPEC on top, %d to %d lines; if the box balks at the size, say so and the
   builder stamps only the half a row uses. **Target database apps on a wiki row is `wiki_js_mcp`**,
   the service whose tools every archived run called, `wiki_js_mcp_wikijs_mcp_create_page` among
   them, and the picker offers Wiki.js and Wiki.js MCP as two entries. The 09/21/2026 paste took
   Wiki.js and every wiki row read fail on a page the app had returned under the exact title.
   Two causes fit that equally, the service and a ctx without `has_table`, and the row's own
   details line separates them: `no pages table in this snapshot` is the service, an
   `AttributeError` on `has_table` is a row file older than round 6. Select both services until
   a grading names the one that holds the pages table.
4. **Run the per-verifier test-run on the untouched task** and compare with the block's expected
   verdict and last `details` line. %d of %d rows fail on the untouched task by design, every one
   on no page under the title. A row that passes there, or fails on anything else, is a defect to
   read before the next row is pasted.
5. **Paste rows %s first.** Row 1 proves the route to the pages table and the gate proves the
   reader every other row leans on. Their `details` name every table and column the code resolved
   and the route it took, which is the measurement open item 3 in `02_task_metadata.md` owes, so
   copy those lines into the record.
6. If the form offers a dropdown for Target Table, pick the table the block names and record the
   names the dropdown lists; they are the live shape the fixture could not measure.

## One line per row

%s

## The rows

""" % (md5, len(rs), B.PLAN_TOTAL, len(rs), min(_lines(r["file"]) for r in rs), max(_lines(r["file"]) for r in rs),
       sum(1 for r in rs if r["verdict"] == "FAILED"), len(rs), " and ".join(str(n) for n in FIRST), table(rs))
    blocks = []
    for r in rs:
        blocks.append("""### Row %d, weight %d, %s%s

%s

| Field | Value |
|---|---|
| Target app | `%s` |
| Check type | %s |
| Expected Content | %s |
| Target Table | %s |
| Target Record ID | %s |
| Target Record Label | %s |
| Fallback Strategy | **DB only** |
| Additional Notes | empty, the code is pasted |
| Tags | %s |
| Reference Artifacts | %s |
| Code | `%s`, the whole file |
| Test-run on the untouched task | **%s**, last line `%s` |
""" % (r["i"], r["weight"], "Expert Assessment, primary" if r["primary"] == "Yes" else "Objective Compliance",
       ", paste first" if r["i"] in FIRST else "", r["crit"], r["app"], r["check"], r["content"], r["table"],
       r["record"], r["label"], r["tag"], "; ".join(r["refs"]), r["file"], r["verdict"], r["last"]))
    return head + "\n".join(blocks)


def _lines(rel):
    return sum(1 for _ in open(os.path.join(PKG, rel), encoding="utf8"))


def main():
    rs = rows()
    assert all(r["verdict"] == "FAILED" and "no page titled" in r["last"] for r in rs), \
        "a row does not fail the untouched task on the missing page: %r" % [(r["i"], r["last"]) for r in rs if r["verdict"] != "FAILED" or "no page titled" not in r["last"]]
    text = guide(rs)
    assert all(ord(c) < 128 for c in text), "the paste guide is not ASCII"
    open(GUIDE, "w", encoding="utf8", newline="\n").write(text)
    print("paste guide: %d rows, %d pass on the untouched task, %s" % (
        len(rs), sum(1 for r in rs if r["verdict"] == "PASSED"), os.path.basename(GUIDE)))
    if "--table" in sys.argv:
        print(table(rs))


if __name__ == "__main__":
    main()
