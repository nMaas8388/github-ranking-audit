#!/usr/bin/env python3
"""
GitHub Ranking Audit
Audit a repository's search ranking signals on GitHub.
"""

import argparse
import json
import os
import sys
import time
import re

try:
    import requests
except ImportError:
    print("Install requests: pip install requests")
    sys.exit(1)

API = "https://api.github.com"
TOKEN = os.environ.get("GITHUB_TOKEN", "")


def headers():
    h = {"User-Agent": "github-ranking-audit", "Accept": "application/vnd.github.v3+json"}
    if TOKEN:
        h["Authorization"] = f"token {TOKEN}"
    return h


def fetch_repo(owner, name):
    resp = requests.get(f"{API}/repos/{owner}/{name}", headers=headers())
    if resp.status_code == 404:
        print(f"Repository not found: {owner}/{name}")
        return None
    resp.raise_for_status()
    return resp.json()


def fetch_readme(owner, name):
    resp = requests.get(f"{API}/repos/{owner}/{name}/readme", headers=headers())
    if resp.status_code != 200:
        return ""
    import base64
    content = resp.json().get("content", "")
    try:
        return base64.b64decode(content).decode("utf-8", errors="replace")
    except Exception:
        return ""


def fetch_topics(owner, name):
    resp = requests.get(
        f"{API}/repos/{owner}/{name}/topics",
        headers={**headers(), "Accept": "application/vnd.github.mercy-preview+json"},
    )
    if resp.status_code != 200:
        return []
    return resp.json().get("names", [])


def score_name(repo_name, query_words):
    name_words = set(repo_name.lower().replace("-", " ").replace("_", " ").split())
    if not query_words:
        return 100
    matched = len(name_words & query_words)
    return min(100, int((matched / len(query_words)) * 100))


def score_description(description):
    if not description:
        return 0
    length = len(description)
    if length < 20:
        return 30
    if length < 50:
        return 60
    if length <= 300:
        return 100
    return 80


def score_topics(topics):
    count = len(topics)
    if count == 0:
        return 0
    if count < 5:
        return 40
    if count < 10:
        return 70
    if count <= 20:
        return 100
    return 90


def score_readme(readme_text):
    if not readme_text:
        return 0
    words = readme_text.split()
    first_200 = " ".join(words[:200]).lower()
    length = len(words)
    if length < 50:
        return 20
    if length < 200:
        return 50
    if length < 500:
        return 75
    return 100


def score_stars(stars):
    if stars == 0:
        return 0
    if stars < 10:
        return 15
    if stars < 50:
        return 30
    if stars < 100:
        return 50
    if stars < 500:
        return 70
    if stars < 1000:
        return 85
    return 100


def score_activity(pushed_at):
    if not pushed_at:
        return 0
    from datetime import datetime, timezone
    try:
        last = datetime.fromisoformat(pushed_at.replace("Z", "+00:00"))
        days = (datetime.now(timezone.utc) - last).days
    except Exception:
        return 0
    if days <= 7:
        return 100
    if days <= 30:
        return 85
    if days <= 90:
        return 60
    if days <= 180:
        return 35
    return 10


def audit(owner, name, query=None):
    print(f"\nAuditing {owner}/{name}...\n")

    repo = fetch_repo(owner, name)
    if not repo:
        return None

    readme = fetch_readme(owner, name)
    topics = fetch_topics(owner, name)

    query_words = set()
    if query:
        query_words = set(query.lower().split())

    scores = {
        "name": score_name(repo["name"], query_words),
        "description": score_description(repo.get("description", "")),
        "topics": score_topics(topics),
        "readme": score_readme(readme),
        "stars": score_stars(repo.get("stargazers_count", 0)),
        "activity": score_activity(repo.get("pushed_at", "")),
    }

    weights = {
        "name": 0.25,
        "description": 0.15,
        "topics": 0.15,
        "readme": 0.15,
        "stars": 0.20,
        "activity": 0.10,
    }

    overall = sum(scores[k] * weights[k] for k in scores)

    print(f"  Repository:   {repo['full_name']}")
    print(f"  Description:  {repo.get('description', '(none)')[:80]}")
    print(f"  Language:     {repo.get('language', 'unknown')}")
    print(f"  Stars:        {repo.get('stargazers_count', 0):,}")
    print(f"  Forks:        {repo.get('forks_count', 0):,}")
    print(f"  Watchers:     {repo.get('subscribers_count', 0):,}")
    print(f"  Topics:       {len(topics)} ({', '.join(topics[:5])}{'...' if len(topics) > 5 else ''})")
    print(f"  Last push:    {repo.get('pushed_at', 'unknown')[:10]}")
    print(f"  README words: {len(readme.split()) if readme else 0}")

    print(f"\n  Scores:")
    for k, v in scores.items():
        bar = "#" * (v // 5) + "." * (20 - v // 5)
        print(f"    {k:<14} {v:>3}/100  [{bar}]")

    grade = "A" if overall >= 85 else "B" if overall >= 70 else "C" if overall >= 50 else "D" if overall >= 30 else "F"
    print(f"\n  Overall: {overall:.0f}/100 (Grade {grade})")

    if scores["name"] < 50:
        print(f"\n  Tip: rename the repo to include your target search keywords")
    if scores["topics"] < 50:
        print(f"  Tip: add 8-15 relevant topics to improve discoverability")
    if scores["readme"] < 50:
        print(f"  Tip: expand the README, especially the first 200 words")
    if scores["activity"] < 50:
        print(f"  Tip: push a commit to signal the repo is actively maintained")
    if scores["stars"] < 50:
        print(f"  Tip: the repo needs more stars to compete in search results")

    return {"repo": f"{owner}/{name}", "scores": scores, "overall": round(overall), "grade": grade}


def main():
    parser = argparse.ArgumentParser(description="Audit GitHub repository search ranking signals")
    parser.add_argument("repos", nargs="+", help="Repository in owner/repo format")
    parser.add_argument("--query", "-q", help="Target search query to check name match against")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    args = parser.parse_args()

    results = []
    for repo in args.repos:
        if "/" not in repo:
            print(f"Invalid format: {repo}. Use owner/repo.")
            continue
        owner, name = repo.split("/", 1)
        result = audit(owner, name, args.query)
        if result:
            results.append(result)

    if args.json and results:
        print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
