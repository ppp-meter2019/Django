# Generated by Django 2.2.2 on 2019-06-16 18:35

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0002_auto_20190615_2003'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='create_at',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='book',
            name='is_sale',
            field=models.BooleanField(default=False, help_text='Продается ли книга по акции: Да/Нет'),
        ),
        migrations.AddField(
            model_name='book',
            name='isbn_num',
            field=models.CharField(default='', max_length=14, verbose_name='ISBN номер'),
        ),
        migrations.AddField(
            model_name='book',
            name='percent_sale',
            field=models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(100.0)]),
        ),
        migrations.AddField(
            model_name='book',
            name='price',
            field=models.FloatField(default=0.0, verbose_name='Стоимость товара'),
        ),
        migrations.AddField(
            model_name='book',
            name='published_at',
            field=models.DateTimeField(blank=True, default='1990-11-13', verbose_name='Дата издания'),
        ),
        migrations.AddField(
            model_name='book',
            name='publisher',
            field=models.CharField(blank=True, max_length=60, verbose_name='Издатель'),
        ),
    ]