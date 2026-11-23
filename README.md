# Novel Harness

**A reusable, skill-driven harness for AI-assisted long-form fiction.**

Novel Harness is the **tool repository**, not an individual novel. Install its scaffold into any new novel Git repository, then let an Agent Skills-compatible assistant guide planning, outlining and 30-chapter writing batches.

## Quick start

```bash
git clone https://github.com/Chenzy-zero/Novel-Harness.git
cd Novel-Harness
git checkout feat/initial-harness   # until PR #1 is merged
python3 scripts/install.py /path/to/my-new-novel --dry-run
python3 scripts/install.py /path/to/my-new-novel
cd /path/to/my-new-novel
git init                       # only if not already a Git repo
python3 scripts/validate_novel.py --mode structure
```

Open the **novel repository** with an Agent Skills-compatible assistant and ask it to run `novel-init`. The installer copies `.agents/skills/`, `workflow.md`, story bibles, outlines, state ledgers, GitHub templates and validation scripts.

## Workflow

1. `novel-init`: collaborative premise, author approval, GitHub bootstrap.
2. `novel-outline`: master arcs, first 100 chapter beats, first 30 chapter contracts.
3. `novel-continue`: write 30 chapters, audit continuity, reconcile Issues, produce handoff.
4. Every 300 chapters: full continuity audit and author review.

## Repository layout

- `scaffold/` — files installed into each novel project.
- `scripts/install.py` — idempotent local installer; preserves existing files by default.
- `tests/` — harness-level tests.

## Safety and status

The installer **does not create GitHub repositories or modify GitHub Issues**. GitHub bootstrap/sync runs separately inside the novel repository, requires authentication and author authorization, and is not yet fully end-to-end validated. The current implementation is an early engineering preview; literary quality, state reconciliation and 30-chapter orchestration still require validation.

To update an existing novel project, first use `--dry-run`. `--force` overwrites existing files and should only be used after reviewing diffs/backups.

## Development

```bash
python3 -m unittest discover -s tests -v
```
