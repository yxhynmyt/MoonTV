# 组件规范

> 说明 MoonTV 当前前端代码中组件是如何组织和实现的。

---

## 总览

当前项目以 function component、Tailwind utility class 和“谁拥有交互，谁拥有本地状态”为主。

组件文件通常是自包含的，结构大致如下：

1. 按需添加 `'use client'`
2. imports
3. 本地 `interface` / helper type
4. 组件实现
5. 与该组件强相关的小型 helper function 或局部子组件

---

## 组件结构

### Client boundary

- 只有在文件实际使用 hooks、浏览器 API、事件处理器或 client-only library 时，才添加 `'use client'`。
- 当前项目里正确使用 client boundary 的例子：
  - `src/components/ThemeToggle.tsx`
  - `src/components/Sidebar.tsx`
  - `src/components/UserMenu.tsx`
- 不要因为父组件是 client component，就把整棵子树都标成 client-only。

### 文件形态

- props 定义要贴近组件本身。
- 一个文件默认只放一个主组件。
- 如果 helper 与组件强耦合，可以就地保留，不必强拆出去：
  - `ThemeToggle.tsx` keeps `setThemeColor` in the same file
  - `VideoCard.tsx` keeps variant config and aggregate logic in the same file
  - `Sidebar.tsx` keeps `Logo` local because it only serves the sidebar

### Export 方式

- 对复用型叶子组件，当前项目更常用 default export：
  - `PageLayout.tsx`
  - `Sidebar.tsx`
  - `VideoCard.tsx`
- provider 或 utility 风格组件常用 named export：
  - `ThemeProvider.tsx`
  - `GlobalErrorIndicator.tsx`
  - `SiteProvider.tsx`

---

## Props 约定

- props 对象统一使用 `interface <ComponentName>Props`。
- `children` 类型写成 `React.ReactNode` 或 `ReactNode`。
- 优先使用明确的可选字段，而不是模糊的“大杂烩对象”。
- 已知的 mode / variant 优先用 literal union。

当前例子：

- `VideoCardProps` in `src/components/VideoCard.tsx`
  - uses an explicit `from` union: `'playrecord' | 'favorite' | 'search' | 'douban'`
- `PageLayoutProps` in `src/components/PageLayout.tsx`
  - keeps `activePath` optional and defaults it in the component signature
- `SiteProvider` props in `src/components/SiteProvider.tsx`
  - type `children` and provider values explicitly

对新代码的要求：

- 对可选展示型 props，优先在参数解构里给默认值。
- props 只暴露组件真正需要的契约，不要把整份 route state 对象整体透传给子组件，除非子组件确实依赖全部内容。

---

## 样式模式

- 默认样式方案是把 Tailwind utility class 直接写进 `className`。
- dark mode class 直接跟随组件 markup 一起写。
- 响应式行为通常直接编码在同一个 `className` 里。
- 只有在值是动态的，或者依赖浏览器环境时，才用 inline `style`：
  - `env(safe-area-inset-bottom)`
  - dynamic indicator width/left values
  - backdrop filter settings

项目中的典型例子：

- `src/components/PageLayout.tsx`
  - uses responsive grid/flex classes and safe-area padding
- `src/components/MobileBottomNav.tsx`
  - mixes Tailwind with safe-area inline styles
- `src/components/CapsuleSwitch.tsx`
  - uses dynamic inline style for the sliding indicator
- `src/app/globals.css`
  - contains shared app-wide utilities such as `scrollbar-hide` and view transition animation support

---

## 组合规则

- 只有当父组件本身就是 layout 或 provider 时，才优先通过 `children` 做组合。
- 对可复用的卡片、选择器类组件，优先用明确 props，而不是 render props。
- route 级编排逻辑留在 page 内，传给子组件的只应是它实际需要的数据和动作。
- 如果一个视觉模式会在多个 route 复用，就迁移到 `src/components`，不要在多个 page 里复制 markup。

---

## 可访问性

- 结构型组件应尽量使用语义化容器：
  - `main` in `PageLayout.tsx`
  - `nav` in `MobileBottomNav.tsx`
  - `section` in `ContinueWatching.tsx`
- 纯图标按钮必须提供可访问的 label。
  - 正例：`ThemeToggle.tsx`
  - 正例：`GlobalErrorIndicator.tsx`
- 移动端可点击区域不能太小，当前导航和操作按钮通常保持在 `40px` 到 `56px` 左右。
- hover / active / focus 反馈需要可见，不能把交互状态做成“看起来没变化”。

---

## 常见错误

- 实际只有一个叶子组件需要浏览器 API，却把整棵组件树都加上 `'use client'`。
- 做了一个可复用组件，却在内部偷偷读取 route param、`window` 或 `localStorage`，导致契约不透明。
- 忘记为 theme、portal、browser storage 相关逻辑加 mounted guard。
  - 参考 `ThemeToggle.tsx`
  - 参考 `UserMenu.tsx`
- 样式只考虑桌面端，遗漏移动端导航、安全区或 dark mode。
- 把 `src/app/play/page.tsx` 这种历史大文件当成新组件应该效仿的目标尺寸。

---

## 示例

- `src/components/PageLayout.tsx`：带有结构语义和响应式布局的共享页面外壳。
- `src/components/VideoCard.tsx`：有明确 variant 和派生显示逻辑的复用卡片。
- `src/components/ThemeToggle.tsx`：体量较小、带 mounted guard 的 client 组件。
- `src/components/UserMenu.tsx`：带 portal / modal 交互、显式本地状态管理的 client 组件。
- `src/components/SiteProvider.tsx`：足够轻量的 provider + accessor 模式，没有过度设计。
