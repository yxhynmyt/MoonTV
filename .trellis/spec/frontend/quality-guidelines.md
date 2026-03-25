# 质量规范

> 说明 MoonTV 前端代码在质量、验证和评审上的最低要求。

---

## 总览

当前项目主要通过这些机制保证质量：

- ESLint
- Prettier
- TypeScript strict mode
- Husky + lint-staged
- 手动 UI regression testing
- 在有测试文件时，通过 Jest configuration 执行单测

目前仓库里虽然已经有 Jest setup，但还没有提交到仓库的 `src/**/*.test.*` 文件，所以代码评审质量和手动回归仍然非常重要。

---

## 必跑命令

只要是有意义的前端改动，至少跑：

- `pnpm lint`
- `pnpm typecheck`

以下命令按改动内容决定是否要跑：

- `pnpm test`
- `pnpm format:check`

如果你修改了共享工具逻辑、route payload 结构、或者复杂的客户端持久化行为，优先四个都跑。

---

## 禁止模式

- 没有明确、局部、可解释理由时，新增宽泛的 `eslint-disable` 或 `@ts-ignore`。
- 在共享 / 服务端代码里，未加 client boundary 或 runtime guard 就访问浏览器 API。
- 明明需要 `.client.ts` 分层，却把 server-only 逻辑导入 client component。
- 在 URL param、本地 state、runtime config、`localStorage` 之间悄悄制造多个数据真源。
- 新增的复用 UI 没有考虑移动端布局、dark mode 或 safe-area。
- 没有先搜索全局用法，就直接复制 storage key、query param name 或 config field name。

旧文件里确实存在历史违规写法，但不要把它们视为新代码默认标准。

---

## 必须遵守的模式

- 交互型 page 和数据驱动组件必须显式处理 loading、error、empty state。
- effect 里创建的 subscription、timeout、animation frame、DOM event listener 必须清理。
- import 顺序遵循 `simple-import-sort`。
- 格式化必须与当前 Prettier config 保持一致：
  - single quotes
  - semicolons
  - 2-space indentation
  - JSX single quotes
- 对 `window`、`document`、`localStorage`、`document.cookie` 的访问必须有 guard。
- 可恢复的 UI 失败优先走现有反馈通道：
  - admin 流程优先使用 `SweetAlert2`
  - 全局客户端错误优先走 `GlobalErrorIndicator` / `globalError` event

---

## 测试要求

### 当前最低要求

- `lint` 和 `typecheck` 必跑。
- 如果改动触及纯逻辑、容易回归的数据转换，且可以独立隔离出来，就应补自动化测试。
- UI 相关改动必须做手动验证，因为当前自动化覆盖仍然偏弱。

### 手动回归检查清单

前端改动后，至少针对相关范围验证：

- desktop and mobile layout
- dark and light theme behavior when the touched component supports both
- route/query persistence for pages using `useSearchParams`
- `localStorage` / cookie backed behavior
- favorites, play records, and search history synchronization if touched
- admin save and rollback paths if touched

### 适合补 Jest 测试的内容

- `src/lib` 下的 pure helper
- 数据归一化、聚合逻辑
- 边界解析逻辑
- 小型、无状态的格式化 helper

---

## Code Review 清单

- 改动是否遵守了 server / client boundary？
- 浏览器专用 API 是否都加了 guard？
- loading / error / empty state 是否仍然正确？
- 是否引入了新的重复数据真源？
- dark mode、移动端布局和 safe-area 行为是否仍然正确？
- import 是否已排序，类型是否足够明确？
- 如果共享 type 或 storage key 变化了，所有使用点是否都已更新？
- 对当前改动是否有合理的手动或自动化回归验证？

---

## 示例

- `src/app/search/page.tsx`：显式管理 loading 和结果状态切换。
- `src/components/ContinueWatching.tsx`：正确清理 subscription，并处理 empty state。
- `src/components/ThemeToggle.tsx`：client-only theme 逻辑带 mounted guard。
- `src/components/MobileBottomNav.tsx`：只在移动端显示，并处理 safe-area。
- `src/app/admin/page.tsx`：存在 optimistic UI + 失败回滚，是评审时必须重点看的区域。
