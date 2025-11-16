# api/urls.py (ИСПРАВЛЕННАЯ ВЕРСИЯ)

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, GroupViewSet, PostViewSet

router = DefaultRouter()

# Просто регистрируем ViewSet. Роутер сам все поймет из queryset.
router.register('posts', PostViewSet) # <--- ИЗМЕНЕНИЕ ЗДЕСЬ
router.register('groups', GroupViewSet) # <--- И здесь тоже убрал basename для единообразия

router.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router.urls)),
]
#Обратите внимание: для `CommentViewSet` `basename` **нужен**, потому что у него нет `.queryset`, а есть метод `get_queryset()`, из которого роутер не может автоматически определить модель.*