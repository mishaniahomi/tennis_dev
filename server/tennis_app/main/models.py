# -*- coding: utf-8 -*- 
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
from django.urls import reverse
import datetime as dt


class CodeEmail(models.Model):
    code = models.TextField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return "{} {}".format(self.email, self.code)

    class Meta:
        verbose_name = 'код активации через почту'
        verbose_name_plural = 'коды активации через почту'


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    surname = models.CharField(max_length=32, verbose_name='Фамилия')
    name = models.CharField(max_length=16, verbose_name='Имя')
    patronymic = models.CharField(max_length=32, verbose_name='Отчество')
    data_or_birthday = models.DateField(verbose_name='Дата Рождения')
    phone_number = models.CharField(max_length=45, verbose_name='Номер телефона')
    email = models.EmailField(verbose_name='e-mail')
    sex = models.CharField(max_length=7, choices=[('мужской', 'мужской'), ('женский', 'женский')], verbose_name='Пол')

    def __str__(self):
        return "{} {} {}".format(self.surname, self.name, self.patronymic)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Table(models.Model):
    price = models.DecimalField(verbose_name='Цена', max_digits=10, decimal_places=2)
    describe = models.TextField(verbose_name='Описание', blank=True)

    def __str__(self):
        return "Стол № {} ({} рублей)".format(self.pk, self.price)

    class Meta:
        verbose_name = 'Стол'
        verbose_name_plural = 'Столы'

class Servise(models.Model):
    serviseName = models.CharField(max_length=32, verbose_name='НазваниеУслуги')
    image = models.ImageField(null=True, verbose_name='ФотоУслуги')
    describe = models.CharField(max_length=45, verbose_name='ОписаниеУслуги')

class Trener(models.Model):
    surname = models.CharField(max_length=32, verbose_name='Фамилия')
    name = models.CharField(max_length=16, verbose_name='Имя')
    patronymic = models.CharField(max_length=32, verbose_name='Отчество')
    phone_number = models.CharField(max_length=45, verbose_name='Номер телефона')
    email = models.EmailField(verbose_name='e-mail')
    image = models.ImageField(null=True, verbose_name='Фото')
    price = models.DecimalField(verbose_name='Стоимость занятия (руб/час)', max_digits=10, decimal_places=2)
    sports_rank = models.CharField(verbose_name='Спортивныйр азряд', max_length=32, default=" ", blank=True, null=True)
    education = models.TextField(verbose_name='Образование', default=" ", blank=True, null=True)
    peculiarities = models.CharField(verbose_name='Особенности', max_length=32, default=" ", blank=True, null=True)
    is_active = models.BooleanField(verbose_name='Можно ли забронировать', default=True)

    class Meta:
        verbose_name = 'Тренера'
        verbose_name_plural = 'Тренер'
        ordering = ['surname']

    def __str__(self):
        return "{} {} {}".format(self.surname, self.name, self.patronymic)


