MY_SECRET = {
    "SECRET_KEY" : "django-insecure-p&ko1%xuxhobqw^tiww&p*1^731bpnmnyjt@f)fbh*&kegg&ze"
}

MY_DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'danjidb',
        'USER': 'root',
        'PASSWORD': 'qwer0502',
        'HOST': 'database-dangi.chs86gugo7e5.ap-northeast-2.rds.amazonaws.com',
        'PORT': '3306',
        'OPTIONS':{
                    'init_command' : "SET sql_mode='STRICT_TRANS_TABLES'"
                }
    }
}