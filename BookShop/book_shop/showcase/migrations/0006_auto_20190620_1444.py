# Generated by Django 2.2.2 on 2019-06-20 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0005_auto_20190620_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='image',
            field=models.ImageField(blank=True, default='no-image.png', null=True, upload_to='covers'),
        ),
    ]