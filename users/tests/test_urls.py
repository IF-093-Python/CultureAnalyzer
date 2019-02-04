from django.test import SimpleTestCase
from django.urls import reverse, resolve

from users import views

class TestUrls(SimpleTestCase):

    def test_url_is_resolved(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func, views.index)

    def test_profile_url_is_resolved(self):
        url = reverse('profile', args=[1])
        self.assertEqual(resolve(url).func.view_class, views.UserUpdateView)