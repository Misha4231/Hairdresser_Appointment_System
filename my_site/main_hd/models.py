from django.db import models
from django.urls import reverse

class HairdressModel(models.Model):
    hairdress = models.CharField('Name', max_length=100)
    photo = models.ImageField('Photo', upload_to='photos/%Y/%m/&d/')
    description = models.TextField('Description')
    time_spend = models.CharField('Avarage time required', blank=True, max_length=50)
    cat = models.ForeignKey('Category', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.hairdress

    class Meta:
        verbose_name = 'Hairdress'
        verbose_name_plural = 'Hairdresses'


class Category(models.Model):
    title = models.CharField('Category', max_length=200)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_id': self.pk})

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

class BlockedModel(models.Model):
    blocked_date = models.CharField('Date', max_length=100)
    blocked_time = models.CharField('Date and time', max_length=100)

    def __str__(self):
        return self.blocked_date


class NotesModel(models.Model):
    user_id = models.CharField('user id', max_length=50)
    time = models.CharField('Time', max_length=100)
    service = models.CharField('Category', max_length=100)
    service_id = models.CharField('Service', max_length=200)
    phone_number = models.CharField('Phone number', max_length=30)
    where_location = models.CharField('Location', max_length=50)
    location = models.CharField('Adress', max_length=200)
    description = models.CharField('Comment', max_length=1000)
    is_accepted = models.CharField('Accepted', max_length=15)

    def __str__(self):
        return self.service

    class Meta:
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'

class ReviewsModel(models.Model):
    name = models.CharField("Name", max_length=200)
    email = models.CharField("E-Mail", max_length=200)
    review_text = models.CharField('Review', max_length=1000)
    ip = models.CharField('IP', max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
