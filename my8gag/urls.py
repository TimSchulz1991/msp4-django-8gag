from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('create_post/', views.createPost, name="create_post")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)