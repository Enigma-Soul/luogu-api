from base import LuoguClient, log, confirm

client = LuoguClient()


def list_contests():
    """获取比赛列表"""
    data = client.lentille("/contest/list", params={"page": 1})
    return data


def joined_contests():
    """获取已参加的比赛"""
    data = client.content("/api/user/joinedContests", params={"page": 1})
    return data


def created_contests():
    """获取创建的比赛"""
    data = client.content("/api/user/createdContests", params={"page": 1})
    return data


def get_contest(cid):
    """获取比赛详情"""
    data = client.lentille(f"/contest/{cid}")
    return data


def get_contest_edit(cid):
    """获取比赛编辑信息"""
    data = client.content(f"/contest/edit/{cid}")
    return data


def get_scoreboard(cid, page=1):
    """获取比赛排行榜"""
    r = client.get(f"/fe/api/contest/scoreboard/{cid}", params={"page": page})
    return r.json()


def join_contest(cid, code=""):
    """参加比赛"""
    body = {"code": code}
    r = client.post(f"/contest/{cid}/join", json=body)
    return r.json()


def create_squad(cid):
    """创建小队"""
    r = client.post(f"/contest/{cid}/squad", json={})
    return r.json()


def squad_member_quit(cid, uid):
    """退出/踢出小队"""
    r = client.post(f"/contest/{cid}/squadMemberQuit", json={"uid": uid})
    return r.json()


def create_contest():
    """创建比赛"""
    name = input("比赛名称: ").strip()
    r = client.post("/fe/api/contest/new", json={"name": name})
    return r.json()


def edit_contest(cid):
    """编辑比赛"""
    r = client.post(f"/fe/api/contest/edit/{cid}", json={})
    return r.json()


def edit_contest_problem(cid, pids=None, scores=None):
    """设置比赛题目"""
    if pids is None:
        pids = input("题目ID (逗号分隔): ").strip().split(",")
    if scores is None:
        scores = {p: 100 for p in pids}
    r = client.post(f"/fe/api/contest/editProblem/{cid}", json={"pids": pids, "scores": scores})
    return r.json()


def delete_contest(cid):
    """删除比赛"""
    log("WARN", f"将删除比赛 {cid}，此操作不可逆!")
    ans = input("确认删除? (y/N): ").strip().lower()
    if ans != "y":
        return None
    r = client.post(f"/fe/api/contest/delete/{cid}")
    return r.json()


if __name__ == "__main__":
    list_contests()
    joined_contests()
    created_contests()

    cid = input("  测试比赛ID (留空跳过详情测试): ").strip()
    if cid:
        get_contest(cid)
        get_contest_edit(cid)
        get_scoreboard(cid)
        if confirm(f"参加比赛 {cid}"):
            code = input("  比赛邀请码 (留空无码): ").strip()
            join_contest(cid, code)
        if confirm(f"创建小队 (比赛 {cid})"):
            create_squad(cid)
        if confirm(f"编辑比赛 {cid}"):
            edit_contest(cid)
        if confirm(f"设置比赛 {cid} 题目"):
            edit_contest_problem(cid)
        if confirm(f"删除比赛 {cid} (不可逆)"):
            delete_contest(cid)
    if confirm("创建新比赛"):
        create_contest()
