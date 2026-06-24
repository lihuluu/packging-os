# AI Concept Assets Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an AI concept asset layer to Packaging OS so visual-direction image/graphic content can produce traceable draft assets without treating them as production-ready files.

**Architecture:** Extend the existing Layer 4 visual flow rather than adding a new skill. `visual-system-builder` creates AI concept asset tasks, `illustration-generator` executes them into `03_Design/02_Assets/AI_Concepts/`, and `asset-register.md` records authorization and usage status.

**Tech Stack:** Markdown-based Claude Skills, Packaging OS templates, existing governance validation scripts.

---

### Task 1: Update Visual System Builder

**Files:**
- Modify: `.claude/skills/visual-system-builder/SKILL.md`
- Modify: `.claude/skills/visual-system-builder/assets/visual-direction-sheet.md`
- Modify: `.claude/skills/visual-system-builder/assets/asset-register-template.md`

- [ ] Add AI concept asset task responsibilities to the skill description and workflow.
- [ ] Add explicit rules that AI outputs are drafts, not final delivery assets.
- [ ] Add an “AI 概念素材任务” section to the visual direction template.
- [ ] Add AI-specific columns to the asset register template.

### Task 2: Update Illustration Generator

**Files:**
- Modify: `.claude/skills/illustration-generator/SKILL.md`

- [ ] Add a project-integrated output mode under `03_Design/02_Assets/AI_Concepts/{task-id}/`.
- [ ] Rename output documents for project integration: `ai-concept-brief.md`, `prompts/prompt.md`, `variants/`, `selection-notes.md`.
- [ ] State that generated images are concept drafts and must be registered before project use.

### Task 3: Update Routing And Human-Facing Docs

**Files:**
- Modify: `.claude/skills/packaging-os/SKILL.md`
- Modify: `.claude/skills/packaging-os/references/workflow-map.md`
- Modify: `.claude/skills/packaging-os/references/output-routing.md`
- Modify: `CLAUDE.md`
- Modify: `README.md`
- Modify: `.claude/references/skills-test-cases.md`

- [ ] Update Layer 4 routing to include AI concept asset tasks.
- [ ] Update output routing for `AI_Concepts`.
- [ ] Add regression samples for visual-direction AI image/graphic tasks.
- [ ] Keep `illustration-generator` and `visual-system-builder` boundaries clear.

### Task 4: Validate

**Files:**
- Read: `.claude/skills/packaging-os-maintainer/scripts/validate-packaging-os.sh`

- [ ] Run `sh .claude/skills/packaging-os-maintainer/scripts/validate-packaging-os.sh`.
- [ ] Fix any governance failures caused by the change.
- [ ] Summarize validation result, risks, and next actions.
