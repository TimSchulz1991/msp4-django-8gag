from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='my8gag/login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='my8gag/logout.html'), name="logout"),
    path('register/', views.registerView, name='register'),
    path('', views.home, name="home"),
    path('create_post/', views.createPost, name="create_post"),
    path('post_view/<str:pk>/', views.postView, name="post_view"),
    path('post_delete/<str:pk>/', views.deletePost, name="post_delete"),
    path('user_delete/<str:pk>/', views.deleteUser, name="user_delete"),
    path('comment_delete/<str:pk>/', views.deleteComment, name="comment_delete"),
    path('edit_profile/<str:pk>/', views.editProfile, name="edit_profile"),
    path('like/<str:pk>/', views.postLike, name="post_like"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
