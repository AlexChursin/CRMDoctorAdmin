from datetime import datetime
from typing import Optional

from ninja import Schema, ModelSchema
from ninja.orm import create_schema
from ninja.params import Param


class ConsulatePost(Schema):
    user_id: int
    reason_petition: Optional[str] = None
    select_day: Optional[str] = None
    select_time: Optional[str] = None
    select_schedule_id: Optional[str] = None
    select_is_emergency: bool = None
    dialog_id: Optional[int] = None
    cons_token: Optional[str] = None


class TelegramUserPut(Schema):
    status: int = 1
    age: Optional[int] = None
    phone: Optional[str] = None
    doctor_token: str = None
    doctor_name: str = None
    doctor_name_p: str = None
    client_token: Optional[str] = None
    first_middle_name: Optional[str] = None
    consulate: Optional[ConsulatePost] = None
    consulate_id: Optional[int] = None


class TelegramUserPost(TelegramUserPut):
    user_id: int
    chat_id: int


class TelegramUser(TelegramUserPut):
    created: datetime
    updated: datetime


class BotConfig(Schema):
    """Схема изменения любого параметра пользователя"""
    param: str = Param(default=None, description='парамметр')
    value: str = Param(default=None, description='значение')


class Message(Schema):
    """Сообщение"""
    detail: str
