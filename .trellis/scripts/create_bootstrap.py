#!/usr/bin/env python3
"""
Create Bootstrap Task for First-Time Setup.

Creates a guided task to help users fill in project guidelines
after initializing Trellis for the first time.

Usage:
    python3 create_bootstrap.py [project-type]

Arguments:
    project-type: frontend | backend | fullstack (default: fullstack)

Prerequisites:
    - .trellis/.developer must exist (run init_developer.py first)

Creates:
    .trellis/tasks/00-bootstrap-guidelines/
        - task.json    # Task metadata
        - prd.md       # Task description and guidance
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

from common.paths import (
    DIR_WORKFLOW,
    DIR_SCRIPTS,
    DIR_TASKS,
    get_repo_root,
    get_developer,
    get_tasks_dir,
    set_current_task,
)
from common.config import get_spec_base, resolve_package


# =============================================================================
# Constants
# =============================================================================

TASK_NAME = "00-bootstrap-guidelines"


# =============================================================================
# PRD Content
# =============================================================================

def write_prd_header() -> str:
    """Write PRD header section."""
    return """# Bootstrap: 补全项目开发规范

## 目的

欢迎使用 Trellis！这是你的第一个任务。

AI Agent 会通过 `.trellis/spec/` 理解你项目自己的编码约定。
**如果从空白开始，AI 更容易写出通用代码，而不是贴合你项目风格的代码。**

把这些规范补齐，是一次性的初始化投入，但会持续提升后续每一轮 AI 协作的质量。

---

## 你的任务

基于你**现有的代码库**，补全这些规范文件。
"""


def write_prd_backend_section(spec_base: str) -> str:
    """Write PRD backend section."""
    return f"""

### 后端规范

| 文件 | 需要记录的内容 |
|------|----------------|
| `.trellis/{spec_base}/backend/directory-structure.md` | route、service、utils 等不同文件的组织方式 |
| `.trellis/{spec_base}/backend/database-guidelines.md` | ORM、migration、query 模式、命名约定 |
| `.trellis/{spec_base}/backend/error-handling.md` | error 如何捕获、记录日志并返回 |
| `.trellis/{spec_base}/backend/logging-guidelines.md` | 日志级别、格式，以及应该记录什么 |
| `.trellis/{spec_base}/backend/quality-guidelines.md` | code review 标准、测试要求 |
"""


def write_prd_frontend_section(spec_base: str) -> str:
    """Write PRD frontend section."""
    return f"""

### 前端规范

| 文件 | 需要记录的内容 |
|------|----------------|
| `.trellis/{spec_base}/frontend/directory-structure.md` | Component / page / hook 的组织方式 |
| `.trellis/{spec_base}/frontend/component-guidelines.md` | 组件模式、props 约定 |
| `.trellis/{spec_base}/frontend/hook-guidelines.md` | 自定义 hook 的命名和实现模式 |
| `.trellis/{spec_base}/frontend/state-management.md` | 状态库、模式，以及不同状态该放在哪里 |
| `.trellis/{spec_base}/frontend/type-safety.md` | TypeScript 约定与类型组织方式 |
| `.trellis/{spec_base}/frontend/quality-guidelines.md` | lint、测试、可访问性要求 |
"""


def write_prd_footer() -> str:
    """Write PRD footer section."""
    return """

### 思考指南（可选）

`.trellis/spec/guides/` 目录里的 thinking guide 已经预填了一般性的最佳实践。
如果你的项目有自己的习惯或额外约束，可以继续按项目实际情况定制。

---

## 如何补全规范

### 第 0 步：优先从现有规范中导入（推荐）

很多项目其实已经在其他工具里记录过编码约定。开始从零写之前，先检查这些文件：

| 文件 / 目录 | 对应工具 |
|------|------|
| `CLAUDE.md` / `CLAUDE.local.md` | Claude Code |
| `AGENTS.md` | Codex / Claude Code / agent-compatible tools |
| `.cursorrules` | Cursor |
| `.cursor/rules/*.mdc` | Cursor（规则目录） |
| `.windsurfrules` | Windsurf |
| `.clinerules` | Cline |
| `.roomodes` | Roo Code |
| `.github/copilot-instructions.md` | GitHub Copilot |
| `.vscode/settings.json` -> `github.copilot.chat.codeGeneration.instructions` | VS Code Copilot |
| `CONVENTIONS.md` / `.aider.conf.yml` | aider |
| `CONTRIBUTING.md` | 通用项目约定 |
| `.editorconfig` | 编辑器格式化规则 |

如果这些文件存在，优先先读它们，再把相关编码约定提炼到对应的 `.trellis/spec/` 文件里。
相比完全从头写，这样会省很多时间。

---

### 第 1 步：分析代码库

可以让 AI 帮你从真实代码里归纳模式：

- “读取现有配置文件（CLAUDE.md、.cursorrules 等），把编码约定提炼到 `.trellis/spec/` 中”
- “分析我的代码库，并把你观察到的模式写成规范”
- “找出 error handling / component / API 模式并记录下来”

