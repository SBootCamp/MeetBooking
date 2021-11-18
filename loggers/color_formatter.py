import logging

from colorama import Fore

from loggers.settings import LOGGING


class ColorFormatter(logging.Formatter):

    format = LOGGING['formatters']['color_formatter']['format']

    FORMATS = {
        logging.DEBUG: "".join([Fore.LIGHTGREEN_EX, format, Fore.RESET]),
        logging.INFO: "".join([Fore.LIGHTWHITE_EX, format, Fore.RESET]),
        logging.WARNING: "".join([Fore.LIGHTYELLOW_EX, format, Fore.RESET]),
        logging.ERROR: "".join([Fore.LIGHTRED_EX, format, Fore.RESET]),
        logging.CRITICAL: "".join([Fore.LIGHTRED_EX, format, Fore.RESET])
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
