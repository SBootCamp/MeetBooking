from typing import Union

from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.utils.serializer_helpers import ReturnDict


def flatten(x):
    """
    Разворачивает dict с произвольной вложенностью в dict с одномерной вложенностью
    """
    y = {}
    for k, v in x.items():
        if v and isinstance(v, list):
            y.update(flatten({f'{k}[{i}]': w for i, w in enumerate(v)}))
        elif v and isinstance(v, dict):
            y.update(flatten({f'{k}.{l}': w for l, w in v.items()}))
        else:
            y[k] = v
    return y


def exc_detail_to_dict(exc_detail):
    """
    Рекурсивно очищает объект ErrorDetail от объектов DRF, делая его JSON-сериализуемым.
    """
    if type(exc_detail) == ErrorDetail:
        return str(exc_detail)
    elif type(exc_detail) == list:
        return [exc_detail_to_dict(item) for item in exc_detail]
    elif hasattr(exc_detail, 'keys'):
        return {key: exc_detail_to_dict(exc_detail[key]) for key in exc_detail.keys()}
    # добавлено на всякий случай, эта ветка не должна появляться
    else:
        return str(exc_detail)


def clear_error_key(error_key):
    """
    Разворачивает ключ, полученный в результате flatten, в человекочитаемый вид.
    Пример: order[0][dishes][1] -> order_dishes
    """
    error_key = error_key.replace(']', ']_')
    res = ''
    remove_flag = False
    for char in error_key:
        if char == '[':
            remove_flag = True
        if not remove_flag:
            res += char
        if char == ']':
            remove_flag = False
    return res.rstrip('_')


def exc_detail_flatten(exc_detail):
    """Разворачивает одномерный dict с описанием ошибок в строку"""

    flattened_error_dict = flatten(exc_detail_to_dict(exc_detail))
    return '\n\r'.join('{k}: {v}'.format(k=k, v=v) for k, v in flattened_error_dict.items())


def map_error_key(error_key):
    """
    Расширяемая функция: предоставляет возможность заменять ключи на переведенные,
    для отображения ошибки на фронтэнде.
    Пример: order_dishes -> Блюда
    """
    return {}.get(error_key, error_key)


def response_error_from_detail(exc_detail):
    """Разворачивает DRF-объект ErrorDetail в строку"""
    error_dict = flatten(exc_detail_to_dict(exc_detail))
    error_dict = {map_error_key(clear_error_key(key)): value for key, value in error_dict.items()}
    return '\n\r'.join('{k}: {v}'.format(k=k, v=v) for k, v in error_dict.items())


class ResponseError:
    """
    Предоставляет единый формат возвращаемого значения в случае ошибки сериализации входных значений.
    """

    def __new__(cls, error_text_or_detail: Union[ErrorDetail, str], status=400):
        if type(error_text_or_detail) is ReturnDict:
            error_text_or_detail = response_error_from_detail(error_text_or_detail)

        return Response(status=status, data={'detail': str(error_text_or_detail)})
