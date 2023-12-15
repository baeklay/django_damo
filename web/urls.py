from django.urls import path
from web.views import account

urlpatterns = [
    path(r'register/$', account.register, name='register')
]
