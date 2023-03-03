from django.urls import include, path
from rest_framework import routers

from users.views import RegistrationViewSet, TokenView, UsersViewSet
from .views import (
    CommentViewSet,
    ReviewViewSet, TitleViewSet, CategoryViewSet, GenresViewSet
)

app_name = 'api'

router = routers.DefaultRouter()

router.register(r'users', UsersViewSet, basename='users')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenresViewSet, basename='genres')
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
urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/auth/token/', TokenView.as_view()),
    # path('api/v1/categories/', CategoriesView.as_view()),
    # path('api/v1/categories/<slug:slug>/', CategoryDeleteView.as_view()),
    # path('api/v1/genres/', GenreView.as_view()),
    # path('api/v1/genres/<slug:slug>/', GenreDeleteView.as_view()),
    # path('api/v1/users/', UsersListCreateView.as_view()),
    # path('api/v1/users/<str:username>/', UserRetrieveUpdateDestroyView.as_view())
    # path('api/v1/users/me/', UserRetrieveUpdateAPIView.as_view()),
]
