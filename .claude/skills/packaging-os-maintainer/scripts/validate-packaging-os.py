#!/usr/bin/env python3
"""validate-packaging-os.py - Packaging OS governance validation (cross-platform).
Works on Python 3.8+ on Mac/Linux/Windows. Uses validation-config.json for heading definitions.
"""
from __future__ import annotations

import argparse
import io
import json
import re
import sys
from pathlib import Path

# Windows GBK 终端兼容：issue 含中文项目名/标题（如 HGT235_特级高山绿茶），print 默认走
# GBK 遇非 GBK 字符会 UnicodeEncodeError。非 UTF-8 终端时把 stdout/stderr 包成
# utf-8(errors=replace)；Mac/Linux 已是 UTF-8，if 条件不成立，零影响。
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf-8-sig"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if sys.stderr.encoding and sys.stderr.encoding.lower() not in ("utf-8", "utf-8-sig"):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


REQUIRED_DOCS = [
    "README.md",
    "CLAUDE.md",
    ".claude/references/skills-test-cases.md",
]

TEMP_FILE_PATTERNS = (".DS_Store", "Thumbs.db", "desktop.ini")
TEXT_SCAN_SUFFIXES = {".md", ".py", ".ps1", ".sh", ".cmd"}
OLD_ROOT_PATTERNS = (
    "/Users/lihulu/Library/CloudStorage/Dropbox/Design_OS",
    "/Users/lihulu/Documents/Packgaing_Design",
)
LEGACY_FILENAMES = {
    "project_tracker.md": "project-tracker.md",
    "structure-selection.md": "structure-decision.md",
}
LEGACY_PATH_SEGMENTS = {
    "03_Design/02_Structure/": "03_Design/04_Production/",
}
LEGACY_TEXT_PATTERNS = {
    "packging-os-maintainer": "packaging-os-maintainer",
    "packging-os": "packaging-os",
    "validate-design-os": "validate-packaging-os",
    "Design OS": "Packaging OS",
    "design-os": "packaging-os",
    "Packging OS": "Packaging OS",
    "Packging Design OS": "Packaging OS",
}

# 保留旧名属正当情况的文件（不判违规）：
# - CHANGELOG.md：记录改名事件本身，必须出现旧名
# - docs/releases/：历史发布快照，不可回溯改写（见 CHANGELOG 的 Kept As-Is 清单）
LEGACY_TEXT_ALLOWLIST_NAMES = {"CHANGELOG.md"}
LEGACY_TEXT_ALLOWLIST_PREFIXES = ("docs/releases/",)

RELATIVE_MARKDOWN_LINK_RE = re.compile(r"\]\(((?:\./|\.\./)[^)#?]+)\)")
ABSOLUTE_MARKDOWN_LINK_RE = re.compile(r"\]\((/[^)#?]+)\)")
README_SKILL_RE = re.compile(r"\|\s*`([^`]+)`\s*\|")


