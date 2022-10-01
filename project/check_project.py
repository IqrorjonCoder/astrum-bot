import pandas as pd
import sqlite3
from datas.mentors import mentors
import numpy as np
from buttons import buttons


def check_project(update, context):
    x = list(mentors.values())
    y = []
    for i in x:
        for j in i:
            y.append(j)
    y = np.array(y)
    if update.message.chat_id in y:

        message = update.message.text
        update.message.reply_text("✅ Tekshirildi ✅")
        username = [i.split(': ') for i in update.message.reply_to_message.caption.split("\n")][-2][-1]

        connection = sqlite3.connect("/home/iqrorjon/PycharmProjects/astrum-bot/database/user_datas.db")
        id = pd.read_sql(f"SELECT chat_id FROM users WHERE qwasar_username='{username}'", connection)['chat_id'][0]

        context.bot.sendDocument(
            chat_id=int(id),
            caption=f"{update.message['reply_to_message']['caption']}\n\n✅ Tekshirildi ✅\n#feedback : {message.replace('#feed', '')}",
            document=update.message['reply_to_message']['document']['file_id'])
    else:
        update.message.reply_text("*❌❌❌*", parse_mode="Markdown", reply_markup=buttons.user_buttons)