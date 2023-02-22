from rest_framework import mixins, viewsets


from .serializers import (
    CategorySerializer, CommentSerializer, GenreSerializer,
    ReviewSerializer, TitleSerializer
)
from reviews.models import ( 
    Category, Comment, Genre, Review, Title
)

# POST, GET(list), DEL методы, остальные запрещены
class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericAPIView):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = ()

# POST, GET(list, single), DEL, PUT, PUTCH методы, остальные запрещены
class CommentViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = ()

# POST, GET(list), DEL методы, остальные запрещены
class GenreViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = ()

# POST, GET(list, single), DEL, PUT, PUTCH методы, остальные запрещены
class ReviewViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = ()

# POST, GET(list, single), DEL, PUT, PUTCH методы, остальные запрещены
class TitleViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericAPIView):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = ()