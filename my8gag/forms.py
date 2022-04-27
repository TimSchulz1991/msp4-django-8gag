from django.forms import ModelForm
from .models import Post, Profile


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('topic', 'title', 'image',)


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'profile_image',)
