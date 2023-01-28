from django.contrib import admin
from .models import *

@admin.register(HairdressModel)
class HairdressAdmin(admin.ModelAdmin):
    list_display = ('hairdress', 'description')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(NotesModel)
class NotesModelAdminModel(admin.ModelAdmin):
    list_display = ('time', 'service')

@admin.register(ReviewsModel)
class ReviewsModelAdmin(admin.ModelAdmin):
    list_display = ('name',)