from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('create_post/', views.create_post, name="create_post")
]