# Generated by Django 4.2.2 on 2023-10-27 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_auto_20230928_1719'),
    ]

    operations = [
        migrations.CreateModel(
            name='Servise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serviseName', models.CharField(max_length=32, verbose_name='НазваниеУслуги')),
                ('image', models.ImageField(null=True, upload_to='', verbose_name='ФотоУслуги')),
                ('describe', models.CharField(max_length=45, verbose_name='ОписаниеУслуги')),
            ],
        ),
    ]