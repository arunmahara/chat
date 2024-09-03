LOGGING = {
    'version': 1,

    'disable_existing_loggers': False,

    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }
    },

    'formatters': {
        'verbose': {
            'format': ' [%(asctime)s] [%(levelname)s] [%(module)s] [%(name)s:%(lineno)s] [%(message)s]'
        },
    },

    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            # 'filters': ['require_debug_true'],
            'formatter': 'verbose'
        },
    },

    'loggers': {
        'chat.apps.main': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },

        # db query logger
        # 'django.db.backends': {
        #     'level': 'DEBUG',
        #     'handlers': ['console'],
        # }
    },
}
