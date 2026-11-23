#!/usr/bin/env python3
"""Small stdlib-only structural and deterministic gates for the novel workspace."""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ("novel-init", "novel-outline", "novel-continue")
REQUIRED = (
    "README.md", "AGENTS.md", "workflow.md", "project/brief.md",
    "project/questions.md", "bible/world.md", "outline/master.md",
    "outline/first-100.md", "state/current.md", "state/foreshadowing.md",
    "state/relationships.md", "state/knowledge.md", "state/timeline.md",
    "docs/issue-model.md", "docs/grilling.md",
)
def text(path):
    return (ROOT / path).read_text(encoding="utf-8")
def fail(message):
    print("FAIL:", message)
    return 1
def structure():
    errors = 0
    for path in REQUIRED:
        if not (ROOT / path).is_file():
            errors += fail("missing: " + path)
    for name in SKILLS:
        path = ".agents/skills/" + name + "/SKILL.md"
        if not (ROOT / path).is_file():
            errors += fail("missing skill: " + path)
            continue
        body = text(path)
        head = re.match(r"\A---\n(.*?)\n---\n", body, flags=re.S)
        if not head:
            errors += fail("no YAML frontmatter: " + path)
        elif not re.search(r"(?m)^name:\s*" + name + r"\s*$", head.group(1)):
            errors += fail("wrong skill name: " + path)
        elif not re.search(r"(?m)^description:\s*\S", head.group(1)):
            errors += fail("missing skill description: " + path)
    if errors == 0: print("PASS: structure")
    return errors
def gate():
    errors = structure()
    brief = text("project/brief.md")
    outline = text("outline/first-100.md")
    if not re.search(r"(?m)^planning_status:\s*APPROVED\s*$", brief):
        errors += fail("planning_status not APPROVED")
    if not re.search(r"(?m)^author_approval:\s*APPROVED\s*$", brief):
        errors += fail("author_approval not APPROVED")
    if not re.search(r"(?m)^coverage:\s*100/100\s*$", outline):
        errors += fail("first-100 coverage not 100/100")
    if not re.search(r"(?m)^author_approved:\s*true\s*$", outline):
        errors += fail("first-100 outline not approved")
    # Gate B also requires human review of 100 detailed lines, arcs, and issue sync.
    if errors == 0: print("PASS: mechanical Gate B only; human and Issue review still required")
    return errors
def hanzi_count(s):
    return sum(0x3400 <= ord(c) <= 0x9FFF for c in s)
def batch(start):
    errors = gate()
    if start < 1 or (start-1) % 30:
        return errors + fail("start must be 1, 31, 61, ...")
    end = start+29
    dirname = "chapters/%04d-%04d" % (start, end)
    for n in range(start,end+1):
        path = ROOT / dirname / ("%04d.md" % n)
        if not path.exists():
            errors += fail("missing chapter " + str(path.relative_to(ROOT)))
            continue
        body = path.read_text(encoding="utf-8")
        # Remove optional metadata, chapter title and markdown formatting where possible.
        body = re.sub(r"\A---\n.*?\n---\n", "", body, flags=re.S)
        body = re.sub(r"(?m)^#.*$", "", body)
        count = hanzi_count(body)
        if not (1800 <= count <= 2200):
            errors += fail("%04d: %d Han characters, expected 1800..2200" % (n,count))
    name = "handoffs/%04d-%04d.md" % (start,end)
    if not (ROOT/name).exists(): errors += fail("missing handoff: " + name)
    current = text("state/current.md")
    if not re.search(r"(?m)^pending_issue_sync:\s*\[\]\s*$", current):
        errors += fail("pending_issue_sync not empty/unknown; require Issue reconciliation")
    if not re.search(r"(?m)^last_published_chapter:\s*"+str(end)+r"\s*$",current):
        errors += fail("last_published_chapter mismatch")
    if errors == 0: print("PASS: mechanical batch gate; story continuity and remote Issue audit still required")
    return errors
def main():
    p = argparse.ArgumentParser()
    p.add_argument("--mode",choices=("structure","gate","batch"),default="structure")
    p.add_argument("--start",type=int,default=1)
    args=p.parse_args()
    checks={"structure":structure,"gate":gate}
    e=batch(args.start) if args.mode=="batch" else checks[args.mode]()
    sys.exit(1 if e else 0)
if __name__=="__main__":
    main()
