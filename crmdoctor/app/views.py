import logging
from http import HTTPStatus
from typing import List, Optional

from django.db import IntegrityError
from django.shortcuts import get_object_or_404, get_list_or_404
from pytrovich.detector import PetrovichGenderDetector
from pytrovich.enums import NamePart, Gender, Case
from pytrovich.maker import PetrovichDeclinationMaker, Gender
from ninja import Router, Query

from . import models
from . import schemas
from .util_schemas import MyGender, Padej, Petrovich

tg_router = Router()
config_router = Router()
util_router = Router()


@tg_router.post("/client", response={HTTPStatus.CREATED: schemas.TelegramUser, HTTPStatus.CONFLICT: schemas.Message})
def create_client(request, client: schemas.TelegramUserPost):
    try:
        client_db = models.TelegramUser.objects.create(**client.dict())
    except Exception as e:
        logging.warning(e)
        return HTTPStatus.CONFLICT, schemas.Message(detail=f'user_id = {client.user_id} already exist')
    return HTTPStatus.CREATED, client_db


@tg_router.post("/client/{user_id}/consulate", response={HTTPStatus.CREATED: schemas.TelegramUser,
                                                         HTTPStatus.NOT_FOUND: schemas.Message})
def create_consulate(request, user_id: int, consulate: schemas.ConsulatePost):
    client_db = get_object_or_404(models.TelegramUser, pk=user_id)
    consulate_db = models.Consulate.objects.create(**consulate.dict())
    client_db.consulate_id = consulate_db.pk
    client_db.save()
    return HTTPStatus.CREATED, client_db


@tg_router.put("/client/{user_id}", response={HTTPStatus.OK: schemas.TelegramUser})
def put_client(request, user_id: int, client: schemas.TelegramUserPut):
    client_db = get_object_or_404(models.TelegramUser, pk=user_id)
    for attr, value in client.dict().items():
        if attr == 'consulate_id':
            continue
        if attr != 'consulate':
            setattr(client_db, attr, value)
        else:
            if client.consulate is not None:
                consulate = schemas.ConsulatePost(**client.consulate.dict())
                if client_db.consulate is not None:
                    for a, v in consulate.dict().items():
                        setattr(client_db.consulate, a, v)
                    client_db.consulate.save()
            else:
                client_db.consulate = None

    client_db.save()
    return HTTPStatus.OK, client_db


@tg_router.get("/client/{user_id}", response={HTTPStatus.OK: schemas.TelegramUser,
                                              HTTPStatus.NOT_FOUND: schemas.Message})
def get_client(request, user_id: int):
    chat_db = get_object_or_404(models.TelegramUser, pk=user_id)
    return HTTPStatus.OK, chat_db


@tg_router.get("/consulate/dialog/{dialog_id}", response={HTTPStatus.OK: schemas.ConsulatePost,
                                                          HTTPStatus.NOT_FOUND: schemas.Message,
                                                          HTTPStatus.NO_CONTENT: schemas.Message})
def get_consulate(request, dialog_id: int):
    consulate_db = get_list_or_404(models.Consulate, dialog_id=dialog_id)[-1]
  #  chat_db = get_object_or_404(models.TelegramUser, pk=consulate_db.user_id)

    if consulate_db.dialog_id is not None:
        return HTTPStatus.OK, consulate_db
    return HTTPStatus.NO_CONTENT, schemas.Message(detail='client dialog_id empty')


@config_router.get("/text_config", response={HTTPStatus.OK: schemas.TextConfig})
def get_text_config(request):
    buttons = models.BotTextConfig.objects.filter(type=2).all()
    texts = models.BotTextConfig.objects.filter(type=1).all()
    buttons = [schemas.BotConfig.from_orm(b) for b in buttons]
    texts = [schemas.BotConfig.from_orm(t) for t in texts]
    return HTTPStatus.OK, schemas.TextConfig(texts=texts, buttons=buttons)


maker = PetrovichDeclinationMaker()
detector = PetrovichGenderDetector()


@util_router.get("/utils/petrovich", response={HTTPStatus.OK: Petrovich})
async def utils(
        request,
        first_name: str = 'Елена',
        middle_name: str = 'Владимировна',
        last_name: str = 'Сидорова',
        case: Padej = Padej.GENITIVE,
        gender: Optional[MyGender] = MyGender.MALE
):
    p_case = [Case(i) for i, p in enumerate(Padej) if case.name == p.name][0]
    gender = detector.detect(firstname=first_name, middlename=first_name)
    f = maker.make(NamePart.FIRSTNAME, gender, p_case, original_name=first_name)
    m = maker.make(NamePart.MIDDLENAME, gender, p_case, middle_name)
    l = maker.make(NamePart.LASTNAME, gender, p_case, last_name)
    return Petrovich(first_name=f, middle_name=m, last_name=l)
