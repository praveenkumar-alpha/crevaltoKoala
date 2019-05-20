import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'koala',
        'USER': 'koala',
        'PASSWORD': 'koala',
        'HOST': 'mdb_db-koala-lms',
    }
}
