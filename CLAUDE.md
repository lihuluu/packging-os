# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with this repository.

---

**关键信息 / Key Information:**
> **默认使用中文回复，除非用户明确要求其他语言。**
> Default to Chinese unless user explicitly requests otherwise.

---

---

**IMPORTANT: This is NOT a software code repository.** This is **Packging OS** — a packaging design studio workflow system built as Claude Skills. It manages packaging projects through a 9-layer workflow from brief to production.

**Domain Strategy:** Packging OS keeps a general packaging-design workflow backbone, because the long-term goal is an independent design studio that can expand into more categories. The current default business domain is **tea packaging design**. When the user does not name another category, interpret projects as tea SKUs, tea gift boxes, tea label systems, tea packaging production, or tea packaging version work.

If a request is clearly outside tea packaging, do not force it through tea-specific assumptions. Use the general workflow, call out that the category module is not yet specialized, and suggest what new category facts must be added before making production-sensitive recommendations.

---

## Architecture Overview

### 9-Layer Workflow

```
0. Status Layer    → project-memory-manager (single source of truth), design-version-tracker
1. Insight Layer   → brief-decomposer, research-analyzer
2. Concept Layer   → concept-generator
3. Structure Layer → structure-selector
4. Visual Layer    → visual-system-builder, visual-direction-validator（含 AI 概念素材草案层）
5. Material Layer  → material-finishing-advisor
6. Prepress Layer  → prepress-checker
7. Commercial Delivery → supplier-brief-writer, quotation-comparator, project-tracker, proposal-builder
8. Retrospective   → project-retrospective, knowledge-synthesizer
```

### Skill-Based System

All business logic lives in `.claude/skills/<skill-name>/`:

- `SKILL.md` — Entry point with frontmatter (name, description)
- `references/` — Frameworks, rules, reference materials
- `assets/` — Templates, forms, reusable outputs
- `scripts/` — Automation scripts for that skill only

### Two Distinct Modes

**Mode A: Working on a packaging project** — Use the appropriate skill based on the 9-layer workflow above. Default to the tea packaging domain unless the user explicitly names another category.

**Mode B: Maintaining Packging OS itself** — Use `packging-os-maintainer` when modifying:
- `.claude/skills/` (adding/modifying skills)
- `CLAUDE.md`, `README.md`, `.claude/references/skills-test-cases.md`
- Shared templates or field glossaries
- Validation scripts

## Common Commands

### Project Initialization

```bash
# Create a new packaging project with standard directory structure
python3 .claude/skills/packging-os-maintainer/scripts/init-project.py "Project Name"
```

This creates:
- `Workspace/Projects/<Project Name>/` with standard directories
- starter files: project-memory-card.md, project-tracker.md, asset-register.md, supplier-brief.md, compliance-review.md, sample-acceptance-record.md, decision-log.md, brief-decomposition.md, packaging-brief.md

### System Maintenance

```bash
# Validate Packging OS consistency (Windows, no Python required)
.claude\skills\packging-os-maintainer\scripts\validate-packging-os.cmd

# Validate Packging OS consistency (Mac/Linux, auto-selects python3/python/pwsh)
sh .claude/skills/packging-os-maintainer/scripts/validate-packging-os.sh

# Preview project temp files before deleting anything
.claude\skills\project-memory-manager\scripts\cleanup-project-temp-files.cmd
sh .claude/skills/project-memory-manager/scripts/cleanup-project-temp-files.sh

# Check which project memory cards are behind latest outputs
python3 .claude/skills/project-memory-manager/scripts/check-memory-drift.py --all
```

The `.cmd` and `.sh` launchers select the platform runtime; the underlying `.ps1` and `.py` validators share `validation-config.json` for heading definitions, keeping behavior consistent across platforms.
Project temp cleanup is dry-run by default; use `-Execute` on Windows or `--execute` on Mac/Linux only after reviewing the file list.

## Routing Rules

- **Unclear where to start** → `packging-os`
- **Need to update project status** → `project-memory-manager`
- **User names a specific stage** → Use that skill directly, don't route through `packging-os`
- **Request spans multiple stages** → Handle the most blocking bottleneck first, then name the next skill
- **Maintaining the system itself** → `packging-os-maintainer`
- **Category unclear** → assume tea packaging; ask only for missing SKU, tea type/process, specification, channel, packaging form, budget, timeline, and compliance details that materially affect the next decision
- **Non-tea category named** → keep the general workflow, but mark category-specific advice as assumptions until a category module or enough facts are provided

## Naming Conventions

| Context | Convention | Example |
|---------|-----------|---------|
| Skill directory & ID | `kebab-case` | `brief-decomposer` |
| Project document filename | `kebab-case` | `project-memory-card.md` |
| Project directory name | Can include Chinese/brands | `山隐_东方高端茶` |

Standard filenames (must not deviate):
- `project-memory-card.md`, `project-tracker.md`, `supplier-brief.md`, `quotation-comparison.md`
- `packaging-brief.md`, `brief-decomposition.md`, `positioning-summary.md`
- `concept-directions.md`, `visual-direction.md`, `structure-decision.md`
- `material-finishing-plan.md`, `prepress-review.md`, `proposal-outline.md`
- `asset-register.md`, `compliance-review.md`, `sample-acceptance-record.md`, `proofing-record.md`
- `packaging-cost-summary.md`
- `project-retrospective.md`, `knowledge-synthesis.md`
- `decision-log.md`

