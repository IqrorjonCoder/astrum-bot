from telegram.ext import CommandHandler, ConversationHandler
from telegram import ReplyKeyboardRemove
import pandas as pd
import numpy as np
import sqlite3
from buttons import buttons
import random

states = {
    "project_name": 1,
    "project_feedback": 2,
    "project_file": 3,
    "submit": 4
}


def start_sending_project(update, context):
    chat_id = update.message.chat_id
    if chat_id in np.array(pd.read_sql("SELECT chat_id FROM users", sqlite3.connect("C:/Users/Student/PycharmProjects/astrummentors/astrummentor/database/user_datas.db")).values).flatten():
        update.message.reply_text("*Project nomini kiriting :*", parse_mode="Markdown", reply_markup=ReplyKeyboardRemove())
        return states["project_name"]
    else:
        update.message.reply_text("*Siz boshqa akkountdan foydalanyapsiz. Shuning uchun qayta tizimga kiring !*", parse_mode="Markdown", reply_markup=buttons.registration_button)
        return ConversationHandler.END


def project_name(update, context):
    message = update.message.text
    context.user_data['project_nomi'] = message
    update.message.reply_text("*Project uchun feedback yozing :*", parse_mode="Markdown", reply_markup=ReplyKeyboardRemove())
    return states["project_feedback"]


def project_feedback(update, context):
    message = update.message.text
    context.user_data['project_feedback'] = message
    update.message.reply_text("*Project faylini yuboring*", parse_mode="Markdown", reply_markup=ReplyKeyboardRemove())
    return states["project_file"]


def project_file(update, context):
    context.user_data['file_id'] = update.message['document']['file_id']
    update.message.reply_text("*Projectni tasdiqlang !*", parse_mode="Markdown", reply_markup=buttons.submit)

    context.bot.sendDocument(chat_id=update.message.chat_id, caption=f"""\n
project nomi : *{context.user_data['project_nomi']}*
project feedback : *{context.user_data['project_feedback']}*
            """, parse_mode="Markdown", document=context.user_data['file_id'])

    return states["submit"]


def submit(update, context):
    message = update.message.text
    if message == "✅Tasdiqlash":

        from datas.mentors import mentors

        connection = sqlite3.connect("C:/Users/Student/PycharmProjects/astrummentors/astrummentor/database/user_datas.db")
        data = pd.read_sql(f"SELECT * FROM users WHERE chat_id={update.message.chat_id}", connection)

        df = pd.read_sql(f"SELECT yonalish FROM users WHERE chat_id={update.message.chat_id}", connection)
        mentor = mentors[df['yonalish'][0]]
        index = random.randint(0, len(mentor)-1)
        id = mentor[index]

        context.bot.sendDocument(chat_id=id, caption=f"""\n
ism : *{data['ism'][0]}*
familiya : *{data['familiya'][0]}*
tme username : *@{data['tme_username'][0]}*
project nomi : *{context.user_data['project_nomi']}*
project feedback : *{context.user_data['project_feedback']}*
qwasar username : [{data['qwasar_username'][0]}](https://upskill.us.qwasar.io/users/{data['qwasar_username'][0]})
telefon raqami : *+{data['telefon_raqam'][0]}*""",
             parse_mode="Markdown",
             document=context.user_data['file_id'])

        update.message.reply_text("✅Tasdiqlandi !!!", reply_markup=buttons.user_buttons)
        return ConversationHandler.END

    else:
        update.message.reply_text("❌Tasdiqlanmadi !!!", reply_markup=buttons.user_buttons)
        return ConversationHandler.END