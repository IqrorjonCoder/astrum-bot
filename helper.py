import pandas as pd
import sqlite3

connection = sqlite3.connect("C:/Users/Student/PycharmProjects/astrummentors/astrummentor/database/user_datas.db")
data = pd.read_sql("SELECT qwasar_username FROM users WHERE chat_id=1035463819", connection)
print(data['qwasar_username'][0])
