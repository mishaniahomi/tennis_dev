# Generated by Django 3.2.13 on 2023-06-23 16:42

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20230623_1538'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competition',
            name='data',
            field=models.DateField(default=datetime.datetime(2023, 6, 23, 16, 42, 37, 197246, tzinfo=utc), verbose_name='Дата соревнований'),
        ),
        migrations.AlterField(
            model_name='registrationcompetition',
            name='data',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 23, 16, 42, 37, 197576, tzinfo=utc), verbose_name='Время записи'),
        ),
    ]
