import telebot 
import requests
import time 
import sqlite3
from telebot import types 

bot = telebot.TeleBot("")

name = 'None'
namelogin = 'None'
password = 'None'
id = 0
def check_credentials(password):
    conn = sqlite3.connect('telegram_users_databases.sql')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE pass=?', (password,))
    user = cur.fetchone()

    cur.close()
    conn.close()
    return user is not None

def oneperson(login):
    conn = sqlite3.connect('telegram_users_databases.sql')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE login=?', (login,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user is not None
from telebot import types

def get_reply_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=1)
    item1 = types.KeyboardButton('Отклонить запрос')
    item2 = types.KeyboardButton('Начислить принты')
    item3 = types.KeyboardButton('Просмотреть профиль пользователя')
    item4 = types.KeyboardButton('Вычесть поинты')
    markup.add(item1, item2, item3, item4)
    return markup


def iff(message):
        if message.text == 'Отклонить запрос': #исправлено
                markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
                item = types.KeyboardButton('Назад')
                markup.add(item)
                bot.send_message(message.chat.id, "Введите id:", reply_markup= markup)
                bot.register_next_step_handler(message, delete)
        elif message.text == 'Начислить принты': #исправлено
                markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
                item = types.KeyboardButton('Назад')
                markup.add(item)
                bot.send_message(message.chat.id, "Введите id:", reply_markup= markup)
                bot.register_next_step_handler(message, mer3)
        elif message.text == 'Просмотреть профиль пользователя': #исправлено
                markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
                item = types.KeyboardButton('Назад')
                markup.add(item)
                bot.send_message(message.chat.id, "Введите id:", reply_markup= markup)
                bot.register_next_step_handler(message, read)
        elif message.text == 'Вычесть поинты':
                markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
                item = types.KeyboardButton('Назад')
                markup.add(item)
                bot.send_message(message.chat.id, "Введите id:", reply_markup= markup)
                bot.register_next_step_handler(message, read123)
        else :
             bot.register_next_step_handler(message, iff)

def mer4(message, user_id):
            if message.text == 'Назад':
                 bot.send_message(message.chat.id, "Выберите категорию", reply_markup=get_reply_keyboard())
                 bot.register_next_step_handler(message, iff)
            else:
                coin1 = int(message.text.strip())
                conn = sqlite3.connect('telegram_users_databases.sql')
                cur = conn.cursor()

                cur.execute('SELECT coin FROM users WHERE users_id = ?', (user_id,))
                current_coin = cur.fetchone()
                if current_coin:  # Проверяем, существует ли значение current_coin
                    current_coin = current_coin[0]
                else:
                    bot.send_message(message.chat.id, "Пользователь с таким id не найден.")
                    cur.close()
                    conn.close()
                    return

                new_coin = current_coin - coin1
                cur.execute('UPDATE users SET coin = ? WHERE users_id = ?', (new_coin, user_id))
                conn.commit()

                bot.send_message(message.chat.id, f"Количество поинтов пользователя успешно обновлено. Текущее количество поинтов: {new_coin}")
                bot.send_message(user_id, f"У вас ушло {coin1} поинтов!")
                cur.close()
                conn.close()

                # Запрашиваем id пользователя для следующей операции
                bot.send_message(message.chat.id, "Введите id")
                bot.register_next_step_handler(message, read123)
def read123(message):
     if message.text == 'Назад':
        bot.send_message(message.chat.id, "Выберите категорию", reply_markup=get_reply_keyboard())
        bot.register_next_step_handler(message, iff)
     else:
          user_id = message.text.strip()  # Переименовали переменную, чтобы избежать конфликта с глобальной переменной
          conn = sqlite3.connect('telegram_users_databases.sql')
          cur = conn.cursor()
          cur.execute('SELECT * FROM users WHERE users_id=?', (user_id,))
          user_exists = cur.fetchone()
          if user_exists:
                bot.send_message(message.chat.id, "Введите количество поинтов для удаления")
                bot.register_next_step_handler(message, mer4, user_id)
          else:
                bot.send_message(message.chat.id, "Пользователь с таким id не найден.")
                bot.send_message(message.chat.id, "Введите id")
                bot.register_next_step_handler(message, read123)
          cur.close()


