import telebot
from telebot import types
bot = telebot.TeleBot('6483038185:AAEkPUufyhe4PotSf4a-6z9Mj61zunLMVGU')

form_webapp = types.WebAppInfo("https://main--euphonious-melba-92fb97.netlify.app/form")


# метод для получения текстовых сообщений
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/start":
        menu(message)
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Для начала работы напиши /start.")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

@bot.message_handler(content_types=["web_app_data"]) #получаем отправленные данные
def answer(webapp_message):
   print(webapp_message) #вся информация о сообщении
   print(webapp_message.web_app_data.data) #конкретно то что мы передали в бота
   bot.send_message(webapp_message.chat.id, f"получили инофрмацию из веб-приложения: {webapp_message.web_app_data.data}")
   #отправляем сообщение в ответ на отправку данных из веб-приложения

def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Найти место', web_app=form_webapp)
    btn2 = types.KeyboardButton('Как сдавать')
    btn3 = types.KeyboardButton('Отметиться')
    btn4 = types.KeyboardButton('Рейтинг')
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.from_user.id, '⬇ Выберите действие', reply_markup=markup)

# метод который бесконечно крутит бота на сервере
bot.polling(none_stop=True, interval=0)
