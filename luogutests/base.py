import json
import logging
import os
import re
import sys
import time

import requests

BASE_URL = "https://www.luogu.com.cn"

# ---------- logging ----------

logger = logging.getLogger("luogu")

_LVL_RESP = 25
logging.addLevelName(_LVL_RESP, "RESP")
logging.addLevelName(logging.WARNING, "WARN")

_C = {
    logging.INFO: "\033[36m",
    _LVL_RESP: "\033[32m",
    logging.WARNING: "\033[33m",
    logging.ERROR: "\033[31m",
}
_R = "\033[0m"


class _Fmt(logging.Formatter):
    def format(self, record):
        ts = time.strftime("%M:%S")
        c = _C.get(record.levelno, "")
        return f"\033[2m[{ts}]\033[0m {c}{record.levelname:<4}{_R} {record.getMessage()}"


_h = logging.StreamHandler(sys.stdout)
_h.setFormatter(_Fmt())
logger.addHandler(_h)
logger.setLevel(logging.DEBUG)

_LVL = {
    "INFO": logging.INFO,
    "RESP": _LVL_RESP,
    "WARN": logging.WARNING,
    "ERROR": logging.ERROR,
    "CONFIRM": logging.INFO,
}


def log(level: str, msg):
    if level == "SKIP":
        return
    logger.log(_LVL.get(level, logging.INFO), str(msg))


# ---------- confirm ----------

_confirm_all = False
_skip_all = False


def confirm(action: str) -> bool:
    global _confirm_all, _skip_all
    if _confirm_all:
        log("INFO", f"[全部确认] {action}")
        return True
    if _skip_all:
        return False
    log("INFO", f"确认{action}? (y/a/n/q)")
    try:
        ans = input().strip().lower()
    except KeyboardInterrupt:
        return False
    if ans == "a":
        _confirm_all = True
        log("INFO", f"[全部确认] {action}")
        return True
    if ans == "q":
        _skip_all = True
        return False
    return ans == "y"


# ---------- client ----------

class LuoguClient:
    _DEFAULT_COOKIE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "cookie.json")

    def __init__(self, cookie_path: str | None = None):
        cookie_path = cookie_path or self._DEFAULT_COOKIE
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Luogu API",
            "Referer": "https://www.luogu.com.cn/",
        })
        self._csrf = None
        self._load_cookies(cookie_path)
        self.csrf

    def _load_cookies(self, path: str):
        try:
            with open(path, encoding="utf-8") as f:
                for c in json.load(f):
                    self.session.cookies.set(
                        c["name"], c["value"], domain=c.get("domain", "")
                    )
            log("INFO", f"已加载 Cookies: {path}")
        except FileNotFoundError:
            log("ERROR", f"找不到 Cookie 文件: {path}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            log("ERROR", f"Cookie 文件格式错误: {e}")
            sys.exit(1)

    @property
    def csrf(self) -> str | None:
        r = self.session.get(BASE_URL)
        m = re.search(r'<meta name="csrf-token" content="([^"]+)"', r.text)
        if m:
            self._csrf = m.group(1)
        else:
            log("WARN", "未找到 CSRF Token")
        return self._csrf

    def _log_resp(self, r: requests.Response):
        code = r.status_code
        labels = {
            200: "OK", 302: "Redirect", 403: "Forbidden",
            404: "Not Found", 429: "Too Many Requests",
        }
        label = labels.get(code)
        if not label:
            if 300 <= code < 400:
                label = "Redirect"
            elif 400 <= code < 500:
                label = "Client Error"
            elif 500 <= code < 600:
                label = "Server Error"
        msg = str(code)
        if label:
            msg += f" {label}"
        if 200 <= code < 300:
            log("RESP", msg)
        elif 300 <= code < 400:
            log("WARN", msg)
        else:
            log("ERROR", msg)

    def get(self, path: str, **kw) -> requests.Response:
        log("INFO", f"GET {path}")
        try:
            r = self.session.get(BASE_URL + path, **kw)
        except requests.RequestException as e:
            log("ERROR", str(e))
            raise
        self._log_resp(r)
        return r

    def post(self, path: str, **kw) -> requests.Response:
        h = kw.pop("headers", {})
        h["x-csrf-token"] = self.csrf
        h["referer"] = "https://www.luogu.com.cn/"
        log("INFO", f"POST {path}")
        try:
            r = self.session.post(BASE_URL + path, headers=h, **kw)
        except requests.RequestException as e:
            log("ERROR", str(e))
            raise
        self._log_resp(r)
        return r

    def delete(self, path: str, **kw) -> requests.Response:
        h = kw.pop("headers", {})
        h["x-csrf-token"] = self.csrf
        h["referer"] = "https://www.luogu.com.cn/"
        log("INFO", f"DELETE {path}")
        try:
            r = self.session.delete(BASE_URL + path, headers=h, **kw)
        except requests.RequestException as e:
            log("ERROR", str(e))
            raise
        self._log_resp(r)
        return r

    def lentille(self, path: str, **kw) -> dict:
        h = kw.pop("headers", {})
        h["x-lentille-request"] = "content-only"
        r = self.get(path, headers=h, **kw)
        j = r.json()
        code = j.get("code")
        if code is not None and code != 200:
            log("WARN", f"code={code} message={j.get('message', '')}")
        return j.get("data", j)

    def content(self, path: str, **kw) -> dict:
        p = kw.pop("params", {})
        p["_contentOnly"] = "1"
        r = self.get(path, params=p, **kw)
        j = r.json()
        code = j.get("code")
        if code is not None and code != 200:
            log("WARN", f"code={code} message={j.get('message', '')}")
        return j.get("currentData", j)

    def captcha(self) -> str:
        p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "captcha.jpg")
        while True:
            r = self.session.get(f"{BASE_URL}/lg4/captcha")
            with open(p, "wb") as f:
                f.write(r.content)
            log("INFO", f"验证码已保存到 {p}")
            try:
                os.startfile(p)
            except AttributeError:
                pass
            log("INFO", "验证码 (r=刷新 / Ctrl+C=跳过)")
            try:
                code = input().strip()
            except KeyboardInterrupt:
                return ""
            if code.lower() == "r":
                log("INFO", "刷新验证码...")
                continue
            return code
