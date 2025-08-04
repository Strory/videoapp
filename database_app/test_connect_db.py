# test_connection.py
from sqlalchemy import create_engine

# Тестовая строка подключения
DATABASE_URL = "postgresql://app_user:1234@localhost/video_app_db"

try:
    engine = create_engine(DATABASE_URL)
    connection = engine.connect()
    print("✅ Подключение успешно!")
    connection.close()
except Exception as e:
    print(f"❌ Ошибка подключения: {e}")