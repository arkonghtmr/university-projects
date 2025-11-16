# api/views.py

from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from posts.models import Group, Post
from .permissions import IsAuthorOrReadOnly
from .serializers import CommentSerializer, GroupSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с постами.
    Предоставляет полный CRUD.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # Применяем кастомное право доступа
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        # При создании поста автором становится текущий пользователь
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для работы с группами.
    Предоставляет только чтение (список и детальная информация).
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    # IsAuthenticatedOrReadOnly здесь можно не указывать,
    # т.к. в settings.py уже стоит IsAuthenticated по умолчанию,
    # а редактирование ReadOnlyModelViewSet и так не позволяет.
    # Но для явности можно оставить.
    permission_classes = [IsAuthenticatedOrReadOnly]


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с комментариями.
    Предоставляет полный CRUD.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_post(self):
        # Получаем пост из URL
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def get_queryset(self):
        # Возвращаем комментарии только для конкретного поста
        post = self.get_post()
        return post.comments.all()

    def perform_create(self, serializer):
        # При создании комментария автором становится текущий пользователь,
        # а пост берется из URL
        post = self.get_post()
        serializer.save(author=self.request.user, post=post)