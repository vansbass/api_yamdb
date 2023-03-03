from django.urls import include, path
from rest_framework import routers

from users.views import RegistrationViewSet, TokenView, UsersViewSet
from .views import (
    CategoriesOrGenresViewSet, ReviewOrCommentViewSet, TitleViewSet
)

app_name = 'api'

router = routers.DefaultRouter()

router.register(r'genres', CategoriesOrGenresViewSet, basename='genres')
router.register(r'categories', CategoriesOrGenresViewSet, basename='categories')
router.register(r'users', UsersViewSet, basename='users')
router.register(r'titles', TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewOrCommentViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    ReviewOrCommentViewSet,
    basename='comments'
)
router.register(r'auth/signup', RegistrationViewSet, basename='signup')
urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/auth/token/', TokenView.as_view()),
]
