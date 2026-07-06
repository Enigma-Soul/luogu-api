from base import LuoguClient, confirm, prompt, run_from_cli

client = LuoguClient()


def list_blogs(uid):
    """获取用户博客列表"""
    r = client.get("/api/blog/userBlogs", params={"user": uid, "page": 1})
    return r.json()


def get_blog(blog_id):
    """获取博客详情"""
    r = client.get(f"/api/blog/detail/{blog_id}")
    return r.json()


def create_blog():
    """创建博客"""
    title = prompt("标题: ").strip()
    content = prompt("内容: ").strip()
    data = {
        "title": title,
        "content": content,
        "identifier": "",
        "type": 0,
        "top": 0,
        "status": 1,
        "csrf-token": client.csrf,
    }
    r = client.post("/blogAdmin/article/post_new", data=data)
    return r.json()


def edit_blog(blog_id):
    """编辑博客"""
    title = prompt("标题: ").strip()
    content = prompt("内容: ").strip()
    data = {
        "title": title,
        "content": content,
        "identifier": "",
        "type": 0,
        "top": 0,
        "status": 1,
        "csrf-token": client.csrf,
    }
    r = client.post(f"/blogAdmin/article/post_edit/{blog_id}", data=data)
    return r.json()


def delete_blog(blog_id):
    """删除博客"""
    client.warn(f"将删除博客 {blog_id}")
    r = client.post(f"/api/blog/delete/{blog_id}")
    return r.json()


def get_blog_replies(blog_id):
    """获取博客评论"""
    r = client.get(f"/api/blog/replies/{blog_id}", params={"page": 1})
    return r.json()


def reply_blog(blog_id):
    """评论博客"""
    content = prompt("评论内容: ").strip()
    r = client.post(f"/api/blog/reply/{blog_id}", json={"content": content})
    return r.json()


def vote_blog(blog_id, vote_type=1):
    """投票博客 (1=赞, -1=踩)"""
    r = client.post(f"/api/blog/vote/{blog_id}", json={"Type": vote_type})
    return r.json()


def delete_blog_comment(blog_id, reply_id):
    """删除博客评论"""
    data = {"reply-id": reply_id, "csrf-token": client.csrf}
    r = client.post(f"/blogAdmin/article/deleteComment/{blog_id}", data=data)
    return r.json()


def batch_blog_operation(page_type="list"):
    """批量博客操作"""
    method = prompt("操作 (update/recover/delete): ").strip()
    blog_ids = prompt("博客ID (逗号分隔): ").strip().split(",")
    data = {
        "method": method,
        "blog-id[]": blog_ids,
        "csrf-token": client.csrf,
    }
    r = client.post(f"/blogAdmin/article/list?pageType={page_type}", data=data)
    return r


APIS = {
    "list": list_blogs,
    "get": get_blog,
    "create": create_blog,
    "edit": edit_blog,
    "delete": delete_blog,
    "replies": get_blog_replies,
    "reply": reply_blog,
    "vote": vote_blog,
    "delete_comment": lambda blog_id, reply_id: delete_blog_comment(blog_id, int(reply_id)),
    "batch": batch_blog_operation,
}

if __name__ == "__main__":
    def _interactive():
        uid = prompt("  用户UID (查看博客列表，留空跳过): ").strip()
        if uid:
            list_blogs(uid)
        blog_id = prompt("  博客ID (留空则只测试创建): ").strip()
        if blog_id:
            get_blog(blog_id)
            get_blog_replies(blog_id)
            if confirm(f"编辑博客 {blog_id}"):
                edit_blog(blog_id)
            if confirm(f"投票博客 {blog_id}"):
                vote_blog(blog_id)
            if confirm(f"评论博客 {blog_id}"):
                reply_blog(blog_id)
            if confirm(f"删除博客 {blog_id} (不可逆)"):
                delete_blog(blog_id)
            reply_id = prompt("  要删除的评论ID (留空跳过): ").strip()
            if reply_id and confirm(f"删除博客 {blog_id} 的评论 {reply_id}"):
                delete_blog_comment(blog_id, int(reply_id))
        else:
            if confirm("创建博客"):
                create_blog()
        if confirm("批量博客操作"):
            batch_blog_operation()
    run_from_cli(APIS, _interactive)
