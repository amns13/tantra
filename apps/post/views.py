from core.views import (CurrentUserListCreateApiView,
                        CurrentUserRetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Post
from .serializers import PostSerializer


class PostListAPIView(CurrentUserListCreateApiView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Post.objects.filter(is_active=True)
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.validated_data['author'] = self.request.user
        return super(PostListAPIView, self).perform_create(serializer)


class PostDetailAPIView(CurrentUserRetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Post.objects.filter(is_active=True)
    serializer_class = PostSerializer
    lookup_field = 'uuid'
