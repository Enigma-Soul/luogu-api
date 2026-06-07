from base import LuoguClient, confirm, prompt, run_from_cli

client = LuoguClient()


def list_trainings():
    """获取题单列表"""
    data = client.lentille("/training/list", params={"page": 1})
    return data


def created_trainings():
    """获取用户创建的题单"""
    data = client.content("/api/user/createdTrainings", params={"page": 1})
    return data


def get_training(tid=1):
    """获取题单详情"""
    data = client.lentille(f"/training/{tid}")
    return data


def marked_trainings():
    """获取收藏的题单"""
    data = client.content("/api/user/markedTrainings", params={"page": 1})
    return data


def mark_training(tid):
    """收藏题单"""
    r = client.post(f"/api/training/mark/{tid}")
    return r.json()


def unmark_training(tid):
    """取消收藏题单"""
    r = client.post(f"/api/training/unmark/{tid}")
    return r.json()


def create_training():
    """创建题单"""
    name = prompt("题单名称: ").strip()
    r = client.post("/api/training/new", json={"settings": {"title": name}, "providerID": 0})
    return r.json()


def edit_training(tid):
    """编辑题单"""
    r = client.post(f"/api/training/edit/{tid}", json={"settings": {}})
    return r.json()


def add_training_problem(tid, pids=None):
    """向题单添加题目"""
    if pids is None:
        pids = prompt("输入题目ID (逗号分隔): ").strip().split(",")
    r = client.post(f"/api/training/addProblem/{tid}", json={"pids": pids})
    return r.json()


def edit_training_problems(tid, pids=None):
    """重排题单题目"""
    if pids is None:
        pids = prompt("输入题目ID (逗号分隔，按顺序): ").strip().split(",")
    r = client.post(f"/api/training/editProblems/{tid}", json={"pids": pids})
    return r.json()


def clone_training(tid):
    """克隆题单"""
    r = client.post(f"/api/training/clone/{tid}", json={"type": 0})
    return r.json()


def delete_training(tid):
    """删除题单"""
    if not confirm(f"删除题单 {tid}"):
        return None
    r = client.post(f"/api/training/delete/{tid}")
    return r.json()


APIS = {
    "list": list_trainings,
    "created": created_trainings,
    "get": get_training,
    "marked": marked_trainings,
    "mark": mark_training,
    "unmark": unmark_training,
    "create": create_training,
    "edit": edit_training,
    "add_problem": add_training_problem,
    "edit_problems": edit_training_problems,
    "clone": clone_training,
    "delete": delete_training,
}

if __name__ == "__main__":
    def _interactive():
        list_trainings()
        created_trainings()
        get_training()
        marked_trainings()
        tid = prompt("  测试题单ID (默认1): ").strip() or "1"
        if confirm(f"收藏题单 {tid}"):
            mark_training(tid)
        if confirm(f"取消收藏题单 {tid}"):
            unmark_training(tid)
        if confirm("创建新题单"):
            create_training()
        if confirm(f"编辑题单 {tid}"):
            edit_training(tid)
        if confirm(f"向题单 {tid} 添加题目"):
            add_training_problem(tid)
        if confirm(f"重排题单 {tid} 题目"):
            edit_training_problems(tid)
        if confirm(f"克隆题单 {tid}"):
            clone_training(tid)
        if confirm(f"删除题单 {tid} (不可逆)"):
            delete_training(tid)
    run_from_cli(APIS, _interactive)
