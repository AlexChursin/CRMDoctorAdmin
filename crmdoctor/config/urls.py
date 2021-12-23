from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from app.views import tg_router, config_router, util_router

admin.site.site_header = 'Doccrm Админ панель пациента'
admin.site.index_title = 'Doccrm конфиг бота и данные о пациенте'
admin.site.site_title = 'Doccrm Админ панель пациента'

api = NinjaAPI(title='API MESSENGER', description='Сервис интеграции мессенжеров CRM-DOC с основным бекендом', docs_url='/swagger')
api.add_router('/api', tg_router, tags=['Telegram'])
api.add_router('/api', config_router, tags=['Text config'])
api.add_router('/api', util_router, tags=['Utils'])

urlpatterns = [
    path('bot/', api.urls),
    path('bot/admin/', admin.site.urls),
]
