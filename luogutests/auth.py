from base import LuoguClient, log, confirm

client = LuoguClient()


def get_captcha():
    """获取验证码图片"""
    code = client.captcha()
    return code


def send_signup_code():
    """发送注册验证码"""
    cap = client.captcha()
    endpoint = input("手机号/邮箱: ").strip()
    body = {"endpoint": endpoint, "captcha": cap}
    r = client.post("/auth/motp/to", params={"endpoint": endpoint, "exist": 0}, json=body)
    return r.json()


def register():
    """注册"""
    username = input("用户名: ").strip()
    password = input("密码: ").strip()
    endpoint = input("手机号/邮箱: ").strip()
    code = input("验证码: ").strip()
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
    username = input("用户名: ").strip()
    password = input("密码: ").strip()
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
    code = input("TOTP 验证码: ").strip()
    r = client.post("/do-auth/totp", json={"code": code})
    return r.json()


def send_motp():
    """发送一次性验证码"""
    cap = client.captcha()
    endpoint = input("手机号/邮箱: ").strip()
    r = client.post("/auth/motp/request", params={"endpoint": endpoint}, json={"captcha": cap})
    return r.json()


def unlock_motp():
    """一次性验证码解锁"""
    code = input("验证码: ").strip()
    r = client.post("/do-auth/motp", json={"code": code})
    return r.json()


def get_unlock_methods():
    """获取解锁方式"""
    data = client.content("/auth/unlock")
    return data


if __name__ == "__main__":
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
