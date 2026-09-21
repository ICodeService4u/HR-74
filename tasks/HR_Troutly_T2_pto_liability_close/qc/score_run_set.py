#!/usr/bin/env python3
"""Score an archived run set with the generated verifiers, the way 06_failure_analysis.md reports it.

    python3 qc/score_run_set.py                       # the set archived on 09/20/2026
    python3 qc/score_run_set.py --set run_set_09-20-2026 --details

Each run's page is read from qc/findings/<set>/<run>_pto_liability.md, exactly as the export
carried it, and its BambooHR end state is rebuilt from the seed tables under apps_data/bamboohr
plus the run's write calls in <run>_bamboohr_writes.json, applied in order with the app's own
results. Both are loaded into the battery's fixture, the seed pages and BambooHR tables plus the
Greenhouse seed, and every row file under qc/verifiers/ is run against it. So the record's
scores are the verifiers' own verdicts on the archived bytes, never a second reading of the plan;
the plan's predicates are checked against the same verifiers on the seven registered paths by
--self-check. It also names the registered path whose schedule the page matches row for row.
"""
import importlib.util
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(PKG, "build"))
import build_package_artifacts as B  # noqa: E402
import scenarios as S  # noqa: E402

ROW = re.compile(r"^\|\s*((?:TRT|CTR)-\d{4})\s*\|(.*)\|\s*$")


def _num(s):
    s = re.sub(r"[^\d.\-]", "", s or "")
    return float(s) if s not in ("", "-", ".") else None


def _tier(cell):
    c = (cell or "").strip()
    if c in B.POLICY_TIER:
        return B.POLICY_TIER[c]
    n = _num(c)
    return int(n) if n is not None and n in (80, 120, 160) else None


def _same(a, b, tol):
    return a is not None and b is not None and abs(a - b) <= tol


def parse_page(text):
    """The ID-keyed rows of a page, for the record's row count, total and path columns."""
    rows = {}
    for ln in text.splitlines():
        m = ROW.match(ln)
        if m:
            cells = [c.strip() for c in m.group(2).split("|")]
            if len(cells) < 6:
                continue
            rows[m.group(1)] = dict(id=m.group(1), raw=cells, tier=_tier(cells[2]), balance=_num(cells[3]),
                                    hourly=_num(cells[4]), liability=_num(cells[5]))
    return rows


def bamboo_state(writes_file):
    """EmployeePolicy and TimeOffBalance after the run's writes, from the seed plus the calls."""
    pol = {}
    for e in B._csv("bamboohr", "EmployeePolicy.csv"):
        pol.setdefault(e["employee_id"], []).append(e["policy_id"])
    bal = {e["employee_id"]: float(e["balance"]) for e in B._csv("bamboohr", "TimeOffBalance.csv")}
    if not os.path.exists(writes_file):
        return {k: v[-1] for k, v in pol.items() if v}, bal, 0
    w = json.load(open(writes_file, encoding="utf8"))
    ids = dict(w.get("id_to_employee_number") or {})
    unresolved = 0
    for call in w.get("writes") or []:
        tool, a, res = call["tool"], call.get("args") or {}, call.get("result")
        if tool.endswith("employees_create") and isinstance(res, dict) and res.get("id") is not None \
                and a.get("employeeNumber"):
            ids[str(res["id"])] = a["employeeNumber"]
            continue
        emp = ids.get(str(a.get("employeeId")))
        if emp is None:
            if tool.endswith(("assign_policy", "update_balance")):
                unresolved += 1
            continue
        if tool.endswith("assign_policy") and isinstance(res, dict):
            lst = pol.setdefault(emp, [])
            for r in res.get("removed") or []:
                if r.get("policyName") in lst:
                    lst.remove(r["policyName"])
            for r in res.get("assigned") or []:
                lst.append(r["policyName"])
        elif tool.endswith("update_balance"):
            if isinstance(res, dict) and res.get("newBalance") is not None:
                bal[emp] = float(res["newBalance"])
            elif a.get("amount") is not None:
                bal[emp] = bal.get(emp, 0.0) + float(a["amount"])
    return {k: v[-1] for k, v in pol.items() if v}, bal, unresolved


def checks():
    vdir = os.path.join(HERE, "verifiers")
    out = {}
    for f in sorted(os.listdir(vdir)):
        if f.startswith("row") and f.endswith(".py"):
            spec = importlib.util.spec_from_file_location(f[:-3], os.path.join(vdir, f))
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            out[int(f[3:5])] = mod.check
    assert len(out) == len(B.RUBRIC), "%d row files against %d rubric rows" % (len(out), len(B.RUBRIC))
    return out


def verdicts(ctx, rows=None):
    rows = rows or checks()
    return {n: bool(rows[n](ctx).get("passed")) for n in sorted(rows)}


def matched_path(rows):
    """The registered path whose schedule the page equals row for row on id, tier, balance and
    hourly rate, or None."""
    for key, desc, flags in B.PATHS:
        s = {r["id"]: r for r in B.schedule(**flags)}
        if set(s) != set(rows):
            continue
        if all(rows[i]["tier"] == s[i]["tier"] and _same(rows[i]["hourly"], s[i]["hourly"], 0.00005) and
               (_same(rows[i]["balance"], s[i]["balance"], 0.005) or _same(rows[i]["balance"], s[i]["balance_posted"], 0.005))
               for i in s):
            return key
    return None


