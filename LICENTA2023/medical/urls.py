from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name = 'home'),
    path('register_pacient/', views.register_pacient, name = 'register_pacient'),
    path('login_pacient/', views.login_pacient, name= 'login_pacient'),
    path('upload_photo_pacient/', views.upload_photo_pacient, name= 'upload_photo_pacient'),

]

