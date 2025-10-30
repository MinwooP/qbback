import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'your-secret-key-here'  # 실제 환경에서는 환경변수로 관리
DEBUG = True
ALLOWED_HOSTS = ['*']

# AI_AGENT 변수 설정
# 환경변수에서 'AI_AGENT_URL' 값을 읽어오고, 값이 없다면 기본값 사용
AI_AGENT_URL = os.getenv('AI_AGENT_URL', 'http://10.220.150.75:8019/api/v1')
# AI Agent 서버 요청 시 최대 대기 시간
# 타임아웃 (초)
AI_AGENT_TIMEOUT = 30 

# AI_AGENT 관련 로깅 설정
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            # 로그 메세지 출력 형식 - 로그 레벨, 로그 발생 시간, 로그 발생 파일 이름, 실제 로그 메시지 
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'api': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'api',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'api.middleware.SessionAuthenticationMiddleware',
]

# CORS 설정
CORS_ALLOW_ALL_ORIGINS = True  # 개발 환경용, 실제 환경에서는 특정 도메인만 허용
CORS_ALLOW_CREDENTIALS = True

# PostgreSQL 데이터베이스 설정
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres', # DB명
        'USER': 'minwoo', # 사용자명
        'PASSWORD': 'asd2981vv@', # 비밀번호
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# REST Framework 설정
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': [],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
}

ROOT_URLCONF = 'qb_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
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

WSGI_APPLICATION = 'qb_backend.wsgi.application'

LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
