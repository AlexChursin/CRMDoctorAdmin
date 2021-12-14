from django.contrib import admin
from .models import *


@admin.register(TelegramChat)
class TelegramChatAdmin(admin.ModelAdmin):
    search_fields = ("chat_id", 'username', 'tg_firstname', 'tg_lastname', 'dialog_id', 'consulate_id')
    list_display = ("chat_id", 'username', 'tg_firstname', 'tg_lastname', 'dialog_id', 'consulate_id', 'created', 'updated')


@admin.register(BotTextConfig)
class BotTextConfigAdmin(admin.ModelAdmin):
    search_fields = ("param", 'value')
    list_display = ("param", 'value')
