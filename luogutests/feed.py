from base import LuoguClient, confirm, prompt, run_from_cli

client = LuoguClient()


def feed_list(uid):
    """获取用户动态"""
    data = client.content("/api/feed/list", params={"user": uid, "page": 1})
    return data


def feed_watching():
    """获取关注用户的动态"""
    data = client.content("/api/feed/watching", params={"page": 1})
    return data


def post_benben():
    """发犇犇"""
    content = prompt("犇犇内容: ").strip()
    r = client.post("/api/feed/postBenben", data={"content": content})
    return r.json()


def delete_benben(benben_id):
    """删除犇犇"""
    r = client.post(f"/api/feed/delete/{benben_id}")
    return r.json()


def report_benben():
    """举报犇犇"""
    benben_id = int(prompt("犇犇ID: ").strip())
    reason = prompt("举报原因: ").strip()
    r = client.post("/api/report/feed", data={"relevantID": benben_id, "reason": reason})
    return r.json()


APIS = {
    "list": feed_list,
    "watching": feed_watching,
    "post": post_benben,
    "delete": delete_benben,
    "report": report_benben,
}

if __name__ == "__main__":
    def _interactive():
        uid = prompt("  用户UID (留空跳过动态测试): ").strip()
        if uid:
            feed_list(uid)
        feed_watching()
        if confirm("发犇犇"):
            post_benben()
        benben_id = prompt("  犇犇ID (用于删除，留空跳过): ").strip()
        if benben_id and confirm(f"删除犇犇 {benben_id}"):
            delete_benben(benben_id)
        if confirm("举报犇犇"):
            report_benben()
    run_from_cli(APIS, _interactive)
