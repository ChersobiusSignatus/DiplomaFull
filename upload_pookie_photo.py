import requests

# 🔗 API endpoint
url = "http://134.209.254.255:8000/plants/86a6c620-c278-4404-97ab-42291bb27892/photos"

# 📸 Путь к изображению на диске
image_path = "20bf04ad-73a1-42e6-8c20-a6d0c85170d3.jpg"  # укажи актуальный путь, если другое имя/папка

# 📤 Загрузка
with open(image_path, "rb") as image_file:
    files = {"file": image_file}
    response = requests.post(url, files=files)

# 📥 Ответ
if response.status_code == 200:
    print("✅ Фото успешно загружено!")
    print(response.json())
else:
    print("❌ Ошибка загрузки:")
    print(response.status_code, response.text)
