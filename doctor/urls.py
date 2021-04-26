from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^index/(\wt)/(\wt)', views.index),
    url(r'^choose/', views.choose.as_view()),


    ]
