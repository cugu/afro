import logging.config


def set_logging(level='DEBUG'):
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
            'colored': {
                '()': 'colorlog.ColoredFormatter',
                'format': "%(log_color)s%(levelname)-8s%(reset)s %(message)s",
                'log_colors': {
                    'DEBUG': 'cyan',
                    'INFO': 'green',
                    'WARNING': 'yellow',
                    'ERROR': 'red',
                    'CRITICAL': 'red,bg_white',
                },
                'secondary_log_colors': {},
                'style': '%'
            }
        },
        'handlers': {
            'default': {
                'level': level,
                'formatter': 'colored',
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            '': {
                'handlers': ['default'],
                'level': level,
                'propagate': False
            },
        }
    })
