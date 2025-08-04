import psycopg2

host = "127.0.0.1"
user = "app_user"
password = "1234"
db_name = "video_app_db"

try:
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
except Exception as _ex:
    print("ex: ", _ex)
finally:
    if connection:
        connection.close()
        print("connection close")
