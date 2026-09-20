#!/usr/bin/env python3
"""Archive a trajectory export under qc/findings/<set>/ the way score_run_set.py reads it.

    python3 qc/archive_run_set.py --set run_set_09-20-2026 G1=/path/G1.json G2=/path/G2.json

For each export it reads the run's two published pages off the wiki_js create_page calls in
trajectory_messages, applies any update_page that follows on the same path, and writes each as
<run>_approved_hiring_view.md or <run>_staffed_role_view.md, bytes as the call carried them. It
merges one row per run into runs.json with the model, trajectory id, tool-call count, assistant
message count, shell-call count, elapsed seconds and both snapshot ids, every value read off the
export and none typed. It asserts the export's prompt is the builder's PROMPT and its world
snapshot the builder's SNAP, and prints the task data id so the builder can carry it.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(PKG, "build"))
from scenarios import A, Bt  # noqa: E402
import build_package_artifacts as B  # noqa: E402

PAGE_FILES = {A: "approved_hiring_view", Bt: "staffed_role_view"}
_DASH = re.compile("\\s*[\u2013\u2014-]\\s*")  # en dash, em dash or hyphen, spaced or not
SHELL_TOOL = "stirrup_code_execution_run_shell"
CREATE = "wiki_js_mcp_wikijs_mcp_create_page"
UPDATE = "wiki_js_mcp_wikijs_mcp_update_page"


def _norm_title(t):
    return _DASH.sub(" - ", (t or "").strip())


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
    pages = {}
    for m in msgs:
        for tc in (m.get("tool_calls") or []):
            tool_calls += 1
            name, a = _args(tc)
            if name == SHELL_TOOL:
                shell += 1
            if name in (CREATE, UPDATE):
                title = _norm_title(a.get("title"))
                path = a.get("path")
                res = results.get(tc.get("id"), "")
                try:
                    rj = json.loads(res)
                except Exception:
                    rj = {}
                if name == CREATE:
                    assert title in PAGE_FILES, "create_page under an unexpected title: %r" % a.get("title")
                    assert rj.get("success") is True, "create_page did not succeed: %s" % res[:200]
                    pages[title] = {"path": path, "page_id": rj.get("page_id"),
                                    "content": a.get("content", ""), "published": a.get("is_published"),
                                    "updated_after_create": False}
                else:
                    hit = next((k for k, v in pages.items()
                                if (path and v["path"] == path) or
                                (a.get("page_id") is not None and v["page_id"] == a.get("page_id"))), None)
                    if hit is not None and rj.get("success") is not False:
                        if a.get("content"):
                            pages[hit]["content"] = a["content"]
                        pages[hit]["updated_after_create"] = True
    um = tr["trajectory_output"]["usage_metrics"]
    assert um.get("tool_calls_count") == tool_calls, "tool_calls_count %s vs counted %d" % (
        um.get("tool_calls_count"), tool_calls)
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
        "agent": tr["agent_name"],
        "platform": tr["platform_name"],
        "shell_calls": shell,
        "status": tr["trajectory_status"],
        "pages": {k: {"path": v["path"], "page_id": v["page_id"], "chars": len(v["content"]),
                      "published": v["published"], "updated_after_create": v["updated_after_create"]}
                  for k, v in pages.items()},
    }
    return row, {k: v["content"] for k, v in pages.items()}


def main():
    argv = sys.argv[1:]
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
        row, contents = read_export(path)
        for title, short in PAGE_FILES.items():
            out = os.path.join(folder, "%s_%s.md" % (run, short))
            if title in contents:
                with open(out, "w", encoding="utf8", newline="") as fh:
                    fh.write(contents[title])
            elif os.path.exists(out):
                os.remove(out)
        runs[run] = dict(run=run, **row)
        print("%-4s %-18s tool_calls %3d  assistant %3d  shell %3d  pages %d  task_data_id %s" % (
            run, row["model"], row["tool_calls"], row["assistant_messages"], row["shell_calls"],
            len(contents), row["task_data_id"]))

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
