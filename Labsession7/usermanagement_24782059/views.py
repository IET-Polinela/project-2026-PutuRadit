from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.db import IntegrityError

from .forms import RegisterForm
from reports.models import Report


# =========================================
# REGISTER VIEW
# =========================================
class RegisterView(View):

    def get(self, request):

        if request.user.is_authenticated:
            return redirect('report_list')

        form = RegisterForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):

        if request.user.is_authenticated:
            logout(request)

        form = RegisterForm(request.POST)

        if form.is_valid():

            try:
                user = form.save(commit=False)

                user.is_admin = False
                user.is_member = True

                user.save()

                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')

                user = authenticate(
                    request,
                    username=username,
                    password=password
                )

                if user:
                    login(request, user)
                    messages.success(request, "Register berhasil!")
                    return redirect('report_list')

                messages.error(request, "Auto login gagal!")
                return redirect('login')

            except IntegrityError:
                messages.error(request, "Username sudah dipakai!")
                return render(request, 'register.html', {'form': form})

        messages.error(request, "Register gagal!")
        return render(request, 'register.html', {'form': form})


# =========================================
# LOGIN VIEW
# =========================================
class LoginView(View):

    def get(self, request):

        if request.user.is_authenticated:
            return redirect('report_list')

        return render(request, 'login.html')

    def post(self, request):

        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not password:
            messages.error(request, "Isi username & password!")
            return render(request, 'login.html')

        if request.user.is_authenticated:
            logout(request)

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, f"Halo {user.username}!")
            return redirect('report_list')

        messages.error(request, "Login gagal!")
        return render(request, 'login.html')


# =========================================
# LOGOUT VIEW
# =========================================
class LogoutView(View):

    def get(self, request):

        logout(request)
        messages.success(request, "Berhasil logout!")
        return redirect('login')


# =========================================
# REPORT LIST
# =========================================
def report_list(request):

    reports = Report.objects.all().order_by('-id')

    return render(request, 'report_list.html', {
        'reports': reports
    })
