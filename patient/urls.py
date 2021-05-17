# -*- coding=utf-8 -*-
# @Time:
# @Author: zjh
# @File: urls.py
# @Software: PyCharm

from django.urls import path
from patient import views

urlpatterns = [
    path("test",views.test),
    path('home/',views.home),
    path('login/',views.Login.login)
]