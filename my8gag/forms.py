from django.forms import ModelForm
from .models import Post, Profile


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

        # ('bio', 'profile_image',)
