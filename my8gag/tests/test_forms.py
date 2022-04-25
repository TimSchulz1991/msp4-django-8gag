from django.test import TestCase
from ..forms import PostForm, ProfileForm


class TestPostForm(TestCase):

    def test_fields_are_explicit_in_form_meta_class(self):
        post = PostForm()
        self.assertEqual(post.Meta.fields, ('topic', 'title', 'image',))


class TestProfileForm(TestCase):

    def test_fields_are_explicit_in_form_meta_class(self):
        profile = ProfileForm()
        self.assertEqual(profile.Meta.fields, ('bio', 'profile_image',))
