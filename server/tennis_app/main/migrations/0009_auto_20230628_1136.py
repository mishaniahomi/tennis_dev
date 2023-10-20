# Generated by Django 3.2.13 on 2023-06-28 11:36

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20230627_1235'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='endtime',
            field=models.TimeField(blank=True, null=True, verbose_name='Время окончания'),
        ),
        migrations.AlterField(
            model_name='competition',
            name='data',
            field=models.DateField(default=datetime.datetime(2023, 6, 28, 11, 36, 22, 442405, tzinfo=utc), verbose_name='Дата соревнований'),
        ),
        migrations.AlterField(
            model_name='order',
            name='duration',
            field=models.TimeField(choices=[(datetime.time(1, 0), '01:00'), (datetime.time(1, 30), '01:30'), (datetime.time(2, 0), '02:00'), (datetime.time(2, 30), '02:30'), (datetime.time(3, 0), '03:00'), (datetime.time(3, 30), '03:30'), (datetime.time(4, 0), '04:00'), (datetime.time(4, 30), '04:30')], verbose_name='Продолжительность'),
        ),
        migrations.AlterField(
            model_name='registrationcompetition',
            name='data',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 28, 11, 36, 22, 442827, tzinfo=utc), verbose_name='Время записи'),
        ),
        migrations.DeleteModel(
            name='OrderTrener',
        ),
    ]