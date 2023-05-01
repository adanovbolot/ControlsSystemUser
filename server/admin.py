from django.contrib import admin
from .models import (User, Position, Profile, Divisions, UserAccess, UserSession, ServerSettings, SessionTimeout)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ['id', 'position']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'profile']


@admin.register(Divisions)
class DivisionsAdmin(admin.ModelAdmin):
    list_display = ['id', 'divisions']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'surname', 'profile', 'divisions', 'position']


@admin.register(UserAccess)
class UserAccessAdmin(admin.ModelAdmin):
    pass


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    pass


@admin.register(ServerSettings)
class ServerSettingsAdmin(admin.ModelAdmin):
    pass


@admin.register(SessionTimeout)
class SessionTimeoutAdmin(admin.ModelAdmin):
    pass