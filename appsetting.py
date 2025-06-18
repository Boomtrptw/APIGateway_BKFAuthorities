import os

protocol = "http://"
host = os.getenv("RENDER_EXTERNAL_HOSTNAME", "127.0.0.1")  # ใช้ค่าจาก Environment Variable ถ้ามี
port = os.getenv("PORT", 1704)  # หรือค่าพอร์ตที่กำหนดใน Render

base_url = f"{protocol}{host}:{port}"

print(base_url)  # สำหรับตรวจสอบการตั้งค่า