
def get_message_error(error):
    if 'check_datetime' in str(error):
        return 'Время окончания мероприятия должно быть больше времени начала мероприятия'
    return f'Указанное время занято'
