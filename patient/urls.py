# -*- coding=utf-8 -*-
# @Time:
# @Author: zjh
# @File: urls.py
# @Software: PyCharm

from django.conf.urls import url
from django.urls import path
from patient import views

urlpatterns = [
    path("test",views.test),

    url(r'^load1/', views.load1),
    url(r'^load7/', views.load7),
    url(r'^load8/',views.load8),
    url(r'^load10/',views.load10),
    url(r'^load11/',views.load11),
    url(r'^load13/',views.load13),
]