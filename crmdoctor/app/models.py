from django.db import models


class Consulate(models.Model):
    user_id = models.IntegerField('id пользователя в телеграмме')
    chat_id = models.IntegerField('id чата в телеграмме', null=True, blank=True)
    reason_petition = models.CharField('Причина обращения', max_length=20, null=True, blank=True)
    select_day = models.CharField('Выбранный день', max_length=20, null=True, blank=True)
    select_time = models.CharField('Выбранное время', max_length=20, null=True, blank=True)
    select_schedule_id = models.CharField('Выбранный id даты', max_length=20, null=True, blank=True)
    select_is_emergency = models.BooleanField('Выбрана срочная консультация', default=False)
    dialog_id = models.IntegerField('id диалога', null=True, blank=True)
    cons_token = models.CharField('токен консультации', max_length=120, null=True, blank=True)

    created = models.DateTimeField('создано', auto_now=True)
    updated = models.DateTimeField('обновлено', auto_now_add=True)

    def __str__(self):
        return f'{self.reason_petition}'

    class Meta:
        verbose_name = 'консультация'
        verbose_name_plural = 'консультации'


class TelegramUser(models.Model):
    user_id = models.IntegerField('id пользователя в телеграмме', unique=True, primary_key=True)
    chat_id = models.IntegerField('id чата в телеграмме')
    status = models.IntegerField('статус', default=1)
    age = models.IntegerField('Возраст', null=True, blank=True)
    phone = models.CharField('Телефон', max_length=20, null=True, blank=True)
    consulate = models.ForeignKey(Consulate, models.CASCADE, verbose_name='текущая консультация', null=True, blank=True)
    first_middle_name = models.CharField('Имя Отчество', max_length=100, null=True, blank=True)
    doctor_name = models.CharField('имя доктора', max_length=120, null=True, blank=True)
    doctor_name_p = models.CharField('имя доктора в падеже', max_length=120, null=True, blank=True)
    doctor_token = models.CharField('токен доктора', max_length=120, null=True, blank=True)
    client_token = models.CharField('токен пациента', max_length=120, null=True, blank=True)

    created = models.DateTimeField('создано', auto_now=True)
    updated = models.DateTimeField('обновлено', auto_now_add=True)

    class Meta:
        db_table = "telegram_users"
        verbose_name = 'телеграмм пользователь'
        verbose_name_plural = 'телеграмм пользователи'


class BotTextConfig(models.Model):
    param = models.CharField('парамметр', max_length=30)
    value = models.CharField('значение', max_length=500)
    type = models.IntegerField('тип', choices=[(1, 'Текст'), (2, 'Кнопка')], null=True)

    class Meta:
        db_table = "bot_text_config"
        verbose_name = 'текстовый конфиг'
        verbose_name_plural = 'текстовые конфиги'
