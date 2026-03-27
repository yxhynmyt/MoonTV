---
name: use-playwright
description: 'Run browser automation in MoonTV with the installed playwright skill, following the project-specific Trellis rules for PowerShell, artifacts, and CLI-first usage.'
---

# Use Playwright in MoonTV

Use this skill when the task needs a real browser for UI debugging, browser automation, screenshots, traces, or page reverse-engineering.

## Before Running

1. Read `.trellis/spec/frontend/playwright-guidelines.md`.
2. Confirm `npx` is available:

```powershell
node --version
npm --version
npx --version
```

3. Create an artifact directory under `output/playwright/<label>/`.

## MoonTV Rules

- Default to Playwright CLI workflows, not `@playwright/test`.
- Prefer the installed external `playwright` skill.
- If `bash` is unavailable in PowerShell, use the equivalent `npx --yes --package @playwright/cli playwright-cli ...` command directly.
- Keep screenshots, traces, PDFs, and related notes under `output/playwright/<label>/`.
- Re-snapshot after navigation or significant DOM changes.

## Standard Loop

```powershell
$label = "replace-with-task-label"
$artifactDir = Join-Path $PWD "output/playwright/$label"
New-Item -ItemType Directory -Force -Path $artifactDir | Out-Null
Push-Location $artifactDir

npx --yes --package @playwright/cli playwright-cli open https://example.com --headed
npx --yes --package @playwright/cli playwright-cli snapshot
npx --yes --package @playwright/cli playwright-cli click e3
npx --yes --package @playwright/cli playwright-cli snapshot

Pop-Location
```

## Reverse-Engineering Focus

For reverse-engineering tasks, prioritize:

1. `open`
2. `snapshot`
3. `console`
4. `network`
5. `tracing-start` / `tracing-stop`

Summarize findings back into the task PRD or the final response instead of leaving them only in artifacts.
