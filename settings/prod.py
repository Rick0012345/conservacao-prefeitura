from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Hosts permitidos para produção - DEVE ser configurado com domínios específicos
ALLOWED_HOSTS = []  # TODO: Adicionar domínios de produção

# TODO: Configurações de produção a serem implementadas:
# 
# # Configurações de segurança
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_SECONDS = 31536000
# SECURE_REDIRECT_EXEMPT = []
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# 
# # Configurações de cache
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.redis.RedisCache',
#         'LOCATION': 'redis://127.0.0.1:6379/1',
#     }
# }
# 
# # Configurações de email
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = os.getenv('EMAIL_HOST')
# EMAIL_PORT = os.getenv('EMAIL_PORT', 587)
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
# 
# # Configurações de logging
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
#             'style': '{',
#         },
#     },
#     'handlers': {
#         'file': {
#             'level': 'INFO',
#             'class': 'logging.FileHandler',
#             'filename': BASE_DIR / 'logs' / 'django.log',
#             'formatter': 'verbose',
#         },
#     },
#     'root': {
#         'handlers': ['file'],
#     },
# }

print("AVISO: Configurações de produção ainda não foram implementadas completamente.")
print("Por favor, configure adequadamente antes de usar em produção.")