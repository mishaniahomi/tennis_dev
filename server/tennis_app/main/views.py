# -*- coding: utf-8 -*- 
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import secrets
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, DeleteView
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime, timedelta
from django.contrib.auth.views import LogoutView
from rest_framework import viewsets
from decimal import Decimal
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.hashers import make_password

from tennis.settings import EMAIL_HOST_USER
import main
from .models import Servise, Trener, Customer, CodeEmail, Table, Order, Competition, RegistrationCompetition, KindPriceListElement, CustomAbon
from .forms import CustomerRegistrtionForm, OrderForm, RegistrationCompetitionForm
from .serializers import TableSerializer, OrderSerializer
from .tasks import send_email_task, send_code_email_task

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        date = self.request.GET.getlist('date')[0]
        table = self.request.GET.getlist('tableID')[0]
        return Order.objects.filter(date=date, tableID=table).order_by('time')


class OrderDeleteView(DeleteView):
    model = Order
    success_url = '/privateOffice'
    template_name = 'main/OrderDeleteView.html'
    context_object_name = 'order'


class RegistrationCompetitionDeleteView(DeleteView):
    model = RegistrationCompetition
    success_url = '/privateOffice'
    template_name = 'main/RegistrationCompetitionDeleteView.html'
    context_object_name = 'reg'


def privateOffice(request):
    if request.user.is_authenticated:
        customer = get_object_or_404(Customer, user=request.user)

        orders = Order.objects.filter(customerID=customer)
        competitions = RegistrationCompetition.objects.filter(customerID=customer)

        tables = Table.objects.all()
        treners = Trener.objects.all()

        comp_name = request.GET.getlist('comp_name')
        comp_date = request.GET.getlist('comp_date')
        comp_price = request.GET.getlist('comp_price')
        if comp_name:
            if request.GET['comp_name'] != '' or request.GET['comp_date'] != '' or request.GET['comp_price'] != '':
                competitions = []
                if len(comp_name) and request.GET['comp_name'] != '':
                    comps = Competition.objects.filter(title=request.GET.getlist('comp_name')[0])
                    for comp in comps:
                        competitions += RegistrationCompetition.objects.select_related('competitionID').filter(competitionID_id=comp.id, customerID=customer)
                if len(comp_date) and request.GET['comp_date'] != '':
                    comps = Competition.objects.filter(data=request.GET.getlist('comp_date')[0])
                    for comp in comps:
                        competitions += RegistrationCompetition.objects.select_related('competitionID').filter(competitionID_id=comp.id, customerID=customer)
                if len(comp_price) and request.GET['comp_price'] != '':
                    comps = Competition.objects.filter(price=Decimal.from_float(float(request.GET.getlist('comp_price')[0])))
                    for comp in comps:
                        competitions += RegistrationCompetition.objects.select_related('competitionID').filter(competitionID_id=comp.id, customerID=customer)
        comp_paginator = Paginator(competitions, 5)
        page_number = request.GET.get("page")
        page_competitions = comp_paginator.get_page(page_number)

        order_date = request.GET.getlist('order_date')
        order_date_max = request.GET.getlist('order_date_max')
        order_time = request.GET.getlist('order_time')
        order_duration = request.GET.getlist('order_duration')
        order_table = request.GET.getlist('order_table')
        order_trener = request.GET.getlist('order_trener')
        order_price = request.GET.getlist('order_price')

        if order_date:
            if request.GET['order_date'] != '' or request.GET['order_time'] != '' or request.GET['order_duration'] != '' \
                    or request.GET['order_table'] != '' or request.GET['order_trener'] != '' or request.GET['order_price'] != '':
                orders = []
                if request.GET['order_date'] != '' and request.GET['order_date_max'] != '' and len(order_date_max) and len(order_date):
                    query = Q(date__gte=order_date[0], date__ltedate__lte=order_date_max[0], customerID=customer)
                    orders += Order.objects.filter(query)
                elif len(order_date) and request.GET['order_date'] != '':
                    orders += Order.objects.filter(date__gte=order_date[0], customerID=customer)
                elif len(order_date_max) and request.GET['order_date_max'] != '':
                    orders += Order.objects.filter(date__lte=order_date_max[0], customerID=customer)
                if len(order_time) and request.GET['order_time'] != '':
                    orders += Order.objects.filter(time=order_time[0], customerID=customer)
                if len(order_duration) and request.GET['order_duration'] != '':
                    orders += Order.objects.filter(duration=order_duration[0], customerID=customer)
                if len(order_table) and request.GET['order_table'] != '':
                    orders += Order.objects.filter(tableID=order_table[0], customerID=customer)
                if len(order_trener) and request.GET['order_trener'] != '':
                    orders += Order.objects.filter(trenerID=order_trener[0], customerID=customer)
                if len(order_price) and request.GET['order_price'] != '':
                    orders += Order.objects.filter(price=order_price[0], customerID=customer)

        context = {'orders': set(orders),  'tables': tables, 'treners': treners, 'page_competitions': page_competitions}
        return render(request, 'main/privateOffice.html', context)
    else:
        return redirect('main_index')


