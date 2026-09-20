#!/usr/bin/env python3
"""Score an archived run set against the plan, the way 06_failure_analysis.md reports it.

    python3 qc/score_run_set.py                       # the set archived on 09/20/2026
    python3 qc/score_run_set.py --set run_set_09-20-2026 --details

Each run's page is read from qc/findings/<set>/<run>_pto_liability.md, exactly as the export
carried it, and its BambooHR end state is rebuilt from the seed tables under apps_data/bamboohr
plus the run's write calls in <run>_bamboohr_writes.json, applied in order with the app's own
results. The 28 planned rows are then read the way the reviewer decision rules in
02_task_metadata.md say the verifier reads them: the hours rows on the balance cell under either
rounding convention, the tier rows on the tier cell with a policy name accepted, the rate rows on
the hourly cell to four decimals, the gate on the stated total, the BambooHR rows on the rebuilt
EmployeePolicy and TimeOffBalance state. The numbers in the record recompute from the archived
bytes on every run of this script and never live in a cell. It also names the registered path
whose schedule the page matches row for row, if any.

This is the plan's reading at the prompt half, not the verifier files: those are generated only
if the set fails, and are tested against a fixture before they are imported.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(PKG, "build"))
import build_package_artifacts as B  # noqa: E402

ROW = re.compile(r"^\|\s*((?:TRT|CTR)-\d{4})\s*\|(.*)\|\s*$")
MONEY = re.compile(r"\$\s?(\d{1,3}(?:,\d{3})*|\d+)\.(\d{2})\b")
HOURS = re.compile(r"(?<![\d.$])(\d{1,3}(?:,\d{3})*|\d+)\.(\d{2})(?![\d.])")


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
    """(rows by id, prose outside the table rows, table header cells, layout). Layout is the
    form row's reading: the count and a dollar figure come before the first employee row, and
    every line from the first employee row to the last is a table line, so one table."""
    rows, prose, header, id_lines = {}, [], None, []
    lines = text.splitlines()
    for n, ln in enumerate(lines):
        m = ROW.match(ln)
        if m:
            cells = [c.strip() for c in m.group(2).split("|")]
            if len(cells) < 6:
                continue
            rows[m.group(1)] = dict(id=m.group(1), raw=cells, tier=_tier(cells[2]), balance=_num(cells[3]),
                                    hourly=_num(cells[4]), liability=_num(cells[5]))
            id_lines.append(n)
        else:
            if ln.startswith("|") and header is None and "---" not in ln:
                header = [c.strip() for c in ln.strip("|").split("|")]
            prose.append(ln)
    layout = False
    if id_lines:
        before = "\n".join(lines[:id_lines[0]])
        between = lines[id_lines[0]:id_lines[-1] + 1]
        layout = (str(len(rows)) in before and bool(MONEY.search(before))
                  and all(l.strip().startswith("|") for l in between if l.strip()))
    return rows, "\n".join(prose), header, layout


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


def verdicts(rows, prose, header, page_meta, pol, bal, layout=False):
    g = B.GOLDEN_BY_ID
    tol_h, tol_r = 0.005, 0.00005

    def bal_ok(i):
        return i in rows and (_same(rows[i]["balance"], g[i]["balance"], tol_h) or
                              _same(rows[i]["balance"], g[i]["balance_posted"], tol_h))

    def rate_ok(i):
        return i in rows and _same(rows[i]["hourly"], g[i]["hourly"], tol_r)

    stated_money = [float(a.replace(",", "") + "." + b) for a, b in MONEY.findall(prose)]
    stated_hours = [float(a.replace(",", "") + "." + b) for a, b in HOURS.findall(prose)]
    row_sum = round(sum(r["liability"] or 0.0 for r in rows.values()), 2)
    hour_sum = round(sum(r["balance"] or 0.0 for r in rows.values()), 2)
    fmt_ok = bool(rows) and all(
        re.fullmatch(r"-?[\d,]+\.\d{2}", r["raw"][3]) and re.fullmatch(r"\$?\s?[\d,]+\.\d{4}", r["raw"][4])
        and re.fullmatch(r"-?\$?\s?[\d,]+\.\d{2}", r["raw"][5]) for r in rows.values())
    total_stated = any(_same(m, row_sum, 0.01) for m in stated_money)
    def bal_in_bamboo(i):
        return i in bal and (_same(bal[i], g[i]["balance"], tol_h) or _same(bal[i], g[i]["balance_posted"], tol_h))

    ended = B.ENDED_IN_BAMBOO + ["TRT-0006"]
    v = {
        1: bool(page_meta) and page_meta.get("published") is True and bool(rows),
        2: set(rows) == set(g),
        3: fmt_ok and total_stated,
        4: bool(rows) and (str(len(rows)) in prose) and any(_same(h, hour_sum, 0.01) for h in stated_hours)
           and total_stated,
        5: bool(rows) and all(r["raw"][0] and r["raw"][1] for r in rows.values()),
        6: bool(rows) and layout,
        7: any(_same(m, B.TOTAL, 0.01) or _same(m, B.TOTAL_POSTED, 0.01) for m in stated_money)
           or _same(row_sum, B.TOTAL, 0.01) or _same(row_sum, B.TOTAL_POSTED, 0.01),
        8: bal_ok("TRT-0005"),
        9: "TRT-0043" in rows and rows["TRT-0043"]["tier"] == 120,
        10: "TRT-0071" in rows and rows["TRT-0071"]["tier"] == 160,
        11: bal_ok("TRT-0018"),
        12: rate_ok("TRT-0088"),
        13: rate_ok("TRT-0117"),
        14: rate_ok("TRT-0096"),
        15: bal_ok("TRT-0141"),
        16: bool(rows) and not any(i.startswith("CTR-") for i in rows),
        17: bool(rows) and ended[0] not in rows,
        18: bool(rows) and ended[1] not in rows,
        19: bool(rows) and ended[2] not in rows,
        20: bool(rows) and ended[3] not in rows,
        21: bal_ok("TRT-0153"),
        22: bal_ok("TRT-0155"),
        23: bal_ok("TRT-0002"),
        24: bal_ok("TRT-0001"),
        25: all(pol.get(i) == B.TIER_POLICY[g[i]["tier"]] for i in B.LOADED_IDS),
        26: all(bal_in_bamboo(i) for i in B.LOADED_IDS),
        27: bal_in_bamboo("TRT-0153"),
        28: bal_in_bamboo("TRT-0155"),
    }
    return v


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
    out = []
    for r in runs:
        p = os.path.join(folder, "%s_pto_liability.md" % r["run"])
        text = open(p, encoding="utf8").read() if os.path.exists(p) else ""
        rows, prose, header, layout = parse_page(text)
        pol, bal, unresolved = bamboo_state(os.path.join(folder, "%s_bamboohr_writes.json" % r["run"]))
        v = verdicts(rows, prose, header, r.get("page"), pol, bal, layout)
        points = sum(weights[n] for n in v if v[n])
        path = matched_path(rows) if rows else None
        row_sum = round(sum(x["liability"] or 0.0 for x in rows.values()), 2)
        if details:
            print("---- %s: %d rows, row sum $%s, path %s, unresolved BambooHR ids %d" % (
                r["run"], len(rows), f"{row_sum:,.2f}", path, unresolved))
            print("     policies on the six: %s" % {i: pol.get(i) for i in B.MIGRATED_WRONG_TIER})
            print("     balances matching the golden: %d of %d" % (
                sum(1 for i in B.GOLDEN_BY_ID if i in bal and (_same(bal[i], B.GOLDEN_BY_ID[i]["balance"], 0.005) or
                                                                _same(bal[i], B.GOLDEN_BY_ID[i]["balance_posted"], 0.005))),
                len(B.GOLDEN_BY_ID)))
        obs = r.get("end_state_observable") or {}
        if obs and not (obs.get("page") and obs.get("bamboohr")):
            print("NOTE %s: end state not fully observable from the export (page %s, bamboohr %s); "
                  "rows read from what was observed, the platform's grading snapshot decides the rest"
                  % (r["run"], obs.get("page"), obs.get("bamboohr")))
        out.append((r, points, v, path, row_sum, len(rows)))
    return out, weights, total


def _render(sched):
    """A page in the memo's shape from a computed schedule, for the self-check."""
    hours = round(sum(r["balance"] for r in sched), 2)
    total = round(sum(r["liability"] for r in sched), 2)
    lines = ["# %s" % B.PAGE, "", "## Summary", "", "- Employees on the schedule: %d" % len(sched),
             "- Total hours: %s" % f"{hours:,.2f}", "- Total dollar liability: $%s" % f"{total:,.2f}", "",
             "| Employee ID | Name | Department | Annual PTO tier | PTO balance at 08/31/2026 | Hourly rate | Liability |",
             "|---|---|---|---|---|---|---|"]
    for r in sched:
        lines.append("| %s | %s | %s | %d | %.2f | %.4f | $%s |" % (
            r["id"], r["name"], r["dept"], r["tier"], r["balance"], r["hourly"], f"{r['liability']:,.2f}"))
    return "\n".join(lines)


