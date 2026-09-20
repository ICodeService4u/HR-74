#!/usr/bin/env python3
"""Archive a trajectory export under qc/findings/<set>/ the way score_run_set.py reads it.

    python3 qc/archive_run_set.py --set run_set_09-20-2026 G1=/path/G1.json G3=/path/G3.json

Only the output is graded, so the archiver reads what the apps hold at the end of the run and not
what the run said or which tool it used. A run reaches the apps two ways: the toolbelt tools, and
the shell, calling the same MCP servers directly. Both are read.

The page: every observation of a page under the exact title, in call order - a toolbelt
create_page or update_page that succeeded (content from the call), a toolbelt get_page result
(content as the app returned it), a shell-route create or update whose content is a literal in
the command, and a shell-route get_page whose result the run printed. The archived page is the
LAST observation that carries content, written as <run>_pto_liability.md, and runs.json records
the route and whether a later shell write left the page unobserved.

BambooHR: every write - employees_create, employees_update, time_off_assign_policy,
time_off_update_balance, create_policy, import_csv, clear_database, reset_state - through the
toolbelt or through the shell as call_tool('bamboo_...', {...}) with a literal argument dict,
each with the result the app returned, paired in order. They are written to
<run>_bamboohr_writes.json with a map from BambooHR's numeric id to the employee number, read
off the directory, get and create results. A shell write whose arguments are not a literal is
recorded as unparsed and flagged: the end state is then not fully observable from the export and
the record says so.

runs.json carries one row per run with the model, trajectory id, tool-call count, assistant
message count, shell-call count, elapsed seconds, both snapshot ids, the verifier set the export
carries and the flags above, every value read off the export and none typed. The prompt is
asserted to be the builder's PROMPT and the world snapshot the builder's SNAP, and the task data
id is printed so the builder can carry it.
"""
import ast
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(PKG, "build"))
import build_package_artifacts as B  # noqa: E402

PAGE_FILE = "pto_liability"
_DASH = re.compile("\\s*[\u2013\u2014-]\\s*")  # en dash, em dash or hyphen, spaced or not
SHELL_TOOL = "stirrup_code_execution_run_shell"
WIKI_CREATE, WIKI_UPDATE, WIKI_GET = "wikijs_mcp_create_page", "wikijs_mcp_update_page", "wikijs_mcp_get_page"
BAMBOO_WRITES = ("bamboo_employees_create", "bamboo_employees_update", "bamboo_time_off_assign_policy",
                 "bamboo_time_off_update_balance", "bamboo_time_off_create_policy",
                 "bamboo_time_off_create_request", "bamboo_time_off_update_request_status",
                 "import_csv", "clear_database", "bamboo_reset_state")
BAMBOO_RESETS = ("import_csv", "clear_database", "bamboo_reset_state")
BAMBOO_ID_READS = ("bamboo_employees_get_directory", "bamboo_employees_get", "bamboo_search_employees")
SHELL_CALL = re.compile(r"call_tool\(\s*['\"](bamboo_[a-z_]+|wikijs_mcp_[a-z_]+|import_csv|clear_database)['\"]"
                        r"\s*,\s*(\{.*?\})\s*\)", re.S)
SHELL_TEXT = re.compile(r"text=\\?'(.*?)\\?'(?:,|\))", re.S)

SEED_BY_EMAIL = {e["work_email"].lower(): e["employee_number"] for e in B._csv("bamboohr", "Employee.csv")
                 if e.get("work_email")}


def _norm_title(t):
    return _DASH.sub(" - ", (t or "").strip())


def _short(name):
    """The MCP tool name under the toolbelt prefix: bamboohr_bamboo_x -> bamboo_x, wiki_js_mcp_wikijs_mcp_x -> wikijs_mcp_x."""
    for pre in ("bamboohr_", "wiki_js_mcp_"):
        if name.startswith(pre):
            return name[len(pre):]
    return name


def _args(tc):
    fn = tc.get("function") or {}
    a = fn.get("arguments")
    a = json.loads(a) if isinstance(a, str) else (a or {})
    if isinstance(a.get("request"), dict):
        a = a["request"]
    return fn.get("name"), a


