from http import HTTPStatus
from typing import List

from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from pytrovich.enums import NamePart, Gender, Case
from pytrovich.maker import PetrovichDeclinationMaker
from ninja import Router, Query

from . import models
from . import schemas
from .util_schemas import MyGender, Padej, Petrovich

tg_router = Router()
config_router = Router()
util_router = Router()


@tg_router.post("/chat", response={HTTPStatus.CREATED: schemas.TelegramChat, HTTPStatus.CONFLICT: schemas.Message})
def create_chat(request, chat: schemas.TelegramChatPost):
    try:
        chat = models.TelegramChat.objects.create(**chat.dict())
    except IntegrityError:
        return HTTPStatus.CONFLICT, schemas.Message(detail=f'chat_id = {chat.chat_id} already exist')
    return HTTPStatus.CREATED, chat


@tg_router.get("/chat/{pk}", response={HTTPStatus.OK: schemas.TelegramChat})
def get_chat(request, pk: int):
    chat_db = get_object_or_404(models.TelegramChat, pk=pk)
    return HTTPStatus.OK, chat_db


@tg_router.patch("/chat/{pk}", response={HTTPStatus.OK: schemas.TelegramChat})
def patch_chat(request, pk: int, chat: schemas.TelegramChatPatch):
    chat_db = get_object_or_404(models.TelegramChat, pk=pk)
    for k, v in chat.dict(exclude_none=True).items():
        setattr(chat_db, k, v)
    chat_db.save()
    return HTTPStatus.OK, chat_db


@tg_router.get("/chats", response={HTTPStatus.OK: List[schemas.TelegramChat]})
def get_chats(request, filter: schemas.TelegramChatPatch = Query(...)):
    chat = models.TelegramChat.objects.filter(**filter.dict(exclude_none=True)).all()
    return HTTPStatus.OK, chat


@config_router.get("/config/text", response={HTTPStatus.OK: List[schemas.BotConfig]})
def get_text_config(request):
    return HTTPStatus.OK, models.BotTextConfig.objects.all()


maker = PetrovichDeclinationMaker()


@util_router.get("/utils/petrovich", response={HTTPStatus.OK: Petrovich})
async def utils(
        request,
        first_name: str = 'Елена',
        middle_name: str = 'Владимировна',
        last_name: str = 'Сидорова',
        case: Padej = Padej.GENITIVE,
        gender: MyGender = MyGender.FEMALE
):
    p_case = [Case(i) for i, p in enumerate(Padej) if case.name == p.name][0]
    p_gender = [Gender(i) for i, p in enumerate(MyGender) if gender.name == p.name][0]

    f = maker.make(NamePart.FIRSTNAME, p_gender, p_case, original_name=first_name)
    m = maker.make(NamePart.MIDDLENAME, p_gender, p_case, middle_name)
    l = maker.make(NamePart.LASTNAME, p_gender, p_case, last_name)
    return Petrovich(first_name=f, middle_name=m, last_name=l)
