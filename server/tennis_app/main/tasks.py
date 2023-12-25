from django.core.mail import send_mail
from celery import shared_task


@shared_task()
def send_email_task(date, time, duration, endtime, customer, phone_number, EMAIL_HOST_USER, trener_email):
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