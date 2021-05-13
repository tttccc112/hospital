
from django.conf.urls import url
from . import views
urlpatterns = [
    # url(r'^index/(\wt)/(\wt)', views.index),
    # url(r'^choose/', views.choose.as_view()),
    url(r'^index/(\w+)/(\w+)', views.index.as_view()),
    url(r'^history/(\w+)/(\w+)', views.history),
    url(r'^check/(\w+)/(\w+)', views.check),
    url(r'^decide/(\w+)/(\w+)', views.decide),
    url(r'^arrange/(\w+)/(\w+)', views.arrange),
    url(r'^evaluation/(\w+)/(\w+)', views.evaluation),


    ]
