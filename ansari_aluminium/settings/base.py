"""
Base settings for ansari_aluminium project.
"""
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR is now one level up compared to old settings.py because of settings dir
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Quick-start development settings - unsuitable for production
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-t2xy^571q_wv*$g^w-sg!-pu3&brqxv9!f$ih4lb2(ia1s$@(w"

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.contrib.sitemaps",
    "django.contrib.sites",
    # Third-party apps
    "dynamic_preferences",
    # Local apps
    "core.apps.CoreConfig",
    "accounts.apps.AccountsConfig",
    "website.apps.WebsiteConfig",
    "customers.apps.CustomersConfig",
    "products.apps.ProductsConfig",
    "quotations.apps.QuotationsConfig",
    "orders.apps.OrdersConfig",
    "billing.apps.BillingConfig",
    "dashboard.apps.DashboardConfig",
    "pwa",
]

SITE_ID = 1

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ansari_aluminium.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.site_settings",
                "dynamic_preferences.processors.global_preferences",
            ],
        },
    },
]

WSGI_APPLICATION = "ansari_aluminium.wsgi.application"

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# Static files
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Custom User Model
AUTH_USER_MODEL = "accounts.User"

# Login URLs
LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "dashboard:index"
LOGOUT_REDIRECT_URL = "website:home"

# Site Settings
SITE_NAME = "Ansari Aluminium"
SITE_TAGLINE = "Aluminium & UPVC Fabrication Services"

# Contact Settings
import os
CONTACT_EMAIL = os.environ.get('CONTACT_EMAIL', 'mohd.shoyab1991@gmail.com')

# PWA Settings
PWA_APP_NAME = 'Ansari Aluminium'
PWA_APP_DESCRIPTION = "Aluminium & UPVC Fabrication Services"
PWA_THEME_COLOR = '#6750A4'
PWA_BACKGROUND_COLOR = '#ffffff'
PWA_DISPLAY = 'standalone'
PWA_APP_ORIENTATION = "portrait-primary"
PWA_SCOPE = '/'
PWA_START_URL = '/'
PWA_APP_ICONS = [
    {
        'src': '/static/assets/icons/icon-192x192.png',
        'sizes': '192x192',
        'type': 'image/png'
    },
    {
        'src': '/static/assets/icons/icon-512x512.png',
        'sizes': '512x512',
        'type': 'image/png'
    }
]
PWA_APP_ICONS_APPLE = [
    {
        'src': '/static/assets/icons/icon-512x512.png',
        'sizes': '512x512',
        'type': 'image/png'
    }
]
PWA_APP_SPLASH_SCREEN = [
    {
        'src': '/static/assets/icons/icon-512x512.png',
        'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
    }
]
PWA_DIR = 'ltr'
PWA_LANG = 'en-US'

# Session Configuration - Disable Auto Logout
# Keep the session cookie alive for 10 years (effectively never expiring)
SESSION_COOKIE_AGE = 315360000  # 10 years in seconds
SESSION_SAVE_EVERY_REQUEST = True  # Refresh the expiration time on every request
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # Ensure session stays active even if they close their browser
