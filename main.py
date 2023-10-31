import telebot
bot = telebot.TeleBot('6483038185:AAEkPUufyhe4PotSf4a-6z9Mj61zunLMVGU')

# метод для получения текстовых сообщений
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, "Привет, это ЭкоБот.")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Для начала работы напиши /start.")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


# метод который бесконечно крутит бота на сервере
bot.polling(none_stop=True, interval=0)
