import asyncio
import os
import sys
from datetime import datetime, timedelta
from random import choice

from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ChatType, ParseMode
from aiogram.filters import Command
from aiogram.types import BotCommand, FSInputFile
from dotenv import load_dotenv

sys.path.append("utils")
from basic import logger, config
from parser import parse_pdf, get_today_schedule, create_message

# Загрузка переменных окружения
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

dp = Dispatcher()

# Идентификатор бота
bot_id = None


# Обработчик команды /code
@dp.message(Command(BotCommand(command='code', description='Получить ссылку на GitHub репозиторий бота')))
async def handle_code_command(message: types.Message) -> None:
    """
    Обрабатывает команду /code и отправляет ссылку на GitHub репозиторий.

    Args:
        message (types.Message): Сообщение, содержащее команду /code.
    """
    github_link = "https://github.com/overklassniy/stankin_schedule_bot/"
    try:
        await message.answer(f"Исходный код бота доступен на GitHub: {github_link}")
        logger.info(f"Sent GitHub link to {message.chat.id}")
    except Exception as e:
        logger.error(f"Error sending GitHub link to {message.chat.id}: {e}")


# Обработчик команды /schedule
@dp.message(Command(BotCommand(command='schedule', description='Получить расписание на сегодня')))
async def handle_schedule_command(message: types.Message) -> None:
    args = message.text.split()
    try:
        increment_day = int(args[-1])
    except Exception:
        increment_day = 0

    date = (datetime.today() + timedelta(increment_day)).strftime('%d.%m')

    today_schedule = get_today_schedule(parse_pdf(config['PDF_PATH']), increment_day)
    message_text = create_message(today_schedule, increment_day, scheduled=False)
    if message_text == 'Выходной':
        message_text = f'<b>{date} - Воскресенье. Занятий нет!</b>'
    await message.answer(text=message_text, parse_mode=ParseMode.HTML)

    logger.info(f"Sent schedule for {date} to {message.from_user.id}")


# Обработчик личных сообщений
@dp.message(F.chat.func(lambda chat: chat.type == ChatType.PRIVATE))
async def handle_private_message(message: types.Message) -> None:
    """
    Обрабатывает личные сообщения пользователей.

    Args:
        message (types.Message): Сообщение, полученное ботом.
    """
    response_text = f"Привет, это эксклюзивный бот для отправки расписания {config['GROUP']} и пока у меня нет функционала в личных сообщениях. Если Вы заинтересованы в настройке этого бота для получения своего расписания, то воспользуйтесь моим исходным кодом (/code)."
    try:
        await message.answer(response_text)
        logger.info(f"Sent private message to {message.chat.id}")
    except Exception as e:
        logger.error(f"Error sending private message to {message.chat.id}: {e}")


# Функция для отправки расписания
async def send_daily_message(bot: Bot) -> None:
    await asyncio.sleep(10)
    chat_id = config['GROUP_ID']

    while True:
        now = datetime.now()
        # Если сейчас HOUR часов и минуты в MINUTES диапазоне включительно
        if now.hour == config['HOUR'] and now.minute in range(config['MINUTES']):
            today_schedule = get_today_schedule(parse_pdf(config['PDF_PATH']))
            message_text = create_message(today_schedule)
            if message_text != 'Выходной':
                if config["ENABLE_IMAGE"]:
                    images_dir = config['IMAGES_DIR']
                    image = FSInputFile(f'{images_dir}/{choice(os.listdir(images_dir))}')
                    await bot.send_photo(chat_id=chat_id, photo=image, caption=message_text, parse_mode=ParseMode.HTML)
                else:
                    await bot.send_message(chat_id=chat_id, text=message_text, parse_mode=ParseMode.HTML)
                logger.info(f"Sent daily schedule to {chat_id}")
            # После отправки сообщения, бот "засыпает" на SLEEP_TIME секунд
            await asyncio.sleep(config['SLEEP_TIME'])
        else:
            # Проверка каждые CHECK_TIME_INTERVAL секунд
            await asyncio.sleep(config['CHECK_TIME_INTERVAL'])


async def main() -> None:
    global bot_id
    bot = Bot(token=TOKEN)
    bot_id = bot.id

    asyncio.create_task(send_daily_message(bot))

    await dp.start_polling(bot, polling_timeout=30)


# Запуск бота
if __name__ == '__main__':
    asyncio.run(main())
