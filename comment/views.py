from rest_framework import viewsets
from comment.models import *
from comment.serializers import *
from comment.permissions import *
# Create your views here.


class CommentViewSet(viewsets.ModelViewSet):
    """
    评论视图集
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)