from django.db import models

from client.models import MailingSettings

NULLABLE = {'blank': True, 'null': True}
# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=50, verbose_name='Заголовок')
    body = models.TextField(max_length=500, verbose_name='Содержимое')
    avatar = models.ImageField(upload_to='', **NULLABLE, verbose_name='Изображение')
    count_view = models.IntegerField(default=0, **NULLABLE, verbose_name='Колличество просмотров')
    date_publication = models.DateField(auto_now=True, verbose_name='Дата публикации')


    def __str__(self):
        return f'{self.title}, {self.date_publication}'

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
