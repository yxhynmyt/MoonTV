# 开发工作流

> 基于 [Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) 的项目内工作流约定。

---

## 目录

1. [快速开始（先做这些）](#快速开始先做这些)
2. [工作流总览](#工作流总览)
3. [会话开始流程](#会话开始流程)
4. [开发流程](#开发流程)
5. [会话结束](#会话结束)
6. [文件说明](#文件说明)
7. [最佳实践](#最佳实践)

---

## 快速开始（先做这些）

### 第 0 步：初始化开发者身份（仅首次需要）

> **多开发者支持**：每位开发者 / Agent 都需要先初始化自己的身份。

```bash
# 检查是否已经初始化
python3 ./.trellis/scripts/get_developer.py

# 如果尚未初始化，执行：
python3 ./.trellis/scripts/init_developer.py <your-name>

# 例子：
python3 ./.trellis/scripts/init_developer.py cursor-agent
```

这会创建：

- `.trellis/.developer`：你的身份文件（gitignore，不提交）
- `.trellis/workspace/<your-name>/`：你的个人工作区目录

命名建议：

- 人类开发者：直接使用你的名字，例如 `john-doe`
- Cursor AI：`cursor-agent` 或 `cursor-<task>`
- Claude Code：`claude-agent` 或 `claude-<task>`
- iFlow cli：`iflow-agent` 或 `iflow-<task>`

### 第 1 步：理解当前上下文

```bash
# 一条命令获取完整上下文
python3 ./.trellis/scripts/get_context.py

# 或者手动检查：
python3 ./.trellis/scripts/get_developer.py      # 当前身份
python3 ./.trellis/scripts/task.py list          # 当前任务列表
git status && git log --oneline -10              # Git 状态
```

### 第 2 步：阅读项目规范 [MANDATORY]

**关键要求**：写任何代码前，都必须先读规范。

```bash
# 查看有哪些 package 和 spec layer
python3 ./.trellis/scripts/get_context.py --mode packages

# 阅读相关模块的 spec index
cat .trellis/spec/<package>/<layer>/index.md

# 始终阅读共享思考指南
cat .trellis/spec/guides/index.md
```

为什么这一步重要：

- 先确认你的改动会受哪些 spec layer 约束
- 先理解对应模块的编码规范
- 先建立对项目质量要求的整体认知

### 第 3 步：开始编码前，阅读具体规范文件（必做）

根据你的任务，继续阅读每个 spec index 中 **开发前检查清单** 列出的详细规范文件：

```bash
# index 只是导航入口，真正要读的是它指向的具体文件
cat .trellis/spec/<package>/<layer>/error-handling.md
cat .trellis/spec/<package>/<layer>/conventions.md
# 其余文件按“开发前检查清单”的要求继续读取
```

---

## 工作流总览

### 核心原则

1. **先读再写**：先理解上下文，再开始写
2. **遵循规范**：编码前必须阅读 `.trellis/spec/`
3. **增量开发**：一次只专注一个任务
4. **及时记录**：完成后及时更新追踪文件
5. **文档边界**：单个 journal 文件最多 2000 行

### 文件系统结构

```text
.trellis/
|-- .developer           # 开发者身份文件（gitignored）
|-- scripts/
|   |-- __init__.py
|   |-- common/
|   |   |-- __init__.py
|   |   |-- paths.py         # 路径工具
|   |   |-- developer.py     # 开发者管理
|   |   `-- git_context.py   # Git 上下文实现
|   |-- multi_agent/
|   |   |-- __init__.py
|   |   |-- start.py         # 启动 worktree agent
|   |   |-- status.py        # 监控 agent 状态
|   |   |-- create_pr.py     # 创建 PR
|   |   `-- cleanup.py       # 清理 worktree
|   |-- init_developer.py    # 初始化身份
|   |-- get_developer.py     # 获取当前身份
|   |-- task.py              # 管理任务
|   |-- get_context.py       # 获取会话上下文
|   `-- add_session.py       # 一键记录 session
|-- workspace/           # 开发者工作区
|   |-- index.md             # 工作区总索引
|   `-- {developer}/         # 每个开发者一个目录
|       |-- index.md         # 个人索引
|       `-- journal-N.md     # Journal 文件（顺序编号）
|-- tasks/               # 任务跟踪
|   `-- {MM}-{DD}-{name}/
|       `-- task.json
|-- spec/                # 编码前必须阅读的规范
|   |-- frontend/
|   |   |-- index.md
|   |   `-- *.md
|   |-- backend/
|   |   |-- index.md
|   |   `-- *.md
|   `-- guides/
|       |-- index.md
|       |-- cross-layer-thinking-guide.md
|       `-- *.md
`-- workflow.md         # 本文档
```

---

## 会话开始流程

### 第 1 步：获取会话上下文

使用统一上下文脚本：

```bash
# 一次性获取全部上下文
python3 ./.trellis/scripts/get_context.py

# 或获取 JSON 格式
python3 ./.trellis/scripts/get_context.py --json
```

### 第 2 步：阅读开发规范 [必做]

根据本次要改的内容，读取对应规范：

```bash
# 查看可用 package 和 spec layer
python3 ./.trellis/scripts/get_context.py --mode packages

# 读取相关模块的 spec index
cat .trellis/spec/<package>/<layer>/index.md

# 如果是跨层功能，还要读共享 guide
cat .trellis/spec/guides/cross-layer-thinking-guide.md
```

### 第 3 步：选择要开发的任务

使用任务管理脚本：

```bash
# 列出当前任务
python3 ./.trellis/scripts/task.py list

# 创建新任务（会自动创建 task 目录与 task.json）
python3 ./.trellis/scripts/task.py create "<title>" --slug <task-name>
```

---

## 开发流程

### 任务开发流

```text
1. 创建或选择任务
   -> python3 ./.trellis/scripts/task.py create "<title>" --slug <name>
   -> 或先 list 再继续已有任务

2. 按规范编写代码
   -> 阅读与你任务相关的 .trellis/spec/ 文档
   -> 如果跨层，再读 .trellis/spec/guides/

3. 自测
   -> 执行项目要求的 lint / test / typecheck
   -> 做必要的手动功能验证

4. 提交代码
   -> git add <files>
   -> git commit -m "type(scope): description"
      格式：feat/fix/docs/refactor/test/chore

5. 记录会话
   -> python3 ./.trellis/scripts/add_session.py --title "会话标题" --commit "hash"
```

### 代码质量检查清单

提交前至少应满足：

- [OK] Lint 通过
- [OK] Type check 通过（如果适用）
- [OK] 手动功能验证通过

项目特定检查项请继续参考：

- `.trellis/spec/<package>/<layer>/quality-guidelines.md`

---

## 会话结束

### 一键记录会话

代码提交后，执行：

```bash
python3 ./.trellis/scripts/add_session.py \
  --title "会话标题" \
  --commit "abc1234" \
  --summary "本次会话摘要"
```

脚本会自动：

1. 检测当前 journal 文件
2. 如果超过 2000 行则新建文件
3. 追加本次 session 内容
4. 更新 `index.md` 中的统计和历史表

### 会话结束前检查清单

使用 `/trellis:finish-work` 逐项确认：

1. [OK] 代码已提交，commit message 符合约定
2. [OK] 已通过 `add_session.py` 记录 session
3. [OK] 没有 lint/test 错误
4. [OK] 工作目录干净，或明确标记为 WIP
5. [OK] 如果有新模式或教训，相关 spec 已更新

---

## 文件说明

### 1. `workspace/` - 开发者工作区

**用途**：记录每个 AI Agent / 开发者每次会话的工作内容。

结构：

```text
workspace/
|-- index.md              # 总索引（活跃开发者表）
`-- {developer}/
    |-- index.md          # 个人索引
    `-- journal-N.md      # Journal 文件（1, 2, 3...）
```

以下情况应更新：

- 每次 session 结束时
- 完成重要任务后
- 修复重要 bug 后

### 2. `spec/` - 开发规范

**用途**：沉淀项目实际采用的开发标准，保证长期一致性。

结构：

```text
spec/
|-- frontend/
|   |-- index.md
|   `-- *.md
|-- backend/
|   |-- index.md
|   `-- *.md
`-- guides/
    |-- index.md
    `-- *.md
```

以下情况应更新：

- 发现新的稳定模式
- 修复某个 bug，暴露出规范缺失
- 团队形成了新的约定

### 3. `tasks/` - 任务跟踪

每个任务目录都包含一个 `task.json`：

```text
tasks/
|-- 01-21-my-task/
|   `-- task.json
`-- archive/
    `-- 2026-01/
        `-- 01-15-old-task/
            `-- task.json
```

常用命令：

```bash
python3 ./.trellis/scripts/task.py create "<title>" [--slug <name>]   # 创建任务目录
python3 ./.trellis/scripts/task.py archive <name>                     # 归档到 archive/{year-month}/
python3 ./.trellis/scripts/task.py list                               # 列出活动任务
python3 ./.trellis/scripts/task.py list-archive                       # 列出已归档任务
```

---

## 最佳实践

### 应该做的事

1. **会话开始前**：

   - 运行 `python3 ./.trellis/scripts/get_context.py` 获取完整上下文
   - 阅读与你任务相关的 `.trellis/spec/`

2. **开发过程中**：

   - 按 `.trellis/spec/` 规范实现
   - 如果是跨层功能，主动使用 `/trellis:check-cross-layer`
   - 如果任务需要浏览器自动化、页面逆向、截图或 trace，先读 `frontend/playwright-guidelines.md`，优先使用 `$use-playwright`
   - 一次只处理一个任务
   - 频繁执行 lint、typecheck 和测试

3. **开发完成后**：
   - 使用 `/trellis:finish-work` 做收尾检查
   - 如果刚修过复杂 bug，使用 `/trellis:break-loop` 做复盘
   - 人类确认测试通过后再提交
   - 用 `add_session.py` 记录进展

### 不应该做的事

1. 不要跳过 `.trellis/spec/` 的阅读
2. 不要让单个 journal 文件超过 2000 行
3. 不要同时并行推进多个无关任务
4. 不要带着 lint/test 错误提交代码
5. 不要忘记把新模式或教训更新回 spec
6. AI 不应自己执行 `git commit`

---

## 快速参考

### 开发前的必读文档

| 任务类型                | 必读文档                               |
| ----------------------- | -------------------------------------- |
| 前端开发                | `frontend/index.md` 及其指向的相关文档 |
| 后端开发                | `backend/index.md` 及其指向的相关文档  |
| 浏览器自动化 / 页面逆向 | `frontend/playwright-guidelines.md`    |
| 跨层功能                | `guides/cross-layer-thinking-guide.md` |

### Commit 约定

```bash
git commit -m "type(scope): description"
```

`type` 可选：

- `feat`
- `fix`
- `docs`
- `refactor`
- `test`
- `chore`

`scope` 使用模块名，例如 `auth`、`api`、`ui`。

### 常用命令

```bash
# 会话管理
python3 ./.trellis/scripts/get_context.py
python3 ./.trellis/scripts/add_session.py

# Task 管理
python3 ./.trellis/scripts/task.py list
python3 ./.trellis/scripts/task.py create "<title>"

# Browser automation
$use-playwright

# Slash commands
/trellis:finish-work
/trellis:break-loop
/trellis:check-cross-layer
```

---

## 总结

遵循这套工作流可以带来：

- [OK] 多次会话之间的连续性
- [OK] 更稳定的一致性与代码质量
- [OK] 可追踪的任务进展
- [OK] 持续积累到 spec 中的项目知识
- [OK] 更透明的团队协作

**核心理念**：先读再写、遵守规范、及时记录、沉淀经验
