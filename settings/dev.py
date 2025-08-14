from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'True').lower() in ('true', '1', 'yes', 'on')

# Hosts permitidos para desenvolvimento
ALLOWED_HOSTS = ['*']

# Configurações específicas de desenvolvimento podem ser adicionadas aqui
# Por exemplo:
# INTERNAL_IPS = ['127.0.0.1']
# if 'django_extensions' not in INSTALLED_APPS:
#     INSTALLED_APPS += ['django_extensions']

# Configurações de logging para desenvolvimento (opcional)
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'root': {
#         'handlers': ['console'],
#     },
# }