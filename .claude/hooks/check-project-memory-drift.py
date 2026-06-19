#!/usr/bin/env python3
"""Cross-platform equivalent of check-project-memory-drift.ps1.
Scans Workspace/Projects; flags project memory cards that lag behind the latest
project files. Silent exit when nothing is stale. Works on Mac and Windows."""
import sys
from pathlib import Path
from datetime import datetime

root = Path(__file__).resolve().parent.parent.parent  # .claude/hooks -> repo root
projects_root = root / "Workspace" / "Projects"

if not projects_root.exists():
    sys.exit(0)

IGNORED = {".DS_Store", "Thumbs.db", "desktop.ini", ".gitkeep", ".gitignore"}
drifted = []

for project in sorted(p for p in projects_root.iterdir() if p.is_dir()):
    card = project / "00_Project_Control" / "project-memory-card.md"

    latest = None  # (path, mtime)
    for f in project.rglob("*"):
        if not f.is_file():
            continue
        if "00_Project_Control" in f.relative_to(project).parts:
            continue
        if ".tmp." in f.name or f.name in IGNORED:
            continue
        m = f.stat().st_mtime
        if latest is None or m > latest[1]:
            latest = (f, m)

    if latest is None:
        continue

    latest_file, latest_mtime = latest
    fmt = lambda t: datetime.fromtimestamp(t).strftime("%Y-%m-%d %H:%M")

    if not card.exists():
        drifted.append((project.name, "missing card", "", fmt(latest_mtime),
                        str(latest_file.relative_to(project))))
        continue

    card_mtime = card.stat().st_mtime
    if latest_mtime > card_mtime + 60:  # 1 分钟
        drifted.append((project.name, "card may be stale", fmt(card_mtime),
                        fmt(latest_mtime), str(latest_file.relative_to(project))))

if not drifted:
    sys.exit(0)

print("<packging-os-reminder>")
print("Some project memory cards may be behind the latest project files. If the user "
      "request touches project status, project memory, dashboards, or handoff state, "
      "consider reminding them or updating the relevant card explicitly.")
for name, status, card_t, latest_t, latest_f in drifted[:5]:
    print(f"- {name}: {status}; card={card_t}; latest={latest_t}; latest_file={latest_f}")
if len(drifted) > 5:
    print(f"- ... plus {len(drifted) - 5} more project(s).")
print("</packging-os-reminder>")
sys.exit(0)
