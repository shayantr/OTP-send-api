from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from user.models import User, OTPRequest


# Register your models here.


@admin.register(User)
class AppUserAdmin(UserAdmin):
    pass

admin.site.register(OTPRequest)