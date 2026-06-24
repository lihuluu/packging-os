# Project Control Dashboard Implementation Plan（已退役 / 2026-06-15）

> 该计划对应的 HTML 仪表盘已于 2026-06-15 退役。本计划保留作为历史决策记录。

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a read-only static HTML project control dashboard that ranks Packaging OS projects by explainable priority and summarizes project cards plus the single allowed `project-tracker.md`.

**Architecture:** Add an independent Python generator beside the existing project dashboard scripts. It scans `Workspace/Projects`, parses `project-memory-card.md` and the unique per-project `project-tracker.md`, calculates an explainable score, and writes `Workspace/Projects/project-dashboard.html`.

**Tech Stack:** Python standard library, `unittest`, Markdown parsing by stable heading/table/list rules, static HTML/CSS/JavaScript with no external dependencies.

---

## File Structure

- Create `.claude/skills/project-memory-manager/scripts/build-project-visual-dashboard.py`: main static HTML generator and parsing/scoring logic.
- Create `.claude/skills/project-memory-manager/scripts/build-project-visual-dashboard.cmd`: Windows entrypoint mirroring existing script wrappers.
- Create `.claude/skills/project-memory-manager/scripts/test_build_project_visual_dashboard.py`: isolated regression tests.
- Output `Workspace/Projects/project-dashboard.html`: generated read-only dashboard.

The repository root is not a Git repository, so task checkpoints use test and output verification instead of commits.

## Task 1: Tracker Discovery And Markdown Parsing

**Files:**
- Create: `.claude/skills/project-memory-manager/scripts/test_build_project_visual_dashboard.py`
- Create: `.claude/skills/project-memory-manager/scripts/build-project-visual-dashboard.py`

- [ ] **Step 1: Write failing tests for tracker discovery and section parsing**

Create tests that build temporary project folders, import the generator module, and verify:

```python
def test_find_tracker_accepts_one_file_anywhere(self):
    tracker = self.write_doc("TeaProject", "03_Design/01_Working/project-tracker.md", "# Tracker\n")
    result = self.module.find_tracker(self.projects_dir / "TeaProject")
    self.assertEqual(result.status, "ok")
    self.assertEqual(result.path, tracker)

def test_find_tracker_reports_conflict_for_multiple_files(self):
    self.write_doc("TeaProject", "03_Design/01_Working/project-tracker.md", "# A\n")
    self.write_doc("TeaProject", "04_Final/project-tracker.md", "# B\n")
    result = self.module.find_tracker(self.projects_dir / "TeaProject")
    self.assertEqual(result.status, "conflict")
    self.assertEqual(len(result.conflicts), 2)

def test_extract_sections_reads_card_and_tracker_fields(self):
    card = "# 包装项目总卡\n\n## 项目摘要\n- 项目名称：岁藏天尖\n- 产品/品类：安化黑茶\n- 当前阶段：视觉方向优化中\n- 目标上市日期：2026-09-10\n\n## 下一步动作\n1. 生成 AI 草案\n\n## 风险\n- 周期紧凑\n"
    tracker = "# 包装项目推进表\n\n## 当前最大瓶颈\n**外箱实地试装**——需要本周安排。\n\n## 任务清单\n| 任务 | 优先级 | 负责人 | 前置条件 | 状态 |\n| --- | --- | --- | --- | --- |\n| 安排试装 | 🔴 最高 | 包装厂 | 实物 | ❌ 待安排 |\n"
    self.write_doc("TeaProject", "00_Project_Control/project-memory-card.md", card)
    self.write_doc("TeaProject", "03_Design/01_Working/project-tracker.md", tracker)
    project = self.module.collect_project(self.projects_dir / "TeaProject", self.root)
    self.assertEqual(project.name, "岁藏天尖")
    self.assertEqual(project.product, "安化黑茶")
    self.assertEqual(project.bottleneck, "外箱实地试装——需要本周安排。")
    self.assertEqual(project.next_action, "安排试装")
```

- [ ] **Step 2: Run tests and verify they fail because the module does not exist**

Run:

