from base import LuoguClient, log, confirm

client = LuoguClient()


def list_themes():
    """获取主题列表"""
    data = client.content("/theme/list", params={"page": 1})
    return data


def get_theme(tid):
    """获取主题详情"""
    data = client.content(f"/theme/design/{tid}")
    return data


def set_theme(tid):
    """应用主题"""
    r = client.post(f"/theme/setTheme/{tid}")
    return r.json()


def create_theme():
    """创建主题"""
    name = input("主题名称: ").strip()
    body = {"name": name, "header": "", "sideNav": "", "footer": ""}
    r = client.post("/theme/edit/", json=body)
    return r.json()


def edit_theme(tid):
    """编辑主题"""
    name = input("主题名称: ").strip()
    body = {"name": name, "header": "", "sideNav": "", "footer": ""}
    r = client.post(f"/theme/edit/{tid}", json=body)
    return r.json()


def delete_theme(tid):
    """删除主题"""
    ans = input(f"确认删除主题 {tid}? (y/N): ").strip().lower()
    if ans != "y":
        return None
    r = client.post(f"/theme/delete/{tid}")
    return r.json()


if __name__ == "__main__":
    list_themes()
    tid = input("  主题ID (查看详情，留空跳过): ").strip()
    if tid:
        get_theme(tid)

    if tid and confirm(f"应用主题 {tid}"):
        set_theme(tid)
    if confirm("创建主题"):
        create_theme()
    if tid and confirm(f"编辑主题 {tid}"):
        edit_theme(tid)
    if tid and confirm(f"删除主题 {tid}"):
        delete_theme(tid)
