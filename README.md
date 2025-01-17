# СТАНКИН Расписание

Этот Telegram бот ежедневно отправляет расписание занятий для группы студентов. Он поддерживает как командное управление расписанием, так и автоматическую отправку расписания в указанные дни и часы.

## Оглавление
- [Особенности](#особенности)
- [Установка](#установка)
- [Настройка](#настройка)
- [Запуск](#запуск)
- [Использование](#использование)
- [Структура проекта](#структура-проекта)
- [Технологии](#технологии)

## Особенности
- Автоматическая ежедневная отправка расписания в указанный чат.
- Отправка расписания на день по команде `/schedule`.
- Поддержка отправки изображений с расписанием.
- Легко настраивается для различных учебных групп.
- Работа как с групповыми чатами (группы / супергруппы), так и с личными сообщениями.

## Установка
Для установки бота выполните следующие шаги:
1. Склонируйте репозиторий:
   ```bash
   git clone https://github.com/overklassniy/stankin_schedule_bot.git
   ```
2. Перейдите в директорию проекта:
   ```bash
   cd stankin_schedule_bot
   ```
3. Установите зависимости:\
   3.1. Установите необходимые Python библиотеки командой:
   ```bash
   pip install -r requirements.txt
   ```
   3.2. Установите Ghostscript по инструкции [здесь](https://camelot-py.readthedocs.io/en/master/user/install-deps.html#install-deps).


## Настройка
1. Создайте файл `.env` в корневой директории и добавьте в него ваш токен Telegram бота:
   ```
   BOT_TOKEN=your_telegram_bot_token
   ```
2. Настройте файл `config.json`:
   - `LOGS_DIR`: Директория, в которой будут сохраняться файлы логов.
   - `GROUP`: Код Вашей группы.
   - `GROUP_ID`: ID чата, в который бот будет отправлять расписание.
   - `THREADED`: Отправлять ли сообщение в подтему Вашей супергруппы (в случае таковой).
   - `THREAD_NUMBER`: ID темы подгруппы для отправки расписания, используется, если параметр _THREADED: true_.
   - `HOUR` и `MINUTES`: Время отправки расписания (например, при _HOUR: 5_ и _MINUTES: 60_ бот будет отправлять расписание сразу же, как наступит 5 часов и бот будет доступен, в 5:00).
   - `PDF_PATH`: Путь к файлу PDF с расписанием.
   - `TEACHERS_FULLNAMES_PATH`: Путь к .json файлу с полными именами преподавателей. В случае его отсутствия будут использоваться имена преподавателей в формате Фамилия И.О. из расписания.
   - `SLEEP_TIME`: Время сна между отправками сообщений (в секундах).
   - `CHECK_TIME_INTERVAL`: Частота проверки времени для отправки расписания (в секундах).
   - `ENABLE_IMAGE`: Включить ли отправку изображения при отправке расписания.
   - `IMAGES_DIR`: Директория с изображениями для отправки используется, если параметр _ENABLE_IMAGE: true_.
   - `ENABLE_SECURE`: Включить ли использование команд только в группе.
   - `ENABLE_TOMORROW_BUTTON`: Включить ли кнопку "Расписание на завтра" под сообщением с ежедневным расписанием.
   
   Пример файла `config.json`:
   ```json
   {
    "GROUP": "ИДБ-12-34",
    "LOGS_DIR": "logs",
    "GROUP_ID": -1234567890,
    "THREADED": true,
    "THREAD_NUMBER": 99,
    "HOUR": 5,
    "MINUTES": 5,
    "PDF_PATH": "data/ИДБ-12-34.pdf",
    "TEACHERS_FULLNAMES_PATH": "data/teachers.json",
    "CHECK_TIME_INTERVAL": 55,
    "SLEEP_TIME": 84600,
    "ENABLE_IMAGE": true,
    "IMAGES_DIR": "images",
    "ENABLE_SECURE": true,
    "ENABLE_TOMORROW_BUTTON": false
   }
   ```

## Запуск
Для запуска бота выполните следующую команду:
```bash
python main.py
```
Бот начнет работу, автоматически получая расписание на день и отправляя его в указанный чат.

## Использование
1. Отправьте команду `/schedule`, чтобы получить расписание на текущий день. Можно указать смещение дней: `/schedule +1` для расписания на завтра.
2. Отправьте команду `/code`, чтобы получить ссылку на исходный код бота на GitHub.
3. Бот автоматически отправляет расписание каждый день в заданное время, настроенное в конфигурационном файле.

## Структура проекта
```
.
├── main.py              # Основной файл для запуска бота
├── logs/                # Логи работы бота
├── utils/
│   └── basic.py         # Базовые утилиты и вспомогательные функции
│   └── parser.py        # Утилиты для парсинга расписания
├── data/
│   └── ИДБ-12-34.pdf    # Файл с расписанием группы
│   └── teachers.json    # Файл с полными именами преподавателей
├── images/              # Директория для изображений (если включена отправка картинок)
├── config.json          # Конфигурационный файл
├── requirements.txt     # Список зависимостей
└── README.md            # Документация
```

## Технологии
- [Python](https://www.python.org/downloads/) - Используемый язык программирования.
- [aiogram](https://github.com/aiogram/aiogram) - Фреймворк для асинхронной работы с Telegram Bot API.
- [python-dotenv](https://pypi.org/project/python-dotenv/) - Библиотека для работы с переменными окружения.
- [camelot](https://pypi.org/project/camelot-py/) - Библиотека для парсинга таблиц из PDF.
