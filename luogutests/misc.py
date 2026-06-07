from base import LuoguClient, confirm, prompt, run_from_cli

client = LuoguClient()


def get_config():
    """获取站点配置"""
    r = client.get("/_lfe/config")
    data = r.json()
    return data


def get_tags():
    """获取题目标签"""
    r = client.get("/_lfe/tags")
    data = r.json()
    return data


def get_ranking():
    """获取 Gu-rating 排名"""
    data = client.lentille("/ranking", params={"page": 1})
    return data


def get_elo_ranking():
    """获取 Elo 排名"""
    data = client.lentille("/ranking/elo", params={"page": 1})
    return data


def get_notifications():
    """获取通知"""
    data = client.lentille("/user/notification", params={"page": 1})
    return data


def get_ad(id):
    """获取广告"""
    r = client.get(f"/api/qiaFan/getFan/{id}")
    return r.json()


def get_paintboard():
    """获取画板内容"""
    r = client.get("/paintboard/board")
    return r.text


def reset_paintboard_token():
    """重置画板 Token"""
    r = client.post("/paintboard/resetToken")
    return r.json()


def paint(token, x, y, color):
    """在画板上绘制"""
    r = client.post(f"/paintboard/paint?token={token}", json={"x": x, "y": y, "color": color})
    return r.json()


APIS = {
    "config": get_config,
    "tags": get_tags,
    "ranking": get_ranking,
    "elo_ranking": get_elo_ranking,
    "notifications": get_notifications,
    "ad": get_ad,
    "paintboard": get_paintboard,
    "reset_paintboard": reset_paintboard_token,
    "paint": paint,
}

if __name__ == "__main__":
    def _interactive():
        get_config()
        get_tags()
        get_ranking()
        get_elo_ranking()
        get_notifications()
        get_paintboard()
        if confirm("重置画板 Token"):
            reset_paintboard_token()
        if confirm("在画板上绘制"):
            token = prompt("  Token: ").strip()
            x = int(prompt("  X: ").strip())
            y = int(prompt("  Y: ").strip())
            color = int(prompt("  颜色: ").strip())
            paint(token, x, y, color)
        ad_id = prompt("  广告ID (留空跳过): ").strip()
        if ad_id:
            get_ad(ad_id)
    run_from_cli(APIS, _interactive)