```powershell
python .claude\skills\project-memory-manager\scripts\test_build_project_visual_dashboard.py
```

Expected: FAIL or import error for missing `build-project-visual-dashboard.py`.

- [ ] **Step 3: Implement parser data types and functions**

Implement:

```python
@dataclass
class TrackerResult:
    status: str
    path: Path | None = None
    conflicts: list[Path] = field(default_factory=list)

def find_tracker(project_dir: Path) -> TrackerResult:
    trackers = sorted(project_dir.rglob("project-tracker.md"))
    if len(trackers) == 1:
        return TrackerResult(status="ok", path=trackers[0])
    if len(trackers) > 1:
        return TrackerResult(status="conflict", conflicts=trackers)
    return TrackerResult(status="missing")
```

Also implement heading extraction, bullet field extraction, table row parsing, `collect_project`, and UTF-8-safe file reading.

- [ ] **Step 4: Run tests and verify parser behavior passes**

Run:

```powershell
python .claude\skills\project-memory-manager\scripts\test_build_project_visual_dashboard.py
```

Expected: the Task 1 tests pass.

## Task 2: Priority Scoring And Status Reliability

**Files:**
- Modify: `.claude/skills/project-memory-manager/scripts/test_build_project_visual_dashboard.py`
- Modify: `.claude/skills/project-memory-manager/scripts/build-project-visual-dashboard.py`

- [ ] **Step 1: Write failing tests for scoring reasons**

Add tests verifying:

```python
def test_priority_score_explains_deadline_risk_task_and_bottleneck(self):
    card = "# 包装项目总卡\n\n## 项目摘要\n- 项目名称：HT2385\n- 当前阶段：商业交付\n- 目标上市日期：2026-06-30\n\n## 风险\n- 排期风险\n"
    tracker = "# 包装项目推进表\n\n## 当前最大瓶颈\n外箱实地试装\n\n## 任务清单\n| 任务 | 优先级 | 负责人 | 前置条件 | 状态 |\n| --- | --- | --- | --- | --- |\n| 安排包装厂实地试装时间 | 🔴 最高 | 包装厂 | 实物 | ❌ 待安排 |\n"
    self.write_doc("HT2385", "00_Project_Control/project-memory-card.md", card)
    self.write_doc("HT2385", "03_Design/01_Working/project-tracker.md", tracker)
    project = self.module.collect_project(self.projects_dir / "HT2385", self.root, today=date(2026, 6, 12))
    self.assertGreaterEqual(project.score, 70)
    self.assertEqual(project.priority, "高")
    self.assertTrue(any("距目标日期" in reason for reason in project.reasons))
    self.assertTrue(any("最高优先级任务" in reason for reason in project.reasons))
    self.assertTrue(any("当前瓶颈" in reason for reason in project.reasons))
```

- [ ] **Step 2: Implement scoring**

Implement deterministic scoring:

```python
def score_project(data: ProjectData, today: date) -> tuple[int, str, list[str]]:
    score = 0
    reasons = []
    days = days_until(data.deadline, today)
    if days is not None and days <= 30:
        score += 30
        reasons.append(f"距目标日期 {days} 天")
    elif days is not None and days <= 90:
        score += 15
        reasons.append(f"距目标日期 {days} 天")
    if data.risks:
        score += min(20, 8 + len(data.risks) * 4)
        reasons.append("存在风险节点")
    if data.high_tasks:
        score += min(25, len(data.high_tasks) * 15)
        reasons.append("存在最高优先级任务")
    if data.bottleneck:
        score += 15
        reasons.append("当前瓶颈未解除")
    if data.card_stale or data.tracker_stale:
        score += 10
        reasons.append("状态记录落后于最近产出")
    score = min(score, 100)
    priority = "高" if score >= 70 else "中" if score >= 40 else "低"
    return score, priority, reasons or ["暂无明显推进压力"]
```

- [ ] **Step 3: Run scoring tests**

Run:

```powershell
python .claude\skills\project-memory-manager\scripts\test_build_project_visual_dashboard.py
```

Expected: all parser and scoring tests pass.

## Task 3: Static HTML Generation

