from telegram.ext import ConversationHandler, MessageHandler, CommandHandler
import numpy as np
import pandas as pd
import sqlite3
from buttons import buttons
from database import data_to_sql

states = {
    "qwasar_username": 1,
    "password": 2
}


def start_sign_in(update, context):
    update.message.reply_text("*Qwasar usernamingizni kiriting :*", parse_mode="Markdown")
    return states["qwasar_username"]


def username(update, context):
    message = update.message.text

    if message in np.array(pd.read_sql("""SELECT qwasar_username FROM users""", sqlite3.connect("C:/Users/student.ASTRUM-DOMAIN/AppData/IqrorjonCoder/python-projects/astrum-bot/database/user_datas.db"))).flatten():
        context.user_data['qwasar_username'] = message
        update.message.reply_text("*Parolingizni kiriting :*", parse_mode="Markdown")
        return states["password"]
    else:
        update.message.reply_text("*Siz hali ro'yhatdan o'tmagansiz ❗*", parse_mode="Markdown", reply_markup=buttons.registration_button)
        return ConversationHandler.END


def submit(update, context):
    message = update.message.text
    if message == pd.read_sql(f"SELECT parol FROM users WHERE qwasar_username='{context.user_data['qwasar_username']}'", sqlite3.connect("C:/Users/student.ASTRUM-DOMAIN/AppData/IqrorjonCoder/python-projects/astrum-bot/database/user_datas.db"))['parol'][0]:

        context.user_data['tme_username'] = update.message.from_user.username
        if context.user_data['tme_username'] == None:
            context.user_data['tme_username'] = "none"

        data_to_sql.update_user_chatid(context.user_data['qwasar_username'], update.message.chat_id, context.user_data['tme_username'])
        update.message.reply_text("*Siz tizimga muvaffaqiyatli kirdingiz ✅*", parse_mode="Markdown", reply_markup=buttons.user_buttons)
        return ConversationHandler.END
    else:
        update.message.reply_text("*❌ Parol xato ❌*", parse_mode="Markdown", reply_markup=buttons.registration_button)
        return ConversationHandler.END