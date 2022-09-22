from telegram import ReplyKeyboardMarkup, KeyboardButton

registration_button = ReplyKeyboardMarkup([["📋Ro'yhatdan o'tish", "📋Tizimga kirish"]], resize_keyboard=True)
contact = [[KeyboardButton(text="📲Contact Yuborish", request_contact=True)]]
seasons = ReplyKeyboardMarkup([[u"🎓Season 1", u"‍🎓Season 2"],[u"‍🎓Season 3", u"‍🎓Season 4"]], resize_keyboard=True)
study_types = ReplyKeyboardMarkup([["💻Data Science", "💻Software Engineering"],["💻Full Stack"]], resize_keyboard=True)
submit = ReplyKeyboardMarkup([["✅Tasdiqlash", "❌Tasdiqlamaslik"]], resize_keyboard=True)
user_buttons = ReplyKeyboardMarkup([["📚Proyektni topshirish"], ["📚 Progress ko'rish 📖"]], resize_keyboard=True, one_time_keyboard=True)