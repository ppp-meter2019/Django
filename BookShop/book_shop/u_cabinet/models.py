from django.db import models
from django.contrib.auth.models import User
from showcase.models import Book
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.


class ReviewAuthor(models.Model):
    TYPE_USER_VIEW = (
        ('fio', 'ФИО'),
        ('pseudo_name', 'Псевдоним'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_birth = models.DateField(blank=True, null=True)
    bio = models.TextField(max_length=5000,
                           verbose_name='Bio',
                           blank=True, null=True)
    type_view = models.CharField(max_length=255,
                                 verbose_name='Тип представления',
                                 choices=TYPE_USER_VIEW,
                                 blank=True, null=True)
    pseudoname = models.CharField(max_length=255,
                                  verbose_name='Псевдоним',
                                  blank=True, null=True)
    def __str__(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)


class BookListInBasket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)


class Review(models.Model):
    PUSBLISH_STATUS = (
        ('publish', 'Да'),
        ('unpublish', 'Нет'),
    )
    author = models.ForeignKey(ReviewAuthor, on_delete=models.CASCADE)
    title = models.CharField(max_length=255,
                             verbose_name='Title', blank=True,
                             null=True, default='')
    content = RichTextUploadingField()
    create_at = models.DateTimeField(auto_created=True, auto_now_add=True)
    status = models.CharField(max_length=55, verbose_name='Publish?', choices=PUSBLISH_STATUS)
    #comments = models.ManyToManyField(Comment)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)


class Comment(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE)
    for_book = models.ForeignKey(Review, on_delete=models.CASCADE)
    msg = models.TextField(max_length=1000, verbose_name='Текст комментария')
