# 工作区索引

> 记录所有开发者与 AI Agent 的工作区会话信息。

---

## 概览

这个目录用于追踪项目内各位开发者与 AI Agent 的工作记录，重点包括个人索引和 journal 文件。

### 目录结构

```text
workspace/
|-- index.md              # 本文件，总索引
`-- {developer}/          # 每位开发者一个目录
    |-- index.md          # 个人索引，记录会话历史
    `-- journal-N.md      # Journal 文件（按 1, 2, 3... 顺序递增）
```

---

## 活跃开发者

| 开发者 | 最后活跃时间 | 会话数 | 当前活跃文件   |
| ------ | ------------ | ------ | -------------- |
| `lhw`  | 2026-03-25   | 0      | `journal-1.md` |

---

## 开始使用

### 新开发者

运行初始化脚本：

```bash
python3 ./.trellis/scripts/init_developer.py <your-name>
```

脚本会：

1. 创建你的身份文件（gitignored）
2. 创建你的工作区目录
3. 创建你的个人索引
4. 创建初始 journal 文件

### 已初始化的开发者

1. 获取当前开发者名称：

   ```bash
   python3 ./.trellis/scripts/get_developer.py
   ```

2. 阅读你的个人索引：
   ```bash
   cat .trellis/workspace/$(python3 ./.trellis/scripts/get_developer.py)/index.md
   ```

---

## 记录规则

### Journal 文件规则

- 每个 journal 文件最多 2000 行
- 达到上限后新建 `journal-{N+1}.md`
- 创建新文件后，同步更新个人 `index.md`

### 会话记录格式

每次会话至少应包含：

- 摘要：一句话概述本次工作
- 分支：本次工作的分支
- 主要改动：本次修改了什么
- Git 提交：相关 commit hash 和说明
- 后续事项：下一步需要做什么

---

## 会话模板

记录会话时使用下面的格式：

```markdown
## 会话 {N}: {标题}

**日期**: YYYY-MM-DD
**任务**: {task-name}
**分支**: `{branch-name}`

### 摘要

{一句话摘要}

### 主要改动

- {改动 1}
- {改动 2}

### Git 提交

| 哈希      | 说明             |
| --------- | ---------------- |
| `abc1234` | {commit message} |

### 测试

- [OK] {测试结果}

### 状态

[OK] **已完成** / # **进行中** / [P] **阻塞**

### 后续事项

- {下一步 1}
- {下一步 2}
```

---

**语言约定**：路径、文件名、命令、脚本名、类型名等技术标识保持英文；说明性正文统一使用中文。
