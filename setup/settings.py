import os
from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-%uaj8ai29#!8wo^2eeg*hr9m8hmwxnt1uje_fpe*0zk-buryh%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']  

CORS_ORIGIN_ALLOW_ALL = True

URL_FRONTEND = 'http://98.81.255.202:90'

AUTH_USER_MODEL = 'safekey.User'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'safekey',
    'drf_yasg',
    'rest_framework.authtoken',
    'django_celery_beat',
    'channels',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'setup.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
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

ASGI_APPLICATION = 'setup.asgi.application'
WSGI_APPLICATION = 'setup.wsgi.application'

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"  
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "safekeyifpb@gmail.com"
EMAIL_HOST_PASSWORD = "yptoowqaslxwlwaa"

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  
        'NAME': 'safekey',                          
        'USER': 'admin',                          
        'PASSWORD': 'admin123',                      
        'HOST': 'db',                        
        'PORT': '5432',                             
    }
}

CELERY_BROKER_URL = 'redis://redis:6379/0' 
CELERY_RESULT_BACKEND = 'redis://redis:6379/0' 
CELERY_BEAT_SCHEDULE = {
    'update_status_task_every_seconds': {
        'task': 'safekey.tasks.tasks.update_status_task',  
        'schedule': 10,  # Executa a cada 10 segundos
    },
}

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": ['redis://redis:6379/0'],  
        },
    },
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'safekey.authentication.AuthenticationUser',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),  # Tempo de vida do access token
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),  # Tempo de vida do refresh token
    'ROTATE_REFRESH_TOKENS': False,  # Para evitar rotação automática
    'BLACKLIST_AFTER_ROTATION': True,  # Blacklist após rotação
    'ALGORITHM': 'HS256',  # Algoritmo de criptografia
    'SIGNING_KEY': SECRET_KEY,  # Chave usada para assinar os tokens
}


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")  # Diretório onde os arquivos serão coletados
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]  # Diretório para arquivos estáticos do projeto
# python manage.py collectstatic --noinput

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
