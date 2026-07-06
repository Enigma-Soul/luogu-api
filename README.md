# 洛谷 API 文档

> 洛谷（luogu.com.cn）非官方 API 的多形态文档与测试套件

同一套 API 以三种形态保持同步：人工编写的 Markdown 文档、机器可读的 OpenAPI 3.1 规范、以及针对线上 API 的 Python 测试套件。

## 仓库结构

```
├── docs/                    # Markdown 文档 + luogu-api.d.ts（git submodule）
├── openapi/                 # OpenAPI 3.1 规范
│   ├── openapi.yaml         # 入口，聚合 paths/ 与 components/
│   ├── paths/*.yaml         # 各分类端点定义
│   └── components/schemas.yaml
├── luogutests/              # Python 测试套件（requests + uv）
└── pyproject.toml
```

`docs/` 是 git submodule，指向 [`Enigma-Soul/luogu-api-markdown`](https://github.com/Enigma-Soul/luogu-api-markdown)——上游 [`0f-0b/luogu-api-docs`](https://github.com/0f-0b/luogu-api-docs) 的人工编写镜像。`docs/*.md`、`docs/luogu-api.d.ts`、`docs/deno.json` 均来自此子模块，本仓库根目录不再保留副本。

克隆时带上子模块：

```powershell
git clone --recurse-submodules https://github.com/Enigma-Soul/luogu-api-openapi.git
# 已克隆的仓库补齐子模块
git submodule update --init docs
```

## 快速开始

测试套件通过 `uv` 运行，需在项目根目录放置 `cookie.json`（浏览器导出的 Cookie 数组）。

```powershell
uv run luogutest                     # 运行全部测试
uv run python luogutests/problem.py  # 运行单个模块
uv run python luogutests/article.py list mine  # 运行模块内指定 API
```

## 通用约定

> [!NOTE]
> - Base URL：`https://www.luogu.com.cn`
> - 文本编码 UTF-8
> - `user-agent` 不能含子串 `python-requests`（忽略大小写），也不能以 `mozilla/` 开头

> [!IMPORTANT]
> **非 GET 请求**需附带 `referer: https://www.luogu.com.cn/` 与 `x-csrf-token` 头（CSRF 令牌从页面 HTML 的 `<meta name="csrf-token">` 获取）。

响应主体有两种包装，请求时需对应声明：

| 响应类型 | 触发方式 | 数据位置 |
|---|---|---|
| `DataResponse` | 参数 `_contentOnly` 或头 `x-luogu-type: content-only` | `.currentData` |
| `LentilleDataResponse` | 头 `x-lentille-request: content-only` | `.data` |

## 文档目录

完整文档见 [`docs/index.md`](docs/index.md)，涵盖：

[题目](docs/problems.md) · [题单](docs/problem-sets.md) · [比赛](docs/contests.md) · [记录](docs/records.md) · [讨论](docs/discussions.md) · [动态](docs/activities.md) · [用户](docs/users.md) · [团队](docs/teams.md) · [私信](docs/chat.md) · [主题](docs/themes.md) · [图片](docs/images.md) · [IDE](docs/ide.md) · [剪贴板](docs/pastes.md) · [专栏](docs/articles.md) · [博客](docs/blog.md) · [身份验证](docs/auth.md) · [杂项](docs/misc.md) · [WebSocket](docs/ws.md)

## 许可证

[UNLICENSE](UNLICENSE)
