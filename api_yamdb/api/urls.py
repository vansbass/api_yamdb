from django.urls import include, path
from rest_framework import routers

from users.views import RegistrationViewSet, TokenView

from .views import (
    CategoryViewSet, CommentViewSet, GenreViewSet,
    ReviewViewSet, TitleViewSet, UserViewSet, UsernameViewSet
)

app_name = 'api'

router = routers.DefaultRouter()

router.register(r'^users/(?P<username>[\w.@+-]+)/$', UsernameViewSet, basename='username')
router.register(r'users', UserViewSet, basename='users')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'titles', TitleViewSet, basename='titles')
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
router.register(r'auth/signup', RegistrationViewSet, basename='signup')
# router.register(r'auth/token', TokenView, basename='token')
urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/auth/token/', TokenView.as_view()),
]
