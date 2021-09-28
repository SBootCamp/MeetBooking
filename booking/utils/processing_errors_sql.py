import re


def get_message_error(error):
    if 'check_datetime' in error:
        return 'Время окончания мероприятия должно быть больше времени начала мероприятия'
    datetime = [string.replace('"', '').split(',') for string in re.findall(r"=\(\[(.+?)\)", error)][1]
    return f'Промежуток времени с {datetime[0]} до {datetime[1]} занят'
