import numpy as np
import pandas as pd
import sqlite3
from buttons import buttons


def see_progress(update, context):
    message = update.message.text
    chat_id = update.message.chat_id

    if chat_id in np.array(pd.read_sql("SELECT chat_id FROM users", sqlite3.connect("C:/Users/Student/PycharmProjects/astrummentors/astrummentor/database/user_datas.db")).values).flatten():
        update.message.reply_text(f"islomov iqrorjon 2005.08.24 *{chat_id}*", parse_mode="Markdown", reply_markup=buttons.user_buttons)
    else:
        update.message.reply_text("*Siz boshqa akkountdan foydalanyapsiz. Shuning uchun qayta tizimga kiring !*", parse_mode="Markdown", reply_markup=buttons.registration_button)
