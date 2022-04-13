from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


# connected to the User model via the signals.py file
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    profile_image = CloudinaryField(
        'profile_image', null=True, default=None, blank=True)

    def __str__(self):
        return self.user.username


class Topic(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    image = CloudinaryField('image')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='post_author')
    created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name='post_like')

    def __str__(self):
        return self.title

    def number_of_likes(self):
        return self.likes.count()


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.body[0:50]
