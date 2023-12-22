import telebot
from telebot import types
import json

bot = telebot.TeleBot('6483038185:AAEkPUufyhe4PotSf4a-6z9Mj61zunLMVGU')

form_webapp = types.WebAppInfo("https://euphonious-melba-92fb97.netlify.app/form")
choose_item_webapp_inline = types.WebAppInfo("https://euphonious-melba-92fb97.netlify.app/items")
choose_item_webapp_keyboard = types.WebAppInfo("https://euphonious-melba-92fb97.netlify.app/things")

# метод для получения текстовых сообщений
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/start":
        user_id = message.from_user.id
        username = message.from_user.username
        menu(message)
        # TODO: добавить юзера с user_id и username в БД

    elif message.text == "/help":
        bot.send_message(message.from_user.id,
                         '🌿 Это бот, который поможет тебе сдать мусор экологично.\n' +
                         '*📍 Зона поиска* поможет тебе задать твоё местоположение и радиус поиска.\n' +
                         'А *🔎 Найти точки рядом* покажет актуальные пункты для выбранных типов отходов. \n' +
                         '▶️ Для начала работы напиши /start.', parse_mode='Markdown')
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

@bot.message_handler(content_types=["web_app_data"]) #получаем отправленные от webapp данные
def answer(webapp_message):
   print(webapp_message) #вся информация о сообщении
   print(webapp_message.web_app_data.data) #конкретно то что мы передали в бота
   # ------------------ЗОНА ПОИСКА
   if webapp_message.web_app_data.button_text == '📍 Зона поиска':
       ser_id = webapp_message.from_user.id
       username = webapp_message.from_user.username
       data = json.loads(webapp_message.web_app_data.data)
       try:
           data['radius'] = int(data['radius'])
       except ValueError:
           bot.send_message(webapp_message.chat.id, f"Произошла ошибка, вы ввели в поле \"Радиус\" значение \"{data['radius']}\".\n" +
                            'Пожалуйста, попробуйте еще раз и введите целое число километров.')
           return
       # Формат данных: {"region":"Новосибирская область","city":"Новосибирск","street":"Ильича","radius":"4"}
       # TODO: добавить местоположение юзера в БД
       bot.send_message(webapp_message.chat.id, f"Местоположение сохранено: \nРегион: {data['region']}\n" +
                        f"Город: {data['city']}\nУлица:{data['street']}\nРадиус поиска: {data['radius']} км")

# ---------------------- НАЙТИ ТОЧКИ РЯДОМ
   elif webapp_message.web_app_data.button_text == '🔎 Найти точки рядом':
       #!! выбери какой удобнее список - строчки или айдишники
       # Список названий выбранных категорий (Одежда, Батарейки, Лампочки, Бумага)
       items = [i["title"] for i in json.loads(webapp_message.web_app_data.data)]
       # Список ID выбранных категорий (1: Одежда, 2: Батарейки, 3: Бумага, 4: Лампочки)
       items_ids = [i["id"] for i in json.loads(webapp_message.web_app_data.data)]
       # TODO: условие, если пользователь не ввел местоположение, пусть идет вводит
       #if <пользователь не ввел местоположение>:
       #    bot.send_message(webapp_message.chat.id,"Вы не ввели локацию поиска. Перейдите по кнопке *📍 Зона поиска*", parse_mode='Markdown')
       # TODO: запрос к БД - поиск пунктов
       bot.send_message(webapp_message.chat.id,
                        f"Здесь будут пункты выдачи")


   else:
    bot.send_message(webapp_message.chat.id, f"Произошла ошибка. Попробуйте еще раз.")
   #отправляем сообщение в ответ на отправку данных из веб-приложения

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
