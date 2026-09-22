"""The measured figures the two record writers quote: the battery's verdict line and the archived
run sets re-scored under the current rubric, each read off the script that measures it on every
write, so the record cannot carry a figure from an earlier build."""
import os
import re
import subprocess
import sys

PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _run(*args):
    env = dict(os.environ, T2_VERIFIER_QUIET="1")
    r = subprocess.run([sys.executable] + list(args), cwd=PKG, capture_output=True, text=True, env=env)
    assert r.returncode == 0, "%s failed: %s" % (args, (r.stderr or r.stdout)[-400:])
    return r.stdout


def battery():
    """(correct, total, scenarios) from the harness's last line."""
    m = re.search(r"(\d+) of (\d+) verdicts correct across (\d+) scenarios", _run("qc/verifier_harness.py"))
    return int(m.group(1)), int(m.group(2)), int(m.group(3))


def rescored(run_set, as_lines=False):
    """(mean, low, high) percentages for an archived run set under the current rubric, read as
    printed or with each run's own rows summed onto the lines."""
    args = ["qc/score_run_set.py", "--set", run_set] + (["--as-lines"] if as_lines else [])
    m = re.search(r"mean ([\d.]+)%, low ([\d.]+)%, high ([\d.]+)%", _run(*args))
    return tuple(float(x) for x in m.groups())
