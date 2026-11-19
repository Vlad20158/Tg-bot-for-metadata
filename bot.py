import telebot
from PIL import Image
from PIL.ExifTags import TAGS
import os
import requests

import config

bot = telebot.TeleBot(config.token)
@bot.message_handler(commands=['start'])

def start(message):
    bot.send_message(message.chat.id, "Приветствую тебя,пришли мне файл,я извлеку мета данные!")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open('temp_photo.jpg', 'wb') as new_file:
        new_file.write(downloaded_file)
    img = Image.open('temp_photo.jpg')
    exif_data = img._getexif()
    result = ""
    if exif_data is None:
            bot.reply_to(message, "В этом фото нет метаданных! (Telegram их почистил)")
    else:
        for tag_id,value in exif_data.items():
            tag_name = TAGS.get(tag_id, tag_id)
            result += f"{tag_name}: {value}\n"
        bot.reply_to(message, "Файл успешно скачан! Проверяй папку.")
        bot.reply_to(message, result)
    os.remove('temp_photo.jpg')

@bot.message_handler(content_types=['document'])
def handle_document(message):
    if message.document.mime_type.startswith('image/'):
        message.photo = [message.document]
        handle_photo(message)
    else:
        bot.reply_to(message, "Это не картинка. Пришли мне фото или файл-картинку.")

if __name__ == '__main__':
    print("Бот запущен и слушает сообщения...")
    bot.polling(none_stop=True)


