# Generated by Django 3.2.13 on 2023-07-09 14:17

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20230709_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competition',
            name='data',
            field=models.DateField(default=datetime.datetime(2023, 7, 9, 14, 17, 54, 492175, tzinfo=utc), verbose_name='Дата соревнований'),
        ),
        migrations.AlterField(
            model_name='registrationcompetition',
            name='data',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 9, 14, 17, 54, 492512, tzinfo=utc), verbose_name='Время записи'),
        ),
        migrations.AlterField(
            model_name='trener',
            name='education',
            field=models.CharField(blank=True, default=' ', max_length=32, null=True, verbose_name='Спортивныйразряд'),
        ),
        migrations.AlterField(
            model_name='trener',
            name='peculiarities',
            field=models.CharField(blank=True, default=' ', max_length=32, null=True, verbose_name='Спортивныйразряд'),
        ),
        migrations.AlterField(
            model_name='trener',
            name='sports_rank',
            field=models.CharField(blank=True, default=' ', max_length=32, null=True, verbose_name='Спортивныйразряд'),
        ),
    ]
