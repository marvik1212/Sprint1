DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': '127.0.0.1',
        'PORT': '5435',
        'OPTIONS': {
            'options': '-c search_path=public,content',
            'client_encoding': 'UTF8',
        }
    }
}
