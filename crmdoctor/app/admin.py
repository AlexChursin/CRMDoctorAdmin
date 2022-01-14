from django.contrib import admin
from .models import *


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    search_fields = ("user_id", 'chat_id', 'doctor_token', 'cons_token',)
    list_filter = ('status',)
    list_display = ("user_id", 'consulate', 'chat_id', 'status', 'age', 'phone', 'first_middle_name',  'created', 'updated')

    # add action
    actions = ['make_copy', 'custom_button']

    def custom_button(self, request, queryset):
        pass

    # display text，Consistent with django admin
    custom_button.short_description = 'Test Button'
    # icon，reference：element-ui icon and https://fontawesome.com
    custom_button.icon = 'fas fa-audio-description'

    # Specify button type：https://element.eleme.cn/#/zh-CN/component/button
    custom_button.type = 'danger'

    # Custom style
    custom_button.style = 'color:black;'

    def make_copy(self, request, queryset):
        pass

    make_copy.short_description = 'Copy employe'

@admin.register(Consulate)
class TelegramConsulateAdmin(admin.ModelAdmin):
    search_fields = ("user_id", 'chat_id', 'reason_petition')
    list_filter = ('select_is_emergency',)
    list_display = ("user_id", 'select_day', 'select_time', 'dialog_id',
                    'reason_petition', 'select_is_emergency', 'cons_token',
                    'created', 'updated')


@admin.register(BotTextConfig)
class BotTextConfigAdmin(admin.ModelAdmin):
    search_fields = ("param", 'value')
    list_display = ("param", 'value', 'type')
    list_filter = ('type',)
