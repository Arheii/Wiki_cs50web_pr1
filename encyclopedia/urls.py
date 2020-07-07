from django.urls import path

from . import views

app_name = "pedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/edit", views.edit, name='edit'),
    path("wiki/<str:title>", views.wiki, name="wiki"),
    path("random", views.random, name="random"),
    path("search", views.search, name="search")
]

