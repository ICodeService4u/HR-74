"""A stand-in for the grading harness's `ctx`, built to the shape the platform actually has.

Why it exists: Studio's per-verifier test-run reports whether your code RAN. It cannot report
whether the verdict is RIGHT, because nothing on the platform knows the right answer. This does -
you give it a database with a known answer and a set of planted defects, and it tells you which
ones your check gets wrong.

Two deliberate differences from a permissive stub, both of which make a bad check fail here:

  * Column names default to PLACEHOLDERS (col0, col1, ...). That is what a real grading snapshot
    has been measured to return. A check that looks a column up by name silently gets nothing, and
    one that names a column in SQL raises - exactly as it would in a real run. Pass
    real_names=True to test the other branch.
  * Only the three primitives a graded run has been measured to serve are here: `list_tables`,
    `table_columns` and `query_db`. The 09/21/2026 run set measured them on the platform, on the
    BambooHR rows that returned their metrics. Nothing measured `has_table`, so the stand-in does
    not carry it and a check that reads it raises here rather than on the graded run.
  * `list_files`, `read_text`, `exists` and `trajectory` are present but EMPTY. They exist on the
    real ctx, but a verifier that leans on them is grading the run's narration rather than the
    end state. Here that dependency fails loudly instead of passing by luck.
"""
import sqlite3


class Ctx(object):
    def __init__(self, tables, real_names=False):
        """tables: {"table_name": (column_names, rows)} - rows are lists of values."""
        self.db = sqlite3.connect(":memory:")
        self._names = {}
        for name, (cols, rows) in tables.items():
            labels = list(cols) if real_names else ["col%d" % i for i in range(len(cols))]
            self._names[name] = labels
            self.db.execute("CREATE TABLE %s (%s)"
                            % (name, ", ".join('"%s"' % c for c in labels)))
            if rows:
                self.db.executemany(
                    "INSERT INTO %s VALUES (%s)" % (name, ",".join("?" * len(labels))),
                    [list(r) for r in rows])
        self.db.commit()
        self.queries = []

    # ---- database
    def list_tables(self):
        return [r[0] for r in self.db.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]

    def table_columns(self, name):
        return list(self._names.get(name, []))

    def table_row_count(self, name):
        if name not in self.list_tables():
            return 0
        return self.db.execute("SELECT COUNT(*) FROM %s" % name).fetchone()[0]

    def query_db(self, sql, params=None):
        self.queries.append(sql)
        cur = self.db.execute(sql, tuple(params)) if params else self.db.execute(sql)
        return [tuple(r) for r in cur.fetchall()]

    # ---- the surfaces a DB verifier should not be using. Present, and empty on purpose.
    def list_files(self, pattern=None):
        return []

    def exists(self, path):
        return False

    def read_text(self, path):
        raise FileNotFoundError(
            "verifier_kit: read_text is empty by design. An App DB check grades the database; "
            "if your check needs a file to reach a verdict, it is grading the wrong thing.")

    def read_json(self, path):
        return self.read_text(path)

    @property
    def trajectory(self):
        return []

    @property
    def final_answer(self):
        return ""
