from pathlib import Path  # Ensure this import is consistent
import os
import dj_database_url
from dotenv import load_dotenv

if os.path.exists('env.py'):
    import env

# Build paths inside the project like this: BASE_DIR / 'subdir'
BASE_DIR = Path(__file__).resolve().parent.parent

# Ensure the app binds to the PORT set by Render, falling back to 8000
PORT = int(os.environ.get('PORT', 8000))  # Use 8000 as the default fallback

# Load environment variables
load_dotenv()

# Quick-start development settings
SECRET_KEY = os.environ.get('SECRET_KEY', '')
DEBUG = 'DEVELOPMENT' in os.environ
ALLOWED_HOSTS = ['127.0.0.1',
 'localhost',
 'justus-ai-swahili-bob-tattoo.onrender.com',
'.onrender.com',
]

# Application definition remains unchanged ...
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'crispy_forms',
    'crispy_bootstrap4',  # ← Add this line
    'storages',
    
    # Your apps
    'home',
    'products',
    'bag',
    'checkout',
    'profiles',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
     'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',  # Add this line
]
ROOT_URLCONF = 'swahili_bob_tattoo.urls'
WSGI_APPLICATION = 'swahili_bob_tattoo.wsgi.application'

# Database Configuration
if 'DATABASE_URL' in os.environ:
    DATABASES = {'default': dj_database_url.parse(os.getenv('DATABASE_URL'))}
else:
    if DEBUG:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            }
        }
    else:
        raise RuntimeError("DATABASE_URL is required in production.")

# Static and Media Configuration
# Static and Media Configuration
# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

# Media files (uploads)
MEDIA_URL = '/media/'

# AWS S3 Configuration
# Static files configuration
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Always set these (needed by collectstatic even with S3)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# AWS S3 Configuration
if 'USE_AWS' in os.environ:
    # AWS Settings
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME', 'us-east-1')
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    
    # S3 Static Files
    STATICFILES_LOCATION = 'static'
    STATICFILES_STORAGE = 'custom_storages.StaticStorage'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATICFILES_LOCATION}/'
    
    # S3 Media Files
    MEDIAFILES_LOCATION = 'media'
    DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIAFILES_LOCATION}/'
else:
    # Local development
    MEDIA_URL = '/media/'
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'templates', 'allauth'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # required by Allauth
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'bag.contexts.bag_contents',
            ],
            'builtins': [
                'crispy_forms.templatetags.crispy_forms_tags',
                'crispy_forms.templatetags.crispy_forms_field',
            ]
        },
    },
]
# Logging directory
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(LOGS_DIR, exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGS_DIR, 'django.log'),
        },
    },
    'root': {
        'handlers': ['console', 'file'] if not DEBUG else ['console'],
        'level': 'DEBUG' if DEBUG else 'WARNING',
    },
}

# Email Configuration
if 'DEVELOPMENT' in os.environ:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

    if not all([EMAIL_HOST_USER, EMAIL_HOST_PASSWORD]):
        raise RuntimeError("Missing EMAIL environment variables.")

# Other unchanged settings ...
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Stripe Configuration
STRIPE_CURRENCY = 'sek'
STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY', '')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')
STRIPE_WH_SECRET = os.getenv('STRIPE_WH_SECRET', '')

# Delivery settings
FREE_DELIVERY_THRESHOLD = 500  # Free delivery over 500 SEK
STANDARD_DELIVERY_PERCENTAGE = 10  # 10% delivery charge
# Stripe Configuration
STRIPE_CURRENCY = 'sek'
STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY', '')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')
STRIPE_WH_SECRET = os.getenv('STRIPE_WH_SECRET', '')

# Delivery settings
FREE_DELIVERY_THRESHOLD = 500  # Free delivery over 500 SEK
STANDARD_DELIVERY_PERCENTAGE = 10  # 10% delivery charge

# Site settings
SITE_ID = 1

# Crispy Forms
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Allauth settings
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'optional'  # Change to 'mandatory' when email works
ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = True
ACCOUNT_USERNAME_MIN_LENGTH = 4
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'

# Django Sites Framework
SITE_ID = 1

# Crispy Forms Configuration
# Crispy Forms Configuration
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Django Allauth Configuration
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = True
ACCOUNT_USERNAME_MIN_LENGTH = 4
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
