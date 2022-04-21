from django.test import TestCase
from ..forms import PostForm, ProfileForm


class TestPostForm(TestCase):

    def test_empty_form_is_invalid(self):
        post = PostForm({'topic': '', 'title': '', 'image': ''})
        self.assertFalse(post.is_valid())

    def test_form_without_image_is_invalid(self):
        post = PostForm({'topic': 'Funny', 'title': 'Hello World', 'image': ''})
        self.assertFalse(post.is_valid())

    def test_fields_are_explicit_in_form_meta_class(self):
        post = PostForm()
        self.assertEqual(post.Meta.fields, ('topic', 'title', 'image',))


class TestProfileForm(TestCase):
    def test_empty_form_is_valid(self):
        profile = ProfileForm({'bio': '', 'profile_image': ''})
        self.assertTrue(profile.is_valid())

    def test_fields_are_explicit_in_form_meta_class(self):
        profile = ProfileForm()
        self.assertEqual(profile.Meta.fields, ('bio', 'profile_image',))