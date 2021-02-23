import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'c7*-yo9$3$#x_371l@2)1-)gm$1#xt#cyua*9a302fye6-=1pv'

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMIN = (
    ('Ian Kosen', 'ikosenn@gmail.com'),
    ('Lamech Dete', 'lamech664@gmail.com'),
    ('Elisha Abade', 'elisha.abade@gmail.com'),)
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '45.55.67.27',
                 'crm.cubemovers.co.ke']
# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'corsheaders',
    'datatableview',
    'easy_pdf',
    'markdown_deux',  # Required for Knowledgebase item formatting
    'bootstrapform',  # Required for nicer formatting of forms with the default templates
    'helpdesk',  # This is us!
    # 'tinymce',
    'bootstrap3',
    'core',
    'data',

    'dashboard',
    'customers',
    'inquiries',
    'surveys',
    'quotations',
    'moves',
    'invoices',
    'bookings',
    'reports'
)
MOVE_PDF_TPLS = {
    'OFFICE_MOVE': 'moves/pdf/office.html',
    "STORAGE_AND_WAREHOUSING": 'moves/pdf/storage.html',
    'DEFAULT': 'moves/pdf/default.html'
}

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'core/templates')],
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

WSGI_APPLICATION = 'server.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'movers_crm_db',
        'USER': 'webuser',
        'PASSWORD': 'user@123',
        'HOST': 'localhost',
        'PORT': '5432',
        'OPTIONS': {
            "init_command": "SET default_storage_engine=INNODB, character_set_connection=utf8, collation_connection=utf8_unicode_ci"
        }
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

LOGIN_URL = '/login/'

CORS_ORIGIN_ALLOW_ALL = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_HOST_USER = 'customerrelation@cubemovers.co.ke'

EMAIL_HOST_PASSWORD = 'Customer2016'

EMAIL_PORT = 587

EMAIL_USE_TLS = True

TEMPLATED_EMAIL_BACKEND = 'templated_email.backends.vanilla_django.TemplateBackend'

QUOTATION_EMAILS_CC = 'sales@cubemovers.co.ke'

BOOKING_ORDER_EMAIL = 'team@cubemovers.co.ke'


from django.conf import global_settings

# TEMPLATE_CONTEXT_PROCESSORS = (
#     global_settings.TEMPLATE_CONTEXT_PROCESSORS +
#     ('django.core.context_processors.request',)
# )
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] " +
                      "%(module)s %(process)d %(thread)d %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'propagate': False,
            'level': 'DEBUG',
            'filters': ['require_debug_false'],
        },
    }}
QUEUE_EMAIL_BOX_HOST = 'smtp.gmail.com'
QUEUE_EMAIL_BOX_USER = 'customerrelation@cubemovers.co.ke'
QUEUE_EMAIL_BOX_PASSWORD = 'Customer2016'
QUEUE_EMAIL_BOX_SSL = True

CUBEMOVERS = {
    'quality_email': 'sales@cubemovers.co.ke',
    'sms_username': 'cubecrm',
    'sms_apikey': '835713339ec77ff20f48c1eee88baf79f448a0f5be171f6c647edd4a8b7931ae'
}

# CELERY STUFF
BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['pickle']
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_RESULT_SERIALIZER = 'pickle'
CELERY_TIMEZONE = TIME_ZONE
