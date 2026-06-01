# luogu-api-docs

洛谷（luogu.com.cn）非官方 API 文档。

**[阅读文档](docs/index.md)**

### 文档结构

```
├── docs/*                   # Markdown 文档
├── openapi/*                # OpenAPI 3.1 规范
├── luogutests/*             # API 测试套件
└── luogu-api.d.ts           # TypeScript 类型定义
```

### 快速开始

``````powershell
uv run luogutest                    # 一键运行全部测试
uv run python luogutests/problem.py # 运行单个模块
``````



### 通用约定

- 文本编码为 UTF-8
- `user-agent` 不能含有子串 `python-requests`（忽略大小写），也不能以 `mozilla/` 开头
- 非 GET 请求需要 `referer: https://www.luogu.com.cn/` 和 `x-csrf-token` 头
- CSRF 令牌从页面 HTML 的 `<meta name="csrf-token">` 获取


### 许可证

[UNLIENSE](UNLICENSE)