def read(message):
    if message.text == 'Назад':
        bot.send_message(message.chat.id, "Выберите категорию", reply_markup=get_reply_keyboard())
        bot.register_next_step_handler(message, iff)
    else :
         idid = message.text.strip()  
         conn = sqlite3.connect('telegram_users_databases.sql')
         cur = conn.cursor()
         cur.execute('SELECT login, pass, coin FROM users WHERE  users_id=?', (idid,))
         existing_user = cur.fetchone()
         cur.close()
         if existing_user:
              login, password, coins = existing_user
              bot.send_message(message.chat.id, f"Login: {login}")
              bot.send_message(message.chat.id, f"Password: {password}")
              bot.send_message(message.chat.id, f"Coins: {coins}")
              bot.send_message(message.chat.id, "Введите id")
              bot.register_next_step_handler(message, read)
         else:
              bot.send_message(message.chat.id, "Пользователь не найден.")
              bot.send_message(message.chat.id, "Введите id")
              bot.register_next_step_handler(message, read)


def delete(message):
    if message.text == 'Назад':
        bot.send_message(message.chat.id, "Выберите категорию", reply_markup=get_reply_keyboard())
        bot.register_next_step_handler(message, iff)
    else:
        id = message.text.strip()
        user_info = bot.get_chat_member('-1002009453022', id)
        username = user_info.user.username
        first_name = user_info.user.first_name
        bot.send_message(id, "Начисление поинтов отклонено")
        bot.send_message('-1002009453022', " запрос отклонен у пользователя с именем "  + first_name  + "  ID  " + id)
        bot.send_message(message.chat.id, f"Выберите метод", reply_markup = get_reply_keyboard())
        bot.register_next_step_handler(message, iff)

def mer3(message):
            if message.text == 'Назад':
                 bot.send_message(message.chat.id, "Выберите категорию", reply_markup=get_reply_keyboard())
                 bot.register_next_step_handler(message, iff)
            else:
               user_id = message.text.strip()  # Переименовали переменную, чтобы избежать конфликта с глобальной переменной
               conn = sqlite3.connect('telegram_users_databases.sql')
               cur = conn.cursor()
               cur.execute('SELECT * FROM users WHERE users_id=?', (user_id,))
               user_exists = cur.fetchone()
               if user_exists:
                   bot.send_message(message.chat.id, "Введите количество поинтов")
                   bot.register_next_step_handler(message, mer1, user_id)
               else:
                   bot.send_message(message.chat.id, "Пользователь с таким id не найден.")
                   bot.send_message(message.chat.id, "Введите id")
                   bot.register_next_step_handler(message, mer3)
               cur.close()

def mer1(message, user_id):
            if message.text == 'Назад':
                 bot.send_message(message.chat.id, "Выберите категорию", reply_markup=get_reply_keyboard())
                 bot.register_next_step_handler(message, iff)
            else :
                coin1 = int(message.text.strip())
                conn = sqlite3.connect('telegram_users_databases.sql')
                cur = conn.cursor()
                cur.execute('SELECT coin FROM users WHERE users_id = ?', (user_id,))
                current_coin = cur.fetchone()
                if current_coin:  # Проверяем, существует ли значение current_coin
                    current_coin = current_coin[0]
                else:
                    bot.send_message(message.chat.id, "Пользователь с таким id не найден.")
                    cur.close()
                    conn.close()
                    return

                new_coin = current_coin + coin1
                cur.execute('UPDATE users SET coin = ? WHERE users_id = ?', (new_coin, user_id))
                conn.commit()

                bot.send_message(message.chat.id, f"Количество поинтов пользователя успешно обновлено. Текущее количество поинтов: {new_coin}")
                bot.send_message(user_id, f"Вам начислено {coin1} поинтов!")
                cur.close()
                conn.close()

                # Запрашиваем id пользователя для следующей операции
                bot.send_message(message.chat.id, "Введите id")
                bot.register_next_step_handler(message, mer3)

def start_markup():
    markup = types.InlineKeyboardMarkup(row_width = 2)
    link_keyboard1 = types.InlineKeyboardButton(text = "1-All_from_italy", url = "https://t.me/all_from_italy")
    link_keyboard2 = types.InlineKeyboardButton(text = "2-Vip_brand_italy", url = "https://t.me/vip_brand_italy")
    link_keyboard3 = types.InlineKeyboardButton(text = "3-All_from_italy_man", url = "https://t.me/all_from_italy_man")
    link_keyboard4 = types.InlineKeyboardButton(text = "4-All_from_italy_outlet", url = "https://t.me/all_from_italy_outlet")
    markup.add(link_keyboard1, link_keyboard2)
    markup.add(link_keyboard3, link_keyboard4)
    return markup

