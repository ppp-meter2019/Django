# Generated by Django 2.2.2 on 2019-06-20 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0004_auto_20190616_2157'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenreWithUrl',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('showcase.genre',),
        ),
        migrations.AlterField(
            model_name='book',
            name='image',
            field=models.ImageField(blank=True, default='no_image.jpg', null=True, upload_to='covers'),
        ),
    ]