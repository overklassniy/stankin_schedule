# Подгрузка конфигураций из config.json
import json
import logging
import os
from datetime import datetime
from typing import Union


def load_config() -> dict:
    """
    Загружает конфигурационные данные из файла config.json.

    Returns:
        dict: Словарь с конфигурационными данными.
    """
    with open('config.json', 'r', encoding='UTF-8') as config_file:
        return json.load(config_file)


config = load_config()


# Настройка логирования
def setup_logger() -> logging.Logger:
    """
    Настраивает логирование для вывода в файл и консоль.

    Returns:
        logging.Logger: Объект логгера для записи логов.
    """
    os.makedirs(config['LOGS_DIR'], exist_ok=True)
    current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_file_name = f"{config['LOGS_DIR']}/{current_time}.log"

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(log_file_name)
    console_handler = logging.StreamHandler()

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger


logger = setup_logger()


# Функции для работы с файлами JSON
def load_json_file(file_path: str, default_value: Union[dict, list]) -> Union[dict, list]:
    """
    Загружает данные из JSON файла. Если файл не существует, возвращает значение по умолчанию.

    Args:
        file_path (str): Путь к JSON файлу.
        default_value (dict | list): Значение по умолчанию, если файл не найден.

    Returns:
        dict | list: Данные, загруженные из JSON файла, или значение по умолчанию.
    """
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return default_value


def save_json_file(file_path: str, data: Union[dict, list]) -> None:
    """
    Сохраняет данные в JSON файл.

    Args:
        file_path (str): Путь к JSON файлу.
        data (dict | list): Данные для сохранения.
    """
    # Получаем директорию из пути к файлу
    directory = os.path.dirname(file_path)

    # Проверяем, существует ли директория, и создаем её, если нет
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Сохраняем данные в JSON файл
    with open(file_path, 'w') as f:
        json.dump(data, f)


def days_until_date(date_str: str) -> int:
    """
    Вычисляет количество дней до указанной даты в формате 'день.месяц.год' или 'день.месяц'.

    Если дата указывается в формате 'день.месяц', используется текущий год.
    Если указанная дата уже прошла в текущем году, возвращается количество дней до этой даты в следующем году.

    Args:
        date_str (str): Дата в строковом формате 'день.месяц.год' или 'день.месяц'.

    Returns:
        int: Количество дней до указанной даты.

    Raises:
        ValueError: Если строка даты не соответствует ожидаемому формату 'день.месяц' или 'день.месяц.год'.
    """
    # Получаем текущую дату
    today = datetime.now().date()

    # Парсим входную строку. Если год не указан, используем текущий год.
    try:
        # Если строка имеет формат 'день.месяц.год'
        parsed_date = datetime.strptime(date_str, "%d.%m.%Y").date()
    except ValueError:
        # Если строка имеет формат 'день.месяц', добавляем текущий год
        current_year = today.year
        parsed_date = datetime.strptime(f"{date_str}.{current_year}", "%d.%m.%Y").date()

    # Если дата уже прошла в этом году, добавляем год
    if parsed_date < today:
        parsed_date = parsed_date.replace(year=today.year + 1)

    # Вычисляем количество дней до этой даты
    days_left = (parsed_date - today).days

    return days_left
