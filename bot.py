import logging

import telebot
from telebot import types

from calc import Calc
from calc import GettingData as gd

logging.basicConfig(filename='bot.log',
                    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
log = logging.getLogger('Bot')
bot = telebot.TeleBot("1984568671:AAGvrGzoBsM_LEFDZfnVZa5-vnV3cXmaHKM")
string_2_write = ''

log.info("Bot started")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton('Последние')
    but2 = types.KeyboardButton('Новые')
    but3 = types.KeyboardButton('Все показания')
    but4 = types.KeyboardButton('История изменений')
    markup.add(but1, but2, but3, but4)
    bot.reply_to(message, 'Привет, {0.first_name}'.format(
        message.from_user), parse_mode='html', reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def menu(message):
    if message.chat.type == 'private':
        if message.text == 'Последние':
            log.info('Запрошены последние показания')
            last = gd.read_f()
            log.info(last)
            t1, t2, gor, hol = last
            mes = f'Прошлые показания: Т1 = {t1}, Т2 = {t2}, Горячая = {gor}, Холодная = {hol}'
            log.info(mes)
            bot.send_message(message.chat.id, mes)

        elif message.text == 'Новые':
            log.info('Ввод новых данных активирован')
            msg = bot.reply_to(
                message, 'Введи 4️⃣ числа через пробел (Т1, Т2, Горячая, Холодная)')
            bot.register_next_step_handler(msg, got_new)

        elif message.text == 'Все показания':
            log.info('Запрошены все данные')
            all_data = gd.get_all_data()
            log.info(all_data)
            bot.send_message(message.chat.id, all_data)

        elif message.text == 'История изменений':
            log.info('Запрошена история изменений')
            changes_history = gd.get_changes_history()
            log.info(changes_history)
            bot.send_message(message.chat.id, changes_history)


def got_new(message):
    global string_2_write

    try:
        new = message.text
        log.info(f'Текст сообщения: {new}')
        new = map(int, new.split())
        new_int = list(new)
        log.info(f'Список получился таков: {new_int}')
        ss = Calc.calc(new_int)
        string_2_write = ','.join(str(n) for n in new_int)
        log.info(f'Результат работы функции Calc = {ss}')
        if ss != 'Введено меньше или больше четырёх значений' and ss != 'Новые значения меньше предыдущих':
            log.info(f'Сумма для оплаты: {ss}')
            log.info(f'Новые данные для записи в файл: {string_2_write}')
            bot.send_message(message.chat.id, f'💰 = {ss[0]}\n💡 = {ss[1]}\n🚰 = {ss[2]}')
            msg = bot.reply_to(
                message, 'Y чтобы записать новые показания в файл 💾')
            bot.register_next_step_handler(msg, write_new_data)
        else:
            bot.send_message(message.chat.id, f'💔 {ss}')
    except:
        log.info('Что-то пошло не так')
        bot.send_message(message.chat.id, '🐤 ты ввёл что-то явно не то 🤷‍♂️')


def write_new_data(message):
    log.info(message.text)
    if message.text == 'Y':
        with open('data.txt', 'a') as f:
            f.write('\n' + string_2_write)
            log.info(f'Записано {string_2_write}')
            bot.send_message(message.chat.id, '💾 Записано в файл!')
            f.close()
            last = gd.read_f()
            log.info(last)
            t1, t2, gor, hol = last
            mes = f'Новые последние показания в файле: Т1 = {t1}, Т2 = {t2}, Горячая = {gor}, Холодная = {hol}'
            log.info(mes)
            bot.send_message(message.chat.id, mes)


bot.infinity_polling()
