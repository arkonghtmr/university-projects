# yatube_api/urls.py

from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Подключаем все URL из нашего приложения api
    path('api/', include('api.urls')),
]

# Добавляем эндпоинт для получения токена
# Он будет доступен по адресу api/v1/api-token-auth/
urlpatterns += [
    path('api/v1/api-token-auth/', views.obtain_auth_token),
]