# luogu-api-docs

洛谷（luogu.com.cn）非官方 API 文档。

**[阅读文档](docs/index.md)**

## 文档结构

```
├── docs/                    # Markdown 文档
│   ├── index.md             # 总览与通用约定
│   ├── problems.md          # 题目 API
│   ├── problem-sets.md      # 题单 API
│   ├── contests.md          # 比赛 API
│   ├── records.md           # 记录 API
│   ├── discussions.md       # 讨论 API
│   ├── activities.md        # 动态 API
│   ├── users.md             # 用户 API
│   ├── teams.md             # 团队 API
│   ├── chat.md              # 私信 API
│   ├── articles.md          # 专栏 API
│   ├── blog.md              # 博客 API
│   ├── themes.md            # 主题 API
│   ├── images.md            # 图片 API
│   ├── ide.md               # IDE API
│   ├── pastes.md            # 剪贴板 API
│   ├── auth.md              # 身份验证 API
│   ├── misc.md              # 杂项 API
│   └── ws.md                # WebSocket API
├── openapi/                 # OpenAPI 3.1 规范
│   ├── openapi.yaml         # 根文件
│   ├── paths/               # 按 API 分组的路径定义
│   └── components/          # 共享 Schema、参数、安全方案
└── luogu-api.d.ts           # TypeScript 类型定义
```

## 快速开始

### 获取题目列表（GET）

```bash
curl -G "https://www.luogu.com.cn/problem/list" \
  --header "x-lentille-request: content-only" \
  --data-urlencode "type=P" \
  --data-urlencode "keyword=模板"
```

### 发送私信（POST）

```bash
curl -X POST "https://www.luogu.com.cn/api/chat/new" \
  --header "content-type: application/json" \
  --header "referer: https://www.luogu.com.cn/" \
  --header "x-csrf-token: YOUR_CSRF_TOKEN" \
  --cookie "_uid=YOUR_UID; __client_id=YOUR_CLIENT_ID" \
  --data '{"user":206953,"content":"Hi"}'
```

## 通用约定

- 文本编码为 UTF-8
- `user-agent` 不能含有子串 `python-requests`（忽略大小写），也不能以 `mozilla/` 开头
- 非 GET 请求需要 `referer: https://www.luogu.com.cn/` 和 `x-csrf-token` 头
- CSRF 令牌从页面 HTML 的 `<meta name="csrf-token">` 获取

## 许可证

[Unlicense](UNLICENSE)

---

## API 测试套件

> 覆盖 17 个模块、170+ 个接口的自动化测试

### 快速开始

在项目根目录放置 `cookie.json`（从浏览器导出 Cookie）：

```json
[{"name":"_uid","value":"...","domain":".luogu.com.cn"}, ...]
```

```bash
uv run luogutest                    # 一键运行全部测试
uv run python luogutests/problem.py # 运行单个模块
```

### 交互控制

写入操作（提交代码、发帖、删除等）需要手动确认：

| 按键 | 动作 |
|------|------|
| `y` | 确认本次 |
| `a` | 确认本次 + 后续全部 |
| `n` / 回车 | 跳过本次 |
| `q` | 跳过后续全部 |
| `Ctrl+C` | 跳过当前 |

涉及验证码的接口会自动保存图片到 `captcha.jpg` 并打开，输入 `r` 刷新。

### 文件结构

```
luogutests/
├── base.py         # LuoguClient、log、confirm、captcha
├── run_all.py      # 一键运行入口
├── problem.py      # 题目 (13)
├── training.py     # 题单 (12)
├── contest.py      # 比赛 (13)
├── record.py       # 评测记录 (4)
├── discuss.py      # 讨论 (9)
├── feed.py         # 动态/犇犇 (5)
├── user.py         # 用户 (18)
├── team.py         # 团队 (15)
├── chat.py         # 私信 (5)
├── article.py      # 专栏 (16)
├── blog.py         # 博客 (10)
├── theme.py        # 主题 (6)
├── image.py        # 图片 (4)
├── ide.py          # 在线 IDE (1)
├── paste.py        # 剪贴板 (5)
├── auth.py         # 身份验证 (10)
└── misc.py         # 杂项 (9)
```

- `base.py` 是唯一导入 `requests` 的文件，其余模块 `from base import LuoguClient, log, confirm`
- `LuoguClient` 自动读取 cookie、预取 CSRF、处理 Lentille / ContentOnly 响应格式
- 日志使用 `logging` 模块，ANSI 彩色，格式 `[mm:ss] LVL message`
