#!/usr/bin/env python3
"""Hold every package's Files-and-data-tables selection to the form the picker accepts.

The Studio picker offers one selection per line: a world file on its plain path under the world
root, and an app table as `<app>/<table>.csv`.  It has no wildcards, takes no `apps_data/` prefix
and shows no leading slash.  A package doc that writes a selection any other way -- most easily
`apps_data/greenhouse/*.csv`, which is the repo path for a set of five tables and not a thing
anyone can click -- hands whoever fills the metadata in a string with no referent.

So: every 02_task_metadata.md carries at least one fenced block inside its Required world files
section, every line of it is a selection in picker form, and every one resolves to a real file in
`filesystem/` or `apps_data/`.  The App rows of the section's own table are held to the same
spelling, since they are read as a selection list too.

The block is authoritative for WHICH tables are selected.  Where the section's table names an app
table the block omits, that is reported and not failed: adding a selection is a package-design
call, not a formatting one.

    python3 tasks/check_selection_blocks.py
"""
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
WORLD = os.path.join(REPO, "filesystem")
APPS_DIR = os.path.join(REPO, "apps_data")
APPS = ("greenhouse", "bamboohr", "wiki_js")
HEADING = "## Required world files"


def section(text):
    """The Required world files section: its heading to the next level-two heading."""
    start = text.index(HEADING)
    nxt = text.find("\n## ", start + len(HEADING))
    return text[start:] if nxt < 0 else text[start:nxt]


def blocks(sec):
    """Every fenced block in the section, as lists of non-empty lines."""
    return [[l.strip() for l in b.split("\n") if l.strip()]
            for b in re.findall(r"```\n(.*?)```", sec, re.S)]


def app_row_paths(sec):
    """Every `<app>/<table>.csv` the section's App table rows name."""
    out = []
    for ln in sec.split("\n"):
        if ln.startswith("| App"):
            out += re.findall(r"`((?:%s)/[A-Za-z_]+\.csv)`" % "|".join(APPS), ln)
    return out


def check(pkg):
    """(failures, reports) for one package."""
    fails, notes = [], []
    path = os.path.join(pkg, "02_task_metadata.md")
    text = open(path, encoding="utf8").read()
    name = os.path.basename(pkg).split("_")[2]
    if HEADING not in text:
        return ["%s: no %r section" % (name, HEADING)], []
    sec = section(text)

    picked = []
    for b in blocks(sec):
        picked += b
    if not picked:
        fails.append("%s: the Required world files section carries no selection block" % name)
        return fails, notes

    for line in picked:
        where = "%s: %r" % (name, line)
        if line.startswith("/"):
            fails.append(where + " -- leading slash; the picker shows none")
        elif line.startswith("apps_data/"):
            fails.append(where + " -- `apps_data/` is the repo path, not a selection")
        elif "*" in line or "?" in line:
            fails.append(where + " -- a wildcard is not selectable")
        elif "`" in line or " " in line:
            fails.append(where + " -- not a bare path")
        elif line.split("/")[0] in APPS:
            if not os.path.isfile(os.path.join(APPS_DIR, line)):
                fails.append(where + " -- no such app table")
        elif not os.path.isfile(os.path.join(WORLD, line)):
            fails.append(where + " -- no such world file")

    dupes = sorted({p for p in picked if picked.count(p) > 1})
    for d in dupes:
        fails.append("%s: %r selected twice" % (name, d))

    for ln in sec.split("\n"):
        if ln.startswith("| App") and re.search(r"`apps_data/|\*\.csv", ln):
            fails.append("%s: an App row still spells a selection `apps_data/...` or with a "
                         "wildcard" % name)

    # Report-only: the section's table names a table the block does not select.
    missing = [t for t in app_row_paths(sec) if t not in picked]
    for m in sorted(set(missing)):
        notes.append("%s: the table names %s and the block does not select it" % (name, m))

    world = [p for p in picked if p.split("/")[0] not in APPS]
    print("  %-4s %2d selections: %d world files, %d app tables"
          % (name, len(picked), len(world), len(picked) - len(world)))
    return fails, notes


def main():
    pkgs = sorted(glob.glob(os.path.join(HERE, "HR_*_T*")))
    pkgs = [p for p in pkgs if os.path.isfile(os.path.join(p, "02_task_metadata.md"))]
    print("Selection blocks, %d packages" % len(pkgs))
    fails, notes = [], []
    for pkg in pkgs:
        f, n = check(pkg)
        fails += f
        notes += n
    if notes:
        print("\nreport-only (%d):" % len(notes))
        for n in notes:
            print("  ~ " + n)
    if fails:
        print("\nFAILED (%d):" % len(fails))
        for f in fails:
            print("  x " + f)
        return 1
    print("\nPASSED: every selection is in picker form and resolves on disk")
    return 0


if __name__ == "__main__":
    sys.exit(main())
