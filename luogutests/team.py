from base import LuoguClient, confirm, prompt, run_from_cli

client = LuoguClient()


def get_team(tid):
    """获取团队详情"""
    data = client.lentille(f"/team/{tid}")
    return data


def my_teams():
    """获取已加入的团队"""
    data = client.lentille("/user/mine/team")
    return data


def team_members(tid):
    """获取团队成员"""
    data = client.lentille(f"/team/{tid}/member")
    return data


def team_problems(tid):
    """获取团队题目"""
    data = client.lentille(f"/team/{tid}/problem", params={"page": 1})
    return data


def team_trainings(tid):
    """获取团队题单"""
    data = client.lentille(f"/team/{tid}/training", params={"page": 1})
    return data


def team_contests(tid):
    """获取团队比赛"""
    data = client.lentille(f"/team/{tid}/contest", params={"page": 1})
    return data


def join_team(tid):
    """申请加入团队"""
    msg = prompt("申请理由: ").strip()
    r = client.post(f"/api/team/join/{tid}", json={"applyMessage": msg})
    return r.json()


def exit_team(tid):
    """退出团队"""
    if not confirm(f"退出团队 {tid}"):
        return None
    r = client.post(f"/api/team/exit/{tid}")
    return r.json()


def create_team():
    """创建团队"""
    name = prompt("团队名称: ").strip()
    r = client.post("/api/team/create", json={"name": name})
    return r.json()


def edit_team(tid):
    """编辑团队"""
    desc = prompt("团队描述: ").strip()
    r = client.post(f"/api/team/edit/{tid}", json={"settings": {"description": desc}})
    return r.json()


def set_team_master(tid, uid):
    """转让团队"""
    if not confirm(f"转让团队 {tid} 给用户 {uid}"):
        return None
    r = client.post(f"/api/team/setMaster/{tid}", json={"uid": uid})
    return r.json()


def edit_team_notice(tid):
    """更新团队公告"""
    notice = prompt("公告内容: ").strip()
    r = client.post(f"/api/team/editNotice/{tid}", json={"notice": notice})
    return r.json()


def edit_team_member(tid, uid, real_name="", group=1, permission=0):
    """管理团队成员"""
    body = {"uid": uid, "realName": real_name, "group": group, "permission": permission}
    r = client.post(f"/api/team/editMember/{tid}", json=body)
    return r.json()


def review_team_join(tid, uid, result="apply"):
    """审核加入申请"""
    r = client.post(f"/api/team/review/{tid}", json={"uid": uid, "reviewResult": result})
    return r.json()


def kick_team_member(tid, uid):
    """踢出成员"""
    r = client.post(f"/api/team/kick/{tid}", json={"uid": uid})
    return r.json()


APIS = {
    "get": get_team,
    "my": my_teams,
    "members": team_members,
    "problems": team_problems,
    "trainings": team_trainings,
    "contests": team_contests,
    "join": join_team,
    "exit": exit_team,
    "create": create_team,
    "edit": edit_team,
    "set_master": lambda tid, uid: set_team_master(tid, int(uid)),
    "edit_notice": edit_team_notice,
    "edit_member": lambda tid, uid: edit_team_member(tid, int(uid)),
    "review": lambda tid, uid: review_team_join(tid, int(uid)),
    "kick": lambda tid, uid: kick_team_member(tid, int(uid)),
}

if __name__ == "__main__":
    def _interactive():
        my_teams()
        tid = prompt("  团队ID (留空跳过团队详情测试): ").strip()
        if tid:
            get_team(tid)
            team_members(tid)
            team_problems(tid)
            team_trainings(tid)
            team_contests(tid)
        if confirm("创建团队"):
            create_team()
        if tid:
            if confirm(f"申请加入团队 {tid}"):
                join_team(tid)
            if confirm(f"编辑团队 {tid}"):
                edit_team(tid)
            if confirm(f"更新团队 {tid} 公告"):
                edit_team_notice(tid)
            uid = prompt("  成员UID (用于管理成员/踢出，留空跳过): ").strip()
            if uid:
                if confirm(f"管理团队 {tid} 成员 {uid}"):
                    edit_team_member(tid, int(uid))
                if confirm(f"踢出团队 {tid} 成员 {uid}"):
                    kick_team_member(tid, int(uid))
                if confirm(f"审核团队 {tid} 成员 {uid} 的申请"):
                    review_team_join(tid, int(uid))
            if confirm(f"转让团队 {tid} (不可逆)"):
                master_uid = prompt("  新团长UID: ").strip()
                set_team_master(tid, int(master_uid))
            if confirm(f"退出团队 {tid}"):
                exit_team(tid)
    run_from_cli(APIS, _interactive)
