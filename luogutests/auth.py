from base import LuoguClient, confirm, prompt, run_from_cli

client = LuoguClient()


def get_captcha():
    """获取验证码图片"""
    code = client.captcha()
    return code


def send_signup_code():
    """发送注册验证码"""
    cap = client.captcha()
    endpoint = prompt("手机号/邮箱: ").strip()
    body = {"endpoint": endpoint, "captcha": cap}
    r = client.post("/auth/motp/to", params={"endpoint": endpoint, "exist": 0}, json=body)
    return r.json()


def register():
    """注册"""
    username = prompt("用户名: ").strip()
    password = prompt("密码: ").strip()
    endpoint = prompt("手机号/邮箱: ").strip()
    code = prompt("验证码: ").strip()
    body = {
        "username": username,
        "password": password,
        "endpoint": endpoint,
        "endpointType": 0,
        "verificationCode": code,
    }
    r = client.post("/auth/finish-signup", json=body)
    return r.json()


def login():
    """登录 (密码)"""
    cap = client.captcha()
    username = prompt("用户名: ").strip()
    password = prompt("密码: ").strip()
    body = {"username": username, "password": password, "captcha": cap}
    r = client.post("/do-auth/password", json=body)
    return r.json()


def logout():
    """登出"""
    r = client.post("/auth/logout")
    return r


def lock():
    """锁定会话"""
    r = client.post("/auth/lock")
    return r


def unlock_totp():
    """TOTP 解锁"""
    code = prompt("TOTP 验证码: ").strip()
    r = client.post("/do-auth/totp", json={"code": code})
    return r.json()


def send_motp():
    """发送一次性验证码"""
    cap = client.captcha()
    endpoint = prompt("手机号/邮箱: ").strip()
    r = client.post("/auth/motp/request", params={"endpoint": endpoint}, json={"captcha": cap})
    return r.json()


def unlock_motp():
    """一次性验证码解锁"""
    code = prompt("验证码: ").strip()
    r = client.post("/do-auth/motp", json={"code": code})
    return r.json()


def get_unlock_methods():
    """获取解锁方式"""
    data = client.content("/auth/unlock")
    return data


APIS = {
    "captcha": get_captcha,
    "send_signup_code": send_signup_code,
    "register": register,
    "login": login,
    "logout": logout,
    "lock": lock,
    "unlock_totp": unlock_totp,
    "send_motp": send_motp,
    "unlock_motp": unlock_motp,
    "unlock_methods": get_unlock_methods,
}

if __name__ == "__main__":
    def _interactive():
        get_unlock_methods()
        if confirm("获取验证码"):
            get_captcha()
        if confirm("登录"):
            login()
        if confirm("发送注册验证码"):
            send_signup_code()
        if confirm("注册"):
            register()
        if confirm("锁定会话"):
            lock()
        if confirm("TOTP 解锁"):
            unlock_totp()
        if confirm("发送一次性验证码"):
            send_motp()
        if confirm("一次性验证码解锁"):
            unlock_motp()
        if confirm("登出"):
            logout()
    run_from_cli(APIS, _interactive)
