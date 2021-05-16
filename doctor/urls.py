
from django.conf.urls import url
from . import views
urlpatterns = [
    # url(r'^index/(\wt)/(\wt)', views.index),
    # url(r'^choose/', views.choose.as_view()),
    url(r'^index/(\w+)/(\w+)', views.index.as_view()),
    url(r'^history/(\w+)/(\w+)', views.history.as_view()),
    url(r'^check/(\w+)/(\w+)', views.check.as_view()),
    url(r'^decide/(\w+)/(\w+)', views.decide.as_view()),
    url(r'^arrange/(\w+)/(\w+)', views.arrange),
    url(r'^evaluation/(\w+)/(\w+)', views.evaluation),


    ]
