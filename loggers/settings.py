from meet_booking.settings import LOG_FORMAT


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'color_formatter': {
            'class': 'loggers.color_formatter.ColorFormatter',
            'format': LOG_FORMAT
        },
        'console': {
            'format': LOG_FORMAT
        },
        'file': {
            'format': LOG_FORMAT
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'color_formatter'
        },
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': 'main.log'
        }
    },
    'loggers': {
        'account_user': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        }
    }
}
