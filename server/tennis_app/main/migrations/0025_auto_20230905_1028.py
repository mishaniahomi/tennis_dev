# Generated by Django 3.2.13 on 2023-09-05 10:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_alter_order_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(choices=[(datetime.date(2023, 9, 5), datetime.date(2023, 9, 5)), (datetime.date(2023, 9, 6), datetime.date(2023, 9, 6)), (datetime.date(2023, 9, 7), datetime.date(2023, 9, 7))], verbose_name='Дата заказа'),
        ),
        migrations.AlterField(
            model_name='trener',
            name='education',
            field=models.TextField(blank=True, default=' ', null=True, verbose_name='Образование'),
        ),
    ]
