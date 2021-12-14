from ninja import Schema
from ninja.orm import create_schema
from ninja.params import Param
from . import models

TelegramChat = create_schema(models.TelegramChat)


class TelegramChatPatch(Schema):
    username: str = None
    tg_firstname: str = None
    tg_lastname: str = None
    dialog_id: int = None
    consulate_id: int = None


class TelegramChatPost(TelegramChatPatch):
    chat_id: int


class BotConfig(Schema):
    """Схема изменения любого параметра пользователя"""
    param: str = Param(default=None, description='парамметр')
    value: str = Param(default=None, description='значение')


class Message(Schema):
    """Сообщение"""
    detail: str
