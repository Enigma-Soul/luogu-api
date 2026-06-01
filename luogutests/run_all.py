import os
import runpy

from base import log

_DIR = os.path.dirname(os.path.abspath(__file__))

tests = [
    ("problem", "题目"),
    ("training", "题单"),
    ("contest", "比赛"),
    ("record", "评测记录"),
    ("discuss", "讨论"),
    ("feed", "动态/犇犇"),
    ("user", "用户"),
    ("team", "团队"),
    ("chat", "私信"),
    ("article", "专栏"),
    ("blog", "博客"),
    ("theme", "主题"),
    ("image", "图片"),
    ("ide", "在线IDE"),
    ("paste", "剪贴板"),
    ("auth", "身份验证"),
    ("misc", "杂项"),
]


def main():
    log("INFO", f"共 {len(tests)} 个模块 (y/a/n/q, Ctrl+C=跳过)")
    for mod, label in tests:
        try:
            runpy.run_path(os.path.join(_DIR, f"{mod}.py"), run_name="__main__")
        except KeyboardInterrupt:
            log("WARN", f"跳过 {label}")
        except Exception as e:
            log("ERROR", f"{label} 异常: {e}")
    log("INFO", "全部完成")


if __name__ == "__main__":
    main()
