from base import LuoguClient, confirm, prompt, run_from_cli

client = LuoguClient()


def list_conversations():
    """获取私信列表"""
    data = client.content("/chat")
    return data


def get_messages(uid):
    """获取与某用户的私信记录"""
    data = client.content("/api/chat/record", params={"user": uid, "page": 1})
    return data


def send_message(uid, content):
    """发送私信"""
    r = client.post("/api/chat/new", json={"user": uid, "content": content})
    return r.json()


def delete_message(msg_id):
    """删除私信"""
    r = client.post("/api/chat/delete", json={"id": msg_id})
    return r.json()


def clear_unread(uid):
    """清除未读通知"""
    r = client.post("/api/chat/clearUnread", json={"user": uid})
    return r.json()


APIS = {
    "list": list_conversations,
    "messages": get_messages,
    "send": lambda uid, content: send_message(int(uid), content),
    "delete": lambda msg_id: delete_message(int(msg_id)),
    "clear_unread": lambda uid: clear_unread(int(uid)),
}

if __name__ == "__main__":
    def _interactive():
        list_conversations()
        uid = prompt("  对方UID (查看私信记录，留空跳过): ").strip()
        if uid:
            get_messages(uid)
        if uid and confirm(f"发送私信给 {uid}"):
            content = prompt("  内容: ").strip()
            send_message(int(uid), content)
        if uid and confirm(f"清除与 {uid} 的未读"):
            clear_unread(int(uid))
        msg_id = prompt("  要删除的消息ID (留空跳过): ").strip()
        if msg_id and confirm(f"删除消息 {msg_id}"):
            delete_message(int(msg_id))
    run_from_cli(APIS, _interactive)
