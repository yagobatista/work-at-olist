from project.settings.common import *

import dj_database_url

ALLOWED_HOSTS = ['challenge-olist.herokuapp.com']
DEBUG = False
DEFAULT_FROM_EMAIL = 'yagobatistasilva@Gmail.com'

DATABASES = {
    'default': dj_database_url.config(conn_max_age=600),
}
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'