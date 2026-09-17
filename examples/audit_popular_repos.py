#!/usr/bin/env python3
"""Audit and compare the search ranking signals of popular repositories."""

import subprocess
import sys

repos = [
    "torvalds/linux",
    "facebook/react",
    "vuejs/vue",
    "tensorflow/tensorflow",
]

print("Auditing popular repositories...\n")
for repo in repos:
    subprocess.run([sys.executable, "ranking_audit.py", repo])
    print("-" * 50)
