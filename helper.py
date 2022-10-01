import numpy as np
import pandas as pd
import sqlite3

# connection = sqlite3.connect("C:/Users/Student/PycharmProjects/astrummentors/astrummentor/database/user_datas.db")
# data = pd.read_sql("SELECT qwasar_username FROM users WHERE chat_id=1035463819", connection)
# print(data['qwasar_username'][0])

import numpy
data = np.load("C:/Users/student.ASTRUM-DOMAIN/AppData/IqrorjonCoder/python-projects/astrum-bot/datas/students-usernames.npz")
print(data['usernames'])
print(len(data['usernames']))