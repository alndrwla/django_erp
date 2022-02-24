MYSQL = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        "NAME": "erp",
        "HOST": "127.0.0.1",
        "USER": "root",
        "PASSWORD": "",
    }
}


POSTGRESQL = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        "NAME": "erp",
        "HOST": "127.0.0.1",
        "USER": "erp",
        "PASSWORD": "YourPassword",
        "PORT": 5432,
    }
}
