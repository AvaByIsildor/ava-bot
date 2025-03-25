# main.py
import telebot
import os

# Получаем токен из переменной окружения
TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
        "Привет! Я бот от AvaByIsildor. Сделаю тебе уникальную аватарку!\n\n"
        "Давай начнём. Какой стиль ты хочешь? (например: аниме, киберпанк, реализм и т.д.)")
    user_data[message.chat.id] = {}

@bot.message_handler(func=lambda message: message.chat.id in user_data and 'style' not in user_data[message.chat.id])
def ask_reference(message):
    user_data[message.chat.id]['style'] = message.text
    bot.send_message(message.chat.id, "Есть ли пример аватарки или пожелания? Напиши или пропусти.")

@bot.message_handler(func=lambda message: message.chat.id in user_data and 'reference' not in user_data[message.chat.id])
def ask_photo(message):
    user_data[message.chat.id]['reference'] = message.text
    bot.send_message(message.chat.id, "Можешь прислать фото, если хочешь использовать его в аватарке. Или напиши /skip, если без фото.")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_id = message.photo[-1].file_id
    user_data[message.chat.id]['photo'] = file_id
    send_order_to_admin(message)

@bot.message_handler(commands=['skip'])
def skip_photo(message):
    send_order_to_admin(message)

def send_order_to_admin(message):
    order = user_data.pop(message.chat.id, {})
    text = f"**НОВЫЙ ЗАКАЗ**\n\n"
    text += f"Стиль: {order.get('style', 'Не указано')}\n"
    text += f"Пожелания/пример: {order.get('reference', 'Нет')}\n"
    text += f"От пользователя: @{message.from_user.username or message.from_user.id}"

    admin_id = message.chat.id  # временно отправка себе
    bot.send_message(admin_id, text, parse_mode="Markdown")

    if 'photo' in order:
        bot.send_photo(admin_id, order['photo'])

    bot.send_message(message.chat.id, "Спасибо! Я получил твой заказ и скоро свяжусь с тобой!")

bot.polling()
