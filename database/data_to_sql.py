import sqlite3

# connection = sqlite3.connect("C:/Users/student.ASTRUM-DOMAIN/AppData/IqrorjonCoder/python-projects/astrum-bot/database/user_datas.db")
# connection.execute("""
# CREATE TABLE users (qwasar_username CHAR(20) PRIMARY KEY, ism CHAR(20), familiya CHAR(20), telefon_raqam INTEGER, season CHAR(20), yonalish CHAR(25), chat_id INTEGER, tme_username CHAR(20), parol CHAR(30))
# """)

def insert_to_data(qwasar_username, ism, familiya, telefon_raqam, season, yonalish, chat_id, tme_username, parol):
    connection = sqlite3.connect("C:/Users/student.ASTRUM-DOMAIN/AppData/IqrorjonCoder/python-projects/astrum-bot/database/user_datas.db")
    connection.execute(f"""
    INSERT INTO users(qwasar_username, ism, familiya, telefon_raqam, season, yonalish, chat_id, tme_username, parol)
    VALUES ('{qwasar_username}', '{ism}', '{familiya}', {telefon_raqam}, '{season}', '{yonalish}', {chat_id}, '{tme_username}', '{parol}')
    """)
    connection.commit()
    connection.close()


def update_user_chatid(username, chat_id, tme_username):
    connection = sqlite3.connect("C:/Users/student.ASTRUM-DOMAIN/AppData/IqrorjonCoder/python-projects/astrum-bot/database/user_datas.db")
    connection.execute(f"""
    UPDATE users SET chat_id={chat_id}, tme_username='{tme_username}' WHERE qwasar_username='{username}';
    """)
    connection.commit()
    connection.close()