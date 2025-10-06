from django.test import TestCase, Client
from django.urls import reverse, resolve
from .views import dashboard_view
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

    def test_root_url_resolves_to_dashboard_view(self):
        """
        Testa che l'URL associato al nome 'dashboard' risolva alla vista corretta.
        """
        found = resolve(reverse('dashboard'))
        self.assertEqual(found.func, dashboard_view)