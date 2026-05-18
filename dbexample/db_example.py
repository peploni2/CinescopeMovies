import psycopg2

def connect_to_postgres():
    connection = None
    cursor = None

    try:
        connection = psycopg2.connect(
            dbname="testdb",
            user="postgres",
            password="password",
            host="localhost",
            port="5432"
        )

        print("Подключение успешно установлено")

        cursor = connection.cursor()

        print("Информация о сервере PostgreSQL:")
        print(connection.get_dsn_parameters(), "\n")

        cursor.execute("SELECT version()")

        record = cursor.fetchone()
        print("Вы подключены к - ", record, "\n")

    except Exception as error:
        print("Ошибка при работе с PostgreSQL:", error)

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            print("Соединение с PostgreSQL закрыто")

if __name__ == "__main__":
    connect_to_postgres()
