# Generated by Django 3.0.4 on 2021-01-27 12:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ticker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_code', models.CharField(max_length=32, verbose_name='通貨ペア')),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='日付時間')),
                ('bid', models.FloatField(verbose_name='売値')),
                ('ask', models.FloatField(verbose_name='売値')),
                ('volume', models.IntegerField(verbose_name='ティック数')),
            ],
        ),
    ]
