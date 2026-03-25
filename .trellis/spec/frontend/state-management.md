# 状态管理规范

> 说明当前前端项目如何管理本地状态、共享状态和持久化状态。

---

## 总览

MoonTV 当前采用的是比较直接的分层状态模型：

- 优先使用 component / page 本地 state
- 用 URL state 承载导航态和可分享筛选条件
- 用 Context 承载小范围共享值
- 用 `localStorage` 和 cookie 做持久化
- server state 仍然通过手写异步流程维护

当前代码库没有 Redux、Zustand、MobX 或 React Query。

---

## 状态分类

### 1. 本地 UI state

这是默认选项。

以下情况优先使用本地 `useState`：

- 视图切换
- loading 和 error
- 表单输入
- 临时 UI 状态
- route 私有的数据编排

例子：

- `src/app/search/page.tsx`
- `src/app/douban/page.tsx`
- `src/components/UserMenu.tsx`
- `src/components/CapsuleSwitch.tsx`

### 2. URL state

当某个状态应该出现在地址栏里，或者应该在刷新/分享后仍可恢复时，使用 Next navigation primitives。

例子：

- `useSearchParams` in `src/app/search/page.tsx`
- `useSearchParams` in `src/app/play/page.tsx`
- `usePathname` in `src/components/MobileBottomNav.tsx`
- `usePathname` + `useSearchParams` in `src/components/Sidebar.tsx`

### 3. 通过 Context 共享的小范围状态

Context 只用于小而明确、且被多个位置消费的值。

当前例子：

- `SiteProvider` / `useSite`
  - site name and announcement
- `SidebarContext` / `useSidebar`
  - collapsed state for sidebar-aware UI

当前项目没有中心化 global store。

### 4. 浏览器持久化状态

用户偏好和本地缓存优先放在浏览器存储里。

当前模式：

- `localStorage`
- theme 相关偏好
- proxy 设置
- optimization 开关
- sidebar 折叠状态
- cookies
- 通过 `src/lib/auth.ts` 处理 auth 信息
- 浏览器缓存层
  - `src/lib/db.client.ts`

### 5. 手写 server state

面向服务端的数据当前是手动拉取，并保存在需要它的 page / component 本地。

例子：

- `src/app/search/page.tsx`
- `src/app/douban/page.tsx`
- `src/app/admin/page.tsx`
- `src/components/UserMenu.tsx`

---

## 何时提升为共享状态

只有满足以下任一条件时，才应该把状态提升到局部组件之外：

- 多个相距较远的组件需要同时读取同一个值
- 该值本质上属于 app shell
- 持续的 prop drilling 已经让状态归属不清晰

在 MoonTV 当前代码里，这通常意味着用 Context，而不是引入 store library。

Context 适合承载：

- 以只读为主的共享配置
- layout shell state
- 应用级展示元信息

除非现有模式已经明显无法支撑真实场景，否则不要主动引入 Redux / Zustand 风格的状态管理。

---

## Server State 与同步

### Fetching

- `loading`、`error`、`data` 要显式存在。
- 边界优先放在 route handler 或 `src/lib/*` helper。
- 请求编排尽量贴近真正渲染结果的 page。

### Synchronization

对于 `favorites`、`play records`、`search history` 这类浏览器侧持久化数据：

- 统一从 `src/lib/db.client.ts` 读取
- 统一通过它写入
- 多个组件需要保持一致时，使用 `subscribeToDataUpdates(...)`

例子：

- `src/components/ContinueWatching.tsx`
- `src/app/page.tsx`
- `src/components/VideoCard.tsx`

### Runtime config

只读的部署配置 / runtime config 统一在 `src/app/layout.tsx` 里通过 `window.RUNTIME_CONFIG` 注入一次。

适合放进去的内容：

- storage type
- feature flag
- proxy URL
- custom category

除非组件真的需要“本地覆盖值并持久化”，否则不要把这些值复制成多个独立数据源。

---

## 派生状态

能做派生状态时，就不要重复保存一份源状态的镜像。

当前例子：

- `aggregatedResults` in `src/app/search/page.tsx`
- `aggregateData` and `config` in `src/components/VideoCard.tsx`
- `getRequestParams` and selection-derived request behavior in `src/app/douban/page.tsx`

`useMemo` / `useCallback` 只在计算昂贵、需要稳定 handler、或者 effect dependency 需要稳定引用时按需使用，不要机械地到处加。

---

## 常见错误

- 同一个值同时存在于 URL param、本地 state、`localStorage` 中，却没有同步规则。
- 仅仅因为一个 page 内多个 sibling 需要，就把 route 私有状态提升进 Context。
- 本地 state 或 Context 就能解决的问题，却直接引入 global store。
- optimistic UI 保存失败后，没有把界面回滚。
  - `src/app/admin/page.tsx` 里有失败后回滚 toggle 的例子
- 在 server render 阶段直接读浏览器存储，没有 guard。
- 没有充分理由却使用 module-level mutable state。
  - `src/components/Sidebar.tsx` 里的 `window.__sidebarCollapsed` 是避免闪烁的特例，不是通用模式

---

## 示例

- `src/components/SiteProvider.tsx`：最小化的共享 Context state。
- `src/components/Sidebar.tsx`：本地 state 持久化到 `localStorage`，再辅以轻量 Context。
- `src/app/search/page.tsx`：本地 route state + URL state + 浏览器持久化并存。
- `src/components/ContinueWatching.tsx`：client cache 配合 subscription 同步。
- `src/app/layout.tsx`：为全局只读设置注入 runtime config。
