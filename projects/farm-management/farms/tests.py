from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Farm, Field


class FarmAndFieldTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='manager1',
            email='manager@example.com',
            password='StrongPass123',
        )
        self.profile = self.user.profile
        self.profile.role = 'manager'
        self.profile.save()

    def test_farm_and_field_can_be_created(self):
        farm = Farm.objects.create(name='Green Valley Farm', location='North District', created_by=self.user)
        field = Field.objects.create(farm=farm, name='North Field', area_hectares='12.50')

        self.assertEqual(Farm.objects.count(), 1)
        self.assertEqual(Field.objects.count(), 1)
        self.assertEqual(field.farm, farm)
        self.assertEqual(field.name, 'North Field')

    def test_farms_page_requires_login(self):
        response = self.client.get(reverse('farms:list'))

        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_farms_page_shows_farm_names_for_logged_in_user(self):
        self.client.login(username='manager1', password='StrongPass123')
        Farm.objects.create(name='Sunrise Farm', location='West Sector', created_by=self.user)

        response = self.client.get(reverse('farms:list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sunrise Farm')

    def test_worker_cannot_access_farms_page(self):
        self.profile.role = 'worker'
        self.profile.save()
        self.client.login(username='manager1', password='StrongPass123')

        response = self.client.get(reverse('farms:list'))

        self.assertEqual(response.status_code, 403)

    def test_admin_can_access_farms_page(self):
        self.profile.role = 'admin'
        self.profile.save()
        self.client.login(username='manager1', password='StrongPass123')

        response = self.client.get(reverse('farms:list'))

        self.assertEqual(response.status_code, 200)