class OrderListApiView(APIView):
    def get(self, request):
        date = self.request.GET.getlist('date')[0]
        time = self.request.GET.getlist('time')[0]
        duration = self.request.GET.getlist('duration')[0]
        if date and time and duration:
            time_begin = timedelta(
                    hours=datetime.strptime(time, "%H:%M:%S").time().hour,
                    minutes=datetime.strptime(time, "%H:%M:%S").time().minute + 1
                ) 
            time_end = timedelta(hours=
                                 datetime.strptime(duration, "%H:%M:%S").time().hour +
                                 datetime.strptime(time, "%H:%M:%S").time().hour,
                                 minutes=
                                 datetime.strptime(duration, "%H:%M:%S").time().minute +
                                 datetime.strptime(time, "%H:%M:%S").time().minute-1)
            if datetime.strptime(time, "%H:%M:%S").time().minute != 59:
                time_begin = timedelta(
                    hours=datetime.strptime(time, "%H:%M:%S").time().hour,
                    minutes=datetime.strptime(time, "%H:%M:%S").time().minute + 1
                ) 
            else:
                time_begin = timedelta(
                    hours=datetime.strptime(time, "%H:%M:%S").time().hour+1,
                    minutes=0
                ) 
            orders = set(Order.objects.filter(date=date).values_list("tableID", "time", "endtime")) \
                     - set(Order.objects.filter(
                date=date, time__gt=time_end.__str__()).values_list("tableID", "time", "endtime")) \
                     - set(Order.objects.filter(
                date=date, endtime__lt=time_begin.__str__()).values_list("tableID", "time", "endtime"))
            close_table = set([i[0] for i in orders])
            all_tables = Table.objects.exclude(pk__in=close_table)
            return Response({'free_tablies': TableSerializer(all_tables, many=True).data})
        else:
            return Response({'free_tablies': []})


class GetPriceApiView(APIView):

    def get(self, request):
        # Если абонемент активный, то вернуть 0 рублей

        customer = get_object_or_404(Customer, user=request.user)
        abonements = CustomAbon.objects.filter(customer=customer, )
        if abonements:
            for abonement in abonements:
                if abonement.is_active():
                    return Response({'price': 'У вас есть абонемент! Поэтому цена 0 рублей'})

        duration = self.request.GET.getlist('duration')[0]
        birth_date = customer.data_or_birthday
        current_date = datetime.now()
        age = current_date.year - birth_date.year
        table = self.request.GET.getlist('table')[0]
        trener = None

        table = get_object_or_404(Table, id=table)
        my_time_obj = datetime.strptime(str(duration), "%H:%M:%S").time()
        hours = my_time_obj.hour
        minuties = my_time_obj.minute
        if customer.sex == 'женский' or age < 18:
            price = hours * Decimal.from_float(250.00) + minuties * Decimal.from_float(250.00) / 60
        else:
            price = hours * table.price + minuties * table.price / 60
        if self.request.GET.getlist('trener'):

            if self.request.GET.getlist('trener') != ['']:
                trener_id = self.request.GET.getlist('trener')[0]
                trener = get_object_or_404(Trener, id=trener_id)
        if trener:
            price = hours * trener.price + minuties * trener.price / 60

        return Response({'price': price})


def CreateRegistrationCompetition(request, pk):
    if request.user.is_authenticated:
        treners = Trener.objects.all()
        forms = OrderForm()
        customer = get_object_or_404(Customer, user=request.user)
        competition = get_object_or_404(Competition, pk=pk)
        try:
            RegistrationCompetition.objects.get(customerID=customer, competitionID=competition)
            return render(request, 'main/index.html',
                          {'Mainmessage': 'Внимание! ', 'alerttype': 'warning', 'form': forms, 'treners': treners,
                           'flag': 1, 'message': 'Вы уже зарегистрировались на соревнование.'})
        except main.models.RegistrationCompetition.MultipleObjectsReturned:
            return render(request, 'main/index.html',
                          {'Mainmessage': 'Внимание! ', 'alerttype': 'warning', 'form': forms, 'treners': treners,
                           'flag': 1, 'message': 'Вы зарегистрировались на это соревнование уже несколько раз'})
        except main.models.RegistrationCompetition.DoesNotExist:
            if request.method == 'POST':
                form = RegistrationCompetitionForm(request.POST)
                if form.is_valid():
                    new_reg_comp = RegistrationCompetition()
                    new_reg_comp.customerID = customer
                    new_reg_comp.competitionID = competition
                    new_reg_comp.price = competition.price
                    new_reg_comp.rating = form.data['rating']
                    new_reg_comp.save()
                return render(request, 'main/index.html',
                              {'Mainmessage': 'Поздравляем! ', 'alerttype': 'success', 'form': forms, 'treners': treners,
                               'flag': 1, 'message': 'Вы успешно зарегистрировались на соревнование.'})
    return redirect('login')


