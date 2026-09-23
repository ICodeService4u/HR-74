#!/usr/bin/env python3
"""Score an archived run set with the generated verifiers, the way 06_failure_analysis.md reports it.

    python3 qc/score_run_set.py                       # the set archived on 09/21/2026
    python3 qc/score_run_set.py --set run_set_09-20-2026 --details
    python3 qc/score_run_set.py --self-check          # the registered paths, by the plan and by the code
    python3 qc/score_run_set.py --set run_set_09-20-2026 --as-lines   # each run's own rows summed onto the lines

Each run's page is read from qc/findings/<set>/<run>_pto_liability.md, exactly as the export
carried it, loaded into the battery's fixture and read by every row file under qc/verifiers/. So
the record's scores are the verifiers' own verdicts on the archived bytes, never a second reading
of the plan. v2 grades one page, so nothing here rebuilds an app's write state.

`run_set_09-23-2026` is v2's own, the first trajectory against this memo, archived 09/23/2026; its
page states the five lines, so it is read as printed and `--as-lines` adds nothing to it.
The two earlier sets are T2's, scored under T2's own rubric on 09/20/2026 and 09/21/2026.
They are carried into v2 because the pages they hold are the same deliverable in kind, a row per
employee with a balance and an hourly rate beside it, so they measure what v2's rubric does to a
response that copies the load. Their own record stays in the T2 package.

Since review round 1 of 09/22/2026 the request asks for five department lines and no employee
row, and these pages were written to the earlier ask, so they carry no line and the plain score
reads 1 point each by construction. `--as-lines` is the fair reading: each run's own employee
rows, read by the engine's own row reader, summed by department onto the request's five lines
and written back onto the page, so the verifiers score what the run computed and not what it
was asked to print.
"""
import importlib.util
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
os.environ["T2_VERIFIER_QUIET"] = "1"
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(PKG, "build"))
import build_package_artifacts as B  # noqa: E402
import scenarios as S  # noqa: E402

DEFAULT_SET = "run_set_09-21-2026"


def checks():
    out = {}
    vdir = os.path.join(HERE, "verifiers")
    for f in sorted(os.listdir(vdir)):
        if not (f.startswith("row") and f.endswith(".py")):
            continue
        n = int(f[3:5])
        spec = importlib.util.spec_from_file_location(f[:-3], os.path.join(vdir, f))
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        m.QUIET = True
        out[n] = m.check
    assert len(out) == len(B.PLAN), "%d row files against %d planned rows" % (len(out), len(B.PLAN))
    return out


def verdicts(ctx, rowchecks):
    return {n: bool(rowchecks[n](ctx).get("passed")) for n in sorted(rowchecks)}


def weights():
    return {i + 1: r[1] for i, r in enumerate(B.PLAN)}


AS_LINES = "--as-lines" in sys.argv


def _employee_rows(text):
    """{ID: (balance, hourly)} off every table whose header names a balance and a rate, keyed by
    a whole-cell employee ID. The engine reads no employee row, so this reader lives here, with
    the one reading that needs it."""
    out, header = {}, None
    for line in text.split("\n"):
        if line.count("|") < 2:
            header = None
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c or "--") for c in cells):
            continue
        if header is None:
            header = [c.lower() for c in cells]
            continue
        bi = next((i for i, h in enumerate(header) if "balance" in h), None)
        ri = next((i for i, h in enumerate(header) if "rate" in h), None)
        key = next((c.upper() for c in cells if re.fullmatch(r"trt-\d{4}", c.strip().lower())), None)
        if key and bi is not None and ri is not None and max(bi, ri) < len(cells):
            try:
                out.setdefault(key, (float(re.sub(r"[^\d.]", "", cells[bi])), float(re.sub(r"[^\d.]", "", cells[ri]))))
            except ValueError:
                pass
    return out


def with_lines(text):
    """The page with a line table appended, each line the sum of the run's own employee rows: its
    balance, and its balance times its hourly rate, by the department the roster gives the ID."""
    sums = {name: [0.0, 0.0] for name, ds in B.LINES}
    for k, (bal, rate) in _employee_rows(text).items():
        if k in B.GOLDEN_BY_ID:
            line = B.LINE_OF[B.GOLDEN_BY_ID[k]["dept"]]
            sums[line][0] += bal
            sums[line][1] += round(bal * rate, 2)
    rows = ["", "| Line | PTO hours | PTO liability |", "|---|---|---|"]
    rows += ["| %s | %.2f | $%.2f |" % (n, sums[n][0], sums[n][1]) for n, ds in B.LINES]
    return text.rstrip("\n") + "\n" + "\n".join(rows) + "\n"


