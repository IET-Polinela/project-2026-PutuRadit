from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView

from usermanagement_24782059.views import (
    LoginView,
    RegisterView,
)

# JWT
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [

    # =========================
    # ADMIN
    # =========================
    path(
        'admin/',
        admin.site.urls
    ),

    # =========================
    # WEB APPS
    # =========================
    path(
        '',
        include('main_app.urls')
    ),

    path(
        'about/',
        include('about.urls')
    ),

    path(
        'contacts/',
        include('contacts.urls')
    ),

    path(
        'reports/',
        include('reports.urls')
    ),

    # =========================
    # REPORT API
    # =========================
    path(
        'api/',
        include('reports.api_urls')
    ),

    # =========================
    # USER API
    # =========================
    path(
        'user/',
        include('usermanagement_24782059.urls')
    ),

    # =========================
    # JWT TOKEN
    # =========================
    path(
        'api/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),

    path(
        'api/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),

    # =========================
    # WEB AUTH
    # =========================
    path(
        'login/',
        LoginView.as_view(),
        name='login'
    ),

    path(
        'register/',
        RegisterView.as_view(),
        name='register'
    ),

    path(
        'logout/',
        LogoutView.as_view(
            next_page='/login/'
        ),
        name='logout'
    ),
]
