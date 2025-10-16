from django.test import TestCase, Client
from django.urls import reverse, resolve
from .views import homepage_view
import fastf1

class DashboardViewTests(TestCase):

    def setUp(self):
        """
        Configure client before every test
        """
        self.client = Client()
        try:
            fastf1.Cache.enable_cache('cache_test')
        except Exception as e:
                print(f"Cache abilitation error: {e}")

    def test_dashboard_view_status_code(self):
        """
        Test status code 200 (OK) of the dashboard
        """
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_root_url_resolves_to_homepage_view(self):
        """
        Test correct view associated with the homepage
        """
        found = resolve(reverse('homepage'))
        self.assertEqual(found.func, homepage_view)