def _text(c):
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        return " ".join(_text(x.get("text", json.dumps(x)) if isinstance(x, dict) else x) for x in c)
    return json.dumps(c)


def _json(s):
    try:
        return json.loads(s)
    except Exception:
        return None


def _walk_ids(obj, out):
    """Every BambooHR numeric id anywhere in a read result, resolved to an employee number: by
    the employeeNumber field when the result carries it, else by the work email against the seed
    Employee table, which the directory carries and the seed keys uniquely."""
    if isinstance(obj, dict):
        i = obj.get("id")
        if i is not None:
            if obj.get("employeeNumber"):
                out[str(i)] = str(obj["employeeNumber"])
            elif (obj.get("workEmail") or "").lower() in SEED_BY_EMAIL and str(i) not in out:
                out[str(i)] = SEED_BY_EMAIL[obj["workEmail"].lower()]
        for v in obj.values():
            _walk_ids(v, out)
    elif isinstance(obj, list):
        for v in obj:
            _walk_ids(v, out)


def _shell_results(stdout):
    """Every JSON result the run printed from a shell-route call, in order."""
    out = []
    for blob in SHELL_TEXT.findall(stdout):
        j = _json(blob.replace("\\'", "'").replace('\\"', '"'))
        if j is None:
            j = _json(blob)
        out.append(j)
    return out


def _page_obs(seq, route, title, content, published):
    return {"seq": seq, "route": route, "title": title, "content": content, "published": published}


