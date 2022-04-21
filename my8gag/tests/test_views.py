from django.test import TestCase
from ..models import Post, Topic
from django.contrib.auth.models import User
from django.urls import reverse

class TestView(TestCase):

    def test_that_feed_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my8gag/feed.html')

    def test_that_post_view_loads(self):
        topic = Topic.objects.create(name="Funny")
        user = User.objects.create(username="testuser", password="abcdef1")
        # user = User.objects.create(username="testuser", password="abcdef1", email="test@test.com")
        post = Post.objects.create(topic=topic, title='Hej', image='abc.png', author=user)
        url = reverse('post_view', kwargs={"pk":1})
        response = self.client.get(url)
        # response = self.client.get(f'/post_view/{post.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my8gag/post_view.html')

    def test_can_add_a_post(self):
        pass