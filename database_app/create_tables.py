# # Этот скрипт нужно запустить один раз для создания таблиц
# from database import Base, engine
# import models  # Импортируем модели (это важно!)
#
# # Создаём все таблицы, описанные в models.py
# Base.metadata.create_all(bind=engine)
#
# print("Таблицы созданы успешно!")


from database_app.database import Base, engine
import database_app.models


def create_tables():
    print("Подключаюсь к базе данных...")
    print(f"URL: {engine.url}")

    # Проверим, что модели импортировались
    print("Зарегистрированные таблицы:")
    for table_name in Base.metadata.tables:
        print(f"  - {table_name}")

    print("Создаю таблицы...")
    try:
        Base.metadata.create_all(bind=engine, checkfirst=True)
        print("✅ Таблицы созданы успешно!")

        # Проверим, что таблицы действительно есть
        from sqlalchemy import text
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
            tables = [row[0] for row in result]
            print("Таблицы в базе данных:", tables)

    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    create_tables()
