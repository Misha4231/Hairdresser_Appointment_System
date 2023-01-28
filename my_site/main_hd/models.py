from django.db import models
from django.urls import reverse

class HairdressModel(models.Model):
    hairdress = models.CharField('Назва', max_length=100)
    photo = models.ImageField('Фото', upload_to='photos/%Y/%m/&d/')
    description = models.TextField('Опис')
    time_spend = models.CharField('Час, який витрачається на послугу', blank=True, max_length=50)
    cat = models.ForeignKey('Category', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.hairdress

    class Meta:
        verbose_name = 'Зачіска'
        verbose_name_plural = 'Зачіски'


class Category(models.Model):
    title = models.CharField('Категорія', max_length=200)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_id': self.pk})

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'

class BlockedModel(models.Model):
    blocked_date = models.CharField('Тільки дата', max_length=100)
    blocked_time = models.CharField('Дата і час', max_length=100)

    def __str__(self):
        return self.blocked_date


class NotesModel(models.Model):
    user_id = models.CharField('id Користувача', max_length=50)
    time = models.CharField('Час', max_length=100)
    service = models.CharField('Категорія', max_length=100)
    service_id = models.CharField('Послуги', max_length=200)
    phone_number = models.CharField('Номер телефону', max_length=30)
    where_location = models.CharField('Місце', max_length=50)
    location = models.CharField('Адреса', max_length=200)
    description = models.CharField('Коментарій', max_length=1000)
    is_accepted = models.CharField('Підтаерджено', max_length=15)

    def __str__(self):
        return self.service

    class Meta:
        verbose_name = 'Запис'
        verbose_name_plural = 'Записи'

class ReviewsModel(models.Model):
    name = models.CharField("Ім'я", max_length=200)
    email = models.CharField("E-Mail", max_length=200)
    review_text = models.CharField('Відгук', max_length=1000)
    ip = models.CharField('IP-адреса', max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Відгук'
        verbose_name_plural = 'Відгуки'
