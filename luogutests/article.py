from base import LuoguClient, log, confirm

client = LuoguClient()


def list_articles():
    """获取专栏列表"""
    data = client.lentille("/article", params={"page": 1})
    return data


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


def create_article():
    """创建专栏"""
    title = input("标题: ").strip()
    content = input("内容: ").strip()
    r = client.post("/api/article/new", json={"title": title, "content": content})
    return r.json()


def edit_article(lid):
    """编辑专栏"""
    title = input("标题: ").strip()
    content = input("内容: ").strip()
    r = client.post(f"/api/article/edit/{lid}", json={"title": title, "content": content})
    return r.json()


def delete_article(lid):
    """删除专栏"""
    log("WARN", f"将删除专栏 {lid}")
    ans = input("确认删除? (y/N): ").strip().lower()
    if ans != "y":
        return None
    r = client.post(f"/api/article/delete/{lid}")
    return r.json()


def batch_edit_articles():
    """批量编辑专栏"""
    lids = input("专栏ID (逗号分隔): ").strip().split(",")
    r = client.post("/api/article/batchEdit", json={"lids": lids})
    return r.json()


def favor_article(lid, remove=False):
    """收藏/取消收藏专栏"""
    r = client.post(f"/api/article/favor/{lid}", params={"remove": remove})
    return r.json()


def vote_article(lid, vote=1):
    """投票 (1=赞, -1=踩, 0=取消)"""
    r = client.post(f"/api/article/vote/{lid}", params={"vote": vote})
    return r.json()


def request_promotion(lid):
    """申请推广"""
    r = client.post(f"/api/article/requestPromotion/{lid}")
    return r


def withdraw_promotion(lid):
    """撤回推广"""
    r = client.post(f"/api/article/withdrawPromotion/{lid}")
    return r


def get_article_replies(lid):
    """获取专栏评论"""
    r = client.get(f"/article/{lid}/replies")
    return r.json()


def reply_article(lid):
    """评论专栏"""
    content = input("评论内容: ").strip()
    r = client.post(f"/article/{lid}/reply", json={"content": content})
    return r.json()


def delete_article_reply(lid, reply_id):
    """删除专栏评论"""
    r = client.post(f"/article/{lid}/deleteReply/{reply_id}")
    return r.json()


if __name__ == "__main__":
    list_articles()
    my_articles()
    lid = input("  专栏ID (留空跳过详情测试): ").strip()
    if lid:
        get_article(lid)
        get_article_replies(lid)
        article_available_collections(lid)

    if confirm("创建专栏"):
        create_article()
    if lid:
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
        if confirm(f"删除专栏 {lid} (不可逆)"):
            delete_article(lid)
    collection_id = input("  合集ID (留空跳过): ").strip()
    if collection_id:
        article_collection(collection_id)
    if confirm("批量编辑专栏"):
        batch_edit_articles()
    if lid and confirm(f"撤回专栏 {lid} 推广"):
        withdraw_promotion(lid)
    reply_id = input("  要删除的评论ID (留空跳过): ").strip()
    if lid and reply_id and confirm(f"删除专栏 {lid} 的评论 {reply_id}"):
        delete_article_reply(lid, int(reply_id))
