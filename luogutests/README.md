# luogutests

洛谷 API 测试套件，覆盖 17 个模块、170+ 个接口。

## 快速开始

```bash
# 在项目根目录放置 cookie.json（从浏览器导出 Cookie）
# 格式：[{"name":"_uid","value":"...","domain":".luogu.com.cn"}, ...]

# 一键运行全部测试
uv run luogutest

# 运行单个模块
uv run python luogutests/problem.py
uv run python luogutests/contest.py
```

## 交互控制

写入操作（提交代码、发帖、删除等）需要手动确认：

| 按键 | 动作 |
|------|------|
| `y` | 确认本次操作 |
| `a` | 确认本次 + 后续全部 |
| `n` / 回车 | 跳过本次 |
| `q` | 跳过后续全部 |
| `Ctrl+C` | 跳过当前操作 |

## 验证码

涉及验证码的接口会自动保存验证码图片到 `captcha.jpg` 并打开系统图片查看器。
输入 `r` 可刷新验证码，`Ctrl+C` 跳过。

## 文件结构

```
luogutests/
├── __init__.py     # 入口注册
├── base.py         # LuoguClient 类、log、confirm、captcha
├── run_all.py      # 一键运行全部模块
├── problem.py      # 题目 (13 接口)
├── training.py     # 题单 (12 接口)
├── contest.py      # 比赛 (13 接口)
├── record.py       # 评测记录 (4 接口)
├── discuss.py      # 讨论 (9 接口)
├── feed.py         # 动态/犇犇 (5 接口)
├── user.py         # 用户 (18 接口)
├── team.py         # 团队 (15 接口)
├── chat.py         # 私信 (5 接口)
├── article.py      # 专栏 (16 接口)
├── blog.py         # 博客 (10 接口)
├── theme.py        # 主题 (6 接口)
├── image.py        # 图片 (4 接口)
├── ide.py          # 在线 IDE (1 接口)
├── paste.py        # 剪贴板 (5 接口)
├── auth.py         # 身份验证 (10 接口)
└── misc.py         # 杂项 (9 接口)
```

## 架构

- **`base.py`** 是唯一导入 `requests` 的文件，其余模块通过 `from base import LuoguClient, log, confirm` 引用
- `LuoguClient` 自动读取 `cookie.json`、预取 CSRF Token、处理响应格式（Lentille / ContentOnly）
- 日志使用 `logging` 模块，带 ANSI 颜色，格式 `[mm:ss] LVL message`
- 通过 `pyproject.toml` 的 `[project.scripts]` 注册 `luogutest` 命令
