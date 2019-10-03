# Generated by Django 2.2.2 on 2019-06-15 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите жанр - Фантастика, Исторический ромаб Поєзия и тд ', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_title', models.CharField(max_length=255, verbose_name='Краткое название кники')),
                ('full_title', models.CharField(blank=True, max_length=500, verbose_name='Полное название кники')),
                ('annotation', models.TextField(blank=True, max_length=1000, verbose_name='Краткая аннотация')),
                ('image', models.ImageField(blank=True, default='', null=True, upload_to='covers')),
                ('genre', models.ManyToManyField(help_text='Укажите жанр для єтой книи. Может быть > 1', to='showcase.Genre')),
            ],
        ),
    ]