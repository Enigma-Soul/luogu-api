from base import LuoguClient, log, confirm, prompt, run_from_cli

client = LuoguClient()


def list_problems():
    """获取题目列表"""
    data = client.lentille("/problem/list", params={"page": 1, "orderBy": "pid", "order": "asc"})
    return data


def created_problems():
    """获取用户创建的题目"""
    data = client.content("/api/user/createdProblems", params={"page": 1})
    return data


def get_problem(pid="P1001"):
    """获取题目详情"""
    data = client.lentille(f"/problem/{pid}")
    return data


def get_solutions(pid="P1001"):
    """获取题解"""
    data = client.lentille(f"/problem/solution/{pid}")
    return data


def bookmark_problem(pid="P1001"):
    """收藏题目"""
    r = client.post("/fe/api/problem/tasklistAdd", json={"pid": pid})
    return r.json()


def remove_bookmark(pid="P1001"):
    """取消收藏"""
    r = client.post("/fe/api/problem/tasklistRemove", json={"pid": pid})
    return r.json()


def submit_code(pid="P1001", code='print("Hello World")', lang=7, enable_o2=0):
    """提交代码 (需要验证码)"""
    cap = client.captcha()
    body = {"code": code, "lang": lang, "enableO2": enable_o2, "captcha": cap}
    r = client.post(f"/fe/api/problem/submit/{pid}", json=body)
    return r.json()


def submit_translation(pid="P1001"):
    """提交翻译"""
    translation = prompt("请输入翻译内容: ").strip()
    r = client.post(f"/fe/api/problem/translate/{pid}", json={"translation": translation})
    return r


def create_problem():
    """创建题目 (交互式)"""
    log("WARN", "此操作会创建新题目，请确认")
    title = prompt("题目标题: ").strip()
    r = client.post("/fe/api/problem/new", json={"title": title})
    return r.json()


def edit_problem(pid):
    """编辑题目"""
    log("WARN", f"将编辑题目 {pid}")
    r = client.post(f"/fe/api/problem/edit/{pid}", json={"settings": {}})
    return r.json()


def edit_testcase(pid):
    """编辑测试数据"""
    r = client.post(f"/fe/api/problem/editTestCase/{pid}", json={})
    return r


def transfer_problem(pid):
    """转移/克隆题目"""
    log("WARN", f"将转移题目 {pid}")
    r = client.post(f"/fe/api/problem/transfer/{pid}", json={})
    return r.json()


def delete_problem(pid):
    """删除题目"""
    if not confirm(f"删除题目 {pid}"):
        return None
    r = client.post(f"/fe/api/problem/delete/{pid}")
    return r.json()


APIS = {
    "list": list_problems,
    "created": created_problems,
    "get": get_problem,
    "solutions": get_solutions,
    "bookmark": bookmark_problem,
    "remove_bookmark": remove_bookmark,
    "submit": submit_code,
    "translate": submit_translation,
    "create": create_problem,
    "edit": edit_problem,
    "edit_testcase": edit_testcase,
    "transfer": transfer_problem,
    "delete": delete_problem,
}

if __name__ == "__main__":
    def _interactive():
        list_problems()
        created_problems()
        get_problem()
        get_solutions()
        if confirm("收藏题目 P1001"):
            bookmark_problem("P1001")
        if confirm("取消收藏 P1001"):
            remove_bookmark("P1001")
        if confirm("提交代码到 P1001"):
            submit_code()
        if confirm("提交翻译到 P1001"):
            submit_translation("P1001")
        if confirm("创建新题目"):
            create_problem()
        pid = prompt("  测试编辑/测试数据/转移/删除的题目ID (留空跳过): ").strip()
        if pid:
            if confirm(f"编辑题目 {pid}"):
                edit_problem(pid)
            if confirm(f"编辑测试数据 {pid}"):
                edit_testcase(pid)
            if confirm(f"转移题目 {pid}"):
                transfer_problem(pid)
            if confirm(f"删除题目 {pid} (不可逆)"):
                delete_problem(pid)
    run_from_cli(APIS, _interactive)