def read_export(path):
    d = json.load(open(path, encoding="utf8"))
    t, tr = d["task"], d["trajectory"]
    prompts = [m for m in t["task_prompt_messages"] if m.get("role") == "user"]
    assert len(prompts) == 1 and prompts[0]["content"] == B.PROMPT, "the export's prompt is not PROMPT"
    assert tr["world_snapshot_id"] == B.SNAP, "world snapshot %s is not SNAP" % tr["world_snapshot_id"]
    assert tr["task_data_id"] == t["task_data_id"], "task data id differs between task and trajectory"
    msgs = tr["trajectory_messages"]
    results = {m.get("tool_call_id"): _text(m.get("content", "")) for m in msgs if m.get("role") == "tool"}
    tool_calls = shell = 0
    page_obs = []          # every observation of the page, in order
    unobserved_page = []   # shell writes to the page whose content the call did not carry
    writes = []
    unparsed = []
    ids = {}
    for m in msgs:
        for tc in (m.get("tool_calls") or []):
            tool_calls += 1
            name, a = _args(tc)
            res = results.get(tc.get("id"), "")
            rj = _json(res)
            short = _short(name)
            if name == SHELL_TOOL:
                shell += 1
                cmd = a.get("cmd") or a.get("command") or json.dumps(a)
                found = SHELL_CALL.findall(cmd)
                if not found:
                    continue
                printed = _shell_results(res)
                for k, (tool, lit) in enumerate(found):
                    try:
                        sa = ast.literal_eval(lit)
                    except Exception:
                        sa = None
                    sr = printed[k] if k < len(printed) else None
                    if tool in BAMBOO_ID_READS:
                        _walk_ids(sr, ids)
                    elif tool in BAMBOO_WRITES:
                        if sa is None:
                            unparsed.append({"seq": tool_calls, "tool": tool, "literal": lit[:300]})
                        writes.append({"seq": tool_calls, "route": "shell", "tool": tool, "args": sa,
                                       "result": sr if sr is not None else res[:500]})
                        if tool == "bamboo_employees_create" and isinstance(sr, dict) and sr.get("id") is not None \
                                and isinstance(sa, dict) and sa.get("employeeNumber"):
                            ids[str(sr["id"])] = str(sa["employeeNumber"])
                    elif tool in (WIKI_CREATE, WIKI_UPDATE):
                        ok = isinstance(sr, dict) and sr.get("success") is True
                        title = _norm_title(sa.get("title")) if isinstance(sa, dict) else None
                        if isinstance(sa, dict) and sa.get("content") and (title == B.PAGE or tool == WIKI_UPDATE) and ok:
                            page_obs.append(_page_obs(tool_calls, "shell " + tool, sa.get("title"), sa["content"],
                                                      sa.get("is_published")))
                        elif ok or sa is None:
                            unobserved_page.append({"seq": tool_calls, "tool": tool, "literal": lit[:200]})
                    elif tool == WIKI_GET and isinstance(sr, dict) and isinstance(sr.get("page"), dict):
                        pg = sr["page"]
                        if _norm_title(pg.get("title")) == B.PAGE and pg.get("content"):
                            page_obs.append(_page_obs(tool_calls, "shell " + WIKI_GET, pg.get("title"), pg["content"],
                                                      pg.get("is_published", pg.get("isPublished"))))
                continue
            if short in BAMBOO_ID_READS:
                _walk_ids(rj, ids)
            elif short in BAMBOO_WRITES:
                writes.append({"seq": tool_calls, "route": "toolbelt", "tool": short, "args": a,
                               "result": rj if rj is not None else res[:500]})
                if short == "bamboo_employees_create" and isinstance(rj, dict) and rj.get("id") is not None \
                        and a.get("employeeNumber"):
                    ids[str(rj["id"])] = str(a["employeeNumber"])
            elif short in (WIKI_CREATE, WIKI_UPDATE):
                ok = isinstance(rj, dict) and rj.get("success") is True
                title = _norm_title(a.get("title"))
                if short == WIKI_CREATE:
                    assert title == B.PAGE, "create_page under an unexpected title: %r" % a.get("title")
                if ok and a.get("content"):
                    page_obs.append(_page_obs(tool_calls, "toolbelt " + short, a.get("title"), a["content"],
                                              a.get("is_published")))
                elif ok:
                    unobserved_page.append({"seq": tool_calls, "tool": short, "literal": json.dumps(a)[:200]})
            elif short == WIKI_GET and isinstance(rj, dict) and isinstance(rj.get("page"), dict):
                pg = rj["page"]
                if _norm_title(pg.get("title")) == B.PAGE and pg.get("content"):
                    page_obs.append(_page_obs(tool_calls, "toolbelt " + WIKI_GET, pg.get("title"), pg["content"],
                                              pg.get("is_published", pg.get("isPublished"))))
    um = tr["trajectory_output"]["usage_metrics"]
    assert um.get("tool_calls_count") == tool_calls, "tool_calls_count %s vs counted %d" % (
        um.get("tool_calls_count"), tool_calls)
    last = page_obs[-1] if page_obs else None
    published = next((o["published"] for o in reversed(page_obs) if o["published"] is not None), None)
    later_write = [u for u in unobserved_page if last is None or u["seq"] > last["seq"]]
    resets = [w for w in writes if w["tool"] in BAMBOO_RESETS]
    vers = d.get("verifiers", {}).get("verifiers", [])
    targets = sorted({re.sub(r"\s+", " ", (v.get("verifier_values") or {}).get("target_record_label") or "")
                      for v in vers} - {""})
    row = {
        "trajectory_id": tr["trajectory_id"],
        "model": tr["orchestrator_llm_model"],
        "provider": tr["orchestrator_llm_provider"],
        "tool_calls": tool_calls,
        "assistant_messages": sum(1 for m in msgs if m.get("role") == "assistant"),
        "elapsed_seconds": int(round(tr["trajectory_time_elapsed"])),
        "world_snapshot_id": tr["world_snapshot_id"],
        "task_data_id": tr["task_data_id"],
        "task_version": tr["task_version"],
        "task_name_on_platform": tr.get("task_name"),
        "agent": tr["agent_name"],
        "platform": tr["platform_name"],
        "shell_calls": shell,
        "status": tr["trajectory_status"],
        "verifiers_on_export": {"count": len(vers), "target_record_labels": targets},
        "page": None if last is None else {
            "title": last["title"], "chars": len(last["content"]), "published": published,
            "observed_by": last["route"], "observed_at_call": last["seq"],
            "observations": [{"seq": o["seq"], "route": o["route"], "chars": len(o["content"])} for o in page_obs],
            "unobserved_later_writes": later_write},
        "page_writes_without_content": unobserved_page,
        "bamboohr_writes": {"count": len(writes),
                            "by_tool": {n: sum(1 for w in writes if w["tool"] == n)
                                        for n in sorted({w["tool"] for w in writes})},
                            "by_route": {r: sum(1 for w in writes if w["route"] == r)
                                         for r in sorted({w["route"] for w in writes})},
                            "unparsed": unparsed, "resets": [w["tool"] for w in resets]},
        "end_state_observable": {"page": last is not None and not later_write,
                                 "bamboohr": not unparsed and not resets},
    }
    return row, None if last is None else last["content"], {"id_to_employee_number": ids, "writes": writes}


