from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('login/', views.loginView, name="login"),
    path('', views.home, name="home"),
    path('create_post/', views.createPost, name="create_post"),
    path('post_view/<str:pk>/', views.postView, name="post_view"),
    path('post_delete/<str:pk>/', views.deletePost, name="post_delete")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)