LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'color_formatter': {
            'class': 'loggers.color_formatter.CustomFormatter',
            'format': '%(asctime)s - [%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s'
        },
        'console': {
            'format': '%(asctime)s - [%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s'
        },
        'file': {
            'format': '%(asctime)s - [%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s'
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