def start_markup2():
    markup2 = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    check_button = types.KeyboardButton("Проверить")
    markup2.add(check_button)
    return markup2

def initialize_db():
    conn = sqlite3.connect('telegram_users_databases.sql')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            login TEXT UNIQUE,
            pass TEXT,
            coin INTEGER,
            users_id INTEGER UNIQUE
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

initialize_db()

@bot.message_handler(commands=['start'])
def start(message):
    initialize_db()
    chat_id = message.chat.id
    first_name = message.chat.first_name
    bot.send_message(chat_id, f"Здравствуйте, {first_name}!\n 👋 \n Добро пожаловать в чат бот от @All_from_italy !\n\nМы предлагаем вам использовать уникальную возможность при покупке нашего товара получать дополнительные скидки,а также подарки!\n\n ⚠Чтобы полноценно использовать все функции бота вам следует:\n \n 1️⃣Подписаться на наши каналы: \n 1-Основной канал: <b>All_from_italy</b> \n 2-Второй канал: <b>Vip_brand_italy</b> \n 3-Мужской канал: <b>All_from_italy_man</b> \n 4-Outlet канал: <b>All_from_italy_outlet</b>", reply_markup=start_markup(), parse_mode="HTML")
    bot.send_message(chat_id, "2️⃣Нажмите проверить подписки на каналы", reply_markup=start_markup2())
    bot.register_next_step_handler(message, check)

def check(message):
    if message.text == 'Проверить':
        channels = ["-1001351872902", "-1001416403261", "-1001438647099", "-1002072049733"]
        subscribed_channels = []
        for channel_id in channels:
            try:
                chat_member = bot.get_chat_member(chat_id=channel_id, user_id=message.chat.id)
                if chat_member.status in ['creator', 'administrator', 'member']:
                    subscribed_channels.append(channel_id)
            except Exception as e:
                print(e)  # Выводим ошибку для отладки

        if len(subscribed_channels) == len(channels):
            markup2 = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            button1 = types.KeyboardButton("Зарегистрироваться ✍")
            button2 = types.KeyboardButton("Авторизоваться")
            markup2.add(button1, button2)
            bot.send_message(message.chat.id, "Поздравляю! Вы успешно подписались на каналы.\n\nЕсли вы <b>новый пользователь</b>, нажмите зарегистрироваться ✍.\nЕсли у вас <b>уже есть аккаунт</b>, нажмите авторизоваться", reply_markup=markup2, parse_mode="HTML")
            bot.register_next_step_handler(message, handle_next_step)
        else:
            bot.send_message(message.chat.id, "Подпишитесь на все каналы", reply_markup=start_markup())
            bot.register_next_step_handler(message, check)
    elif message.text == '/start':
        start(message)

