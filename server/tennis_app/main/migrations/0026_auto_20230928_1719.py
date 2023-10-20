# Generated by Django 3.2.13 on 2023-09-28 17:19

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_auto_20230905_1028'),
    ]

    operations = [
        migrations.CreateModel(
            name='Abonement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_limit', models.TimeField(blank=True, null=True, verbose_name='Время ограничения')),
                ('competition_limit', models.CharField(choices=[('все', 'все'), ('Только детям и женщинам', 'Только детям и женщинам')], max_length=50, verbose_name='Ограничения по турнирам')),
            ],
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(verbose_name='Дата заказа'),
        ),
        migrations.CreateModel(
            name='AbonementСustomer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_begin', models.DateField(default=django.utils.timezone.now, verbose_name='Дата активации абонемента')),
                ('duration', models.IntegerField(default=30, verbose_name='на сколько дней')),
                ('data_end', models.DateField(blank=True, null=True, verbose_name='Дата оканчания абонемента')),
                ('abonement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.abonement', verbose_name='Вид абонемента')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.customer', verbose_name='Клиент')),
            ],
        ),
    ]