from django.contrib import admin
from .models import CustomUser

<<<<<<< HEAD
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
=======

# =========================
# ACTIONS
# =========================

@admin.action(description="Set selected users as MEMBER")
def make_member(modeladmin, request, queryset):
    queryset.update(is_member=True, is_admin=False, is_staff=False)


@admin.action(description="Set selected users as ADMIN")
def make_admin(modeladmin, request, queryset):
    queryset.update(is_admin=True, is_member=False, is_staff=True)


@admin.action(description="Reset role (USER biasa)")
def reset_role(modeladmin, request, queryset):
    queryset.update(is_admin=False, is_member=False, is_staff=False, is_superuser=False)


@admin.action(description="Activate selected users")
def activate_users(modeladmin, request, queryset):
    queryset.update(is_active=True)


@admin.action(description="Deactivate selected users")
def deactivate_users(modeladmin, request, queryset):
    queryset.update(is_active=False)


# =========================
# ADMIN CLASS
# =========================

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):

>>>>>>> bf6ccbf (Menambahkan sistem status laporan (VERIFIED, IN_PROGRESS, RESOLVED), aksi admin, dan pengelolaan status langsung dari halaman reports.)
    list_display = (
        'username',
        'email',
        'is_admin',
        'is_member',
        'is_staff',
<<<<<<< HEAD
        'is_superuser'
=======
        'is_superuser',
        'is_active'
    )

    list_filter = (
        'is_admin',
        'is_member',
        'is_staff',
        'is_active'
    )

    search_fields = (
        'username',
        'email'
    )

    actions = (
        make_member,
        make_admin,
        reset_role,
        activate_users,
        deactivate_users
>>>>>>> bf6ccbf (Menambahkan sistem status laporan (VERIFIED, IN_PROGRESS, RESOLVED), aksi admin, dan pengelolaan status langsung dari halaman reports.)
    )
