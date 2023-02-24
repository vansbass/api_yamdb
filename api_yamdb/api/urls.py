from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import (
    CategoryViewSet, CommentViewSet, GenreViewSet,
    ReviewViewSet, TitleViewSet
)

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'titles', TitleViewSet, basename='titles')
router.register(
    r'titles/?P<title_id>\d+/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/?P<title_id>\d+/reviews/?P<review_id>\d+/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/auth/token/',
         TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
]
