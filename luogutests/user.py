from base import LuoguClient, confirm, prompt, run_from_cli

client = LuoguClient()


def get_user(uid):
    """获取用户主页"""
    data = client.lentille(f"/user/{uid}")
    return data


def search_user(keyword):
    """搜索用户"""
    r = client.get("/api/user/search", params={"keyword": keyword})
    return r.json()


def get_practice(uid):
    """获取练习统计"""
    data = client.lentille(f"/user/{uid}/practice")
    return data


def get_followings(uid):
    """获取关注列表"""
    data = client.content("/api/user/followings", params={"user": uid, "page": 1})
    return data


def get_followers(uid):
    """获取粉丝列表"""
    data = client.content("/api/user/followers", params={"user": uid, "page": 1})
    return data


def get_blacklist(uid):
    """获取黑名单"""
    data = client.content("/api/user/blacklist", params={"user": uid, "page": 1})
    return data


def get_settings():
    """获取账号设置"""
    data = client.lentille("/user/setting")
    return data


def get_preferences():
    """获取偏好设置"""
    data = client.lentille("/user/setting/preference")
    return data


def update_preferences(prefs):
    """更新偏好设置"""
    r = client.post("/user/setting/preference/update", json=prefs)
    return r.json()


def get_prize():
    """获取奖项认证设置"""
    data = client.lentille("/user/setting/prize")
    return data


def get_security():
    """获取安全设置"""
    data = client.lentille("/user/setting/security")
    return data


def update_slogan():
    """更新个性签名"""
    slogan = prompt("个性签名: ").strip()
    r = client.post("/api/user/updateSlogan", json={"slogan": slogan})
    return r.json()


def update_introduction():
    """更新个人简介"""
    intro = prompt("个人简介: ").strip()
    r = client.post("/api/user/updateIntroduction", json={"introduction": intro})
    return r.json()


def update_header_image(image_id=None):
    """更新封面图"""
    r = client.post("/api/user/updateHeaderImage", json={"imageID": image_id})
    return r.json()


def bind_vjudge():
    """绑定 RemoteJudge 账号"""
    cap = client.captcha()
    oj = prompt("OJ 名称: ").strip()
    username = prompt("用户名: ").strip()
    password = prompt("密码: ").strip()
    body = {"oj": oj, "username": username, "password": password, "captcha": cap}
    r = client.post("/api/user/bindVjudgeAccount", json=body)
    return r.json()


def unbind_vjudge(oj):
    """解绑 RemoteJudge"""
    r = client.post("/api/user/unbindVjudgeAccount", json={"oj": oj})
    return r.json()


def unbind_openid(openid_id):
    """解绑 OpenID"""
    r = client.post(f"/api/user/unbindOpenId/{openid_id}")
    return r.json()


APIS = {
    "get": get_user,
    "search": search_user,
    "practice": get_practice,
    "followings": get_followings,
    "followers": get_followers,
    "blacklist": get_blacklist,
    "settings": get_settings,
    "preferences": get_preferences,
    "update_preferences": update_preferences,
    "prize": get_prize,
    "security": get_security,
    "update_slogan": update_slogan,
    "update_introduction": update_introduction,
    "update_header_image": update_header_image,
    "bind_vjudge": bind_vjudge,
    "unbind_vjudge": unbind_vjudge,
    "unbind_openid": unbind_openid,
}

if __name__ == "__main__":
    def _interactive():
        uid = prompt("  用户UID (默认查看自己，留空跳过): ").strip()
        if uid:
            get_user(uid)
            get_practice(uid)
            get_followings(uid)
            get_followers(uid)
            get_blacklist(uid)
        search_user("admin")
        get_settings()
        get_preferences()
        get_prize()
        get_security()
        if confirm("更新个性签名"):
            update_slogan()
        if confirm("更新个人简介"):
            update_introduction()
        if confirm("更新封面图"):
            update_header_image()
        if confirm("绑定 RemoteJudge"):
            bind_vjudge()
        if confirm("更新偏好设置"):
            update_preferences({})
        oj = prompt("  要解绑的OJ名称 (留空跳过): ").strip()
        if oj and confirm(f"解绑 {oj}"):
            unbind_vjudge(oj)
        openid_id = prompt("  要解绑的OpenID ID (留空跳过): ").strip()
        if openid_id and confirm(f"解绑 OpenID {openid_id}"):
            unbind_openid(openid_id)
    run_from_cli(APIS, _interactive)
