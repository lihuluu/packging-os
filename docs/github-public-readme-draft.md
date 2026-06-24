# Packaging OS

Packaging OS is a packaging-design studio workflow system built around Claude Skills.

It helps an independent packaging designer or small studio move from messy early briefs to structured packaging decisions, supplier communication, visual validation, prepress checks, production handoff, and retrospective knowledge capture.

The current default domain is tea packaging, but the backbone is meant to support broader packaging categories over time.

## What This Is

Packaging OS is not a traditional software application. It is an agent-readable operating system for packaging work:

- Claude Skills encode repeatable design and production workflows.
- Project memory cards keep each project's facts and decisions grounded.
- Templates turn recurring outputs into consistent working documents.
- Governance checks help maintain the system as it evolves.

## 9-Layer Workflow

1. Status Layer: project memory, trackers, version state.
2. Insight Layer: brief decomposition and research analysis.
3. Concept Layer: packaging concept directions.
4. Structure Layer: box type, format, and structural tradeoffs.
5. Visual Layer: visual system design and direction validation.
6. Material Layer: paper, finishing, and production feasibility.
7. Prepress Layer: file readiness and production risk checks.
8. Commercial Delivery Layer: supplier briefs, quote comparison, proposals, and schedules.
9. Retrospective Layer: project review and reusable knowledge capture.

## Repository Contents

```text
.claude/
  skills/          Claude Skills for each workflow layer
  references/      Shared standards and routing rules
  hooks/           Optional local automation helpers
Workspace/
  Templates/       Reusable packaging templates
  Knowledge/
    Library/       Public reusable knowledge notes
docs/              Specs, plans, release notes, and audits
examples/          Fictional demo projects
```

## Quick Start

1. Clone the repository.
2. Open it with Claude Code or another Claude Skills-compatible workflow.
3. Read `CLAUDE.md` for agent behavior rules.
4. Start with the demo project in `examples/demo-tea-project/`.
5. Create your own private project under `Workspace/Projects/`.

Private project data should stay local. The repository intentionally ignores `Workspace/Projects/**`.

## Safety Notes

Do not commit:

- `.claude/settings.local.json`
- `.env` files or tokens
- real client projects
- supplier contact details
- quotes, pricing sheets, proofs, final artwork, or production files
- AI-generated draft assets that have not been reviewed for rights and production use

## Status

This is an early public release candidate. The workflow is already useful for packaging-design operations, but category-specific modules, demo projects, and installation docs will continue to improve.

