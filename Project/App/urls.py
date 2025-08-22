from django.contrib import admin
from django.urls import path
from App import views
urlpatterns = [
    path("collect/", views.collect_data, name="collect_data"),
    path("", views.get_data, name="get_data"),
]