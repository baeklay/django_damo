from django.urls import path
from app01 import views

urlpatterns = [
    path(r'register/', views.register, name='register')
]
