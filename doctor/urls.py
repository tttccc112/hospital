# -*- coding=utf-8 -*-
# @Time:
# @Author: zjh
# @File: urls.py
# @Software: PyCharm

from django.urls import path
from doctor import views

urlpatterns = [
    path("test",views.test)
]