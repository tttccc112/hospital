# -*- coding=utf-8 -*-
# @Time:
# @Author: zjh
# @File: urls.py
# @Software: PyCharm

from django.urls import path

from django.conf.urls import url
from . import views

urlpatterns = [
    # path("test",views.test),
    path('home/',views.home),
    path('login/',views.Loginclass.as_view()),
    path('signup/',views.Signupclass.as_view()),
    path('base/',views.base),
    
    url(r'^history/(\w+)', views.Case_history.as_view()),
    url(r'^index/(\w+)', views.Index.as_view()),
]