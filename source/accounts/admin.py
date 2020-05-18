
from accounts.models import Token
from django.contrib import admin
from accounts.models import User, Profile
from django.contrib.auth.admin import UserAdmin


class ProfileInline(admin.StackedInline):
    model = Profile
    exclude = []


class ProfileAdmin(UserAdmin):
    inlines = [ProfileInline]


admin.site.unregister(User)
admin.site.register(User, ProfileAdmin)
admin.site.register(Profile)

admin.site.register(Token)

# Register your models here.