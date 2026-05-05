from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView

from usermanagement_24782059.views import LoginView, RegisterView

urlpatterns = [
    # =========================
    # ADMIN
    # =========================
    path('admin/', admin.site.urls),

    # =========================
    # APPS
    # =========================
    path('', include('main_app.urls')),
    path('about/', include('about.urls')),
    path('contacts/', include('contacts.urls')),
    path('reports/', include('reports.urls')),

    # =========================
    # AUTH (CUSTOM CBV KAMU)
    # =========================
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),

    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),

    # =========================
    # USER MANAGEMENT (opsional kalau ada page lain)
    # =========================
    path('user/', include('usermanagement_24782059.urls')),
]
