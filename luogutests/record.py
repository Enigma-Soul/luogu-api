from base import LuoguClient, confirm, prompt, run_from_cli

client = LuoguClient()


def list_records():
    """获取评测记录列表"""
    data = client.content("/record/list", params={"page": 1})
    return data


def get_record(rid):
    """获取评测记录详情"""
    data = client.content(f"/record/{rid}")
    return data


def query_downloadable_testcase(rid):
    """查询可下载的测试点"""
    r = client.get(f"/fe/api/record/queryDownloadableTestcase/{rid}")
    return r.json()


def download_testcase(rid, testcase_id):
    """下载测试点内容"""
    r = client.post(f"/fe/api/record/downloadTestcase/{rid}", json={"testcaseId": testcase_id})
    return r.json()


APIS = {
    "list": list_records,
    "get": get_record,
    "query_downloadable": query_downloadable_testcase,
    "download": download_testcase,
}

if __name__ == "__main__":
    def _interactive():
        list_records()
        rid = prompt("  测试记录ID (留空跳过): ").strip()
        if rid:
            get_record(rid)
            if confirm(f"查询可下载测试点 (记录 {rid})"):
                result = query_downloadable_testcase(rid)
                tc_id = result.get("testcaseId")
                if tc_id and confirm(f"下载测试点 {tc_id}"):
                    download_testcase(rid, tc_id)
    run_from_cli(APIS, _interactive)
