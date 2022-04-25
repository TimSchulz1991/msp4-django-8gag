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
        User = get_user_model()
        self.users = [
            {
                'username': 'testuser1',
                'password': 'test',
                'user': User.objects.create_user(
                    username='testuser1', password='test')
            },
            {
                'username': 'testuser2',
                'password': 'test',
                'user': User.objects.create_user(
                    username='testuser2', password='test')
            }
        ]


    def tearDown(self):
        del self.topic
        del self.users


    def test_that_feed_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my8gag/feed.html')


    def test_that_post_view_loads(self):
        post = Post.objects.create(
            topic=self.topic, title='Hej', image='abc.png',
            author=self.users[0]['user'])
        url = reverse('post_view', kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my8gag/post_view.html')


    def test_logged_in_user_can_add_a_post(self):
        # tutor service of CodeInstitute helped with this test

        # login
        logged_in = self.client.login(
            username=self.users[0]['username'],
            password=self.users[0]['password'])

        # check we are indeed logged in
        self.assertTrue(logged_in)

        # upload image
        upload_file = open(os.path.join(
            settings.BASE_DIR, 'static/img/test.jpg'), "rb")

        # make post request
        response = self.client.post('/create_post/', {
            'topic': Topic.objects.first().id,
            'title': 'Hej',
            'image': upload_file,
        })

        # check response and status code
        self.assertEquals(response.status_code, 302)

        # check that new post has been made
        posts = Post.objects.filter(title='Hej')

        # assets that the newly created post is the right one
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0].title, 'Hej')

        # def test_can_delete_post(self):
        #     self.client.login(username="testuser", password="abcdef1")
        #     post = Post.objects.create(
        #         topic=self.topic, title='Hej', image='abc.png', author=self.user)
        #     print(Post.objects.count())
        #     url = reverse('post_delete', kwargs={"pk": 1})
        #     response = self.client.post(url, follow=True)
        #     self.assertRedirects(response, '/')
