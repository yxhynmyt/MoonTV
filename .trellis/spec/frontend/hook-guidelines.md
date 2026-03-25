# Hook 规范

> 说明 MoonTV 当前代码里 Hook 是如何真实使用的。

---

## 总览

当前项目没有独立的 `src/hooks` 目录，也没有大规模 custom hook 分层。

大部分有状态逻辑直接留在拥有它的 page 或 component 内。可复用的“Hook 式能力”目前主要有两种形态：

1. 与 provider 同文件或同区域定义的 Context accessor hook
2. 放在 `src/lib/*.ts` 或 `src/lib/*.client.ts` 里的 plain helper function

默认不要为了“看起来更抽象”就新建 custom hook。只有当逻辑已经真实复用，或者组件本身已经难以阅读时，才考虑抽取。

---

## 当前 Hook 模式

### Context accessor

目前真正意义上的 custom hook，基本都是 `useContext` 的轻封装：

- `useSite` in `src/components/SiteProvider.tsx`
- `useSidebar` in `src/components/Sidebar.tsx`

这种模式适合小范围共享 UI 状态，或者全局只读/弱可变的共享值。

### route 私有逻辑优先就地保留

如果逻辑只属于一个 route，就先留在对应 page 文件里，不要过早抽 Hook。

例子：

- `src/app/search/page.tsx`
  - query param sync, search history subscription, scroll state, and fetch flow stay local to the page
- `src/app/douban/page.tsx`
  - selector state, infinite-scroll observer state, and request orchestration stay in the route file
- `src/app/play/page.tsx`
  - player lifecycle, source preference, persistence, and playback state all stay in the route file

### 能用 plain function，就不要硬抽 Hook

如果逻辑可复用，但本身不依赖 React state / lifecycle，就应该保留为 plain utility，而不是伪装成 Hook。

例子：

- `src/lib/db.client.ts`
- `src/lib/auth.ts`
- `src/lib/utils.ts`

---

## 数据获取

MoonTV 当前还是手写异步编排，没有 React Query 或 SWR 这一层。

### 推荐的数据获取模式

在 client component 内部，优先使用这种模式：

1. 在 effect 或事件内定义内部 async function
2. 显式维护 loading state
3. 调用 `fetch(...)` 或 `src/lib/*` helper
4. 显式更新 `data`、`error`、`loading`
5. 如果 effect 注册了 listener、timer、observer，就必须清理

例子：

- `src/app/search/page.tsx`
  - fetches `/api/search`
- `src/app/douban/page.tsx`
  - calls `getDoubanCategories` and `getDoubanList`
- `src/components/ContinueWatching.tsx`
  - reads local/browser persistence through `getAllPlayRecords`
- `src/components/UserMenu.tsx`
  - posts to `/api/logout` and `/api/change-password`

### 浏览器侧同步模式

对于持久化在浏览器侧的数据，当前项目常用的模式是：

- 从 `src/lib/db.client.ts` 直接异步读取
- 用本地 React state 驱动渲染
- 通过 `subscribeToDataUpdates(...)` 在数据变更后同步多个视图

例子：

- `src/components/ContinueWatching.tsx`
- `src/app/page.tsx`
- `src/components/VideoCard.tsx`

---

## 命名约定

- Hook 名称必须以 `use` 开头。
- Context accessor 尽量简短，并以名词语义为主：
  - `useSite`
  - `useSidebar`
- effect 或事件流里的 async helper 应以动词命名：
  - `fetchConfig`
  - `loadInitialData`
  - `updatePlayRecords`
  - `fetchSearchResults`

如果以后真的要引入独立共享 Hook，优先靠近所属 domain 放置，不要新建一个泛化的“垃圾收纳区”。

---

## 何时抽取 custom hook

只有满足以下至少一项时，才创建 custom hook：

- 多个组件需要复用同一套有状态逻辑
- 一个组件因为 lifecycle 和渲染逻辑缠在一起而变得难读
- 某个 provider/context 需要独立的访问 API

不要为了“把代码挪出去”而机械抽 Hook。

---

## 常见错误

- 把一个 page 私有的 effect 链过早抽成“通用 Hook”。
- 在 Hook 里隐藏 URL / router 耦合，导致导航行为难以追踪。
- 没有 client boundary 或 runtime guard，就直接访问 `window`、`document`、`localStorage`。
- 忘记清理 subscription、timeout、animation frame 或 DOM listener。
- 本来 plain utility 更简单安全，却硬写成 Hook。

---

## 示例

- `src/components/SiteProvider.tsx`：最小化的 provider + accessor hook。
- `src/components/Sidebar.tsx`：局部 context 配合 `useSidebar` accessor。
- `src/app/search/page.tsx`：route 内部直接组合 Hook，没有为抽象而抽象。
- `src/app/douban/page.tsx`：`useCallback` 与 `useEffect` 直接服务于请求编排，没有额外包装。
- `src/lib/db.client.ts`：可复用的浏览器逻辑用 plain function 实现，而不是包装成 React Hook。
