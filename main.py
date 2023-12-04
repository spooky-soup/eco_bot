import telebot
import pymysql

bot = telebot.TeleBot('6483038185:AAEkPUufyhe4PotSf4a-6z9Mj61zunLMVGU')

conn = pymysql.connect(
    host='localhost',
    user='admin',
    password="admin",
)

# метод для получения текстовых сообщений
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, "Привет, это ЭкоБот.")
    elif message.text == "/dbs":
        cur = conn.cursor()
        cur.execute("SHOW TABLES FROM mysql;")
        strlist = []
        for x in cur:
            strlist.append(str(x) + "\n")
        bot.send_message(message.from_user.id, ''.join(strlist))
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Для начала работы напиши /start." + "\n" +
                         "Для вывода всех табличек напиши /dbs.")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


# метод который бесконечно крутит бота на сервере
bot.polling(none_stop=True, interval=0)
