from datetime import timedelta
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third Party Apps
    'rest_framework',
    'django_celery_beat',
    'drf_yasg',

    # Local Apps
    'app_account.apps.AppAccountConfig',
    'app_store.apps.AppStoreConfig',
    'app_product.apps.AppProductConfig',
    'app_ticket.apps.AppTicketConfig',
    'app_order.apps.AppOrderConfig',
    'app_bookmark.apps.AppBookmarkConfig',
    'app_like.apps.AppLikeConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'DrfShop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'DrfShop.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Active User
AUTH_USER_MODEL = 'app_account.User'

# Toman
MIN_CHECKOUT = 10000
MAX_CHECKOUT = 100000

# Length of Bank Number
BANK_NUMBER_LENGTH = 16

# Time For Expire SMS
TIME_EXPIRE = 150

# Send SMS
KAVENEGAR_SECRET_KEY = config('KAVENEGAR_SECRET_KEY')

# Redis Config
REDIS_HOST = config('REDIS_HOST', default='localhost')
REDIS_PORT = config('REDIS_PORT', cast=int, default=6379)

# Redis DB Numbers
PHONE_REGISTER_DB = 1
FORGET_PASSWORD_DB = 2

SESSION_SAVE_EVERY_REQUEST = True
CART_SESSION_ID = 'cart'

CELERY_BROKER_URL = config('CELERY_BROKER_URL', default='amqp://guest:guest@localhost')
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default='rpc://')

# Rest Framework Config
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

# JWT Config
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=14),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'UPDATE_LAST_LOGIN': True,
}

# Confog For Authorization in Swagger
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
        }
    },
}
