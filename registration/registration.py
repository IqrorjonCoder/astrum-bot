import numpy as np
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler, MessageHandler, Filters, CommandHandler
from buttons import buttons
import sqlite3
import pandas as pd

states = {
    'qwasar_username': 1,
    'ism': 2,
    'familiya': 3,
    'telefon_raqami': 4,
    'season': 5,
    'yonalish': 6,
    'parol1': 7,
    'parol2': 8,
    'tasdiqlash': 9
}


def start_registration(update, context):
    update.message.reply_text("*Qwasardagi usernamingizni kiriting ?*", parse_mode="Markdown",
                              reply_markup=ReplyKeyboardRemove())
    return states['qwasar_username']


def username(update, context):
    connection = sqlite3.connect("C:/Users/Student/PycharmProjects/astrummentors/astrummentor/database/user_datas.db")
    message = update.message.text

    if message in np.array(pd.read_sql("""SELECT qwasar_username FROM users""", connection)).flatten():
        update.message.reply_text("*Siz allaqachon ro'yxatdan o'tgansiz !*", parse_mode="Markdown", reply_markup=buttons.registration_button)
        return ConversationHandler.END
    elif message in np.load('C:/Users/Student/PycharmProjects/astrummentors/astrummentor/datas/students-usernames.npz')[
        'usernames'] and (message in np.array(pd.read_sql("""SELECT qwasar_username FROM users""", connection)).flatten()) == False:
        context.user_data['qwasar_username'] = message
        update.message.reply_text("*Ismingizni kiriting ?*", parse_mode="Markdown")
        return states['ism']
    else:
        update.message.reply_text("*Qwasardagi usernamingiz xato. tog'ri kiriting ?*", parse_mode="Markdown")
        return states['qwasar_username']


def firstname(update, context):
    message = update.message.text
    context.user_data['ism'] = message
    update.message.reply_text("*Familiyangizni kiriting ?*", parse_mode="Markdown")
    return states['familiya']


def lastname(update, context):
    message = update.message.text
    context.user_data['familiya'] = message
    update.message.reply_text("*Telefon raqamingizni jo'nating ?*", parse_mode="Markdown",
                              reply_markup=ReplyKeyboardMarkup(buttons.contact, resize_keyboard=True))
    return states['telefon_raqami']


def phone_number(update, context):
    message = update.message.contact.phone_number
    context.user_data['telefon_raqami'] = message
    update.message.reply_text("*Qaysi season o'quvchisisiz ?*", parse_mode="Markdown", reply_markup=buttons.seasons)
    return states['season']


def season(update, context):
    message = update.message.text
    context.user_data['season'] = message
    update.message.reply_text("*Qaysi yo'nalishda o'qiysiz ?*", parse_mode="Markdown", reply_markup=buttons.study_types)
    return states['yonalish']


def study_type(update, context):
    message = update.message.text
    context.user_data['yonalish'] = message
    update.message.reply_text("* Akkountingiz uchun parol kiriting *",
                              parse_mode="Markdown", reply_markup=ReplyKeyboardRemove())

    return states['parol1']


def parol1(update, context):
    message = update.message.text
    context.user_data['parol1'] = message
    update.message.reply_text(f"* Akkountingiz uchun parolingizni (_{context.user_data['parol1']}_) qayta kiriting *",
                              parse_mode="Markdown")
    return states['parol2']

def parol2(update, context):
    message = update.message.text
    if message != context.user_data['parol1']:
        update.message.reply_text(f"Xato. (_{context.user_data['parol1']}_)parolni qayta kiriting !", parse_mode="Markdown")
        return states['parol2']
    else:
        context.user_data['parol2'] = message
        update.message.reply_text(
            f"""username : *{context.user_data['qwasar_username']}*\nism : *{context.user_data['ism']}*\nfamiliya : *{context.user_data['familiya']}*\ntelefon : *+{context.user_data['telefon_raqami']}*\nseason : *{context.user_data['season']}*\nyo'nalish : *{context.user_data['yonalish']}*\nparol : *{context.user_data['parol2']}*""",
            parse_mode="Markdown")
        update.message.reply_text("*tasdiqlang ?*", parse_mode="Markdown", reply_markup=buttons.submit)
        return states['tasdiqlash']

def submit(update, context):

    message = update.message.text
    if message == "❌Tasdiqlamaslik":
        i = 0
        while True:
            try:
                context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id - i)
                i += 1
            except:
                break
        update.message.reply_text("*❌ Tasdiqlanmadi* \n /start ni bosing", parse_mode="Markdown", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    elif message == "✅Tasdiqlash":
        i = 0
        while True:
            try:
                context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id - i)
                i += 1
            except:
                break
        update.message.reply_text("*muffaqiyatli ro'yxatda o'tdingiz !!!*", parse_mode="Markdown",
                                  reply_markup=ReplyKeyboardRemove())
        update.message.reply_text(
            f"""username : *{context.user_data['qwasar_username']}*\nism : *{context.user_data['ism']}*\nfamiliya : *{context.user_data['familiya']}*\ntelefon : *+{context.user_data['telefon_raqami']}*\nseason : *{context.user_data['season']}*\nyo'nalish : *{context.user_data['yonalish']}*\nparol : *{context.user_data['parol2']}*""",
            parse_mode="Markdown")
        update.message.reply_text("*✅ Tasdiqlandi*", parse_mode="Markdown", reply_markup=buttons.user_buttons)

        context.user_data['chat_id'] = update.message.chat_id
        context.user_data['tme_username'] = update.message.from_user.username

        if context.user_data['tme_username'] == None:
            context.user_data['tme_username'] = "none"

        from database.data_to_sql import insert_to_data
        insert_to_data((context.user_data['qwasar_username']),
                       (context.user_data['ism']),
                       (context.user_data['familiya']),
                       (context.user_data['telefon_raqami']),
                       (context.user_data['season']),
                       (context.user_data['yonalish']),
                       (context.user_data['chat_id']),
                       (context.user_data['tme_username']),
                       (context.user_data['parol2']))

        return ConversationHandler.END