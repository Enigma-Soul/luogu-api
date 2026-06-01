from base import LuoguClient, log, confirm

client = LuoguClient()


def list_images(uid):
    """获取图片列表"""
    data = client.content("/image", params={"user": uid, "content": ""})
    return data


def get_image(image_id):
    """获取图片详情"""
    r = client.get(f"/api/image/detail/{image_id}")
    return r.json()


def generate_upload_link(watermark_type=0):
    """获取上传参数 (需要验证码)"""
    cap = client.captcha()
    r = client.get("/api/image/generateUploadLink", params={
        "watermarkType": watermark_type,
        "captcha": cap,
    })
    return r.json()


def delete_images(image_ids):
    """删除图片"""
    if isinstance(image_ids, str):
        image_ids = [image_ids]
    r = client.post("/api/image/delete", json={"images": image_ids})
    return r.json()


if __name__ == "__main__":
    uid = input("  用户UID (查看图片列表，留空跳过): ").strip()
    if uid:
        list_images(uid)
    image_id = input("  图片ID (查看详情，留空跳过): ").strip()
    if image_id:
        get_image(image_id)

    if confirm("获取上传参数"):
        generate_upload_link()
    ids = input("  要删除的图片ID (逗号分隔，留空跳过): ").strip()
    if ids and confirm(f"删除图片 {ids}"):
        delete_images(ids.split(","))