## Project Directory Structure

```
Workspace/Projects/{项目名称}/
├── 00_Project_Control/          ← project-memory-card.md (single source of truth), project-tracker.md
├── 01_Brief/                    ← Requirements
├── 02_Research/                 ← Analysis
├── 03_Design/                   ← Working files
│   ├── 01_Working/              ← Iterations, drafts
│   ├── 02_Assets/               ← Fonts, images, icons, AI concept drafts
│   │   ├── asset-register.md    ← asset source and authorization status
│   │   └── AI_Concepts/         ← AI-generated concept drafts, not finals
│   ├── 03_Presentation/         ← Proposals
│   ├── 04_Production/           ← Production docs
│   ├── 05_Renders/              ← Mockups
│   ├── 06_Proof_Record/         ← Sampling records
│   │   ├── prepress-review.md
│   │   ├── compliance-review.md
│   │   └── sample-acceptance-record.md
├── 04_Final/                    ← APPROVED FINALS ONLY
│   ├── 01_Print_Files/
│   ├── 02_Source_Files/
│   ├── 03_Assets/
│   ├── 04_Previews/
│   └── 05_Dielines/
└── 05_Retrospective/            ← Post-project review
```

## Output Requirements

Every response must:
1. Distinguish between `Known Facts` / `Assumptions` / `Recommendations`
2. Include `Risks` if recommendation affects cost, schedule, production, or compliance
3. End with `Next Actions` and recommended next skill
4. Use tables for comparing concepts, structures, materials, suppliers, schedules, or risks
5. Specify default archive path and recommended filename for reusable documents
6. Tag cost-related conclusions with evidence level [C0]-[C5] per [cost-evidence-standard.md](.claude/references/cost-evidence-standard.md); never output real cost without C3+ evidence
7. For commercial packaging outputs, surface compliance / asset authorization status when visual assets, AI concept drafts, label content, supplier files, samples, or final production are affected

## Validation Requirements

Before declaring work complete:

- **Modifying a skill**: Verify SKILL.md frontmatter, local references exist, routing is consistent with `packging-os`
- **Modifying templates**: Verify linked files exist, archive paths are correct
- **Modifying the system**: Run `validate-packging-os.cmd` on Windows or `validate-packging-os.sh` on Mac/Linux, check `README.md` and `.claude/references/skills-test-cases.md` consistency

## Phase Transition Rules

Never skip phases:
- Positioning unclear → No concept
- Structure undecided → No visual
- Material untested → No mass production

## Horizontal Commercial Checkpoints

Supplier engagement, cost awareness, and schedule risk are NOT exclusive to Layer 7. Every layer must check:

- **Layer 0**: Is MOQ / supplier status / approval authority / hard deadline documented? Cost ceiling tagged [C1]? Compliance, asset, and sample acceptance status recorded?
- **Layer 1**: Are channel, budget, batch size, hard deadline, and cost ceiling clear? Budget / cost evidence level? Label/compliance blockers identified?
- **Layer 2**: Has user resonance, shelf/e-commerce performance, and supply-chain dependency been validated? Cost variables identified [C0]?
- **Layer 3**: Have packing efficiency, sampling lead time, supplier capability, and structural cost been checked? Cost pressure decomposed [C0-C2]?
- **Layer 4**: Have e-commerce thumbnail, shelf far-view, print adaptability, regulatory info zone, AI concept draft status, and asset authorization been checked? Print complexity cost pressure [C0]?
- **Layer 5**: Have MOQ, material stability, process yield rate, cost, lead time, food-contact material status, and supplier documents been confirmed? Supplier quotation [C3+] or cost pressure [C0]?
- **Layer 6**: Have proof approval, color sign-off, file responsibility boundaries, compliance review, and sample acceptance been confirmed? Final cost confirmed [C4-C5]?
- **Layer 8**: Which commercial risks should be front-loaded into the next project's intake? Cost estimate vs. actual gap?

## Language

Default to Chinese unless user explicitly requests otherwise. Keep responses concise, structured, and decision-oriented.

## Forbidden

- Don't edit files when user asks for analysis/review only
- Don't install skills globally for project-level requests
- Don't repeat intake questions already answered by user/attachments
- Don't invent archive paths, filenames, supplier facts, production specs, or consumer insights
- Don't treat missing `rules/`, hooks, or CI as defects (this is a workflow system, not software)
- Don't output real cost, unit price, or "can be controlled under ¥XX" without C3+ evidence (see [cost-evidence-standard.md](.claude/references/cost-evidence-standard.md))
- Don't mark fonts, images, illustrations, AI-generated visuals, certification marks, or partner logos as final-delivery ready without recorded authorization status
- Don't place AI concept drafts directly in `04_Final`; route them through `03_Design/02_Assets/AI_Concepts/{task-id}/`, register them in `asset-register.md`, and treat them as reference until design refinement and prepress review are complete
- Don't mark commercial packaging as ready for mass production without sample / sign-off status; white sample, color sample, and bulk acceptance must be explicit when applicable
