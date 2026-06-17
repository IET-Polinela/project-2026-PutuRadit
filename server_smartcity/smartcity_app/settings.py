"""
Django settings for smartcity_app project.
"""

from pathlib import Path
from datetime import timedelta
from django.contrib.messages import constants as messages


# =========================
# BASE DIR
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent


# =========================
# SECURITY
# =========================
SECRET_KEY = (
    'django-insecure-j^xzx_fjtn1pqt&#zvmu138er+-z9o6y'
    '#73n_$o^z*ms2mb&r6'
)

DEBUG = True

ALLOWED_HOSTS = [
    '*',
]

CSRF_TRUSTED_ORIGINS = [
    'http://103.151.63.86:8009',
]


# =========================
# INSTALLED APPS
# =========================
INSTALLED_APPS = [
    # Django internal apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',

    # OpenAPI documentation
    'drf_spectacular',
    'django_scalar',

    # Project apps
    'main_app',
    'about',
    'contacts',
    'reports',
    'dashboard_24782059',
    'usermanagement_24782059',
]


# =========================
# MIDDLEWARE
# =========================
MIDDLEWARE = [
    # CORS harus ditempatkan sebelum CommonMiddleware
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# =========================
# ROOT URL
# =========================
ROOT_URLCONF = 'smartcity_app.urls'


# =========================
# TEMPLATES
# =========================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# =========================
# WSGI
# =========================
WSGI_APPLICATION = 'smartcity_app.wsgi.application'


# =========================
# DATABASE
# =========================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'smartcity_db',
        'USER': 'postgres',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# =========================
# CUSTOM USER MODEL
# =========================
AUTH_USER_MODEL = 'usermanagement_24782059.CustomUser'


# =========================
# AUTHENTICATION BACKENDS
# =========================
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]


# =========================
# PASSWORD VALIDATION
# =========================
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'UserAttributeSimilarityValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'MinimumLengthValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'CommonPasswordValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'NumericPasswordValidator'
        ),
    },
]


# =========================
# INTERNATIONALIZATION
# =========================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'

USE_I18N = True
USE_TZ = True


# =========================
# STATIC FILES
# =========================
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'


# =========================
# DEFAULT PRIMARY KEY
# =========================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# =========================
# LOGIN / LOGOUT
# =========================
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/reports/'
LOGOUT_REDIRECT_URL = '/login/'


# =========================
# MESSAGE TAGS
# =========================
MESSAGE_TAGS = {
    messages.SUCCESS: 'success',
    messages.ERROR: 'danger',
    messages.WARNING: 'warning',
    messages.INFO: 'info',
}


# =========================
# DJANGO REST FRAMEWORK
# =========================
REST_FRAMEWORK = {
    # Menggunakan drf-spectacular untuk menghasilkan OpenAPI Schema
    'DEFAULT_SCHEMA_CLASS': (
        'drf_spectacular.openapi.AutoSchema'
    ),

    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],

    # Autentikasi API menggunakan JWT Bearer Token
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}


# =========================
# SIMPLE JWT
# =========================
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),

    'AUTH_HEADER_TYPES': (
        'Bearer',
    ),
}


# =========================
# OPENAPI / DRF SPECTACULAR
# =========================
SPECTACULAR_SETTINGS = {
    'TITLE': 'Smart City Portal API',

    'DESCRIPTION': (
        'Dokumentasi REST API resmi untuk Portal Pelaporan '
        'Laporan Warga'
    ),

    'VERSION': '1.0.0',

    # Endpoint schema tidak dimunculkan sebagai endpoint API biasa
    'SERVE_INCLUDE_SCHEMA': False,

    # Mengurutkan endpoint berdasarkan nama/path
    'SORT_OPERATIONS': True,
}


# =========================
# CORS SETTINGS
# =========================
CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_CREDENTIALS = True
