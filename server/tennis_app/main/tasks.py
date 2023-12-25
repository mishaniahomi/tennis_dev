from django.core.mail import send_mail
from celery import shared_task


@shared_task()
def send_email_task(date, time, duration, endtime, customer, phone_number, trener_email):
    send_mail(
        'Здравствуйте',
        f'''К Вам записались на занятие!
        Дата: {date};
        Время: {time};
        Продолжительность: {duration};
        Окончание: {endtime};
        Ученик: {customer};
        Телефон: {phone_number};
        ''',
        'misha.homi@gmail.com',
        [trener_email],
        fail_silently=False
    )


@shared_task
def send_code_email_task(code, email):
    send_mail(
        'Здравствуйте',
        '''Был запрос на создание аккаунта!\n
        Ccылка для подтверждения: http://tennis57.ru/code_control/{}'''.format(code),
        'misha.homi@gmail.com',
        [email],
        fail_silently=False
    )