# GitHub Publish Next Steps

This file is the final launch checklist after the release audit.

## 1. Decide The Public Name

Current local name: `Packging OS`.

Options:

- Keep `Packging OS` as a distinctive project name.
- Rename publicly before launch if a fully spelled English name is preferred.

Do this before the first public push. Repository renames are possible later, but early naming clarity is cleaner.

## 2. Rotate Local Secrets

`.claude/settings.local.json` is ignored, but it previously contained an external authorization value.

Before publishing:

- rotate that external token
- keep `.claude/settings.local.json` local only
- never copy local command allowlists into README examples

## 3. Choose License

Read `docs/license-options.md`.

Current decision: MIT.

The root `LICENSE` file should be included in the first commit.

## 4. Optional Local Workspace Cleanup

The public surface is safe, but whole-workspace validation still reports private workspace issues:

- temporary files under `Workspace/Projects/HGT235_特级高山绿茶500g/00_Project_Control/`
- missing `茶+康养调味茶系列` entries in two `Workspace/Knowledge/Operations/` files

These paths are ignored for GitHub, but cleaning them will make local validation green again.

## 5. Initialize Git

Run only after the decisions above:

```powershell
git init
git status --ignored
```

Review the ignored list carefully. Confirm these stay ignored:

- `.claude/settings.local.json`
- `.obsidian/`
- `Workspace/Projects/` real project contents
- `Workspace/Knowledge/Operations/`
- generated assets and final artwork

## 6. Stage The Public Surface

```powershell
git add README.md CLAUDE.md .gitignore
git add LICENSE
git add .claude/settings.json .claude/hooks .claude/references .claude/skills
git add Workspace/Projects/README.md Workspace/Templates Workspace/Knowledge/Library
git add docs examples
git status
```

## 7. Commit

```powershell
git commit -m "chore: prepare Packging OS public release"
```

## 8. Create GitHub Repo And Push

Create an empty GitHub repository, then connect it:

```powershell
git branch -M main
git remote add origin https://github.com/<your-account>/<repo-name>.git
git push -u origin main
```

Before pushing, run one final scan against staged files:

```powershell
git diff --cached --name-only
```
