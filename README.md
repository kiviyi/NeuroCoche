# NeuroCoche

Проект представляет собой телеграм-бота, который выполняет сегментацию автомобилей на фотографиях с помощью нейронной сети. Бот разработан с использованием библиотеки telebot и интегрирован с облачным хранилищем cloud.ru для обработки и хранения изображений.

## Структура проекта

- tg_bot.py: Файл для запуска телеграмм бота.
- worker.py: Файл для создания очереди RabbitMQ и работы с ней.
- segmentation.py: Файл для подключения нейросети для сегментации изображений.
- validator.py: Файл для подключения нейросети для валидации изображений.
- requirements.txt: Файл с зависимостями для установки необходимых библиотек.
- docker-compose.yml: Файл с инструкциями для запуска сервисов.
- ResNet50_nsfw_model.pth: Файл нейросети для валидации изображений.
- my_model_v11\: Файл конфигурации для сборки Docker-образа.
- Dockerfile: Файл конфигурации для сборки Docker-образа.
- README.md: Этот файл.
## Сборка и запуск проекта
### Запуск проекта Docker-контейнера

Сначала необходимо распаковать архив `my_model_v11.tar`

Для запуска проекта в контейнере необходимо запустить команду:

```bash
 docker-compose up --build
 ```

Поздавляю, проект запущен.

### Запуск проекта без Docker

1. Запустите RabbitMQ.

2.  Запустите файл `worker.py`:
```
python3 woker.py
```
3.  Паралельно запустите файл `tg_bot.py`:
```
python3 tg_bot.py
```

Поздавляю, проект запущен.

## Пример работы
Вы можете протестировать проект в [телеграмм боте](https://t.me/OOP_Segmentation_bot)
![пример](video.gif)<img src="example.gif" width="200" height="100">


## Лицензия

Этот проект распространяется под лицензией [MIT](https://choosealicense.com/licenses/mit/). Вы можете свободно использовать, изменять и распространять код при условии указания авторства.
