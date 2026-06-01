from base import LuoguClient, log, confirm

client = LuoguClient()


def list_pastes():
    """获取剪贴板列表"""
    data = client.content("/paste")
    return data


def get_paste(pid):
    """获取剪贴板详情"""
    data = client.content(f"/paste/{pid}")
    return data


def create_paste(data_text, public=True):
    """创建剪贴板"""
    r = client.post("/paste/new", json={"data": data_text, "public": public})
    return r.json()


def edit_paste(pid, data_text, public=True):
    """编辑剪贴板"""
    r = client.post(f"/paste/edit/{pid}", json={"data": data_text, "public": public})
    return r.json()


def delete_paste(pid):
    """删除剪贴板"""
    r = client.post(f"/paste/delete/{pid}")
    return r.json()


if __name__ == "__main__":
    list_pastes()
    pid = input("  剪贴板ID (查看详情，留空跳过): ").strip()
    if pid:
        get_paste(pid)

    if confirm("创建剪贴板"):
        text = input("  内容: ").strip()
        create_paste(text)
    if pid and confirm(f"编辑剪贴板 {pid}"):
        text = input("  新内容: ").strip()
        edit_paste(pid, text)
    if pid and confirm(f"删除剪贴板 {pid}"):
        delete_paste(pid)
