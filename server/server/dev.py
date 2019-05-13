from .settings import *

CUBEMOVERS = {
    'quality_email': 'collinskivale@gmail.com',
    'sms_username': 'cubecrm',
    'sms_apikey': '835713339ec77ff20f48c1eee88baf79f448a0f5be171f6c647edd4a8b7931ae'
}
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cubemovercrm',
        'USER': 'local',
        'PASSWORD': 'local',
        'HOST': 'localhost',
        'OPTIONS': {
            "init_command": "SET default_storage_engine=INNODB, character_set_connection=utf8, collation_connection=utf8_unicode_ci"
        }
    }
}
