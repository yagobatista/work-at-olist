from project.settings.common import *

DATABASES = {
    'default': {        
        'ENGINE': 'django.db.backends.sqlite3',        
        'NAME': os.path.join(BASE_DIR, '../db.sqlite3'),    
    }
}

ALLOWED_HOSTS = ['*']
DEBUG = True
DEFAULT_FROM_EMAIL = 'yagobatistasilva@Gmail.com'