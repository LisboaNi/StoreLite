from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-!s-iql*z(k%l%tm(n$#)a%fs73^gsh+3bmkw4sc7gdntj)jfdo"

DEBUG = False

ALLOWED_HOSTS = ["storelite.onrender.com"]

INSTALLED_APPS = [
    "store",
    "product",
    "public",
    "jazzmin", 
    "storages",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "colorfield",
]

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

print("💥[STORELITE S3 DEBUG]🔑 AWS_ACCESS_KEY_ID =>", AWS_ACCESS_KEY_ID)
print("💥[STORELITE S3 DEBUG]🕵️ AWS_SECRET_ACCESS_KEY =>", AWS_SECRET_ACCESS_KEY)
print("💥[STORELITE S3 DEBUG]🪣 AWS_STORAGE_BUCKET_NAME =>", AWS_STORAGE_BUCKET_NAME)
print("💥[STORELITE S3 DEBUG]🌎 AWS_S3_REGION_NAME =>", AWS_S3_REGION_NAME)
print("💥[STORELITE S3 DEBUG]🚀 AWS_S3_CUSTOM_DOMAIN =>", AWS_S3_CUSTOM_DOMAIN)

AWS_DEFAULT_ACL = None
AWS_QUERYSTRING_AUTH = False

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

JAZZMIN_SETTINGS = {
    "site_title": "StoreLite Admin",
    "site_header": "StoreLite",
    "site_brand": "StoreLite",
    "welcome_sign": "Bem-vindo ao painel administrativo StoreLite",
    "copyright": "© 2025 StoreLite. Todos os direitos reservados.",
    "site_logo": "img/logo.svg",
    "topmenu_links": [
        {"name": "Site", "url": "/", "new_window": True},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "order_with_respect_to": ["auth", "store"],
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "GMT"

USE_I18N = True

USE_TZ = True

BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'