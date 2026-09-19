#!/usr/bin/env python3
"""The world is frozen: filesystem/ and apps_data/ are the bytes inside HR 74.zip and nothing else.

    python3 world/checks/world_manifest.py

Every task package recomputes its graded values from these bytes, so a byte that moves here moves
every answer silently. This compares the extracted tree against the archive entry by entry, in
both directions, and exits non-zero on any difference. Run it before every commit that touches a
task, beside `git status filesystem apps_data`.
"""
import hashlib
import os
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
ZIP = os.path.join(REPO, "HR 74.zip")
ROOTS = ("filesystem", "apps_data")


def main():
    zf = zipfile.ZipFile(ZIP)
    archive = {i.filename: hashlib.md5(zf.read(i.filename)).hexdigest()
               for i in zf.infolist() if not i.is_dir()}
    tree = {}
    for root in ROOTS:
        for dirpath, _dirs, files in os.walk(os.path.join(REPO, root)):
            for f in files:
                p = os.path.join(dirpath, f)
                rel = os.path.relpath(p, REPO).replace(os.sep, "/")
                tree[rel] = hashlib.md5(open(p, "rb").read()).hexdigest()
    missing = sorted(set(archive) - set(tree))
    extra = sorted(set(tree) - set(archive))
    changed = sorted(p for p in archive if p in tree and archive[p] != tree[p])
    for label, items in (("missing from the tree", missing), ("not in the archive", extra),
                         ("changed", changed)):
        for p in items:
            print("%s: %s" % (label.upper(), p))
    print("world: %d archive entries, %d in the tree, %d missing, %d extra, %d changed"
          % (len(archive), len(tree), len(missing), len(extra), len(changed)))
    return 1 if (missing or extra or changed) else 0


if __name__ == "__main__":
    sys.exit(main())
