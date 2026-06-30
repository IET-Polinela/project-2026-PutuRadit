from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect

from usermanagement_24782059.views import (
    LoginView,
    RegisterView,
)

# JWT
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# OPENAPI DOCUMENTATION
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from django_scalar.views import scalar_viewer


def redirect_to_real_dashboard(request):
    return redirect('/reports/dashboard/')


urlpatterns = [

    # =========================
    # ADMIN
    # =========================
    path(
        'admin/',
        admin.site.urls
    ),

    # =========================
    # DASHBOARD ALIAS FOR LAB 15 PLAYWRIGHT
    # =========================
    path(
        'dashboard/',
        redirect_to_real_dashboard,
        name='dashboard'
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
    # OPENAPI DOCUMENTATION
    # =========================
    path(
        'api/schema/',
        SpectacularAPIView.as_view(),
        name='schema'
    ),

    path(
        'api/docs/swagger/',
        SpectacularSwaggerView.as_view(
            url_name='schema'
        ),
        name='swagger-ui'
    ),

    path(
        'api/docs/scalar/',
        scalar_viewer,
        name='scalar-ui'
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