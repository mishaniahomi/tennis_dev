# -*- coding: utf-8 -*- 
from django import forms
from .models import Customer, Order, RegistrationCompetition
import datetime as dt


class RegistrationCompetitionForm(forms.ModelForm):
    class Meta:
        model = RegistrationCompetition
        fields = ('rating',)
        widgets = {
            'rating': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class OrderForm(forms.ModelForm):
    choices = [(dt.datetime.now().date(), dt.datetime.now().date()),
                                                                 (
                                                                     (dt.datetime.now() + dt.timedelta(days=1)).date(),
                                                                     (dt.datetime.now() + dt.timedelta(days=1)).date()
                                                                  ),
                                                                 #(
                                                                     #(dt.datetime.now() + dt.timedelta(days=2)).date(),
                                                                     #(dt.datetime.now() + dt.timedelta(days=2)).date()
                                                                 #)
                                                                 ]

    date = forms.ChoiceField(label='Дата', choices=choices, widget=forms.Select(attrs={'class': 'form-control', 'onchange': 'get_free_tables()'}) )

    class Meta:
        model = Order
        fields = ('date', 'time', 'duration', 'tableID', 'trenerID')
        widgets = {
            'duration': forms.Select(attrs={'class': 'form-control',  'onchange': 'get_free_tables()'}),
            'tableID': forms.Select(attrs={'class': 'form-control', 'onchange': 'get_price()'}),
            'trenerID': forms.Select(attrs={'class': 'form-control', 'onchange': 'get_price()'}),
            'date': forms.Select(attrs={'class': 'form-control', 'onchange': 'get_free_tables()'}),
            'time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'time', 'onchange': 'get_free_tables()'}),
        }


class CustomerRegistrtionForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтверждение пароля',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Customer
        fields = ('surname', 'name', 'patronymic', 'data_or_birthday', 'phone_number', 'sex', 'email')
        widgets = {
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'patronymic': forms.TextInput(attrs={'class': 'form-control'}),
            'data_or_birthday': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control tel', 'type': 'tel'}),
            'sex': forms.Select(attrs={'class': 'form-control'},
                                choices=[('мужской', 'мужской'), ('женский', 'женский')]),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return cd['password2']
