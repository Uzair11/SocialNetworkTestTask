from django.urls import include, path
from users.views import UserModelViewSet, UserRegisterViewSet, TokenObtainUserView, PostView, PostViewSet, LikesPostViewSet
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)


from rest_framework.routers import DefaultRouter, Route, escape_curly_brackets


class HyphenatedRouter(DefaultRouter):
    """Same as Default Router only switches _ with -"""

    def _get_dynamic_route(self, route, action):
        init_kwargs = route.initkwargs.copy()
        init_kwargs.update(action.kwargs)

        url_path = escape_curly_brackets(action.url_path)

        return Route(
            url=route.url.replace("{url_path}", url_path.replace("_", "-")),
            mapping=action.mapping,
            name=route.name.replace("{url_name}", action.url_name),
            detail=route.detail,
            initkwargs=init_kwargs,
        )


router = HyphenatedRouter()
router.register("api/post", PostViewSet, basename="post")
urlpatterns = [
    path('api/token/', TokenObtainUserView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/register/', UserRegisterViewSet.as_view({'post': 'register_user'}), name='register_user'),
    path('api/me/', UserRegisterViewSet.as_view({'get': 'get_user_profile'}), name='get_user_profile'),
    path('api/like_post/', LikesPostViewSet.as_view({'post': 'like_post'}), name='like_post'),
    path('api/unlike_post/', LikesPostViewSet.as_view({'delete': 'unlike_post'}), name='unlike_post'),
    path('api/user_post/', LikesPostViewSet.as_view({'get': 'user_posts'}), name='user_posts'),
] +router.urls