def handle_next_step(message):
    if message.text == 'Зарегистрироваться ✍':
        bot.send_message(message.chat.id, "Введите имя для регистрации")
        bot.register_next_step_handler(message, user_name)
    elif message.text == 'Авторизоваться':
        bot.send_message(message.chat.id, "Введите логин")
        bot.register_next_step_handler(message, Login)
    elif message.text == '/start':
        start(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, выберите одну из опций.")
        bot.register_next_step_handler(message, handle_next_step)


def Login(message):
    if message.text == 'Авторизоваться':
         bot.send_message(message.chat.id, "Введите логин")
         bot.register_next_step_handler(message, Login)
    elif message.text == 'Зарегистрироваться ✍':
         bot.send_message(message.chat.id, "Введите имя для регистрации")
         bot.register_next_step_handler(message, user_name)
    elif message.text == '/start':
        start(message)
    else :
         global namelogin
         namelogin = message.text.strip()
         if oneperson(namelogin):
            if namelogin == 'Admin':
                 bot.send_message(message.chat.id, "Введите пароль")
                 bot.register_next_step_handler(message, pass1)
            else:
                 bot.send_message(message.chat.id, "Введите пароль")
                 bot.register_next_step_handler(message, pass1)
         else:
              bot.send_message(message.chat.id, "Такого пользователя нету, ->")
              bot.register_next_step_handler(message, handle_next_step)

def pass1(message):
    passlogin = message.text.strip()
    if check_credentials(passlogin):
        if passlogin == 'Qwerty123@@':
            bot.send_message(message.chat.id, "Вы вошли в систему Admin, Выберите x,d,v,y", reply_markup= get_reply_keyboard())
            bot.register_next_step_handler(message, iff)
        else:
            bot.send_message(message.chat.id, "Вы вошли в систему")
            step10(message)
    elif message.text == '/start':
        start(message)
    else:
        bot.send_message(message.chat.id, "Возникла Ошибка")
        bot.send_message(message.chat.id, "Введите логин")
        bot.register_next_step_handler(message, Login)

def user_name(message):
    if message.text == 'Авторизоваться':
         bot.send_message(message.chat.id, "Введите логин")
         bot.register_next_step_handler(message, Login)
    elif message.text == 'Зарегистрироваться ✍':
         bot.send_message(message.chat.id, "Введите имя для регистрации")
         bot.register_next_step_handler(message, user_name)
    elif message.text == '/start':
        start(message)
    else :
         global name
         name = message.text.strip()
         conn = sqlite3.connect('telegram_users_databases.sql')
         cur = conn.cursor()
         cur.execute('SELECT * FROM users WHERE login=?', (name,))
         existing_user = cur.fetchone()
         cur.close()
         conn.close()
         if existing_user:
              bot.send_message(message.chat.id, 'Такой логин уже занят. Введите другое имя для регистрации.')
              bot.register_next_step_handler(message, user_name)
         else:
              bot.send_message(message.chat.id, "Создайте пароль")
              bot.register_next_step_handler(message, password1)

def password1(message):
    global password
    password = message.text.strip()
    conn = sqlite3.connect('telegram_users_databases.sql')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE users_id=?', (message.from_user.id,))
    user_exists = cur.fetchone()
    cur.close()
    conn.close()
    if user_exists:
        bot.send_message(message.chat.id, 'Вы уже зарегистрированы под другим аккаунтом!! Введите Логин')
        bot.register_next_step_handler(message, Login)
    elif message.text == '/start':
        start(message)
    else:
        bot.send_message(message.chat.id, "Введите пароль еще раз")
        bot.register_next_step_handler(message, password22)

def password22(message):
    password2 = message.text.strip()
    if password == password2:
        conn = sqlite3.connect('telegram_users_databases.sql')
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE users_id=?', (message.from_user.id,))
        user_exists = cur.fetchone()
        if not user_exists:
            cur.execute('INSERT INTO users(login, pass, coin, users_id) VALUES (?, ?, ?, ?)', (name, password2, 0, message.from_user.id))
            conn.commit()
            bot.send_message(message.chat.id, 'Вы успешно зарегистрировались')
            step10(message)
        else:
            bot.send_message(message.chat.id, 'Вы уже зарегистрированы под другим аккаунтом!! Введите Логин')
            bot.register_next_step_handler(message, Login)
        cur.close()
        conn.close()
    elif message.text == '/start':
        start(message)
    else:
        bot.send_message(message.chat.id, "Пароли не совпадают. Введите пароль еще раз")
        bot.register_next_step_handler(message, password1)

def step10(message):
    markup3 = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button1 = types.KeyboardButton("Мой профиль 👤")
    button2 = types.KeyboardButton("Мануал")
    button3 = types.KeyboardButton("Обменять поинты") 
    button4 = types.KeyboardButton("Начисления поинтов")
    button5 = types.KeyboardButton("Тех поддержка")
    markup3.add(button2, button1, button4, button3, button5)
    bot.send_message(message.chat.id, "Выберите категорию", reply_markup=markup3)

@bot.message_handler(func=lambda message: message.text == 'Тех поддержка')
def nachis(message):
    text = "Свяжитесь с ним"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="Нажмите здесь", url="https://t.me/Vladislav_mrk"))
    bot.send_message(message.chat.id, text, reply_markup=markup)
    step10(message)

@bot.message_handler(func=lambda message: message.text == 'Мой профиль 👤')
def myprofile(message):
    with sqlite3.connect('telegram_users_databases.sql') as conn:
        cur = conn.cursor()
        cur.execute('SELECT login, pass, coin FROM users WHERE users_id=?', (message.from_user.id,))
        user_info = cur.fetchone()
        if user_info:
            login, password, coins = user_info
            message10 = f"Логин: {login}\nПоинты: {coins}"
            bot.send_message(message.chat.id, message10)
            step10(message)
        else:
            bot.send_message(message.chat.id, "Профиль не найден.")

