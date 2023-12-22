import telebot
from telebot import types
import pymysql
import json

bot = telebot.TeleBot('6483038185:AAEkPUufyhe4PotSf4a-6z9Mj61zunLMVGU')
form_webapp = types.WebAppInfo("https://euphonious-melba-92fb97.netlify.app/form")
choose_item_webapp_inline = types.WebAppInfo("https://euphonious-melba-92fb97.netlify.app/items")
choose_item_webapp_keyboard = types.WebAppInfo("https://euphonious-melba-92fb97.netlify.app/things")

# поднимаем базу
conn = pymysql.connect(
    host='localhost',
    user='admin',
    password="admin",
)
cur = conn.cursor()


# метод для получения текстовых сообщений
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/start":
        user_id = message.from_user.id
        username = message.from_user.username
        # проверяем пользователя
        query = "INSERT IGNORE INTO mysql.telegram_user (uuid,username) VALUES (" + str(user_id) + \
                ", \"" + str(username) + "\" );"
        cur.execute(query)
        conn.commit()

        menu(message)

    elif message.text == "/dbs":
        cur.execute("SELECT t.* FROM mysql.point-self t LIMIT 501;")
        strlist = []
        for x in cur:
            strlist.append(str(x) + "\n")
        bot.send_message(message.from_user.id, ''.join(strlist))
    elif message.text == "/help":
        bot.send_message(message.from_user.id,
                         '🌿 Это бот, который поможет тебе сдать мусор экологично.\n' +
                         '*📍 Зона поиска* поможет тебе задать твоё местоположение и радиус поиска.\n' +
                         'А *🔎 Найти точки рядом* покажет актуальные пункты для выбранных типов отходов. \n' +
                         '▶️ Для начала работы напиши /start.', parse_mode='Markdown')
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


@bot.message_handler(content_types=["web_app_data"])  # получаем отправленные от webapp данные
def answer(webapp_message):
    print(webapp_message)  # вся информация о сообщении
    print(webapp_message.web_app_data.data)  # конкретно то что мы передали в бота
    # ------------------ЗОНА ПОИСКА
    if webapp_message.web_app_data.button_text == '📍 Зона поиска':
        user_id = webapp_message.from_user.id
        data = json.loads(webapp_message.web_app_data.data)
        try:
            data['radius'] = int(data['radius'])
        except ValueError:
            bot.send_message(webapp_message.chat.id,
                             f"Произошла ошибка, вы ввели в поле \"Радиус\" значение \"{data['radius']}\".\n" +
                             'Пожалуйста, попробуйте еще раз и введите целое число километров.')
            return
        # Формат данных: {"region":"Новосибирская область","city":"Новосибирск","street":"Ильича","radius":"4"}
        query = "UPDATE mysql.telegram_user SET region_name= \"" + str(data['region']) + \
                "\", city_name= \"" + str(data['city']) + \
                "\", address= \"" + str(data['street']) + \
                "\", radius=" + str(data['radius']) + \
                " WHERE uuid=" + str(user_id) + ";"
        cur.execute(query)
        conn.commit()

        bot.send_message(webapp_message.chat.id, f"Местоположение сохранено: \nРегион: {data['region']}\n" +
                         f"Город: {data['city']}\nУлица:{data['street']}\nРадиус поиска: {data['radius']} км")

    # ---------------------- НАЙТИ ТОЧКИ РЯДОМ
    elif webapp_message.web_app_data.button_text == '🔎 Найти точки рядом':
        # Список ID выбранных категорий (1: Одежда, 2: Батарейки, 3: Бумага, 4: Лампочки)
        items_ids = [i["id"] for i in json.loads(webapp_message.web_app_data.data)]
        # Одежда 10, батарейки 8,бумага 9, лампочки 12

        cur.execute("(SELECT DISTINCT city_name FROM mysql.telegram_user WHERE uuid= \"" + \
                str(webapp_message.from_user.id) + "\" );")

        for r in cur:
            if (r[0] is None):
                bot.send_message(webapp_message.chat.id,
                                 "Вы не ввели локацию поиска. Перейдите по кнопке *📍 Зона поиска*",
                                 parse_mode='Markdown')
                return

        # достаем id города
        cur.execute("USE `mysql`;")
        query = "SELECT DISTINCT uuid FROM `city-self` WHERE city_name IN" \
                "(SELECT DISTINCT city_name FROM telegram_user WHERE uuid= \"" + \
                str(webapp_message.from_user.id) + "\" );"
        cur.execute(query)
        cur_list = []
        for x in cur:
            cur_list.append(str(x))
        city_id = cur_list[0]
        city_id = city_id[1]
        # форматируем id категорий
        id_given = query_ids(items_ids)
        id_converted = convert_ids(id_given)
        #ищем адреса по категориям и городу
        query = "SELECT DISTINCT street_name FROM `address` WHERE uuid IN" \
                "(SELECT DISTINCT address_uuid FROM `point-self` WHERE uuid IN" \
                " (SELECT DISTINCT uuid FROM `point-types` WHERE avl_types in" \
                + id_converted + ") AND city_uuid= " + city_id + ");"
        cur.execute(query)
        strlist = []
        for x in cur:
            temp = str(x)
            for char in '()\'':
                temp = temp.replace(char, '')
            strlist.append(temp + "\n")
        bot.send_message(webapp_message.chat.id,
                         ''.join(strlist))

    else:
        bot.send_message(webapp_message.chat.id, f"Произошла ошибка. Попробуйте еще раз.")
    # отправляем сообщение в ответ на отправку данных из веб-приложения


def query_ids(ids):
    res = "("
    for x in ids:
        res = res + str(x) + ","
    res = res[:-1]
    res += ")"
    return res


def convert_ids(str_ids):
    if "1" in str_ids:
        str_ids = str_ids.replace("1", "10")
    elif "2" in str_ids:
        str_ids = str_ids.replace("2", "8")
    elif "3" in str_ids:
        str_ids = str_ids.replace("3", "9")
    elif "4" in str_ids:
        str_ids = str_ids.replace("4", "12")
    return str_ids


def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('📍 Зона поиска', web_app=form_webapp)
    btn2 = types.KeyboardButton('🔎 Найти точки рядом', web_app=choose_item_webapp_keyboard)
    btn3 = types.KeyboardButton('🤔 Как сдавать')
    btn4 = types.KeyboardButton('✅ Отметиться')
    btn5 = types.KeyboardButton('💯 Рейтинг')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    bot.send_message(message.from_user.id, '⬇ Выберите действие', reply_markup=markup)


# метод который бесконечно крутит бота на сервере
bot.polling(none_stop=True, interval=0)
