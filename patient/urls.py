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
    
    url(r'^history/(\w+)', views.Case_history.as_view()),
    url(r'^index/(\w+)', views.Index.as_view()),
    url(r'^check/(\w+)', views.Check.as_view()),
    url(r'^fee/(\w+)', views.Fee.as_view()),
    url(r'^register/(\w+)', views.Register.as_view()),
    
    url(r'^register2/(\w+)/(\w+)', views.Register2.as_view()),
    url(r'^register3/(\w+)/(\w+)/(\w+)', views.Register3.as_view()),
    url(r'^feedback/(\w+)', views.Feedback.as_view()),
]