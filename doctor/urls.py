<<<<<<< HEAD
from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^index/(\wt)/(\wt)', views.index),
    url(r'^choose/', views.choose.as_view()),


    ]
=======
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
>>>>>>> 987c382be1ba2fd9935466dacf5f664e696244d2
