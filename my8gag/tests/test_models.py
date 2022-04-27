from django.test import TestCase
from ..models import Topic


class TestModels(TestCase):

    def test_that_topic_is_created_properly(self):
        topic = Topic.objects.create(name="Funny")
        self.assertEqual(topic.name, "Funny")
