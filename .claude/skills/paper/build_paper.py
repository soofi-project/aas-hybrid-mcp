#!/usr/bin/env python
"""Canonical paper-build invocation for the ETFA 2026 paper.

Wraps `docker compose -f paper/etfa2026/docker-compose.yml up --build` with:
- automatic repo-root resolution (works from any CWD)
- pass-through exit code from docker compose
- explicit success/failure marker before exit

Usage:
    python .claude/skills/paper/build_paper.py

Exits non-zero if the build fails or '=== BUILD SUCCESS ===' is not seen in output.

Why this wrapper exists: the skill ships its tool. The compose file itself must
stay at paper/etfa2026/ (volume-mount coupling), but the invocation is hardened
here so agents don't reinvent the command.
"""

import os
import subprocess
import sys


def find_repo_root() -> str:
    """Walk up from this script's location to find paper/etfa2026/docker-compose.yml."""
    cur = os.path.dirname(os.path.abspath(__file__))
    for _ in range(6):
        candidate = os.path.join(cur, "paper", "etfa2026", "docker-compose.yml")
        if os.path.isfile(candidate):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            break
        cur = parent
    print("Error: could not locate paper/etfa2026/docker-compose.yml from script location.", file=sys.stderr)
    sys.exit(1)


def main():
    repo_root = find_repo_root()
    compose_file = os.path.join(repo_root, "paper", "etfa2026", "docker-compose.yml")

    cmd = ["docker", "compose", "-f", compose_file, "up", "--build", "--abort-on-container-exit"]
    print(f"$ {' '.join(cmd)}", file=sys.stderr)

    result = subprocess.run(cmd, capture_output=True, text=True)

    # Stream output so user sees it
    sys.stdout.write(result.stdout)
    sys.stderr.write(result.stderr)

    success_marker = "=== BUILD SUCCESS ==="
    if success_marker in result.stdout or success_marker in result.stderr:
        print(f"\nBuild OK — PDF at {os.path.join(repo_root, 'paper', 'etfa2026', 'conference_etfa_2026.pdf')}", file=sys.stderr)
        sys.exit(0)
    else:
        print("\nBuild FAILED — '=== BUILD SUCCESS ===' marker not found.", file=sys.stderr)
        sys.exit(result.returncode if result.returncode != 0 else 1)


if __name__ == "__main__":
    main()
