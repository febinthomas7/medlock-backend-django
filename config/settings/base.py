import os
import sys
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv
from datetime import timedelta

# 1. Base Directory Setup
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# 2. Load Environment Variables from .env
load_dotenv(os.path.join(BASE_DIR, '.env'))

# 3. CRITICAL: Inject 'apps' folder into Python path
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-fallback-key-change-this')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = ['*']

# Whitelist your React frontend ports (CRA uses 3000, Vite uses 5173)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "https://reliable-jalebi-ace0ca.netlify.app",
]

# 4. Application Registry
INSTALLED_APPS = [
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
    
    # Custom Application Modules (Directly imported thanks to sys.path modification)
    'core',
    'common',
    'events',
    'notifications',
    'saas_core_admin',
    'plugin_rbac',
    'network_biometric',
    'hr_attendance_department',
    'user',
    'claim',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # You can add global template directories here later if needed
        'APP_DIRS': True,  # Tells Django to look for template folders inside apps
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

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'apps.user.views.auth_api.ERPJWTAuthentication',
    ),
    # Optional but good practice: set the default permission globally
    # 'DEFAULT_PERMISSION_CLASSES': (
    #     'rest_framework.permissions.IsAuthenticated',
    # )
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),  # Lasts 1 day instead of 5 minutes
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}