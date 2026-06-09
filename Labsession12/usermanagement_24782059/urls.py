from django.urls import path

from .views import (
    RegisterView,
    LoginView,
)

from .api_views import (
    RegisterAPIView,
)


urlpatterns = [

    # =========================
    # WEB AUTH
    # =========================
    path(
        'register/',
        RegisterView.as_view(),
        name='register'
    ),

    path(
        'login/',
        LoginView.as_view(),
        name='login'
    ),

    # =========================
    # API REGISTER
    # =========================
    path(
        'api/register/',
        RegisterAPIView.as_view(),
        name='api_register'
    ),
]