def self_check():
    """The scorer's reading of a page agrees with the plan's predicates on every registered path,
    with BambooHR brought to that path's schedule; a planted defect on the golden goes red."""
    weights = {i + 1: r[1] for i, r in enumerate(B.PLAN)}
    for (key, desc, flags), (k2, d2, pts, failed, tot, n) in zip(B.PATHS, B.score_paths()):
        sched = B.schedule(**flags)
        rows, prose, header, layout = parse_page(_render(sched))
        pol = {r["id"]: B.TIER_POLICY[r["tier"]] for r in sched}
        bal = {r["id"]: r["balance"] for r in sched}
        v = verdicts(rows, prose, header, {"published": True}, pol, bal, layout)
        got = sum(weights[i] for i in v if v[i])
        bad = [i for i in sorted(v) if not v[i]]
        assert got == pts and bad == failed, "%s: scorer %d %s vs plan %d %s" % (key, got, bad, pts, failed)
        print("  %s scores %d of %d by both readings, rows failed %s" % (key, pts, sum(weights.values()), failed or "none"))
    gold = B.schedule()
    bent = [dict(r) for r in gold]
    k = [r["id"] for r in bent].index(B.CAPPED_IDS[0])
    bent[k]["balance"] += 1.0
    bent[k]["liability"] = round(bent[k]["balance"] * bent[k]["hourly"], 2)
    rows, prose, header, layout = parse_page(_render(bent))
    v = verdicts(rows, prose, header, {"published": True},
                 {r["id"]: B.TIER_POLICY[r["tier"]] for r in gold}, {r["id"]: r["balance"] for r in gold}, layout)
    assert not v[8] and not v[7], "a capped balance moved by an hour must fail rows 7 and 8"
    print("  control: one capped balance moved by an hour fails rows 7 and 8: RED")
    v = verdicts(rows, prose, header, {"published": False}, {}, {}, layout)
    assert not v[1] and not v[25] and not v[26] and not v[27] and not v[28], "an unpublished page and an untouched BambooHR must fail"
    print("  control: unpublished page, BambooHR untouched, fails rows 1, 25, 26, 27 and 28: RED")
    two = _render(gold) + "\n\n## Contractors\n\n| Employee ID | Name | Department | Annual PTO tier | PTO balance at 08/31/2026 | Hourly rate | Liability |\n|---|---|---|---|---|---|---|\n| CTR-2001 | Henrike Sato | Engineering | 80 | 0.00 | 0.0000 | $0.00 |"
    rows, prose, header, layout = parse_page(two)
    assert not layout, "a second employee table must fail the layout reading"
    print("  control: a second employee table below the first fails row 6: RED")
    print("self-check: the scorer reads the seven registered paths as the plan does")


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
