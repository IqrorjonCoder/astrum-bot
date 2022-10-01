import telegram
from telegram.ext import MessageHandler, CommandHandler, ConversationHandler, Updater, Filters
from buttons import buttons
from registration import registration, sign_in
import sqlite3
import numpy as np
import pandas as pd
from project import send_project
from datas import see_progress
from project import check_project


def start(update, context):
    if update.message.chat_id in np.array(pd.read_sql("""SELECT chat_id FROM users""", sqlite3.connect(
            "/home/iqrorjon/PycharmProjects/astrum-bot/database/user_datas.db"))).flatten():
        update.message.reply_text("*Siz allaqachon ro'yhatdan o'tgansiz*", parse_mode="Markdown",
                                  reply_markup=buttons.user_buttons)
    else:
        update.message.reply_text("<b>Salom !\nBu Astrum IT Academiyasining mentorlari va studentlari uchun bot !</b>",
                                  parse_mode=telegram.ParseMode.HTML,
                                  reply_markup=buttons.registration_button)


def runner():
    updater = Updater(token="5333086108:AAHWOxN_ZQf0oBFKYC0MbIX0NRa0sRoPDlU")
    dispacher = updater.dispatcher

    dispacher.add_handler(CommandHandler('start', start))
    dispacher.add_handler(CommandHandler('stop', start))

    dispacher.add_handler(ConversationHandler(
        entry_points=[MessageHandler(Filters.regex("📋Ro'yhatdan o'tish"), registration.start_registration)],
        states={
            1: [MessageHandler(Filters.text, registration.username)],
            2: [MessageHandler(Filters.text, registration.firstname)],
            3: [MessageHandler(Filters.text, registration.lastname)],
            4: [MessageHandler(Filters.contact, registration.phone_number)],
            5: [MessageHandler(Filters.text, registration.season)],
            6: [MessageHandler(Filters.text, registration.study_type)],
            7: [MessageHandler(Filters.text, registration.parol1)],
            8: [MessageHandler(Filters.text, registration.parol2)],
            9: [MessageHandler(Filters.text, registration.submit)],
        },
        fallbacks=[CommandHandler('stop', start)]
    ))

    dispacher.add_handler(ConversationHandler(
        entry_points=[MessageHandler(Filters.regex("📋Tizimga kirish"), sign_in.start_sign_in)],
        states={
            1: [MessageHandler(Filters.text, sign_in.username)],
            2: [MessageHandler(Filters.text, sign_in.submit)]
        },
        fallbacks=[CommandHandler('stop', start)]
    ))

    dispacher.add_handler(MessageHandler(Filters.regex("📚 Progress ko'rish 📖"), see_progress.see_progress))

    dispacher.add_handler(ConversationHandler(
        entry_points=[MessageHandler(Filters.regex("📚Proyektni topshirish"), send_project.start_sending_project)],
        states={
            1: [MessageHandler(Filters.text, send_project.project_name)],
            2: [MessageHandler(Filters.text, send_project.project_feedback)],
            3: [MessageHandler(Filters.document, send_project.project_file)],
            4: [MessageHandler(Filters.text, send_project.submit)]
        },
        fallbacks=[CommandHandler('stop', start)]
    ))

    dispacher.add_handler(MessageHandler(Filters.regex("(#feed {1,5}\S.+)"), check_project.check_project))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    print("Ishga tushdi ...")
    runner()
