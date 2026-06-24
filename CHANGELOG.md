# Changelog

All notable public releases of Packaging OS are recorded here.

## [Unreleased] - Rename Packging → Packaging

Corrected the historical misspelling "Packging" → "Packaging" across the entire system: documentation, skill IDs, script names, the auto-managed memory index, the GitHub remote, and the local repository directory.

### Renamed
- Skill directories and IDs: `packging-os` → `packaging-os`, `packging-os-maintainer` → `packaging-os-maintainer`.
- Governance scripts: `validate-packging-os.{py,sh,cmd}` → `validate-packaging-os.{py,sh,cmd}` (launchers' internal cross-references updated).
- Internal team-share folder and assets under `docs/team-share/packaging-os-value-share-2026-06-22/`.
- Auto-managed Claude Code memory file `project-packging-os-architecture.md` → `project-packging-os-architecture.md` (with `MEMORY.md` index synced).
- GitHub remote URL `lihuluu/packging-os.git` → `lihuluu/packaging-os.git` (2026-06-24: local `origin` updated, 9 pending commits pushed).
- Local repo directory `Packging_OS` → `Packaging_OS` on both Mac (`~/Library/CloudStorage/Dropbox/`) and Windows (`D:\Dropbox\`); Claude Code memory bucket migrated to match the new path.

### Kept As-Is (Historical / External)
- `docs/releases/2026-06-18-v0.1.0.md`, `docs/releases/2026-06-18-v0.1.1.md` — historical release notes recording the state at the time of release (including `Repository: lihuluu/packging-os`).
- `CHANGELOG.md` entries for v0.1.0 and v0.1.1 — kept verbatim as historical record.
- Git history commit messages — never rewritten.

## v0.1.1 - Demo Template Expansion

Date: 2026-06-18

Expanded `examples/demo-tea-project/` from a minimal 5-file demo into a complete 9-layer blank template set (21 files covering Layer 0-8). Each template has structured fields, placeholders, cost-evidence levels `[C0]-[C5]`, and compliance/asset/sample status slots. Project header uses 山隐·东方高端茶 as example placeholder.

Examples and documentation only — no changes to core skills, routing, CLAUDE.md, or template field definitions.

See the full release notes:

- `docs/releases/2026-06-18-v0.1.1.md`

## v0.1.0 - Initial Public Release

Date: 2026-06-18

Packging OS is now published as a public packaging-design workflow system built around Claude Skills.

See the full release notes:

- `docs/releases/2026-06-18-v0.1.0.md`

