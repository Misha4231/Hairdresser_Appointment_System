from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePage, name='home'),
    path('sing_up', views.SingUp, name='singup'),
    path('reviews', views.Reviews, name='reviews'),
    path('ourservices', views.OurServices, name='ourservices'),
    path('ourservices/<int:category_id>', views.OurServicesDetail.as_view(), name='OurServicesDetail'),
]