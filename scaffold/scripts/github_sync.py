#!/usr/bin/env python3
"""Idempotent GitHub Issue bootstrap/sync for the novel workspace (stdlib only)."""
import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KINDS = ("ARC", "BEAT", "CHAR", "THREAD", "AUDIT")
MARKER = "<!-- novel-id: {} -->"

def github_token():
    token = os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN")
    if token:
        return token
    try:
        return subprocess.check_output(["gh", "auth", "token"], text=True, stderr=subprocess.DEVNULL).strip()
    except (OSError, subprocess.CalledProcessError):
        raise RuntimeError("Set GH_TOKEN/GITHUB_TOKEN or log in with gh auth login")

def api(method, path, token, payload=None):
    url = "https://api.github.com" + path
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method=method, headers={
        "Authorization": "Bearer " + token, "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "novel-workspace-v0.2"})
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        raise RuntimeError("GitHub API {} {} failed: {} {}".format(method, path, exc.code, exc.read().decode("utf-8")[:300]))

def repo_name():
    override = os.getenv("NOVEL_GITHUB_REPO")
    if override:
        if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", override):
            raise ValueError("Invalid NOVEL_GITHUB_REPO")
        return override
    remote = subprocess.check_output(["git", "-C", str(ROOT), "remote", "get-url", "origin"], text=True).strip()
    match = re.search(r"github\.com[:/]([^/]+)/([^/]+?)(?:\.git)?$", remote)
    if not match:
        raise RuntimeError("Cannot resolve GitHub origin; set NOVEL_GITHUB_REPO")
    return match.group(1) + "/" + match.group(2)

def pages(path, token):
    result = []
    for page in range(1, 101):
        join = "&" if "?" in path else "?"
        chunk = api("GET", path + join + "per_page=100&page=" + str(page), token)
        result.extend(chunk)
        if len(chunk) < 100:
            return result
    raise RuntimeError("Pagination exceeded 100 pages; refusing incomplete sync")

def labels(repo, token, dry_run=False):
    path = "/repos/{}/labels".format(repo)
    existing = {x["name"] for x in pages(path, token)}
    for kind in KINDS:
        name = "novel:" + kind.lower()
        if name not in existing:
            if dry_run:
                print("WOULD CREATE label", name)
            else:
                api("POST", path, token, {"name": name, "color": "486581", "description": "Novel tracking: " + kind})
                print("CREATED label", name)

def issue_index(repo, token):
    items = pages("/repos/{}/issues?state=all".format(repo), token)
    result = {}
    for item in items:
        if "pull_request" in item:
            continue
        for stable_id in re.findall(r"<!-- novel-id: ([A-Z]+-[A-Za-z0-9_-]+) -->", item.get("body") or ""):
            if stable_id in result:
                raise RuntimeError("Duplicate stable ID {} in remote issues".format(stable_id))
            result[stable_id] = item
    return result

def sync(repo, token, manifest, dry_run=False):
    records = json.loads(Path(manifest).read_text(encoding="utf-8"))
    if not isinstance(records, list):
        raise ValueError("Manifest must be a list")
    index = issue_index(repo, token)
    seen = set()
    for item in records:
        stable_id, title, path = item["id"], item["title"], item["path"]
        if not re.fullmatch(r"(ARC|BEAT|CHAR|THREAD|AUDIT)-[A-Za-z0-9_-]+", stable_id):
            raise ValueError("Invalid stable ID: " + stable_id)
        if stable_id in seen:
            raise ValueError("Duplicate manifest ID: " + stable_id)
        seen.add(stable_id)
        relative = Path(path)
        if relative.is_absolute() or ".." in relative.parts or not (ROOT / relative).is_file():
            raise ValueError("Missing/unsafe document path: " + path)
        kind = stable_id.split("-", 1)[0]
        body = MARKER.format(stable_id) + "\n\nCanonical document: `{}`\n\n{}".format(path, item.get("description", ""))
        payload = {"title": title, "body": body, "labels": ["novel:" + kind.lower()]}
        old = index.get(stable_id)
        if old:
            if old["title"] == title and (old.get("body") or "") == body:
                print("UNCHANGED", stable_id, old["number"])
                continue
            if dry_run:
                print("WOULD UPDATE", stable_id, old["number"])
            else:
                api("PATCH", "/repos/{}/issues/{}".format(repo, old["number"]), token, {"title": title, "body": body})
                print("UPDATED", stable_id, old["number"])
        else:
            if dry_run:
                print("WOULD CREATE", stable_id)
            else:
                created = api("POST", "/repos/{}/issues".format(repo), token, payload)
                index[stable_id] = created
                print("CREATED", stable_id, created["html_url"])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("bootstrap", "sync", "reconcile"))
    parser.add_argument("--manifest", default="state/github-issues.json")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    token = github_token()
    repo = repo_name()
    api("GET", "/repos/" + repo, token)
    if args.command == "bootstrap":
        labels(repo, token, args.dry_run)
    else:
        manifest = ROOT / args.manifest
        if args.command == "reconcile":
            args.dry_run = True
        sync(repo, token, manifest, args.dry_run)

if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, ValueError, KeyError, OSError) as exc:
        print("ERROR:", exc, file=sys.stderr)
        sys.exit(1)
