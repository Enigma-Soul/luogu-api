from base import LuoguClient, log, confirm

client = LuoguClient()


def ide_submit(code='print("Hello World")', lang=7, input_text="", o2=False):
    """提交代码到在线 IDE (需要验证码)"""
    cap = client.captcha()
    data = {
        "code": code,
        "lang": lang,
        "input": input_text,
        "o2": o2,
        "csrf-token": client.csrf,
        "captcha": cap,
    }
    r = client.post("/api/ide_submit", data=data)
    return r.json()


if __name__ == "__main__":
    if confirm("提交代码到在线 IDE"):
        ide_submit()
