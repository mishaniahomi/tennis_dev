# -*- coding: utf-8 -*- 
from django.contrib import admin

from .models import Servise, Customer, Table, Trener, Order, Competition, RegistrationCompetition, CodeEmail, PriceList, KindPriceListElement, Photo, Abonement, CustomAbon
from django_admin_filters import DateRangePicker


class MyDateRangePicker(DateRangePicker):
    FILTER_LABEL = "Интервал данных"
    FROM_LABEL = "От"
    TO_LABEL = "До"
    ALL_LABEL = 'Все'
    CUSTOM_LABEL = "пользовательский"
    NULL_LABEL = "без даты"
    BUTTON_LABEL = "Задать интервал"
    DATE_FORMAT = "YYYY-MM-DD HH:mm"

    is_null_option = True

    options = (
        ('1da', "24 часа вперед", 60 * 60 * 24),
        ('1dp', "последние 24 часа", 60 * 60 * -24),
    )
    WIDGET_LOCALE = 'ru'
    WIDGET_BUTTON_LABEL = "Выбрать"
    WIDGET_WITH_TIME = True

    WIDGET_START_TITLE = 'Начальная дата'
    WIDGET_START_TOP = -350
    WIDGET_START_LEFT = -400

    WIDGET_END_TITLE = 'Конечная дата'
    WIDGET_END_TOP = -350
    WIDGET_END_LEFT = -400

@admin.register(Servise)
class ServiseAdmin(admin.ModelAdmin):
    list_display = ("serviseName", "image", "describe")
    list_filter = ("serviseName", "image", "describe")

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("date", "time", "endtime", "duration", "tableID", "customerID", "price", "trenerID")
    list_filter = ("date", "time", "endtime", "duration", "tableID", "customerID", "price", "trenerID")
    list_filter = (('date', MyDateRangePicker), ('endtime', MyDateRangePicker))

@admin.register(CodeEmail)
class CodeEmailAdmin(admin.ModelAdmin):
    list_display = ("code", "email")
    list_filter = ("code", "email")


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("user", "surname", "name", "patronymic", "data_or_birthday", "phone_number", "email", "sex")
    list_filter = ("user", "surname", "name", "patronymic", "data_or_birthday", "phone_number", "email", "sex")


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ("__str__", "price", "describe")
    list_filter = ("price", "describe")


@admin.register(Trener)
class TrenerAdmin(admin.ModelAdmin):
    list_display = ("surname", "name", "patronymic", "phone_number", "email", "image", "price", "sports_rank", "education", "peculiarities", "is_active")
    list_filter = ("surname", "name", "patronymic", "phone_number", "email", "image", "price", "sports_rank", "education", "peculiarities", "is_active")


@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ("title", "describe", "data", "price")
    list_filter = ("title", "describe", "data", "price")


@admin.register(RegistrationCompetition)
class RegistrationCompetitionAdmin(admin.ModelAdmin):
    list_display = ("customerID", "competitionID", "data", "price", "rating")
    list_filter = ("customerID", "competitionID", "data", "price", "rating")


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ("file", "date")
    list_filter = ("file", "date")


@admin.register(KindPriceListElement)
class KindPriceListElementAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    list_filter = ("name", "is_active")


@admin.register(CustomAbon)
class KindPriceListElementAdmin(admin.ModelAdmin):
    list_display = ("customer", "abonement", "data_begin", "duration", "data_end")
    list_filter = ("customer", "abonement", "data_begin", "duration", "data_end")


@admin.register(Abonement)
class KindPriceListElementAdmin(admin.ModelAdmin):
    list_display = ("time_limit", "competition_limit")
    list_filter = ("time_limit", "competition_limit")


@admin.register(PriceList)
class PriceListdmin(admin.ModelAdmin):
    list_display = ("item_type", "item_name", "description", "price", "duration", "is_active")
    list_filter = ("item_type", "item_name", "description", "price", "duration", "is_active")
