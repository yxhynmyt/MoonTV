# Bootstrap: 补全项目开发规范

## 目的

欢迎使用 Trellis！这是你的第一个任务。

AI Agent 会通过 `.trellis/spec/` 理解你项目自己的编码约定。
**如果从空白开始，AI 更容易写出通用代码，而不是贴合你项目风格的代码。**

把这些规范补齐，是一次性的初始化投入，但会持续提升后续每一轮 AI 协作的质量。

---

## 你的任务

基于你**现有的代码库**，补全这些规范文件。

### 前端规范

| 文件                                             | 需要记录的内容                       |
| ------------------------------------------------ | ------------------------------------ |
| `.trellis/spec/frontend/directory-structure.md`  | Component / page / hook 的组织方式   |
| `.trellis/spec/frontend/component-guidelines.md` | 组件模式、props 约定                 |
| `.trellis/spec/frontend/hook-guidelines.md`      | 自定义 hook 的命名和实现模式         |
| `.trellis/spec/frontend/state-management.md`     | 状态库、模式，以及不同状态该放在哪里 |
| `.trellis/spec/frontend/type-safety.md`          | TypeScript 约定与类型组织方式        |
| `.trellis/spec/frontend/quality-guidelines.md`   | lint、测试、可访问性要求             |

### 思考指南（可选）

`.trellis/spec/guides/` 目录里的 thinking guide 已经预填了一般性的最佳实践。
如果你的项目有自己的习惯或额外约束，可以继续按项目实际情况定制。

---

## 如何补全规范

### 第 0 步：优先从现有规范中导入（推荐）

很多项目其实已经在其他工具里记录过编码约定。开始从零写之前，先检查这些文件：

| 文件 / 目录                                                                  | 对应工具                                     |
| ---------------------------------------------------------------------------- | -------------------------------------------- |
| `CLAUDE.md` / `CLAUDE.local.md`                                              | Claude Code                                  |
| `AGENTS.md`                                                                  | Codex / Claude Code / agent-compatible tools |
| `.cursorrules`                                                               | Cursor                                       |
| `.cursor/rules/*.mdc`                                                        | Cursor（规则目录）                           |
| `.windsurfrules`                                                             | Windsurf                                     |
| `.clinerules`                                                                | Cline                                        |
| `.roomodes`                                                                  | Roo Code                                     |
| `.github/copilot-instructions.md`                                            | GitHub Copilot                               |
| `.vscode/settings.json` -> `github.copilot.chat.codeGeneration.instructions` | VS Code Copilot                              |
| `CONVENTIONS.md` / `.aider.conf.yml`                                         | aider                                        |
| `CONTRIBUTING.md`                                                            | 通用项目约定                                 |
| `.editorconfig`                                                              | 编辑器格式化规则                             |

如果这些文件存在，优先先读它们，再把相关编码约定提炼到对应的 `.trellis/spec/` 文件里。
相比完全从头写，这样会省很多时间。

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
