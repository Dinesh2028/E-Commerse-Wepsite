from django.urls import path
from . import views
from .login import user_login

urlpatterns = [
    path('', views.register, name='register'),
    path('login/', user_login, name='login'),
]