def _fake_export(calls, verifiers=0):
    """A minimal export: calls is a list of (tool name, args, result string)."""
    msgs = [{"role": "user", "content": B.PROMPT}]
    for k, (name, a, res) in enumerate(calls):
        msgs.append({"role": "assistant", "tool_calls": [{"id": "c%d" % k, "function": {"name": name, "arguments": json.dumps(a)}}]})
        msgs.append({"role": "tool", "tool_call_id": "c%d" % k, "content": res})
    return {"task": {"task_data_id": "snap_x", "task_prompt_messages": [{"role": "user", "content": B.PROMPT}]},
            "trajectory": {"trajectory_id": "traj_x", "world_snapshot_id": B.SNAP, "task_data_id": "snap_x",
                           "trajectory_messages": msgs, "orchestrator_llm_model": "m", "orchestrator_llm_provider": "p",
                           "trajectory_time_elapsed": 1.0, "task_version": 0, "agent_name": "a", "platform_name": "pl",
                           "trajectory_status": "completed",
                           "trajectory_output": {"usage_metrics": {"tool_calls_count": len(calls)}}},
            "verifiers": {"verifiers": []}}


def self_check():
    """The archiver reads the page and the writes off both routes, takes the last observation, and
    flags what the export does not show."""
    import tempfile
    page = "# %s\n\n| Employee ID | x |\n|---|---|\n| TRT-0001 | 1 |\n" % B.PAGE
    ok_create = json.dumps({"success": True, "page_id": 11, "path": "p"})
    get_res = json.dumps({"success": True, "page": {"id": 11, "title": B.PAGE, "content": page + "v2", "is_published": True}})
    shell_create = {"cmd": "python3 -c \"x=open('f.md').read(); call_tool('wikijs_mcp_create_page', {'title': '%s', 'content': x, 'is_published': True})\"" % B.PAGE}
    shell_create_res = "<stdout>Create page response: CallToolResult(content=[TextContent(type='text', text='%s')])</stdout>" % ok_create
    shell_write = {"cmd": "python3 -c \"call_tool('bamboo_time_off_update_balance', {'employeeId': '1', 'timeOffTypeId': 1, 'amount': 2.5})\""}
    shell_write_res = "<stdout>CallToolResult(content=[TextContent(type='text', text='{\"adjustmentId\":\"1\",\"newBalance\":25.37}')])</stdout>"
    shell_loop = {"cmd": "python3 -c \"for e in rows: call_tool('bamboo_time_off_update_balance', {'employeeId': e['id'], 'amount': e['amt']})\""}
    cases = [
        ("toolbelt create then get_page: the read wins, observable",
         [("wiki_js_mcp_wikijs_mcp_create_page", {"title": B.PAGE, "content": page, "is_published": True}, ok_create),
          ("wiki_js_mcp_wikijs_mcp_get_page", {"id": 11}, get_res),
          ("bamboohr_bamboo_time_off_update_balance", {"employeeId": "1", "amount": 2.5}, json.dumps({"newBalance": 25.37}))],
         dict(page_ok=True, bamboo_ok=True, content=page + "v2", route="toolbelt wikijs_mcp_get_page", writes=1)),
        ("shell create from a file, never read back: page unobserved",
         [(SHELL_TOOL, shell_create, shell_create_res)],
         dict(page_ok=False, bamboo_ok=True, content=None, route=None, writes=0)),
        ("shell create from a file, then a toolbelt get_page: observable through the read",
         [(SHELL_TOOL, shell_create, shell_create_res), ("wiki_js_mcp_wikijs_mcp_get_page", {"id": 11}, get_res)],
         dict(page_ok=True, bamboo_ok=True, content=page + "v2", route="toolbelt wikijs_mcp_get_page", writes=0)),
        ("shell write with literal args: read with the app's result",
         [(SHELL_TOOL, shell_write, shell_write_res)],
         dict(page_ok=False, bamboo_ok=True, content=None, route=None, writes=1)),
        ("shell write in a loop over variables: unparsed, BambooHR unobservable",
         [(SHELL_TOOL, shell_loop, "<stdout>done</stdout>")],
         dict(page_ok=False, bamboo_ok=False, content=None, route=None, writes=1)),
    ]
    for label, calls, want in cases:
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
            json.dump(_fake_export(calls), fh)
        row, content, bamboo = read_export(fh.name)
        os.unlink(fh.name)
        obs = row["end_state_observable"]
        assert obs["page"] == want["page_ok"] and obs["bamboohr"] == want["bamboo_ok"], (label, obs)
        assert content == want["content"], (label, content)
        assert (row["page"] or {}).get("observed_by") == want["route"], (label, row["page"])
        assert len(bamboo["writes"]) == want["writes"], (label, bamboo["writes"])
        if want["writes"] and want["bamboo_ok"]:
            assert bamboo["writes"][0]["result"].get("newBalance") == 25.37, (label, bamboo["writes"])
        print("  %s: as expected" % label)
    print("self-check: the archiver reads both routes and flags what it cannot see")


