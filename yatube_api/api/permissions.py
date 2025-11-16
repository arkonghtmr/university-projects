# api/permissions.py

from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Разрешает редактирование только автору объекта.
    Для остальных пользователей разрешено только чтение.
    """
    def has_object_permission(self, request, view, obj):
        # Разрешаем любые безопасные запросы (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Разрешаем редактирование и удаление только автору объекта
        return obj.author == request.user