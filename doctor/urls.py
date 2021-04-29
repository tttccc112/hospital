
from django.conf.urls import url
from . import views
urlpatterns = [
    #url(r'^index/(\wt)/(\wt)', views.index),
    #url(r'^choose/', views.choose.as_view()),
    url(r'^home/', views.home),
    url(r'^load3/',views.load3),
    url(r'^load4/',views.load4),
    url(r'^load5/',views.load5),

    url(r'^load9/',views.load9),
    url(r'^load12/',views.load12),
    url(r'^load14/',views.load14),
    ]

