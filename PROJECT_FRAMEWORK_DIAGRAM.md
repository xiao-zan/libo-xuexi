# 项目框架关系图

这个仓库的外层目录很薄，核心项目位于 `zero-to-tech/`。前端是 Next.js App Router，后端是 FastAPI，`data/site.js` 作为前端本地兜底内容，`backend/history.json` 是后端分析记录的本地文件存储。

## 1. 目录与路由总览

```mermaid
flowchart TB
  Repo[("hellocode/")]
  Repo --> ZT["zero-to-tech/"]

  ZT --> App["app/ Next.js App Router"]
  ZT --> Components["components/ React 组件"]
  ZT --> Css["css/ 样式表"]
  ZT --> Data["data/site.js 前端兜底内容"]
  ZT --> Backend["backend/ FastAPI 后端"]
  ZT --> Out["out/ 静态导出产物"]

  App --> Layout["app/layout.jsx 全站外壳 + CSS 注入"]
  App --> RootPage["app/page.jsx 路由 /"]
  App --> TextLabPage["app/text-lab/page.jsx 路由 /text-lab"]

  RootPage --> HomeView["components/HomeView.jsx"]
  TextLabPage --> TextLabView["components/TextLabView.jsx"]

  Backend --> Main["backend/main.py API 服务"]
  Backend --> Handmade["backend/handmade.py 早期手写 HTTP 示例"]
  Backend --> History[("backend/history.json 历史记录")]
```

## 2. 页面组件关系

```mermaid
flowchart TB
  Layout["app/layout.jsx"] --> Main["<main className=\"page-content\">"]
  Main --> HomePage["/ app/page.jsx"]
  Main --> TextLabPage["/text-lab app/text-lab/page.jsx"]

  HomePage --> HomeView["HomeView.jsx"]
  TextLabPage --> TextLabView["TextLabView.jsx"]

  HomeView --> Nav1["Nav.jsx"]
  HomeView --> Heading["PageHeading.jsx"]
  HomeView --> Grid1["AnimatedCardGrid.jsx"]
  HomeView --> SiteData["data/site.js: home"]

  TextLabView --> Nav2["Nav.jsx"]
  TextLabView --> Heading2["PageHeading.jsx"]
  TextLabView --> Grid2["AnimatedCardGrid.jsx"]
  TextLabView --> InputCard["InputCard.jsx"]
  TextLabView --> ResultCard["ResultCard.jsx"]
  TextLabView --> SiteData2["data/site.js: textLab"]

  TextLabView -. "result state 状态提升" .-> InputCard
  TextLabView -. "result prop" .-> ResultCard
  InputCard -. "onResult(result)" .-> TextLabView
```

## 3. 前后端数据流

```mermaid
sequenceDiagram
  participant Browser as 浏览器 / Next.js
  participant Env as .env.local
  participant API as FastAPI backend/main.py
  participant NLP as pypinyin + SnowNLP
  participant Hist as history.json

  Env-->>Browser: NEXT_PUBLIC_API_BASE_URL=http://localhost:8000

  Browser->>API: GET /api/profile
  API-->>Browser: profile JSON
  Browser-->>Browser: HomeView 用 profile 覆盖 site.js 兜底内容

  Browser->>API: POST /api/analyze { text }
  API->>NLP: 计算拼音和情感分数
  NLP-->>API: pinyin + score
  API->>Hist: append result + created_at
  API-->>Browser: { text, score, label, pinyin, created_at }
  Browser-->>Browser: TextLabView setResult -> ResultCard 展示
```

## 关键结论

- 路由层由 Next.js App Router 接管：`app/page.jsx` 对应 `/`，`app/text-lab/page.jsx` 对应 `/text-lab`。
- `app/layout.jsx` 是全站外壳，负责 `<html>`、`<body>`、页面容器和全局 CSS 导入。
- `HomeView.jsx` 先使用 `data/site.js` 中的 `home` 作为初始数据，再用 `GET /api/profile` 的结果覆盖展示。
- `TextLabView.jsx` 持有 `result` state：`InputCard.jsx` 发请求并把结果通过 `onResult` 交回父组件，`ResultCard.jsx` 再通过 prop 显示结果。
- `backend/main.py` 是实际 API 入口，提供 `/api/profile`、`/api/analyze`、`/api/history`；`/api/analyze` 会把分析记录追加到 `backend/history.json`。
- `backend/handmade.py` 是更早期的手写 HTTPServer 示例，只提供 `/api/profile`，不是当前主流程。
- `vite.config.js` 仍保留在目录里，但 `package.json` 的脚本只运行 `next dev/build/start`，所以当前主框架是 Next.js，不是 Vite。
