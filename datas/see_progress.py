import numpy as np
import pandas as pd
import sqlite3
from buttons import buttons


def see_progress(update, context):
    message = update.message.text
    chat_id = update.message.chat_id

    if chat_id in np.array(pd.read_sql("SELECT chat_id FROM users", sqlite3.connect("C:/Users/student.ASTRUM-DOMAIN/AppData/IqrorjonCoder/python-projects/astrum-bot/database/user_datas.db")).values).flatten():
        data = pd.read_sql(f"SELECT qwasar_username FROM users WHERE chat_id={chat_id}", sqlite3.connect("C:/Users/student.ASTRUM-DOMAIN/AppData/IqrorjonCoder/python-projects/astrum-bot/database/user_datas.db"))['qwasar_username'][0]
        update.message.reply_text(data)

        df = pd.read_csv("C:/Users/student.ASTRUM-DOMAIN/AppData/IqrorjonCoder/python-projects/astrum-bot/database/data.csv")
        df = df[df['username'] == f"{data}"].values.flatten()[-1]
        update.message.reply_text(df)

    else:
        update.message.reply_text("*Siz boshqa akkountdan foydalanyapsiz. Shuning uchun qayta tizimga kiring !*", parse_mode="Markdown", reply_markup=buttons.registration_button)
