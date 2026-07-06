from base import LuoguClient, log, confirm, prompt, run_from_cli

client = LuoguClient()


def list_articles():
    """获取专栏列表"""
    data = client.lentille("/article", params={"page": 1})
    return data


def find_articles(user):
    """列出用户文章"""
    r = client.get("/api/article/find", params={"user": user, "page": 1})
    return r.json()


def favored_articles():
    """列出收藏的文章"""
    r = client.get("/article/favored", params={"page": 1})
    return r.json()


def my_articles():
    """获取我的专栏"""
    data = client.lentille("/article/mine", params={"page": 1})
    return data


def get_article(lid):
    """获取专栏详情 (域名 www.luogu.com)"""
    data = client.lentille(f"/article/{lid}")
    return data


def article_collection(collection_id):
    """获取专栏合集"""
    data = client.lentille(f"/article/collection/{collection_id}", params={"page": 1})
    return data


def article_available_collections(lid):
    """获取可添加的合集"""
    r = client.get(f"/article/{lid}/availableCollection")
    return r.json()


# 专栏分类: 1=个人记录 2=题解 3=科技·工程 4=算法·理论 5=生活·游记 6=学习·文化课 7=休闲·娱乐 8=闲话
# 状态: 1=私有 2=公开
# 置顶: 0=置顶 1=次级置顶 2=不置顶


def create_article():
    """创建专栏"""
    title = prompt("标题: ").strip()
    content = prompt("内容: ").strip()
    category = int(prompt("分类 (默认1): ").strip() or "1")
    solution_for = prompt("题解题目ID (留空): ").strip()
    status = int(prompt("状态 (默认1): ").strip() or "1")
    top = int(prompt("置顶 (默认2): ").strip() or "2")
    r = client.post("/article/_newSubmit", json={
        "title": title, "category": category, "content": content,
        "solutionFor": solution_for, "status": status, "top": top
    })
    return r.json()


def get_article_edit(lid):
    """获取专栏编辑数据"""
    data = client.lentille(f"/article/{lid}/edit")
    return data


def edit_article(lid):
    """编辑专栏"""
    title = prompt("标题: ").strip()
    content = prompt("内容: ").strip()
    category = int(prompt("分类 (默认1): ").strip() or "1")
    solution_for = prompt("题解题目ID (留空): ").strip()
    status = int(prompt("状态 (默认1): ").strip() or "1")
    top = int(prompt("置顶 (默认2): ").strip() or "2")
    r = client.post(f"/article/{lid}/editSubmit", json={
        "title": title, "category": category, "content": content,
        "solutionFor": solution_for, "status": status, "top": top
    })
    return r.json()


def delete_article(lid):
    """删除专栏"""
    client.warn(f"将删除专栏 {lid}")
    r = client.post(f"/article/{lid}/delete", json={})
    return r.json()


def batch_edit_articles():
    """批量编辑专栏 (未测试)"""
    lids = prompt("专栏ID (逗号分隔): ").strip().split(",")
    r = client.post("/api/article/batchEdit", json={"lids": lids})
    return r.json()


def favor_article(lid, remove=False):
    """收藏/取消收藏专栏"""
    r = client.post(f"/article/{lid}/favor", params={"remove": remove}, json={})
    return r.json()


def vote_article(lid, vote=1):
    """投票 (1=赞, -1=踩, 0=取消)"""
    r = client.post(f"/article/{lid}/vote", params={"vote": vote}, json={})
    return r.json()


# 以下端点未测试，可能已变更
def request_promotion(lid):
    """申请推广 (未测试)"""
    r = client.post(f"/api/article/requestPromotion/{lid}")
    return r


def withdraw_promotion(lid):
    """撤回推广 (未测试)"""
    r = client.post(f"/api/article/withdrawPromotion/{lid}")
    return r


def get_article_replies(lid):
    """获取专栏评论"""
    r = client.get(f"/article/{lid}/replies")
    return r.json()


def reply_article(lid):
    """评论专栏"""
    content = prompt("评论内容: ").strip()
    r = client.post(f"/article/{lid}/reply", json={"content": content})
    return r.json()


def delete_article_reply(lid, reply_id):
    """删除专栏评论"""
    r = client.post(f"/article/{lid}/deleteReply/{reply_id}", json={})
    return r.json()


APIS = {
    "list": list_articles,
    "find": find_articles,
    "favored": favored_articles,
    "mine": my_articles,
    "get": get_article,
    "collection": article_collection,
    "available_collections": article_available_collections,
    "create": create_article,
    "edit_data": get_article_edit,
    "edit": edit_article,
    "delete": delete_article,
    "batch_edit": batch_edit_articles,
    "favor": favor_article,
    "vote": vote_article,
    "request_promotion": request_promotion,
    "withdraw_promotion": withdraw_promotion,
    "replies": get_article_replies,
    "reply": reply_article,
    "delete_reply": lambda lid, reply_id: delete_article_reply(lid, int(reply_id)),
}

if __name__ == "__main__":
    def _interactive():
        list_articles()
        my_articles()
        favored_articles()
        find_uid = prompt("  列出某用户的专栏，输入UID (留空跳过): ").strip()
        if find_uid:
            find_articles(find_uid)

        lid = None
        if confirm("创建专栏"):
            result = create_article()
            lid = result.get("article", {}).get("lid")
            log("INFO", f"创建成功，lid={lid}")

        if not lid:
            lid = prompt("  专栏ID (留空跳过后续测试): ").strip() or None
        if lid:
            get_article(lid)
            get_article_replies(lid)
            article_available_collections(lid)
            if confirm(f"编辑专栏 {lid}"):
                edit_article(lid)
            if confirm(f"收藏专栏 {lid}"):
                favor_article(lid)
            if confirm(f"投票专栏 {lid}"):
                vote_article(lid)
            if confirm(f"申请推广专栏 {lid}"):
                request_promotion(lid)
            if confirm(f"评论专栏 {lid}"):
                reply_article(lid)
            if confirm(f"撤回专栏 {lid} 推广"):
                withdraw_promotion(lid)
            reply_id = prompt("  要删除的评论ID (留空跳过): ").strip()
            if reply_id and confirm(f"删除专栏 {lid} 的评论 {reply_id}"):
                delete_article_reply(lid, int(reply_id))
            if confirm(f"删除专栏 {lid} (不可逆)"):
                delete_article(lid)
        collection_id = prompt("  合集ID (留空跳过): ").strip()
        if collection_id:
            article_collection(collection_id)
        if confirm("批量编辑专栏"):
            batch_edit_articles()
    run_from_cli(APIS, _interactive)
