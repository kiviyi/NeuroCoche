# для обработки изображений из очереди и отправки результата пользователю

import pika
import telebot
import os
from segmentation import segmentation  # Импорт функции для обработки

RABBITMQ_HOST = 'localhost'
QUEUE_NAME = 'image_queue'
TOKEN = '5945863355:AAGGTTUlRDQhXXqWI1CiR9EkGVXI7pof69E'
bot = telebot.TeleBot(TOKEN)

def callback(ch, method, properties, body):
    chat_id = properties.headers['chat_id']
    input_path = 'input.jpg'
    output_path = 'output.jpg'
    
    # Сохраняем полученное фото
    with open(input_path, 'wb') as f:
        f.write(body)

    # Вызываем функцию сегментации
    segmentation(input_path, output_path)
    
    # Отправляем результат пользователю
    input = open(input_path, 'rb')
    output = open(output_path, 'rb')
    bot.send_media_group(chat_id, [telebot.types.InputMediaPhoto(input), telebot.types.InputMediaPhoto(output)])
    bot.send_message(chat_id,"Я сделялъ!!!")
    input.close()
    output.close()
    #with open(output_path, 'rb') as f:
    #    bot.send_photo(chat_id, f)

    os.remove(input_path)
    os.remove(output_path)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_worker():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)
    
    print(" [*] Ожидание сообщений...")
    channel.start_consuming()

if __name__ == '__main__':
    start_worker()
