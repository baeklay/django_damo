from django.urls import re_path
from web.views import account

urlpatterns = [
    re_path(r'^register/$', account.register)
]