class CompetitionDetailView(DetailView):
    model = Competition
    pk_url_kwarg = 'pk'
    template_name = 'main/our_competition_detail.html'
    extra_context = {'form': RegistrationCompetitionForm}


class CompetitionListView(ListView):
    model = Competition
    template_name = 'main/our_competition.html'
    context_object_name = 'competitions'

    def get_queryset(self):
        return Competition.objects.filter(data__gte=datetime.now())


def index(request):
    flag = False
    message = ""
    servises = Servise.objects.all()
    treners = Trener.objects.all()
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = OrderForm(request.POST)
            if form.is_valid():
                order = Order()
                order.date = form.data['date']
                order.duration = form.data['duration']
                order.time = form.data['time']
                table = get_object_or_404(Table, id=form.data['tableID'])
                if 'trenerID' in form.data:
                    if form.data['trenerID'] :
                        trener = get_object_or_404(Trener, id=form.data['trenerID'])      
                else:
                    trener = None
                order.trenerID = trener
                order.tableID = table
                customer = get_object_or_404(Customer, user=request.user)
                order.customerID = customer
                hours, minuties = order.get_hours_and_minutes()
                birth_date = customer.data_or_birthday
                current_date = datetime.now()
                age = current_date.year - birth_date.year
                if customer.sex == 'женский' or age < 18:
                    order.price = hours * Decimal.from_float(250.00) + minuties * Decimal.from_float(250.00) / 60
                else:
                    order.price = hours * table.price + minuties * table.price / 60
                if order.trenerID is not None:
                    order.price = hours * trener.price + minuties * trener.price / 60
                    order.save()
                    send_email_task.delay(
                        order.date,
                        order.time,
                        order.duration,
                        order.endtime,
                        customer.__str__(),
                        customer.phone_number,
                        trener.email
                    )
                else:
                    order.save()
                    flag = 1
                    message = "Вы успешно забронировали стол! Детали заказа находятся в личном кабиненте, ждём Вас!"

        else:
            return redirect('login')
    form = OrderForm()
    form.fields['trenerID'].queryset = Trener.objects.filter(is_active=True)
    services_types = KindPriceListElement.objects.filter(is_active=True)

    return render(request, 'main/index.html', {'form': form, 'treners': treners, 'servises': servises, 'services_types': services_types, 'flag': flag, 'message': message})


def code_control(request, code):
    code_email = get_object_or_404(CodeEmail, code=code)
    user = get_object_or_404(User, email=code_email.email)
    user.is_active = True
    user.save()
    code_email.delete()
    return render(request, 'registration/code_control_done.html')


def registrations(request):
    if request.method == 'POST':
        form = CustomerRegistrtionForm(request.POST)
        if form.is_valid():
            new_user = User()
            new_user.username = form.data['email']
            new_user.password = make_password(form.data['password'])
            new_user.email = form.data['email']
            new_user.is_active = False
            new_user.save()

            new_customer = Customer()
            new_customer.user = new_user
            new_customer.surname = form.data['surname']
            new_customer.name = form.data['name']
            new_customer.patronymic = form.data['patronymic']
            new_customer.data_or_birthday = form.data['data_or_birthday']
            new_customer.phone_number = form.data['phone_number']
            new_customer.email = form.data['email']
            new_customer.sex = form.data['sex']
            new_customer.save()

            token_href = secrets.token_hex()[:15]
            new_code_email = CodeEmail(email=new_user.email, code=token_href)
            new_code_email.save()
            send_code_email_task.delay(new_code_email.code, new_code_email.email)
            return render(request, 'registration/register_done.html')

    form = CustomerRegistrtionForm()
    return render(request, 'main/form_registration.html', {'form': form})


class OurLogoutView(LogoutView):
    next_page = 'main_index'


def check_free_table(request):
    form = OrderForm()
    form.fields['trenerID'].queryset = Trener.objects.filter(is_active=True)
    tables = Table.objects.all()
    return render(request, 'main/check_free_table.html', {'form': form, 'tables': tables})
