from django.urls import include, path
from rest_framework import routers

from api.views import (
    CategoryViewSet, CommentViewSet, GenresViewSet,
    ReviewViewSet, TitleViewSet
)
from users.views import (
    AuthSignupAPIView, TokenAPIView, UsersViewSet
)

app_name = 'api'

router = routers.DefaultRouter()

router.register(r'users', UsersViewSet, basename='users')
router.register(r'titles', TitleViewSet, basename='titles')
router.register(r'genres', GenresViewSet, basename='genres')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/auth/signup/', AuthSignupAPIView.as_view()),
    path('api/v1/auth/token/', TokenAPIView.as_view()),
]
