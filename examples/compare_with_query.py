#!/usr/bin/env python3
"""Audit repos against a specific search query to see which one would rank first."""

import subprocess
import sys

query = "github star history"
repos = [
    "facebook/react",
    "vuejs/vue",
    "sveltejs/svelte",
]

print(f"Query: \"{query}\"\n")
for repo in repos:
    subprocess.run([sys.executable, "ranking_audit.py", repo, "--query", query])
    print()
