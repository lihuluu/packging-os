# GitHub Release Audit

Date: 2026-06-18

## Current Recommendation

Publish Packaging OS as an open workflow system, not as a mirror of the current working folder.

The public value is the packaging-design operating method: Claude Skills, shared references, templates, maintainer checks, and a fictional demo project. The private value is the live project memory, supplier context, pricing evidence, client language, and local tool configuration. Those must stay out of GitHub.

## Candidate Public Surface

These paths are reasonable candidates for a first public repository:

- `README.md`
- `CLAUDE.md`
- `.claude/settings.json`
- `.claude/hooks/`
- `.claude/references/`
- `.claude/skills/`
- `Workspace/Templates/`
- `Workspace/Knowledge/Library/`
- `docs/`
- `examples/demo-tea-project/`

## Blocked From Public Release

These paths should not be committed to a public GitHub repository:

- `.claude/settings.local.json`
- `.obsidian/`
- `Workspace/Projects/**`
- `Workspace/Knowledge/Operations/current/`
- `Workspace/Knowledge/Operations/queue/`
- `Workspace/Knowledge/Operations/history/`
- `Workspace/Knowledge/Operations/coverage/`
- Any `03_Design/02_Assets/AI_Concepts/` folder
- Any `04_Final/` folder
- PDFs, images, Adobe files, source design files, and production proofs unless explicitly sanitized

## Findings

### 1. Local settings contain sensitive command history

`.claude/settings.local.json` is machine-local and must remain ignored. It contains local command permissions and at least one external API authorization value. Treat any token previously stored there as exposed to the local workspace and rotate it before public release.

Status: blocked from public release by `.gitignore`.

### 2. Real project folders contain private business context

`Workspace/Projects/**` includes real project names, supplier state, budget/quote context, proofing records, client/brand facts, and production notes. This is useful operating evidence, but it is not public training material unless deliberately anonymized.

Status: blocked from public release by `.gitignore`.

### 3. Operational knowledge folders are live working state

`Workspace/Knowledge/Operations/**` contains review sessions, history, inboxes, and coverage tracking. These files describe how the system is being maintained, but they can expose internal timing, priorities, and project workflow details.

Status: blocked from public release by `.gitignore` except for any future curated public examples.

### 4. The public story needs a short GitHub-facing README

The existing `README.md` is strong as an internal operating manual. GitHub visitors also need a shorter entry point: what this is, who it is for, how to try it, what is safe to publish, and how to adapt it.

Status: drafted in `docs/github-public-readme-draft.md`.

### 5. Naming should be decided before launch

The current folder and docs use `Packaging OS`. If this is intentional branding, keep it and explain it. If the public name should use the fully spelled English word instead, fix it before publishing, because renaming after launch is noisier.

Status: manual decision required.

## First Public Release Shape

Recommended repository shape:

```text
packaging-os/
  README.md
  CLAUDE.md
  LICENSE
  .gitignore
  .claude/
    hooks/
    references/
    skills/
    settings.json
  Workspace/
    Templates/
    Knowledge/
      Library/
  docs/
  examples/
    demo-tea-project/
```

## Pre-Publish Checklist

- [ ] Confirm whether the public name stays `Packaging OS` or changes to a fully spelled alternative.
- [x] Choose a license.
- [ ] Rotate any token that has appeared in `.claude/settings.local.json`.
- [ ] Run the Packaging OS validation script.
- [ ] Run secret/contact searches against the future public surface.
- [ ] Initialize git only after the ignore rules are in place.
- [ ] Review `git status --ignored` before the first commit.
- [ ] Create the GitHub repository.
- [ ] Push only the reviewed public surface.

## Suggested First Commit

```bash
git init
git add README.md CLAUDE.md LICENSE .gitignore .claude/settings.json .claude/hooks .claude/references .claude/skills Workspace/Templates Workspace/Knowledge/Library docs examples
git status
git commit -m "chore: prepare Packaging OS public release"
```

Do not run the `git add` command until the checklist above is complete.

## Verification Notes

Current verification on 2026-06-18:

- Public-surface secret scan found no actual external API token pattern in the candidate public paths.
- Public-surface contact scan found no phone number or email pattern in the candidate public paths.
- Packaging OS validation no longer reports a release-document naming issue.
- Whole-workspace validation still reports pre-existing private workspace issues:
  - four temporary files under `Workspace/Projects/HGT235_特级高山绿茶500g/00_Project_Control/`
  - `Workspace/Knowledge/Operations/coverage/project-knowledge-coverage.md` missing `茶+康养调味茶系列`
  - `Workspace/Knowledge/Operations/current/current-review-session.md` missing `茶+康养调味茶系列`

These remaining validation issues are outside the recommended public surface and are covered by `.gitignore`, but they should be cleaned up before treating the local workspace itself as fully healthy.
