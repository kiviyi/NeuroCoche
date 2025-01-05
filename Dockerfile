# Используем официальный Python образ
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем все файлы проекта в контейнер
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем RabbitMQ (если нужно в этом контейнере)
RUN apt-get update && apt-get install -y rabbitmq-server

# Открываем порты для RabbitMQ и бота
EXPOSE 5000 # Порт для tg_bot.py

# Для работы с RabbitMQ используем entrypoint или команду через docker-compose
CMD ["bash", "-c", "python worker.py"]
