"""
Django settings for drf project.

Generated by 'django-admin startproject' using Django 3.2.14.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-3jyxjkjft9t=x%#_wv*tce6wv2e*s4!70vovmmnzr9q^-r^4mp'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  #drf注册
    'django_filters', #drf过滤
    'coreapi',  #接口文档
    'drf_yasg',  #接口文档
    
    'stu_api', #提供原生django代码实现的api接口
    'students', #提供drf代码实现的api接口，完全drf简写
    'sers', #序列化器的学习
    'school', #序列化器的嵌套
    'req', #drf提供的请求与响应
    'demo', #视图（从复杂到精简）
    'opt', #drf组件使用
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'drf.urls'

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

WSGI_APPLICATION = 'drf.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'students',
        'HOST':'127.0.0.1',
        'PORT':3306,
        'USER':'root',
        'PASSWORD':'mysql123456',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# https://www.django-rest-framework.org/
# opt组件
#位于环境包下的site-packages/rest_framework/settings.py

# drf配置信息必须全部写在REST_FRAMEWORK配置项中
REST_FRAMEWORK = {
    #常见认证方式cookie,session,token
    #restframework认证 全局
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'drf.authentication.ExampleAuthentication', #自定义
        'rest_framework.authentication.SessionAuthentication',  #session认证
        'rest_framework.authentication.BasicAuthentication'  #基本认证
    ],
    #权限 全局
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'drf.permissions.ExamplePermission', #自定义
    #     # 大部分企业在工作中用下面这句作为权限，同时在登录注册视图中设置permission_classes=[]来覆盖这句，局部优先级高于全局
    #     # 'rest_framework.permissions.IsAuthenticated',
    # ],
    #限流设置(全局或者局部)
    # 'DEFAULT_THROTTLE_CLASSES': [
    #     'rest_framework.throttling.AnonRateThrottle', #未认证用户【未登录用户】
    #     'rest_framework.throttling.UserRateThrottle', #已认证用户【已登录用户】
    # ],
    'DEFAULT_THROTTLE_RATES': { #频率配置
        'anon': '2/min', #针对游客的访问频率进行限制，实际上drf只是识别首字母，为了提高代码维护性，建议写完整单词,可以是day,hour,min,sec
        'user': '5/min', #针对登录用户
        #自定义限流分类
        'vip':'3/d',
        'vvip':'60/d',
    },
    # #过滤查询，全局配置
    # 'DEFAULT_FILTER_BACKENDS':[
    #     'django_filters.rest_framework.DjangoFilterBackend'  #过滤，还要在视图类中添加filter_fields属性
    # ]
    #排序，过滤和排序使用一个公用配置项，所以两者要么一起全局要么一起局部
    # 'DEFAULT_FILTER_BACKENDS':[
    #     'rest_framework.filters.OrderingFilter'  #排序
    # ]
    #分页全局配置-基本不用
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',#偏移量分页器
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination', #页码分页器
    # 'PAGE_SIZE': 5, # 每⻚数⽬

    #自定义异常[全局配置]
    'EXCEPTION_HANDLER':'drf.exceptions.my_exception_handler',

    #接口文档生成 coreapi或者yasg,注册后这里配置再url配置
    'DEFAULT_SCHEMA_CLASS':'rest_framework.schemas.AutoSchema',

}

