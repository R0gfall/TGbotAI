from multiprocessing import connection
import bcrypt

import psycopg2
from config import host, user, port, password, database_name
from app.states import TypeLog
from backend.crypt import check_password, hash_password


def connect_to_database(type_doing: TypeLog, id_chat: int, login_user: str, password_user: str) -> str:
    connection = None
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            port=port,
            password=password,
            database=database_name
        )
        connection.autocommit = True
        print("Connected to PostgreSQL")
        message_to_await = user_in_database(id_chat, login_user, password_user, type_doing, connection)
        print(message_to_await)



    except psycopg2.Error as e:
        print("[ERROR] Failed to connect to PostgreSQL instance:", e)
    finally:
        if connection:
            connection.close()
            print("PostgreSQL connection closed")
        return message_to_await


def user_in_database(id_chat: int, login_user: str, password_user: str, type_doing: TypeLog, connection: connection) -> str:

    if type_doing == TypeLog.REGISTRATION:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM users_table WHERE id_user_chat = %s;", (id_chat,)
            )
            if cursor.fetchone() is not None:
                print("User already exists for this ID chat")
                # Доделать вывод через бота await
                return "This ID chat already exists!"

            else:
                cursor.execute(
                    """INSERT INTO users_table (id_user_chat, login_user, password_user, stable_flag, admin_count)
                    VALUES (%s, %s, %s, true, 0);""", (id_chat, login_user, password_user.decode('utf-8')),
                )
                print("User registered for this ID chat")
                print(password_user)
                return "User registered successfully!"

    elif type_doing == TypeLog.LOGIN:
        with connection.cursor() as cursor:
            # cursor.execute(
            #     """SELECT * FROM users_table
            #     WHERE login_user = %s and password_user = %s;""", (login_user, password_user,)
            # )
            cursor.execute(
                """SELECT password_user FROM users_table
                WHERE login_user = %s""", (login_user,)
            )
            result = cursor.fetchone()

            if check_password(password_user, result[0]) == False:
                print("Incorrect credentials")
                return "Incorrect credentials!"

            else:
                print("Login successful")
                # добавить флаг, что под этим id человек зашел
                cursor.execute(
                    """UPDATE users_table
                    SET stable_flag = true
                    WHERE login_user = %s and password_user = %s;""", (login_user, password_user,)
                )
                print("Login successful!")
                return "Login successful!"

    elif type_doing == TypeLog.LOGOUT:
        with connection.cursor() as cursor:
            cursor.execute(
                """UPDATE users_table
                SET stable_flag = false
                WHERE login_user = %s and password_user = %s;""", (login_user, password_user,)
            )
            print("Logout successful!")
            return "Logout successful!"