def score(set_name, details=False):
    folder = os.path.join(HERE, "findings", set_name)
    runs = json.load(open(os.path.join(folder, "runs.json"), encoding="utf8"))
    weights = {i + 1: r[1] for i, r in enumerate(B.PLAN)}
    total = sum(weights.values())
    rowchecks = checks()
    out = []
    for r in runs:
        p = os.path.join(folder, "%s_pto_liability.md" % r["run"])
        text = open(p, encoding="utf8").read() if os.path.exists(p) else ""
        rows = parse_page(text)
        pol, bal, unresolved = bamboo_state(os.path.join(folder, "%s_bamboohr_writes.json" % r["run"]))
        hires = {h: S.HIRES[h] for h in S.HIRES if h in bal}
        published = bool((r.get("page") or {}).get("published"))
        ctx = S.snap([(B.PAGE, text, 1 if published else 0)] if text else [], S.bamboo_tables(pol, bal, hires))
        v = verdicts(ctx, rowchecks)
        points = sum(weights[n] for n in v if v[n])
        path = matched_path(rows) if rows else None
        row_sum = round(sum(x["liability"] or 0.0 for x in rows.values()), 2)
        if details:
            print("---- %s: %d rows, row sum $%s, path %s, unresolved BambooHR ids %d" % (
                r["run"], len(rows), f"{row_sum:,.2f}", path, unresolved))
            print("     policies on the six: %s" % {i: pol.get(i) for i in B.MIGRATED_WRONG_TIER})
        obs = r.get("end_state_observable") or {}
        if obs and not (obs.get("page") and obs.get("bamboohr")):
            print("NOTE %s: end state not fully observable from the export (page %s, bamboohr %s); "
                  "rows read from what was observed, the platform's grading snapshot decides the rest"
                  % (r["run"], obs.get("page"), obs.get("bamboohr")))
        out.append((r, points, v, path, row_sum, len(rows)))
    return out, weights, total


def self_check():
    """The verifiers' reading of each registered path, rendered as a page with BambooHR brought to
    it, agrees with the plan's predicates row for row; and three planted defects go red."""
    weights = {i + 1: r[1] for i, r in enumerate(B.PLAN)}
    rowchecks = checks()
    for (key, desc, flags), (k2, d2, pts, failed, tot, n) in zip(B.PATHS, B.score_paths()):
        page, bamboo = S.path_page(key)
        v = verdicts(S.snap([(B.PAGE, page)], bamboo), rowchecks)
        got = sum(weights[i] for i in v if v[i])
        bad = [i for i in sorted(v) if not v[i]]
        assert got == pts and bad == failed, "%s: verifiers %d %s vs plan %d %s" % (key, got, bad, pts, failed)
        print("  %s scores %d of %d by both readings, rows failed %s" % (key, pts, sum(weights.values()), failed or "none"))
    gold = B.GOLDEN
    bent = [dict(r, balance=r["balance"] + 1.0, liability=round((r["balance"] + 1.0) * r["hourly"], 2)) if r["id"] == B.CAPPED_IDS[0] else r for r in gold]
    v = verdicts(S.snap([(B.PAGE, B.render_page(bent))], S.correct_bamboo()), rowchecks)
    assert not v[15] and not v[14], "a capped balance moved by an hour must fail rows 14 and 15"
    print("  control: one capped balance moved by an hour fails rows 14 and 15: RED")
    v = verdicts(S.snap([(B.PAGE, B.GOLDEN_PAGE, 0)]), rowchecks)
    assert not v[1] and not any(v[i] for i in S.POL_ROWS | S.BAL_ROWS | S.HIRE_ROWS), "an unpublished page and an untouched BambooHR must fail"
    print("  control: unpublished page, BambooHR untouched, fails row 1 and every BambooHR record row: RED")
    v = verdicts(S.snap([(B.PAGE, S.split_tables(B.GOLDEN_PAGE))], S.correct_bamboo()), rowchecks)
    assert not v[13], "a second employee table must fail the layout row"
    print("  control: a second employee table fails row 13: RED")
    print("self-check: the verifiers read the seven registered paths as the plan does")


def main():
    if "--self-check" in sys.argv:
        self_check()
        return 0
    set_name = "run_set_09-20-2026"
    if "--set" in sys.argv:
        set_name = sys.argv[sys.argv.index("--set") + 1]
    out, weights, total = score(set_name, "--details" in sys.argv)
    print("| Run | Model | Tool calls | Assistant turns | Rows | Total it prints | Path | Score | Rows failed |")
    print("|---|---|---|---|---|---|---|---|---|")
    by_model = {}
    for r, points, v, path, row_sum, n in out:
        failed = [k for k in sorted(v) if not v[k]]
        print("| %s | %s | %d | %d | %d | $%s | %s | %d of %d, %.1f%% | %s |" % (
            r["run"], r["model"], r["tool_calls"], r["assistant_messages"], n, f"{row_sum:,.2f}", path or "none",
            points, total, 100.0 * points / total, ", ".join(str(k) for k in failed) or "none"))
        by_model.setdefault(r["model"], []).append(100.0 * points / total)
    print()
    for m, xs in by_model.items():
        print("%s: %d run%s, mean %.1f%%, low %.1f%%, high %.1f%%" % (
            m, len(xs), "" if len(xs) == 1 else "s", sum(xs) / len(xs), min(xs), max(xs)))
    print()
    print("rows failed by run (X fails):")
    tags = [r["run"] for r, _, _, _, _, _ in out]
    print("         " + " ".join("%-4s" % t[:4] for t in tags))
    for k in sorted(weights):
        marks = ["X" if not v[k] else "." for _, _, v, _, _, _ in out]
        if "X" in marks:
            print("row %02d w%-2d %s" % (k, weights[k], "    ".join(marks)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
