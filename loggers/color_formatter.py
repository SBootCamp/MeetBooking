import logging

from loggers.settings import LOGGING


COLORS_LOG = {
    'green': '\033[0;32m',
    'white': '\033[24;11m',
    'yellow': '\033[33;11m',
    'red': '\033[31;11m',
    'purple': '\033[37;35m',
    'reset': '\033[0m'
}


class CustomFormatter(logging.Formatter):

    format = LOGGING['formatters']['color_formatter']['format']

    FORMATS = {
        logging.DEBUG: "".join([COLORS_LOG['green'], format, COLORS_LOG['reset']]),
        logging.INFO: "".join([COLORS_LOG['white'], format, COLORS_LOG['reset']]),
        logging.WARNING: "".join([COLORS_LOG['yellow'], format, COLORS_LOG['reset']]),
        logging.ERROR: "".join([COLORS_LOG['red'], format, COLORS_LOG['reset']]),
        logging.CRITICAL: "".join([COLORS_LOG['purple'], format, COLORS_LOG['reset']])
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