### 第 2 步：记录真实情况，而不是理想状态

写代码库**现在实际怎么做**，不要写成“希望以后怎么做”。
AI 需要匹配现有模式，而不是擅自引入一套新风格。

- **先看现有代码**：每种模式尽量找 2-3 个真实例子
- **带上文件路径**：引用真实文件作为例子
- **写出反模式**：团队明确不希望继续出现什么写法？

---

## 完成检查清单

- [ ] 已按项目类型补全规范
- [ ] 每份规范至少包含 2-3 个真实代码示例
- [ ] 已记录反模式

完成后执行：

```bash
python3 ./.trellis/scripts/task.py finish
python3 ./.trellis/scripts/task.py archive 00-bootstrap-guidelines
```

---

## 为什么这件事重要

完成之后：

1. AI 会更容易写出符合你项目风格的代码
2. 相关 `/trellis:before-*-dev` 命令能注入真实项目上下文
3. `/trellis:check-*` 命令会按你的实际标准做校验
4. 后续开发者（人类或 AI）上手会更快
"""


def write_prd(task_dir: Path, project_type: str, spec_base: str) -> None:
    """Write prd.md file."""
    content = write_prd_header()

    if project_type == "frontend":
        content += write_prd_frontend_section(spec_base)
    elif project_type == "backend":
        content += write_prd_backend_section(spec_base)
    else:  # fullstack
        content += write_prd_backend_section(spec_base)
        content += write_prd_frontend_section(spec_base)

    content += write_prd_footer()

    prd_file = task_dir / "prd.md"
    prd_file.write_text(content, encoding="utf-8")


# =============================================================================
# Task JSON
# =============================================================================

def write_task_json(task_dir: Path, developer: str, project_type: str, spec_base: str) -> None:
    """Write task.json file."""
    today = datetime.now().strftime("%Y-%m-%d")

    # Generate subtasks and related files based on project type
    if project_type == "frontend":
        subtasks = [
            {"name": "补全前端规范", "status": "pending"},
            {"name": "补充代码示例", "status": "pending"},
        ]
        related_files = [f".trellis/{spec_base}/frontend/"]
    elif project_type == "backend":
        subtasks = [
            {"name": "补全后端规范", "status": "pending"},
            {"name": "补充代码示例", "status": "pending"},
        ]
        related_files = [f".trellis/{spec_base}/backend/"]
    else:  # fullstack
        subtasks = [
            {"name": "补全后端规范", "status": "pending"},
            {"name": "补全前端规范", "status": "pending"},
            {"name": "补充代码示例", "status": "pending"},
        ]
        related_files = [f".trellis/{spec_base}/backend/", f".trellis/{spec_base}/frontend/"]

    task_data = {
        "id": TASK_NAME,
        "name": "Bootstrap 开发规范",
        "description": "为 AI Agent 补全项目开发规范",
        "status": "in_progress",
        "dev_type": "docs",
        "priority": "P1",
        "creator": developer,
        "assignee": developer,
        "createdAt": today,
        "completedAt": None,
        "commit": None,
        "subtasks": subtasks,
        "children": [],
        "parent": None,
        "relatedFiles": related_files,
        "notes": f"由 trellis init 创建的首次初始化任务（{project_type} 项目）",
        "meta": {},
    }

    task_json = task_dir / "task.json"
    task_json.write_text(json.dumps(task_data, indent=2, ensure_ascii=False), encoding="utf-8")


# =============================================================================
# Main
# =============================================================================

def main() -> int:
    """Main entry point."""
    # Parse project type argument
    project_type = "fullstack"
    if len(sys.argv) > 1:
        project_type = sys.argv[1]

    # Validate project type
    if project_type not in ("frontend", "backend", "fullstack"):
        print(f"Unknown project type: {project_type}, defaulting to fullstack")
        project_type = "fullstack"

    repo_root = get_repo_root()
    developer = get_developer(repo_root)

    # Check developer initialized
    if not developer:
        print("Error: Developer not initialized")
        print(f"Run: python3 ./{DIR_WORKFLOW}/{DIR_SCRIPTS}/init_developer.py <your-name>")
        return 1

    # Resolve spec base path (monorepo: spec/<package>, single-repo: spec)
    package = resolve_package(repo_root=repo_root)
    spec_base = get_spec_base(package, repo_root)

    tasks_dir = get_tasks_dir(repo_root)
    task_dir = tasks_dir / TASK_NAME
    relative_path = f"{DIR_WORKFLOW}/{DIR_TASKS}/{TASK_NAME}"

    # Check if already exists
    if task_dir.exists():
        print(f"Bootstrap task already exists: {relative_path}")
        return 0

    # Create task directory
    task_dir.mkdir(parents=True, exist_ok=True)

    # Write files
    write_task_json(task_dir, developer, project_type, spec_base)
    write_prd(task_dir, project_type, spec_base)

    # Set as current task
    set_current_task(relative_path, repo_root)

    # Silent output - init command handles user-facing messages
    # Only output the task path for programmatic use
    print(relative_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