**Files:**
- Modify: `.claude/skills/project-memory-manager/scripts/test_build_project_visual_dashboard.py`
- Modify: `.claude/skills/project-memory-manager/scripts/build-project-visual-dashboard.py`

- [ ] **Step 1: Write failing tests for generated HTML**

Add tests verifying:

```python
def test_build_dashboard_html_contains_cards_links_and_details(self):
    self.write_doc("TeaProject", "00_Project_Control/project-memory-card.md", "# 包装项目总卡\n\n## 项目摘要\n- 项目名称：岁藏天尖\n- 产品/品类：安化黑茶\n- 当前阶段：视觉方向优化中\n- 目标上市日期：2026-09-10\n\n## 下一步动作\n1. 生成 AI 草案\n")
    self.write_doc("TeaProject", "03_Design/01_Working/project-tracker.md", "# 包装项目推进表\n\n## 当前最大瓶颈\n外箱实地试装\n")
    html = self.module.build_dashboard_html(self.root, today=date(2026, 6, 12))
    self.assertIn("<!doctype html>", html)
    self.assertIn("项目总控台", html)
    self.assertIn("岁藏天尖", html)
    self.assertIn("外箱实地试装", html)
    self.assertIn("project-memory-card.md", html)
    self.assertIn("project-tracker.md", html)
    self.assertIn("<details", html)
```

- [ ] **Step 2: Implement HTML renderer**

Render one static page with:

- summary metrics
- priority-sorted project cards
- reason chips
- status reliability warnings
- `<details>` expansion for milestones, high-priority tasks, critical path, supplier communication, risks, and data anomalies
- `file:///`-safe relative links from `Workspace/Projects/project-dashboard.html`

- [ ] **Step 3: Run HTML tests**

Run:

```powershell
python .claude\skills\project-memory-manager\scripts\test_build_project_visual_dashboard.py
```

Expected: all tests pass.

## Task 4: CLI Wrapper And Real Workspace Generation

**Files:**
- Create: `.claude/skills/project-memory-manager/scripts/build-project-visual-dashboard.cmd`
- Modify: `.claude/skills/project-memory-manager/scripts/build-project-visual-dashboard.py`
- Generate: `Workspace/Projects/project-dashboard.html`

- [ ] **Step 1: Add command-line entrypoint**

Implement `main()` with:

```python
parser.add_argument("--root", default=None)
parser.add_argument("--output", default=None)
```

Default root should be `Path(__file__).resolve().parents[4]`. Default output should be `Workspace/Projects/project-dashboard.html`.

- [ ] **Step 2: Add Windows wrapper**

Create:

```bat
@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
set "ROOT_DIR=%SCRIPT_DIR%..\..\..\.."

powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; $OutputEncoding = [System.Text.Encoding]::UTF8; python '%SCRIPT_DIR%build-project-visual-dashboard.py' --root '%ROOT_DIR%' %*; exit $LASTEXITCODE"
exit /b %ERRORLEVEL%
```

- [ ] **Step 3: Generate the real dashboard**

Run:

```powershell
.claude\skills\project-memory-manager\scripts\build-project-visual-dashboard.cmd
```

Expected output includes:

```text
Updated Workspace/Projects/project-dashboard.html
```

- [ ] **Step 4: Verify real workspace behavior**

Run:

```powershell
python .claude\skills\project-memory-manager\scripts\test_build_project_visual_dashboard.py
```

Expected: all tests pass.

Run:

```powershell
Select-String -Path Workspace\Projects\project-dashboard.html -Pattern "HT2385","项目总控台","project-tracker.md","追踪表冲突"
```

Expected: includes the title, HT2385, and tracker link. The conflict pattern should appear only if the real workspace has multiple trackers.

## Self-Review

- Spec coverage: the plan covers static generation, project card parsing, unique tracker scanning, priority score, explainable reasons, detail expansion, anomaly states, output path, and no Markdown writes.
- Placeholder scan: no placeholder task remains; each task lists concrete code behavior and commands.
- Type consistency: shared types are `TrackerResult` and project data returned by `collect_project`; later tasks use the same names.