@bot.message_handler(func=lambda message: message.text == 'Обменять поинты')
def bypoint(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Перейти по ссылке', url='https://t.me/+8RBBEHKnnG9lN2I0 '))
    bot.send_message(message.chat.id, "Вы можете купить за принты по ссылке ниже:", reply_markup=markup)
    step10(message)

@bot.message_handler(func=lambda message: message.text == 'Мануал')
def coming(message):
    bot.send_message(message.chat.id, f'Данный раздел находится в разработке \n Выберите категорию:')
    bot.register_next_step_handler(message, step10)

photo_message_ids = {}  # Словарь для хранения ID сообщений с фото

@bot.message_handler(func=lambda message: message.text == 'Начисления поинтов')
def handle_prints_command(message):
    markup678 = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    cancel_button = types.KeyboardButton("Отменить")
    markup678.add(cancel_button)
    bot.send_message(message.chat.id, "Отправьте первую фотографию", reply_markup=markup678)
    bot.register_next_step_handler(message, handle_photos)

def handle_photos(message):
    if message.content_type == 'photo':
        user = message.from_user
        if user.username:
             username = f"@{user.username}"
        else:
             username = "Username не установлен"
        user_info = f"Отправитель: {message.from_user.first_name} (ID: <code>{message.from_user.id}</code>)   {username}"
        message_text = f"{user_info}\n\nПервая фотография:\n"
        sent_message = bot.send_photo('-1002009453022', message.photo[0].file_id, caption=f"Первая фотография {message_text}", parse_mode='HTML')
        
        # Сохраняем ID сообщения с фото в списке
        if message.from_user.id not in photo_message_ids:
            photo_message_ids[message.from_user.id] = []
        photo_message_ids[message.from_user.id].append(sent_message.message_id)
        
        bot.send_message(message.chat.id, "Отправьте вторую фотографию")
        bot.register_next_step_handler(message, handle_photos1)
    elif message.text == 'Отменить':
        user_id = message.from_user.id
        if user_id in photo_message_ids:
            for msg_id in photo_message_ids[user_id]:
                bot.delete_message('-1002009453022', msg_id)  # Удаляем сообщения с фотографиями
            del photo_message_ids[user_id]  # Удаляем запись из словаря

        bot.send_message(message.chat.id, "Отмена операции", reply_markup=types.ReplyKeyboardRemove())
        step10(message)
    else:
        bot.send_message(message.chat.id, "Отправьте фото!")
        bot.register_next_step_handler(message, handle_photos)

def handle_photos1(message):
    if message.content_type == 'photo':
        user = message.from_user
        if user.username:
             username = f"@{user.username}"
        else:
             username = "Username не установлен"
        user_info = f"Отправитель: {message.from_user.first_name} (ID: <code>{message.from_user.id}</code>)  {username}"
        message_text = f"{user_info}\n\nВторая фотография:\n"
        sent_message = bot.send_photo('-1002009453022', message.photo[0].file_id, caption=f"Вторая фотография {message_text}", parse_mode='HTML')
        
        # Сохраняем ID второго сообщения с фото в списке
        photo_message_ids[message.from_user.id].append(sent_message.message_id)
        
        bot.send_message(message.chat.id, "Молодец")
        step10(message)
    elif message.text == 'Отменить':
        user_id = message.from_user.id
        if user_id in photo_message_ids:
            for msg_id in photo_message_ids[user_id]:
                bot.delete_message('-1002009453022', msg_id)  # Удаляем сообщения с фотографиями
            del photo_message_ids[user_id]  # Удаляем запись из словаря

        bot.send_message(message.chat.id, "Отмена операции", reply_markup=types.ReplyKeyboardRemove())
        step10(message)
    else:
        bot.send_message(message.chat.id, "Отправьте второе фото!")
        bot.register_next_step_handler(message, handle_photos1)

while True:
    try:
        bot.polling(none_stop=True, timeout=60)  # Увеличение времени тайм-аута до 60 секунд
    except requests.exceptions.ReadTimeout:
        print("Read timeout, retrying in 15 seconds...")
        time.sleep(15)
    except Exception as e:
        print(f"Unexpected error: {e}")
        time.sleep(15)
