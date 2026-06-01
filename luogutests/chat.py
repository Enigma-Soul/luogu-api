from base import LuoguClient, log, confirm

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


if __name__ == "__main__":
    list_conversations()
    uid = input("  对方UID (查看私信记录，留空跳过): ").strip()
    if uid:
        get_messages(uid)

    if uid and confirm(f"发送私信给 {uid}"):
        content = input("  内容: ").strip()
        send_message(int(uid), content)
    if uid and confirm(f"清除与 {uid} 的未读"):
        clear_unread(int(uid))
    msg_id = input("  要删除的消息ID (留空跳过): ").strip()
    if msg_id and confirm(f"删除消息 {msg_id}"):
        delete_message(int(msg_id))
