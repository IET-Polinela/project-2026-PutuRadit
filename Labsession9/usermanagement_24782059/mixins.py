from django.contrib import messages
from django.shortcuts import redirect

class AdminOnlyMixin:
    def dispatch(self, request, *args, **kwargs):

        # belum login
        if not request.user.is_authenticated:
            messages.error(request, "Silakan login dulu!")
            return redirect('login')

        # bukan admin & bukan superuser
        if not (request.user.is_admin or request.user.is_superuser):
            messages.error(request, "Akses ditolak! Hanya admin yang boleh mengakses fitur ini.")
            return redirect('report_list')

        return super().dispatch(request, *args, **kwargs)