class Order(models.Model):
    date = models.DateField(verbose_name='Дата заказа')
    time = models.TimeField(verbose_name='Время заказа')
    duration = models.TimeField(verbose_name='Продолжительность', choices=[(dt.time(hour=x//2, minute=(x%2)*30), '{:02d}:{:02d}'.format(x//2, (x%2)*30)) for x in range(2, 5)])
    tableID = models.ForeignKey(Table, on_delete=models.CASCADE, verbose_name='Стол')
    customerID = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Заказчик')
    price = models.DecimalField(verbose_name='Цена', max_digits=10, decimal_places=2)
    trenerID = models.ForeignKey(Trener, on_delete=models.CASCADE, verbose_name='Тренер', blank=True, null=True)
    endtime = models.TimeField(verbose_name='Время окончания', blank=True, null=True)


    def save(self, *args, **kwargs):
        try:
            self.endtime = timedelta(hours=
                      datetime.strptime(self.duration.__str__(), "%H:%M:%S").time().hour +
                      datetime.strptime(self.time.__str__(), "%H:%M").time().hour,
                      minutes=
                      datetime.strptime(self.duration.__str__(), "%H:%M:%S").time().minute +
                      datetime.strptime(self.time.__str__(), "%H:%M").time().minute).__str__()
        except:
            pass
        super(Order, self).save(*args, **kwargs)

    def is_active(self):
        if self.date >= timezone.now().date():
            return True
        return False

    def delete(self, *args, **kwargs):
        order = Order.objects.get(pk=self.pk)
        if order.date >= timezone.now().date():
            super(Order, self).delete(*args, **kwargs)


    def get_hours_and_minutes(self):
        my_time_obj = datetime.strptime(str(self.duration), "%H:%M:%S").time()
        hours = my_time_obj.hour
        minutes = my_time_obj.minute
        return hours, minutes

    def __str__(self):
        return "Заказ на {} в {} на имя {}".format(self.date, self.time, self.customerID)

    class Meta:
        verbose_name = 'Бронирование стола'
        verbose_name_plural = 'Бронирование стола'


class Competition(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название соревнований')
    describe = models.TextField(verbose_name='Описание', blank=True)
    data = models.DateField(verbose_name='Дата соревнований', default=timezone.now)
    price = models.DecimalField(verbose_name='Цена', max_digits=10, decimal_places=2)

    def __str__(self):
        return "{}-{}-{}".format(self.title, self.data, self.price)

    class Meta:
        verbose_name = 'Соревнование'
        verbose_name_plural = 'Соревнования'
        ordering = ['data']

    def get_absolute_url(self):
        return reverse('home_detail', kwargs={'wargost_id': self.pk})

    def is_active(self):
        if self.data >= timezone.now().date():

            return True
        return False

class RegistrationCompetition(models.Model):
    customerID = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Участник')
    competitionID = models.ForeignKey(Competition, on_delete=models.CASCADE, verbose_name='Соревнования')
    data = models.DateField(verbose_name='Время записи', default=timezone.now)
    price = models.DecimalField(verbose_name='Цена', max_digits=10, decimal_places=2)
    rating = models.IntegerField(verbose_name='Рейтинг', default=0)

    def __str__(self):
        return "{}-{}".format(self.customerID, self.competitionID)

    class Meta:
        verbose_name = 'Запись на соревнование'
        verbose_name_plural = 'Записи на соревнования'


class Photo(models.Model):
    file = models.ImageField(verbose_name='Фотография')
    date = models.DateTimeField(verbose_name='Дата фотографии', default=timezone.now)

    class Meta:
        verbose_name = 'Фотографию'
        verbose_name_plural = 'Фотографии'
        ordering = ['date']


class KindPriceListElement(models.Model):
    name = models.CharField(verbose_name='Название типа элемента прайс-листа', max_length=32)
    is_active = models.BooleanField(verbose_name='Активен', default=False)

    def __str__(self):
        return "{}-{}".format(self.name, self.is_active)

    class Meta:
        verbose_name = 'тип элементов прайс-листа'
        verbose_name_plural = 'типы элементов прайс-листа'


class PriceList(models.Model):
    item_type = models.ForeignKey(KindPriceListElement, verbose_name='Тип элемента прайс-листа', on_delete=models.CASCADE)
    item_name = models.CharField(verbose_name='Название элемента', max_length=255)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    price = models.DecimalField(verbose_name='Цена', max_digits=10, decimal_places=2)
    duration = models.DurationField(verbose_name='Продолжительность')
    is_active = models.BooleanField(verbose_name='Активен', default=False)

    def __str__(self):
        return "{}-{}-{}".format(self.item_type, self.item_name, self.description)
    class Meta:
        verbose_name = 'Элемент'
        verbose_name_plural = 'Прайс-лист'


class CustomAbon(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, verbose_name='Клиент')
    abonement = models.ForeignKey('Abonement', on_delete=models.CASCADE, verbose_name='Вид абонемента')
    data_begin = models.DateField(verbose_name='Дата активации абонемента', default=timezone.now)
    duration = models.IntegerField(verbose_name='на сколько дней', default=30)
    data_end = models.DateField(verbose_name='Дата оканчания абонемента', null=True, blank=True)

    def is_active(self):
        if self.data_begin <= timezone.now().date() and self.data_end >= timezone.now().date():
            return True
        return False

    def save(self, *args, **kwargs):
        try:
            self.data_end = self.data_begin + timedelta(days=self.duration)
        except:
            pass
        super(AbonementСustomer, self).save(*args, **kwargs)


class Abonement(models.Model):
    time_limit = models.TimeField(verbose_name='Время ограничения', null=True, blank=True)
    competition_limit = models.CharField(max_length=50, verbose_name="Ограничения по турнирам", choices=[('все', 'все'), ('Только детям и женщинам', 'Только детям и женщинам')])

    