def main():
    argv = sys.argv[1:]
    if "--self-check" in argv:
        self_check()
        return
    assert "--set" in argv, "name the set: --set run_set_MM-DD-YYYY"
    set_name = argv[argv.index("--set") + 1]
    pairs = [a for a in argv if "=" in a and not a.startswith("--")]
    assert pairs, "name the exports as RUN=path"
    folder = os.path.join(HERE, "findings", set_name)
    os.makedirs(folder, exist_ok=True)
    rj = os.path.join(folder, "runs.json")
    runs = {r["run"]: r for r in json.load(open(rj, encoding="utf8"))} if os.path.exists(rj) else {}
    for pair in pairs:
        run, path = pair.split("=", 1)
        row, content, bamboo = read_export(path)
        out = os.path.join(folder, "%s_%s.md" % (run, PAGE_FILE))
        if content is not None:
            with open(out, "w", encoding="utf8", newline="") as fh:
                fh.write(content)
        elif os.path.exists(out):
            os.remove(out)
        with open(os.path.join(folder, "%s_bamboohr_writes.json" % run), "w", encoding="utf8") as fh:
            json.dump(bamboo, fh, indent=1)
            fh.write("\n")
        runs[run] = dict(run=run, **row)
        pg = row["page"]
        print("%-4s %-18s tool_calls %3d  assistant %3d  shell %3d  page %-28s  bamboo writes %2d (%s)  observable page %s bamboo %s" % (
            run, row["model"], row["tool_calls"], row["assistant_messages"], row["shell_calls"],
            ("via " + pg["observed_by"]) if pg else "none", row["bamboohr_writes"]["count"],
            ", ".join("%s %d" % kv for kv in row["bamboohr_writes"]["by_route"].items()) or "-",
            row["end_state_observable"]["page"], row["end_state_observable"]["bamboohr"]))

    def key(r):
        return (r["run"][0], int(re.sub(r"\D", "", r["run"]) or 0), r["run"])
    ordered = sorted(runs.values(), key=key)
    with open(rj, "w", encoding="utf8") as fh:
        json.dump(ordered, fh, indent=1)
        fh.write("\n")
    ids = sorted({r["task_data_id"] for r in ordered})
    print("%d runs in %s; task data id(s): %s" % (len(ordered), set_name, ", ".join(ids)))


if __name__ == "__main__":
    main()
