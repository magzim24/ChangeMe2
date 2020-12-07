import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
print(BASE_DIR)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-o#z@x5h79x26=pj_hp8z57+@m%cf1#m7b!ksny58s0-bozwti'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['10.11.12.110', '127.0.0.1', 'localhost']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'psycopg2',
    'crispy_forms',
    'social_django',

    'authorization.apps.AuthorizationConfig',

]

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'social_auth.context_processors.social_auth_by_name_backends',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'projectschool.urls'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)
# SOCIAL_AUTH_CREATE_USERS = True
SOCIAL_AUTH_FACEBOOK_KEY = '380175313193800'
SOCIAL_AUTH_FACEBOOK_SECRET = '387f6742fb6268ba86cfc2ae5a3d4e8f'
SOCIAL_AUTH_VK_OAUTH2_KEY = '7682476'
SOCIAL_AUTH_VK_OAUTH2_SECRET = 'FrSfBL4MOy7IVVODil1H'
# FACEBOOK_EXTENDED_PERMISSIONS = ['email']
AUTHENTICATION_BACKENDS = (
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.vk.VKOAuth2',

    'django.contrib.auth.backends.ModelBackend',
)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR + '/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'social_django.context_processors.backends',  # <-- Here
                'social_django.context_processors.login_redirect',  # <-- Here
            ],
        },
    },
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [BASE_DIR + '/templates'],

    },
]

WSGI_APPLICATION = 'projectschool.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
# LOGIN_REDIRECT_URL = 'http://localhost:8000'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': '',
        'HOST': '',
        'PASSWORD': 'Kiillofs2',
        'PORT': '5432',
    }
}

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static', 'staticfiles'),
)
# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

# SOCIAL_AUTH_PIPELINE = (
#    # Получает по backend и uid инстансы social_user и user
#    'social_auth.backends.pipeline.social.social_auth_user',
#    # Получает по user.email инстанс пользователя и заменяет собой тот, который получили выше.
#    # Кстати, email выдает только Facebook и GitHub, а Vkontakte и Twitter не выдают
#    'social_auth.backends.pipeline.associate.associate_by_email',
#    # Пытается собрать правильный username, на основе уже имеющихся данных
#    'social_auth.backends.pipeline.user.get_username',
#    # Создает нового пользователя, если такого еще нет
#    'social_auth.backends.pipeline.user.create_user',
#    # Пытается связать аккаунты
#    'social_auth.backends.pipeline.social.associate_user',
#    # Получает и обновляет social_user.extra_data
#    'social_auth.backends.pipeline.social.load_extra_data',
#    # Обновляет инстанс user дополнительными данными с бекенда
#    'social_auth.backends.pipeline.user.update_user_details'
# )

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'myformatter': {
            'format': "{levelname} {asctime} {module} {message}",
            'style': '{',
        }
    },
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': '\\Users\\Admin2\\Documents\\fileCharge\\projectschool\\projectschool\\debug.log',
            'level': 'DEBUG',
            'formatter': 'myformatter'
        },
    },
    'loggers': {
        'authorization': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        }
    }
}

ASGI_APPLICATION = 'projectschool.asgi.application'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'maksimochkin04@gmail.com'
EMAIL_HOST_PASSWORD = 'Kiillofs2'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'maksimochkin04@gmail.com'
