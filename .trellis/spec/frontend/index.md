# 前端开发规范

> 基于 MoonTV 当前前端代码库整理，更新日期为 2026-03-25。

---

## 项目快照

- Framework：Next.js 14 App Router
- 语言：TypeScript，开启 `strict: true`
- 样式：Tailwind CSS，主入口为 `src/app/globals.css`，另有少量全局 utility CSS
- 状态模型：优先使用本地 React state，小范围共享状态使用 Context，异步请求仍以手写流程为主，没有 React Query / SWR
- 质量工具：ESLint、Prettier、Jest config、Husky + lint-staged

这些文档描述的是项目“当前真实做法”，同时会注明代码库里仍然存在的历史包袱，而不是只写理想状态。

---

## 规范索引

| Guide                                         | 说明                                               | 状态   |
| --------------------------------------------- | -------------------------------------------------- | ------ |
| [目录结构](./directory-structure.md)          | 路由结构、共享目录、命名方式与文件放置规则         | Active |
| [组件规范](./component-guidelines.md)         | 组件结构、props、样式与可访问性规则                | Active |
| [Hook 规范](./hook-guidelines.md)             | 当前 Hook 使用方式、数据获取模式，以及何时抽取逻辑 | Active |
| [状态管理](./state-management.md)             | 本地 state、Context、URL state、持久化与同步方式   | Active |
| [质量规范](./quality-guidelines.md)           | 必做检查项、评审重点与常见回归风险                 | Active |
| [Playwright 指南](./playwright-guidelines.md) | 浏览器自动化、UI 流调试、截图与 trace 产物规范     | Active |
| [类型安全](./type-safety.md)                  | 共享类型、运行时边界与 TypeScript 约束             | Active |

---

## 开发前检查清单

修改前端代码前，至少先读这些文档：

1. 默认必读：
   - `directory-structure.md`
   - `component-guidelines.md`
   - `quality-guidelines.md`
2. 如果改动涉及以下任一项，还要读 `hook-guidelines.md` 与 `state-management.md`：
   - client page
   - `useEffect` / `useMemo` / `useCallback`
   - router query state
   - `localStorage`、cookie 或其他浏览器侧状态
3. 如果改动涉及以下任一项，还要读 `playwright-guidelines.md`：
   - 浏览器自动化
   - Playwright CLI
   - 截图、trace、pdf 等浏览器产物
   - 页面逆向、网络抓包、UI 流调试
4. 如果新增或修改以下内容，还要读 `type-safety.md`：
   - API payload shape
   - config object
   - 共享 DTO
   - context value
5. 如果改动跨越以下边界，还要读 `../guides/cross-layer-thinking-guide.md`：
   - `src/app/api`
   - `src/lib/config.ts`
   - `src/lib/db.client.ts`
   - 鉴权 cookie 或 runtime config 注入链路
6. 真正改代码前，先全局搜索已有用法：
   - route query name
   - storage key
   - runtime config field
   - shared type field

---

## 快速建立上下文的锚点文件

重新理解项目时，优先看这些文件：

- 路由与应用外壳：`src/app/layout.tsx`、`src/app/page.tsx`、`src/app/search/page.tsx`
- 共享布局与导航：`src/components/PageLayout.tsx`、`src/components/Sidebar.tsx`、`src/components/MobileBottomNav.tsx`
- 浏览器侧共享数据层：`src/lib/db.client.ts`、`src/lib/auth.ts`、`src/lib/types.ts`
- runtime config 与服务端配置桥接：`src/lib/config.ts`、`src/app/layout.tsx`

---

## 历史债务说明

- 项目虽然开启了 TypeScript strict mode，但旧文件中仍然存在 `any`、文件级 `eslint-disable`，以及 `src/app/play/page.tsx`、`src/app/admin/page.tsx` 这种超大路由文件。
- 这些模式应视为兼容性债务，而不是新代码的推荐默认值。
- 新改动应在不破坏现有结构的前提下，尽量缩小不安全边界和历史包袱。
