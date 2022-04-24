from django.test import TestCase
from ..models import Post, Topic
from django.contrib.auth.models import User
from django.urls import reverse


class TestView(TestCase):

    def setUp(self):
        self.topic = Topic.objects.create(name="Funny")
        self.user = User.objects.create(username="testuser", password="abcdef1")
    
    def tearDown(self):
        del self.topic
        del self.user

    def test_that_feed_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my8gag/feed.html')

    def test_that_post_view_loads(self):
        
        post = Post.objects.create(
            topic=self.topic, title='Hej', image='abc.png', author=self.user)
        url = reverse('post_view', kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my8gag/post_view.html')

    def test_can_add_a_post(self):
        response = self.client.post('create_post/', {})
