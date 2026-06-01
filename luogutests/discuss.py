from base import LuoguClient, log, confirm

client = LuoguClient()


def list_discussions():
    """获取讨论列表"""
    data = client.lentille("/discuss", params={"forum": "", "page": 1})
    return data


def created_posts():
    """获取用户发布的帖子"""
    data = client.content("/api/user/createdPosts", params={"page": 1})
    return data


def get_discussion(post_id):
    """获取帖子详情"""
    data = client.lentille(f"/discuss/{post_id}")
    return data


def create_post():
    """发帖 (需要验证码)"""
    cap = client.captcha()
    title = input("帖子标题: ").strip()
    content = input("帖子内容: ").strip()
    forum = input("板块: ").strip()
    body = {"captcha": cap, "content": content, "title": title, "forum": forum}
    r = client.post("/api/discuss/post", json=body)
    return r.json()


def reply_post(post_id):
    """回复帖子 (需要验证码)"""
    cap = client.captcha()
    content = input("回复内容: ").strip()
    body = {"captcha": cap, "content": content}
    r = client.post(f"/api/discuss/reply/{post_id}", json=body)
    return r.json()


def delete_post(post_id):
    """删除帖子"""
    log("WARN", f"将删除帖子 {post_id}")
    ans = input("确认删除? (y/N): ").strip().lower()
    if ans != "y":
        return None
    r = client.delete(f"/api/discuss/delete/{post_id}")
    return r.json()


def delete_reply(reply_id):
    """删除回复"""
    r = client.delete(f"/api/discuss/deleteReply/{reply_id}")
    return r.json()


def report_post():
    """举报帖子"""
    post_id = int(input("帖子ID: ").strip())
    reason = input("举报原因: ").strip()
    r = client.post("/api/report/post", json={"relevantID": post_id, "reason": reason})
    return r.json()


def report_reply():
    """举报回复"""
    reply_id = int(input("回复ID: ").strip())
    reason = input("举报原因: ").strip()
    r = client.post("/api/report/post_reply", json={"relevantID": reply_id, "reason": reason})
    return r.json()


if __name__ == "__main__":
    list_discussions()
    created_posts()

    if confirm("发帖"):
        create_post()
    post_id = input("  帖子ID (用于回复/查看/删除，留空跳过): ").strip()
    if post_id:
        get_discussion(post_id)
        if confirm(f"回复帖子 {post_id}"):
            reply_post(post_id)
        if confirm(f"删除帖子 {post_id}"):
            delete_post(post_id)
    reply_id = input("  回复ID (用于删除回复，留空跳过): ").strip()
    if reply_id and confirm(f"删除回复 {reply_id}"):
        delete_reply(reply_id)
    if confirm("举报帖子"):
        report_post()
    if confirm("举报回复"):
        report_reply()