def load_config(script_dir: Path) -> dict:
    config_path = script_dir / "validation-config.json"
    if not config_path.exists():
        print(f"[fatal] Missing validation-config.json in {script_dir}", file=sys.stderr)
        sys.exit(2)
    return json.loads(config_path.read_text(encoding="utf-8"))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def relpath(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def get_markdown_links(path: Path) -> list[str]:
    content = read_text(path)
    return RELATIVE_MARKDOWN_LINK_RE.findall(content) + ABSOLUTE_MARKDOWN_LINK_RE.findall(content)


def test_markdown_links(base_path: Path, display_path: str, issues: list[str]) -> None:
    for link in get_markdown_links(base_path):
        target = Path(link) if link.startswith("/") else (base_path.parent / link).resolve()
        if not target.exists():
            issues.append(f"[broken-link] {display_path} -> {link}")


def test_required_headings(template_path: Path, headings: list[str], issues: list[str], root: Path) -> None:
    if not template_path.exists():
        issues.append(f"[missing-template] {relpath(template_path, root)}")
        return
    content = read_text(template_path)
    for heading in headings:
        if heading not in content:
            display = heading.lstrip("# ")
            issues.append(f"[missing-heading] '{display}' in {relpath(template_path, root)}")


def test_project_doc_headings(
    project_root: Path,
    filename: str,
    headings: list[str],
    issues: list[str],
    root: Path,
) -> None:
    if not project_root.exists():
        return
    for path in sorted(project_root.rglob(filename)):
        content = read_text(path)
        for heading in headings:
            if heading not in content:
                display = heading.lstrip("# ")
                issues.append(f"[missing-heading] '{display}' in {relpath(path, root)}")


def is_temp_file(path: Path) -> bool:
    name = path.name
    return (
        name in TEMP_FILE_PATTERNS
        or name.startswith("~$")
        or name.endswith(".tmp")
        or ".tmp." in name
        or name.endswith(".bak")
        or name.endswith(".log")
        or (name == ".gitkeep" and path.is_file() and path.stat().st_size == 0)
    )


def test_temp_files(root: Path, issues: list[str]) -> None:
    for path in sorted(root.rglob("*")):
        if path.is_file() and is_temp_file(path):
            issues.append(f"[temp-file] {relpath(path, root)}")
        elif path.is_dir() and path.name == "__pycache__":
            issues.append(f"[temp-dir] {relpath(path, root)}")



def test_legacy_filenames(project_root: Path, issues: list[str], root: Path) -> None:
    if not project_root.exists():
        return
    for path in sorted(project_root.rglob("*")):
        if not path.is_file():
            continue
        replacement = LEGACY_FILENAMES.get(path.name)
        if replacement:
            issues.append(f"[legacy-filename] {relpath(path, root)} -> should be {replacement}")


def test_legacy_path_references(scan_roots: list[Path], issues: list[str], root: Path) -> None:
    for scan_root in scan_roots:
        if not scan_root.exists():
            continue
        for md_path in sorted(scan_root.rglob("*.md")):
            content = read_text(md_path)
            for legacy_path, replacement in LEGACY_PATH_SEGMENTS.items():
                if legacy_path in content:
                    issues.append(f"[legacy-path] {relpath(md_path, root)} -> '{legacy_path}' should be '{replacement}'")


def test_legacy_text_references(root: Path, issues: list[str]) -> None:
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix not in TEXT_SCAN_SUFFIXES:
            continue
        display_path = relpath(path, root)
        if path.name in {"validate-packaging-os.py", "validate-packaging-os.ps1"}:
            continue
        if display_path in LEGACY_TEXT_ALLOWLIST_NAMES or display_path.startswith(LEGACY_TEXT_ALLOWLIST_PREFIXES):
            continue
        content = read_text(path)
        for legacy_text, replacement in LEGACY_TEXT_PATTERNS.items():
            if legacy_text in content:
                issues.append(f"[legacy-name] {display_path} -> '{legacy_text}' should be '{replacement}'")
        for old_root in OLD_ROOT_PATTERNS:
            if old_root in content:
                issues.append(f"[old-root-path] {display_path} -> {old_root}")


DECISION_ID_RE = re.compile(r"^D-\d{3}$")


def test_decision_log_ids(path: Path, issues: list[str], root: Path, *, allow_placeholder: bool = False) -> None:
    if not path.exists():
        issues.append(f"[missing-template] {relpath(path, root)}")
        return

    in_decision_table = False
    for line_number, line in enumerate(read_text(path).splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("| 编号 |"):
            in_decision_table = True
            continue
        if not in_decision_table:
            continue
        if not stripped.startswith("|"):
            if stripped:
                in_decision_table = False
            continue

        parts = [part.strip() for part in stripped.strip("|").split("|")]
        if not parts:
            continue
        first_cell = parts[0]
        if first_cell in {"", "------"} or set(first_cell) <= {"-"}:
            continue
        if allow_placeholder and first_cell == "D-___":
            continue
        if not DECISION_ID_RE.match(first_cell):
            issues.append(
                f"[decision-id-format] {relpath(path, root)}:{line_number} -> first column should be D-NNN, got '{first_cell}'"
            )


def test_project_decision_log_ids(project_root: Path, issues: list[str], root: Path) -> None:
    if not project_root.exists():
        return
    for path in sorted(project_root.rglob("decision-log.md")):
        test_decision_log_ids(path, issues, root, allow_placeholder=True)


def parse_markdown_table_first_column(path: Path) -> set[str]:
    entries: set[str] = set()
    for line in read_text(path).splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        parts = [part.strip() for part in stripped.strip("|").split("|")]
        if len(parts) < 2:
            continue
        first_cell = parts[0]
        if first_cell in {"Project", "---", ""}:
            continue
        entries.add(first_cell)
    return entries


def test_coverage_sync(root: Path, issues: list[str]) -> None:
    projects_dir = root / "Workspace" / "Projects"
    coverage_file = root / "Workspace" / "Knowledge" / "Operations" / "coverage" / "project-knowledge-coverage.md"
    session_file = root / "Workspace" / "Knowledge" / "Operations" / "current" / "current-review-session.md"
    log_draft_file = root / "Workspace" / "Knowledge" / "Operations" / "current" / "current-review-log-draft.md"

    if not projects_dir.exists():
        return

    project_names = {
        path.name
        for path in projects_dir.iterdir()
        if path.is_dir() and not path.name.startswith(".")
    }

    if coverage_file.exists():
        coverage_projects = parse_markdown_table_first_column(coverage_file)
        for project_name in sorted(project_names):
            if project_name not in coverage_projects:
                issues.append(f"[coverage-missing] {relpath(coverage_file, root)} -> missing project: {project_name}")
        unknown_coverage_projects = sorted(
            project for project in coverage_projects if project not in project_names
        )
        for project_name in unknown_coverage_projects:
            issues.append(f"[coverage-unknown] {relpath(coverage_file, root)} -> unknown project: {project_name}")

    if session_file.exists():
        session_projects = parse_markdown_table_first_column(session_file)
        unknown_session_projects = sorted(
            project for project in session_projects if project not in project_names and project != "Done"
        )
        for project_name in sorted(project_names):
            if project_name not in session_projects:
                issues.append(f"[session-missing] {relpath(session_file, root)} -> missing project: {project_name}")
        for project_name in unknown_session_projects:
            issues.append(f"[session-unknown] {relpath(session_file, root)} -> unknown project: {project_name}")

    if log_draft_file.exists():
        for line in read_text(log_draft_file).splitlines():
            stripped = line.strip()
            if not re.match(r"^- P\d+:", stripped):
                continue
            _, _, value = stripped.partition(":")
            for chunk in value.split(","):
                project_name = chunk.strip()
                if project_name.lower() == "none" or not project_name:
                    continue
                if project_name not in project_names:
                    issues.append(f"[log-draft-unknown] {relpath(log_draft_file, root)} -> unknown project: {project_name}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Packaging OS governance consistency.")
    parser.add_argument(
        "--root",
        default=None,
        help="Repository root. Defaults to the directory four levels above this script.",
    )
    args = parser.parse_args()

    script_path = Path(__file__).resolve()
    script_dir = script_path.parent
    root = Path(args.root).resolve() if args.root else script_path.parents[4]

    config = load_config(script_dir)
    project_memory_headings = config["projectMemoryHeadings"]
    retrospective_headings = config["retrospectiveHeadings"]
    knowledge_headings = config["knowledgeHeadings"]
    decision_log_headings = config["decisionLogHeadings"]

    issues: list[str] = []

    for doc in REQUIRED_DOCS:
        if not (root / doc).exists():
            issues.append(f"[missing-doc] {doc}")

    skill_root = root / ".claude" / "skills"
    if not skill_root.exists():
        issues.append("[missing-dir] .claude/skills")

    shared_glossary = root / ".claude" / "references" / "shared-field-glossary.md"
    if not shared_glossary.exists():
        issues.append("[missing-glossary] .claude/references/shared-field-glossary.md")

    skill_dirs: list[Path] = []
    if skill_root.exists():
        skill_dirs = sorted([path for path in skill_root.iterdir() if path.is_dir()])
        for skill_dir in skill_dirs:
            skill_md = skill_dir / "SKILL.md"
            if not skill_md.exists():
                issues.append(f"[missing-skill-md] {skill_dir.name}")
                continue
            test_markdown_links(skill_md, relpath(skill_md, root), issues)
            for md_path in skill_dir.rglob("*.md"):
                test_markdown_links(md_path, relpath(md_path, root), issues)

    readme = root / "README.md"
    if readme.exists():
        readme_skills = sorted(set(README_SKILL_RE.findall(read_text(readme))))
        actual_skills = sorted(path.name for path in skill_dirs)
        for skill in actual_skills:
            if skill not in readme_skills:
                issues.append(f"[readme-missing-skill] {skill}")

    packaging_skill = skill_root / "packaging-os" / "SKILL.md"
    packaging_scope_exclusions = {"packaging-os", "packaging-os-maintainer"}
    if packaging_skill.exists():
        packaging_content = read_text(packaging_skill)
        for skill_dir in skill_dirs:
            skill_name = skill_dir.name
            if skill_name in packaging_scope_exclusions:
                continue
            skill_token = f"`{skill_name}`"
            if skill_token not in packaging_content:
                issues.append(f"[router-missing-skill] packaging-os does not reference: {skill_name}")

    test_required_headings(
        skill_root / "project-memory-manager" / "assets" / "project-memory-card-template.md",
        project_memory_headings,
        issues,
        root,
    )
    test_required_headings(
        skill_root / "project-retrospective" / "assets" / "project-retrospective-template.md",
        retrospective_headings,
        issues,
        root,
    )
    test_required_headings(
        skill_root / "knowledge-synthesizer" / "assets" / "knowledge-synthesis-template.md",
        knowledge_headings,
        issues,
        root,
    )
    test_project_doc_headings(
        root / "Workspace" / "Projects",
        "project-memory-card.md",
        project_memory_headings,
        issues,
        root,
    )
    test_project_doc_headings(
        root / "Workspace" / "Projects",
        "project-retrospective.md",
        retrospective_headings,
        issues,
        root,
    )
    test_project_doc_headings(
        root / "Workspace" / "Projects",
        "knowledge-synthesis.md",
        knowledge_headings,
        issues,
        root,
    )

    # decision-log template + project doc headings
    test_required_headings(
        skill_root / "design-version-tracker" / "assets" / "decision-log-template.md",
        decision_log_headings,
        issues,
        root,
    )
    test_decision_log_ids(
        skill_root / "design-version-tracker" / "assets" / "decision-log-template.md",
        issues,
        root,
        allow_placeholder=True,
    )
    test_project_doc_headings(
        root / "Workspace" / "Projects",
        "decision-log.md",
        decision_log_headings,
        issues,
        root,
    )
    test_project_decision_log_ids(root / "Workspace" / "Projects", issues, root)

    test_temp_files(root, issues)
    # dashboard 已退役，不再校验
    test_legacy_filenames(root / "Workspace" / "Projects", issues, root)
    test_legacy_path_references(
        [
            root / "Workspace" / "Projects",
            root / "Workspace" / "Knowledge",
        ],
        issues,
        root,
    )
    test_legacy_text_references(root, issues)
    test_coverage_sync(root, issues)

    if issues:
        print(f"Packaging OS validation failed ({len(issues)} issues):", file=sys.stderr)
        for issue in issues:
            print(f"- {issue}", file=sys.stderr)
        return 1

    print("Packaging OS validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
