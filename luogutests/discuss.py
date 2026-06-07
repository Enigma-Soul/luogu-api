from base import LuoguClient, confirm, prompt, run_from_cli

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
    title = prompt("帖子标题: ").strip()
    content = prompt("帖子内容: ").strip()
    forum = prompt("板块: ").strip()
    body = {"captcha": cap, "content": content, "title": title, "forum": forum}
    r = client.post("/api/discuss/post", json=body)
    return r.json()


def reply_post(post_id):
    """回复帖子 (需要验证码)"""
    cap = client.captcha()
    content = prompt("回复内容: ").strip()
    body = {"captcha": cap, "content": content}
    r = client.post(f"/api/discuss/reply/{post_id}", json=body)
    return r.json()


def delete_post(post_id):
    """删除帖子"""
    if not confirm(f"删除帖子 {post_id}"):
        return None
    r = client.delete(f"/api/discuss/delete/{post_id}")
    return r.json()


def delete_reply(reply_id):
    """删除回复"""
    r = client.delete(f"/api/discuss/deleteReply/{reply_id}")
    return r.json()


def report_post():
    """举报帖子"""
    post_id = int(prompt("帖子ID: ").strip())
    reason = prompt("举报原因: ").strip()
    r = client.post("/api/report/post", json={"relevantID": post_id, "reason": reason})
    return r.json()


def report_reply():
    """举报回复"""
    reply_id = int(prompt("回复ID: ").strip())
    reason = prompt("举报原因: ").strip()
    r = client.post("/api/report/post_reply", json={"relevantID": reply_id, "reason": reason})
    return r.json()


APIS = {
    "list": list_discussions,
    "created": created_posts,
    "get": get_discussion,
    "create": create_post,
    "reply": reply_post,
    "delete": delete_post,
    "delete_reply": delete_reply,
    "report_post": report_post,
    "report_reply": report_reply,
}

if __name__ == "__main__":
    def _interactive():
        list_discussions()
        created_posts()
        if confirm("发帖"):
            create_post()
        post_id = prompt("  帖子ID (用于回复/查看/删除，留空跳过): ").strip()
        if post_id:
            get_discussion(post_id)
            if confirm(f"回复帖子 {post_id}"):
                reply_post(post_id)
            if confirm(f"删除帖子 {post_id}"):
                delete_post(post_id)
        reply_id = prompt("  回复ID (用于删除回复，留空跳过): ").strip()
        if reply_id and confirm(f"删除回复 {reply_id}"):
            delete_reply(reply_id)
        if confirm("举报帖子"):
            report_post()
        if confirm("举报回复"):
            report_reply()
    run_from_cli(APIS, _interactive)
