from django.contrib import admin
from .models import *


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    search_fields = ("user_id", 'chat_id', 'doctor_token', 'cons_token',)
    list_filter = ('status',)
    list_display = ("user_id", 'chat_id', 'status', 'age', 'phone', 'first_middle_name',  'created', 'updated')


@admin.register(Consulate)
class TelegramConsulateAdmin(admin.ModelAdmin):
    search_fields = ("user_id", 'chat_id', 'doctor_token', 'cons_token',)
    list_filter = ('select_is_emergency',)
    list_display = ("user_id", 'select_day', 'select_time', 'dialog_id',
                    'reason_petition', 'select_is_emergency', 'cons_token',
                    'created', 'updated')


@admin.register(BotTextConfig)
class BotTextConfigAdmin(admin.ModelAdmin):
    search_fields = ("param", 'value')
    list_display = ("param", 'value')
