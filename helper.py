import numpy as np
import pandas as pd
import sqlite3

connection = sqlite3.connect("/home/iqrorjon/PycharmProjects/astrum-bot/database/user_datas.db")
# data = pd.read_sql("SELECT * FROM users", connection)
# print(data)
connection.execute("""
DELETE FROM users;
""")
connection.commit()
connection.close()
# import numpy
# data = np.load("C:/Users/student.ASTRUM-DOMAIN/AppData/IqrorjonCoder/python-projects/astrum-bot/datas/students-usernames.npz")
# print(data['usernames'])
# print(len(data['usernames']))