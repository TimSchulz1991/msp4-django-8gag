from django.test import TestCase, Client
from ..models import Post, Topic
from django.contrib.auth.models import User
from django.urls import reverse
import os
from django.conf import settings
from django.contrib.auth import get_user_model
        


class TestView(TestCase):

    def setUp(self):
        self.topic = Topic.objects.create(name="Funny")
        self.user = User.objects.create(
            username="testuser", password="abcdef1")

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

        # tutor service of CodeInstitute helped with this test
        
        # set username and password
        username = 'dummyUser'
        password = 'dummyPassword'

        # create a user
        User = get_user_model()
        user = User.objects.create_user(username=username, password=password)

        # login
        logged_in = self.client.login(username=username, password=password)
        
        # check we are indeed logged in
        self.assertTrue(logged_in)

        # upload image
        upload_file = open(os.path.join(settings.BASE_DIR, 'static/img/test.jpg'), "rb")

        # make post request
        response = self.client.post('/create_post/', {
            'topic': Topic.objects.first().id,
            'title': 'Hej',
            'image': upload_file,
            'author': user
        })

        # check response and status code
        self.assertEquals(response.status_code, 302)

        # check that new post has been made
        obj = Post.objects.get(title='Hej')

        # assets that the newly created post is the right one
        self.assertEqual(obj.title, 'Hej')


    def test_can_delete_post(self):
        self.client.login(username="testuser", password="abcdef1")
        post = Post.objects.create(
            topic=self.topic, title='Hej', image='abc.png', author=self.user)
        print(Post.objects.count())
        url = reverse('post_delete', kwargs={"pk": 1})
        response = self.client.post(url, follow=True)
        self.assertRedirects(response, '/')
