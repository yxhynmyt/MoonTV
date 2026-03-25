# 类型安全规范

> 说明当前前端项目在 TypeScript、共享类型和运行时边界上的约定。

---

## 总览

MoonTV 使用 TypeScript，并启用了 `strict: true`。当前 path alias 为：

- `@/*` -> `src/*`
- `~/*` -> `public/*`

共享领域类型集中放在 `src/lib`，组件本地和页面本地类型则尽量贴近拥有它们的文件。

代码库里仍有少量历史 `any`。除非运行时边界真的无法避免，否则新改动不应继续扩大这部分债务。

---

## 类型组织

### 共享领域类型

前端共享模型统一放在 `src/lib`。

当前例子：

- `src/lib/types.ts`
  - `SearchResult`, `DoubanItem`, `SkipConfig`, `IStorage`
- `src/lib/admin.types.ts`
  - admin configuration payloads
- `src/lib/db.client.ts`
  - persisted browser-side `PlayRecord` and `Favorite`

### 文件本地类型

如果某个类型不会在别处复用，就把它放在对应 component / page 文件附近。

例子：

- `VideoCardProps` in `src/components/VideoCard.tsx`
- `PageLayoutProps` in `src/components/PageLayout.tsx`
- `AuthInfo` in `src/components/UserMenu.tsx`
- `SiteConfig`, `DataSource`, `CustomCategory` in `src/app/admin/page.tsx`

### Global augmentation

只有在浏览器 / 运行时边界确实需要时，才使用局部 `declare global`。

例子：

- `window.__sidebarCollapsed` in `src/components/Sidebar.tsx`
- `HTMLVideoElement.hls` in `src/app/play/page.tsx`

---

## 校验与运行时边界

### 当前现状

虽然项目安装了 `zod`，但前端还没有形成统一的 runtime validation 约定。

当前运行时安全主要来自以下手段：

- explicit `response.ok` / `code === 200` checks
- default fallbacks for env/runtime config
- `try/catch` around `JSON.parse`
- defensive null checks before reading browser APIs or optional values

例子：

- `src/lib/auth.ts`
  - defensive cookie parsing
- `src/lib/config.ts`
  - normalizes config from env, runtime file, and storage
- `src/app/search/page.tsx`
  - checks API result shape before using it in UI flows

### 新代码的推荐方向

当某个边界接收的是未知外部数据时，应在它进入 app state 之前完成校验。

更适合放校验的边界位置：

- `src/app/api` 下的 route handler
- `src/lib` 里的共享 adapter
- config reader 和 cookie parser

如果使用 `zod`，应放在边界层，而不是放进深层 presentational component。

---

## 常见模式

- 对对象形状的契约优先使用 `interface`。
- 有限 UI mode 优先使用 literal union。
- 对有键控语义的集合，优先使用 `Record<string, T>`、`Map<K, V>`、`Set<T>`，而不是松散对象。
- 共享 async helper 要写明确返回类型。
- state 泛型优先收窄，不要隐式落成 `any`。

例子：

- literal unions in:
  - `src/components/VideoCard.tsx`
  - `src/app/play/page.tsx`
  - `src/components/UserMenu.tsx`
- generic helper in:
  - `getMostFrequent<T>` inside `src/components/VideoCard.tsx`
- typed maps/records in:
  - `src/app/play/page.tsx`
  - `src/components/ContinueWatching.tsx`
  - `src/lib/db.client.ts`

---

## 禁止模式

- 当数据形状本来可知时，还在应用代码里新增宽泛 `any`。
- 对外部 JSON 不做校验/归一化，就直接 `as SomeType` 强转。
- 本应由 `src/lib/types.ts` 或 `src/lib/admin.types.ts` 维护的共享 payload interface，却在多个 route / component 文件中重复定义。
- 把 non-null assertion 当作默认逃生口。
- 没有明确边界说明，就让浏览器侧 global value 泄漏进通用共享类型。

以下文件仍存在历史例外：

- `src/app/layout.tsx`
- `src/app/play/page.tsx`
- `src/lib/config.ts`
- `src/lib/db.client.ts`

这些都应视为兼容性债务，而不是新代码模板。

---

## 示例

- `src/lib/types.ts`：共享领域模型的 canonical 定义位置。
- `src/lib/auth.ts`：对不可信 cookie 输入做防御式解析。
- `src/components/VideoCard.tsx`：明确的 props typing 与局部泛型。
- `src/app/play/page.tsx`：union 类型的 UI mode 和受控的 global augmentation。
- `src/components/SiteProvider.tsx`：小而明确的 context value typing。
