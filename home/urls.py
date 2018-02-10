from django.conf.urls import include,url
from .import views

app_name = "home"

urlpatterns = [
    url(r'^$', views.index, name = "index"),
    url(r'^tutorial$', views.tutorial, name = "tutorial"),
    url(r'^about$', views.about, name="about"),
]