def score(set_name, details=False):
    folder = os.path.join(HERE, "findings", set_name)
    runs = json.load(open(os.path.join(folder, "runs.json"), encoding="utf8"))
    rowchecks, w = checks(), weights()
    out = []
    for r in runs:
        path = os.path.join(folder, "%s_pto_liability.md" % r["run"])
        text = open(path, encoding="utf8").read() if os.path.exists(path) else ""
        published = bool((r.get("page") or {}).get("published"))
        if text and AS_LINES:
            text = with_lines(text)
        ctx = S.snap([(B.PAGE, text, 1 if published else 0)] if text else [])
        v = verdicts(ctx, rowchecks)
        pts = sum(w[n] for n in v if v[n])
        stated = re.findall(r"\$\s?([\d,]+\.\d{2})", text)
        out.append((r, pts, v, stated[0] if stated else "-"))
    return out, w, sum(w.values())


def self_check():
    """The verifiers' reading of each registered path, rendered as a page, agrees with the plan's
    predicates row for row, and three planted defects go red."""
    w, rowchecks = weights(), checks()
    for (key, desc, flags), (k2, d2, pts, failed, tot, n) in zip(B.PATHS, B.score_paths()):
        page = B.render_page(B.schedule(**flags))
        v = verdicts(S.snap([(B.PAGE, page)]), rowchecks)
        got = sum(w[i] for i in v if v[i])
        bad = [i for i in sorted(v) if not v[i]]
        assert got == pts and bad == failed, "%s: verifiers %d %s vs plan %d %s" % (key, got, bad, pts, failed)
        print("  %s scores %d of %d by both readings, rows failed %s" % (key, pts, sum(w.values()), failed or "none"))
    v = verdicts(S.snap([(B.PAGE, B.GOLDEN_PAGE, 0)]), rowchecks)
    assert not v[1], "an unpublished page must fail the page row"
    print("  control: the golden saved unpublished fails row 1: RED")
    bent = B.render_page([dict(r, balance=r["balance"] + 1.0) if r["id"] == "TRT-0005" else r for r in B.GOLDEN])
    v = verdicts(S.snap([(B.PAGE, bent)]), rowchecks)
    assert not v[S.CELL_ROW[("line_hours", "Engineering")]], "a capped balance moved by an hour must fail its line"
    print("  control: one Engineering balance moved by an hour fails the Engineering hours line: RED")
    v = verdicts(S.snap([(B.PAGE, S.wide_page())]), rowchecks)
    assert all(v.values()), "a page that prints every employee and every department must score every point"
    print("  control: every employee and Sales and Marketing apart beside the joined line still score every point: GREEN by design")
    # --as-lines on a page of employee rows alone must rebuild the golden's lines to the cent
    rows_only = "\n".join(l for l in S.wide_page().split("\n") if not any(
        l.startswith("| %s |" % n) for n in list(B.LINE_OF) + [x for x, _ in B.LINES]))
    v = verdicts(S.snap([(B.PAGE, with_lines(rows_only))]), rowchecks)
    assert all(v.values()), "the golden's own rows summed onto the lines must score every point: %r" % [n for n in v if not v[n]]
    v = verdicts(S.snap([(B.PAGE, rows_only)]), rowchecks)
    assert not any(v[n] for n in v if B.PLAN[n - 1][9]["kind"] in ("line_hours", "line_total")), "a page of employee rows alone states no line"
    print("  control: the golden's employee rows summed onto the lines score every point, unsummed none of the lines: RED and GREEN as planned")
    print("self-check: the verifiers read the seven registered paths as the plan does")


def main():
    if "--self-check" in sys.argv:
        self_check()
        return 0
    set_name = DEFAULT_SET
    if "--set" in sys.argv:
        set_name = sys.argv[sys.argv.index("--set") + 1]
    out, w, total = score(set_name, "--details" in sys.argv)
    print("| Run | Model | Total it prints | Score | Rows passed |")
    print("|---|---|---|---|---|")
    scores = []
    for r, pts, v, stated in out:
        passed = [n for n in sorted(v) if v[n]]
        scores.append(100.0 * pts / total)
        print("| %s | %s | $%s | %d of %d, %.1f%% | %s |"
              % (r["run"], r["model"], stated, pts, total, 100.0 * pts / total,
                 ", ".join(str(n) for n in passed) or "none"))
    print("\n%s: %d runs, mean %.1f%%, low %.1f%%, high %.1f%%"
          % (out[0][0]["model"], len(out), sum(scores) / len(scores), min(scores), max(scores)))
    if "--details" in sys.argv:
        print("\nrows failed by run:")
        names = [r["run"] for r, _, _, _ in out]
        print("         " + "  ".join("%-4s" % n for n in names))
        for n in sorted(out[0][2]):
            line = "  ".join("%-4s" % ("." if v[n] else "X") for _, _, v, _ in out)
            print("row %02d w%-2d %s" % (n, w[n], line))
    return 0


if __name__ == "__main__":
    sys.exit(main())
