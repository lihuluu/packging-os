# GitHub Release Prep Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prepare Packaging OS for a safe first GitHub publication without exposing local secrets, private project records, supplier data, or client work.

**Architecture:** Keep the current working directory intact and add publication guardrails around it. The public release surface is the workflow system, Claude Skills, shared references, templates, docs, and a fictional demo project; private project execution data remains ignored.

**Tech Stack:** Markdown, Claude Skills, PowerShell validation scripts, git ignore rules.

---

## File Structure

- Create: `.gitignore`
  - Prevents local runtime files, secrets, real projects, generated assets, and production files from entering the future Git repository.
- Create: `docs/github-release-audit.md`
  - Records the current publication decision, safe-to-publish surface, blocked files, redaction work, and final checklist.
- Create: `docs/github-public-readme-draft.md`
  - Provides a concise GitHub-facing README draft that can later replace or be merged into `README.md`.
- Create: `examples/demo-tea-project/`
  - Provides fictional project files showing how the OS works without leaking real clients, suppliers, pricing, or contact details.

### Task 1: Publication Boundary

**Files:**
- Create: `docs/github-release-audit.md`

- [ ] **Step 1: Document the public release surface**

Record `.claude/skills/`, `.claude/references/`, `Workspace/Templates/`, `Workspace/Knowledge/Library/`, `CLAUDE.md`, `README.md`, and `docs/` as candidate public content.

- [ ] **Step 2: Document blocked private surfaces**

Record `.claude/settings.local.json`, `.obsidian/`, `Workspace/Projects/**`, real production assets, generated AI concept drafts, and operational current/queue/history files as blocked for public release.

- [ ] **Step 3: Add manual actions**

Record that any token found in local settings must be rotated before publication, even if the file is ignored.

### Task 2: Ignore Rules

**Files:**
- Create: `.gitignore`

- [ ] **Step 1: Ignore local runtime files**

Add `.claude/settings.local.json`, editor folders, environment files, secret key formats, caches, logs, and OS metadata.

- [ ] **Step 2: Ignore private workspace execution data**

Add `Workspace/Projects/**` and operational scratchpad folders under `Workspace/Knowledge/Operations/`.

- [ ] **Step 3: Ignore generated and production design assets**

Add common image, PDF, Adobe, final-output, and AI concept draft patterns.

### Task 3: Public README Draft

**Files:**
- Create: `docs/github-public-readme-draft.md`

- [ ] **Step 1: Write the public positioning**

Position Packaging OS as a packaging-design studio workflow system built with Claude Skills.

- [ ] **Step 2: Explain the 9-layer workflow**

Describe each layer and the role of project memory, supplier communication, visual validation, and retrospective knowledge capture.

- [ ] **Step 3: Add quick start and safety notes**

Explain that users should copy the repo, configure local Claude settings privately, and never commit real project data.

### Task 4: Demo Project

**Files:**
- Create: `examples/demo-tea-project/README.md`
- Create: `examples/demo-tea-project/00_Project_Control/project-memory-card.md`
- Create: `examples/demo-tea-project/01_Brief/packaging-brief.md`
- Create: `examples/demo-tea-project/03_Design/02_Assets/asset-register.md`
- Create: `examples/demo-tea-project/03_Design/04_Production/supplier-brief.md`

- [ ] **Step 1: Use fictional names and numbers**

Use "Demo Tea Co.", "Spring Mountain Oolong 80g", fictional pricing bands, fictional suppliers, and no phone numbers, emails, tokens, or real client facts.

- [ ] **Step 2: Show the workflow shape**

Include project status, brief facts, asset authorization status, and supplier questions.

- [ ] **Step 3: Keep the demo intentionally incomplete**

Make it clear that production-sensitive details require supplier confirmation and compliance review.

### Task 5: Verification

**Files:**
- Read: `.gitignore`
- Read: `docs/github-release-audit.md`
- Run: `.claude\skills\packaging-os-maintainer\scripts\validate-packaging-os.cmd`

- [ ] **Step 1: Run publication-sensitive searches**

Run searches for likely secret markers and real-contact markers in the future public surface.

- [ ] **Step 2: Run Packaging OS validation**

Run the maintainer validation command and record whether it passes.

- [ ] **Step 3: Summarize remaining manual release blockers**

Confirm whether token rotation, spelling choice, license choice, and actual GitHub repository creation remain manual decisions.

