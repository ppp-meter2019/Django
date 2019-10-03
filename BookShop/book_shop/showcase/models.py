from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.timezone import datetime

# Create your models here.


class Genre(models.Model):
    name = models.CharField(max_length=200, help_text="Введите жанр - Фантастика, Исторический ромаб Поєзия и тд ")

    def __str__(self):
        return self.name


class Book(models.Model):
    short_title = models.CharField(max_length=255, verbose_name='Краткое название книги')
    full_title = models.CharField(max_length=500, verbose_name='Полное название книги', blank=True)
    author = models.CharField(max_length=255, verbose_name='Автор книги', default='', null=True)
    annotation = models.TextField(max_length=1000, verbose_name='Краткая аннотация', blank=True)
    image = models.ImageField(upload_to='covers', default='no-image.png', blank=True, null=True)
    isbn_num = models.CharField(max_length=14,verbose_name='ISBN номер', default='')
    publisher = models.CharField(max_length=60, verbose_name='Издатель', blank=True)

    published_at = models.PositiveIntegerField(verbose_name='Год издания',
                                               validators=[MinValueValidator(1900),
                                                           MaxValueValidator(datetime.now().year)],
                                               blank=True, default="1980")

    is_sale = models.BooleanField(default=False,help_text="Продается ли книга по акции: Да/Нет")
    genre = models.ManyToManyField(Genre,help_text='Укажите жанр для єтой книи. Может быть > 1')
    price = models.FloatField(verbose_name='Стоимость товара', default=0.0)
    percent_sale = models.FloatField(validators=[MinValueValidator(0.0),
                                                 MaxValueValidator(100.0)],
                                     default=0.0)
    create_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.short_title

    def display_genre(self):
        """
        Creates a string for the Genre. This is required to display genre in Admin.
        """
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'
