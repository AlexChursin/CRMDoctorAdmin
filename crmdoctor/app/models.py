from datetime import datetime

from django.db import models


class TelegramChat(models.Model):
    chat_id: int = models.IntegerField('id пользователя в телеграмме', unique=True, primary_key=True)
    username = models.CharField('пользователь в телеграмм', max_length=100, null=True, blank=True)
    tg_firstname = models.CharField('имя в телеграмм', max_length=100, null=True, blank=True)
    tg_lastname = models.CharField('фамилия в телеграмм', max_length=100, null=True, blank=True)
    dialog_id: int = models.IntegerField('id диалога', null=True, blank=True)
    consulate_id: int = models.IntegerField('id консультации', null=True, blank=True)
    created: datetime = models.DateTimeField('создано', auto_now=True)
    updated: datetime = models.DateTimeField('обновлено', auto_now_add=True)

    class Meta:
        db_table = "telegram_users"


class BotTextConfig(models.Model):
    param = models.CharField('парамметр', max_length=30)
    value = models.CharField('значение', max_length=500)

    class Meta:
        db_table = "bot_text_config"
