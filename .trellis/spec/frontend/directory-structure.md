# 目录结构规范

> 说明 MoonTV 当前前端代码的目录组织方式。

---

## 总览

当前项目采用 route-first 结构：`src/app` 负责路由与页面入口，`src/components` 放共享 UI 与 provider，`src/lib` 放共享逻辑、配置桥接和类型。

目前项目没有独立的 `src/features` 或 `src/hooks` 层。新增代码应优先贴合现有结构，而不是为单个需求引入一套全新的目录范式。

---

## 目录布局

```text
src/
|-- app/
|   |-- layout.tsx
|   |-- globals.css
|   |-- page.tsx
|   |-- search/page.tsx
|   |-- play/page.tsx
|   |-- douban/page.tsx
|   |-- admin/page.tsx
|   |-- login/page.tsx
|   `-- api/**/route.ts
|-- components/
|   |-- PageLayout.tsx
|   |-- Sidebar.tsx
|   |-- MobileBottomNav.tsx
|   |-- VideoCard.tsx
|   |-- SiteProvider.tsx
|   `-- ...
|-- lib/
|   |-- types.ts
|   |-- admin.types.ts
|   |-- auth.ts
|   |-- config.ts
|   |-- db.client.ts
|   |-- db.ts
|   |-- d1.db.ts
|   |-- redis.db.ts
|   |-- upstash.db.ts
|   `-- ...
`-- styles/
    |-- globals.css
    `-- colors.css
```

`src/` 之外的构建与部署辅助文件位于仓库根目录，例如 `scripts/`、`config.json`、`next.config.js`、`tailwind.config.ts`。

---

## 模块组织

### `src/app`

- 路由目录按 URL segment 组织，并保持小写，例如 `search`、`play`、`login`、`warning`。
- app 级外壳文件放在这里：
  - `src/app/layout.tsx`
  - `src/app/globals.css`
- route handler 与页面就近放在 `src/app/api/**/route.ts`。
- 当前代码库允许存在较重的 route 文件，例如：
  - `src/app/play/page.tsx`
  - `src/app/admin/page.tsx`
- 某些以客户端逻辑为主的页面，会在同一个文件里定义内部 `*Client` 组件，再由默认导出用 `Suspense` 包一层。

### `src/components`

- 复用 UI、布局壳子和轻量 provider 统一放这里。
- 当前目录基本是扁平的；除非复用规模已经足够大，否则不要引入很深的组件层级。
- 典型内容包括：
  - 布局壳子，例如 `PageLayout.tsx`
  - 导航组件，例如 `Sidebar.tsx`、`MobileBottomNav.tsx`
  - 复用卡片或选择器，例如 `VideoCard.tsx`、`CapsuleSwitch.tsx`、`EpisodeSelector.tsx`
  - provider，例如 `SiteProvider.tsx`、`ThemeProvider.tsx`

### `src/lib`

- 非视觉层的共享逻辑统一放这里。
- 通过文件名后缀表达运行时边界：
  - 浏览器专用 helper：`db.client.ts`
  - 存储适配器：`d1.db.ts`、`redis.db.ts`、`upstash.db.ts`
  - 服务端 / runtime config 桥接：`config.ts`
- 共享领域类型也在这里，例如 `types.ts`、`admin.types.ts`。

### `src/styles`

- `src/app/globals.css` 才是当前真正被应用入口使用的全局样式入口。
- `src/styles/*.css` 主要是历史 starter 材料或 token 文件，不是当前主样式入口。
- 不要把新的全局样式默认丢到 `src/styles/*`，除非你明确要把它接入应用入口。

---

## 命名约定

- 路由目录：小写，并贴合 URL 结构，例如 `src/app/search`。
- 组件文件：`PascalCase.tsx`，例如 `PageLayout.tsx`、`ThemeToggle.tsx`。
- 工具 / 服务文件：`camelCase.ts` 或 `dot-suffix.ts`，例如 `fetchVideoDetail.ts`、`db.client.ts`。
- 共享类型文件：使用清晰的名词命名，例如 `types.ts`、`admin.types.ts`。
- CSS 入口：应用级全局样式使用 `globals.css`，辅助 token 或历史样式文件可保留在 `src/styles`。

---

## 放置规则

- page 私有状态和 page 私有的异步编排逻辑，优先留在 route 文件本身。
- 可复用视觉组件放进 `src/components`。
- 非视觉共享逻辑放进 `src/lib`。
- 浏览器专用逻辑不要混入通用 server/shared 模块，必要时用 `.client.ts` 显式切开。
- 不要为了单个需求新建 `src/features`、`src/store`、`src/hooks` 这类顶层目录，当前项目并不采用这种组织方式。

---

## 常见错误

- 某个 UI 最初只服务于一个 route，就直接长期留在 `src/app`，结果后续复用时越来越乱。
- 把浏览器专用代码导入也会在服务端执行的文件里。
- 明明 `src/app/globals.css` 才是主入口，却把新全局样式继续堆进别的样式文件。
- 为单个功能强行引入 `features/`、`modules/`、`store/` 等平行架构，导致仓库结构不一致。

---

## 示例

- `src/app/page.tsx`：route-first 页面，页面内有本地客户端逻辑，再由 `Suspense` 包装。
- `src/app/search/page.tsx`：route 文件自身负责 query param、请求流程和页面状态。
- `src/components/PageLayout.tsx`：多个页面共享的布局外壳。
- `src/components/SiteProvider.tsx`：共享 provider 放在 `src/components`，而不是单独拆一层 app state 目录。
- `src/lib/db.client.ts`：浏览器侧持久化与缓存逻辑集中定义。
- `src/lib/config.ts`：runtime config、env 与存储后端之间的桥接层。
