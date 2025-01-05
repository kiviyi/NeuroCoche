import pika
import telebot
import os

from validator import Validator

token = ''
bot = telebot.TeleBot(token)

RABBITMQ_HOST = 'localhost'
QUEUE_NAME = 'image_queue'

validator = Validator("ResNet50_nsfw_model.pth")

def send_to_queue(image_path: str, chat_id: int):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)

    with open(image_path, 'rb') as f:
        body = f.read()

    # Отправляем фото в очередь с ID чата
    channel.basic_publish(
        exchange='',
        routing_key=QUEUE_NAME,
        body=body,
        properties=pika.BasicProperties(
            headers={'chat_id': chat_id}
        )
    )
    connection.close()

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет! Я - телеграм бот для сегментации картинок. Пришли мне фото, и я выделю на нем машину!")

@bot.message_handler(content_types=['photo'])
def handle_change_photo(message):
    try:
        if message.content_type == 'photo':
            raw = message.photo[-1].file_id  # Получаем лучшее качество фото
            file_info = bot.get_file(raw)
            downloaded_file = bot.download_file(file_info.file_path)
            input_path = f"photos{raw}.jpg"
            # Сохраняем фото локально
            with open(input_path, 'wb') as new_file:
                new_file.write(downloaded_file)

            #print(file_info.file_path)
            
            # Валидация контента (NSFW)
            if validator.isNSFW(input_path):
                bot.send_message(message.chat.id, "Ошибка: это изображение содержит неприемлемый контент.")
                os.remove(input_path)
                return
            #print("isnsfw")
            #bot.send_message(message.chat.id, "Фото принято, обрабатываю...")
            bot.reply_to(message, "Фото принято, обрабатываю...")
            

            # Отправляем фото в очередь
            send_to_queue(input_path, message.chat.id)

            os.remove(input_path)  # Удаляем локальное фото после отправки в очередь
        else:
            bot.reply_to(message, "Вы прислали что-то, отличное от изображения")

    except Exception as e:
        bot.reply_to(message, f"Ошибка: {str(e)}")
        os.remove(input_path)

bot.infinity_polling()
