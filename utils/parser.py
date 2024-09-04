from datetime import datetime, timedelta

import camelot
import numpy as np
import pandas as pd


def fix_labs(df):
    # Создаём копию DataFrame, чтобы не изменять оригинал
    df_copy = df.copy()

    # Заменяем пустые строки на NaN
    df_copy.replace('', np.nan, inplace=True)

    # Итерируем по строкам DataFrame
    for i in range(1, len(df_copy)):
        # Проверяем, что первая ячейка в текущей строке пуста
        if pd.isna(df_copy.iloc[i, 0]):
            # Объединяем не пустые ячейки текущей строки с предыдущей строкой
            for j in range(1, len(df_copy.columns)):
                if pd.notna(df_copy.iloc[i, j]):
                    df_copy.iloc[i - 1, j] = df_copy.iloc[i - 1, j] + '\n' + df_copy.iloc[i, j]
            # Заполняем текущую строку NaN
            df_copy.iloc[i] = np.nan

    # Удаляем строки, которые стали полностью пустыми
    df_copy = df_copy.dropna(how='all')

    df_copy.replace(np.nan, '', inplace=True)

    return df_copy


def parse_pdf(file_path):
    # Извлечение таблиц из PDF файла, обработка всех страниц
    tables = camelot.read_pdf(file_path, pages='all')

    # Выбор первой таблицы
    table = fix_labs(tables[0].df)

    # Инициализация списка расписания
    schedule_ = table.iloc[1:8].stack().tolist()

    # Инициализация словаря для хранения расписания
    schedule = {}
    days_of_week = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
    current_day = None

    # Обработка списка расписания
    for item in schedule_:
        if item in days_of_week:
            current_day = item
            schedule[current_day] = []
        elif current_day:
            if not item:
                schedule[current_day].append(item)
                continue
            item_ = item.replace('\n', ' ').strip().rstrip().replace('. ', '\n')
            if item_.count(']') > 1:
                item__ = []
                for x in item_.split(']'):
                    tmp = (x + ']\n').strip()
                    if tmp != ']':
                        item__.append(tmp)
            else:
                item__ = item_.replace('] ', ']\n').strip()
            schedule[current_day].append(item__)

    return schedule


def parse_date_range(date_range, increment_day=0):
    """Парсит строку с датами и возвращает список дат, когда проводится занятие."""
    today = datetime.today() + timedelta(increment_day)
    day, month = today.day, today.month

    def is_within_period(start, end, is_weekly=False):
        start_day, start_month = map(int, start.split('.'))
        end_day, end_month = map(int, end.split('.'))

        start_date = datetime(today.year, start_month, start_day)
        end_date = datetime(today.year, end_month, end_day)
        if end_date < start_date:
            end_date = datetime(today.year + 1, end_month, end_day)  # Если период охватывает конец года

        if is_weekly:
            if start_date <= today <= end_date:
                return (today - start_date).days % 7 == 0
        else:
            return start_date <= today <= end_date

    date_parts = date_range.split(', ')
    valid_dates = []

    for part in date_parts:
        if '-' in part:
            if 'к.н.' in part:
                part = part.replace(' к.н.', '')
                start_date, end_date = part.split('-')
                if is_within_period(start_date, end_date):
                    valid_dates.append(part)
            elif 'ч.н.' in part:
                part = part.replace(' ч.н.', '')
                start_date, end_date = part.split('-')
                if is_within_period(start_date, end_date, is_weekly=True):
                    valid_dates.append(part)
        else:
            if '.' in part:
                d, m = map(int, part.split('.'))
                if d == day and m == month:
                    valid_dates.append(part)

    return valid_dates


def get_today_schedule(schedule, increment_day=0):
    """Возвращает расписание на текущий день, сохраняя пустые ячейки."""
    today = (datetime.today() + timedelta(increment_day)).strftime('%A')
    day_map = {
        'Monday': 'Понедельник',
        'Tuesday': 'Вторник',
        'Wednesday': 'Среда',
        'Thursday': 'Четверг',
        'Friday': 'Пятница',
        'Saturday': 'Суббота',
        'Sunday': 'Воскресенье'
    }

    today_rus = day_map[today]

    # Инициализация расписания на сегодняшний день как пустого
    today_schedule = []

    if today_rus in schedule:
        day_schedule = schedule[today_rus]

        # Проверка каждого элемента расписания
        for lesson in day_schedule:
            if isinstance(lesson, list):
                found_valid = False
                for sublesson in lesson:
                    lines = sublesson.split('\n')
                    dates_line = lines[-1].strip('[]')
                    if parse_date_range(dates_line, increment_day):
                        today_schedule.append(sublesson)
                        found_valid = True
                if not found_valid:
                    today_schedule.append("Окно")  # Для сохранения структуры
            else:
                lines = lesson.split('\n')
                dates_line = lines[-1].strip('[]')
                if parse_date_range(dates_line, increment_day):
                    today_schedule.append(lesson)
                else:
                    today_schedule.append("Окно")  # Для сохранения структуры

    return today_schedule


def create_message(today_schedule, increment_day=0):
    today = (datetime.today() + timedelta(increment_day)).strftime('%A')
    day_map = {
        'Monday': 'Понедельник',
        'Tuesday': 'Вторник',
        'Wednesday': 'Среда',
        'Thursday': 'Четверг',
        'Friday': 'Пятница',
        'Saturday': 'Суббота',
        'Sunday': 'Воскресенье'
    }
    times = ['8:30 - 10:10', '10:20 - 12:00', '12:20 - 14:00', '14:10 - 15:50', '16:00 - 17:40', '18:00 - 19:30', '19:40 - 21:10', '21:20 - 22:50']
    today_rus = day_map[today]
    message = f'<b>Доброе утро, сегодня {today_rus.lower()}. Расписание на сегодня:</b>\n'

    lessons = []
    time_counter = 0
    for lesson in today_schedule:
        if lesson == 'Окно':
            time_counter += 1
            continue
        if 'лекции' in lesson:
            lesson = lesson.replace('лекции', 'лекция')
        tmp = lesson.split('\n')
        name = '📚 ' + tmp[0]
        if tmp[1] not in ['лекция', 'семинар']:
            prepod = f'👤 ' + tmp[1] + '.'
            lesson_type = '⚙️ ' + tmp[2]
            location = '📍 ' + tmp[3]
            duration = '🗓 ' + tmp[4]
            time = '⏰ ' + times[time_counter]
        else:
            prepod = None
            lesson_type = '⚙️ ' + tmp[1]
            location = '📍 ' + tmp[2]
            duration = '🗓 ' + tmp[3]
            time = '⏰ ' + times[time_counter]
        if prepod:
            lesson_message = f'<blockquote>{name}\n{prepod}\n{lesson_type}\n{location}\n{duration}\n{time}</blockquote>'
        else:
            lesson_message = f'<blockquote>{name}\n{lesson_type}\n{location}\n{duration}\n{time}</blockquote>'
        lessons.append(lesson_message)
        time_counter += 1

    message += '\n'.join(lessons)

    return message