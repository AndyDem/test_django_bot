from django.contrib import admin
from .models import UserProfile, Game


@admin.register(UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'tg_username', 'tg_id')

@admin.register(Game)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title',)
