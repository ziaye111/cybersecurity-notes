from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from farms.models import Farm
from .models import Livestock


class LivestockTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='manager3',
            email='manager3@example.com',
            password='StrongPass123',
        )
        self.user.profile.role = 'manager'
        self.user.profile.save()

        self.farm = Farm.objects.create(
            name='Hilltop Farm',
            location='East Ridge',
            created_by=self.user,
        )

    def test_livestock_can_be_created(self):
        animal = Livestock.objects.create(
            farm=self.farm,
            animal_type='cow',
            breed='Holstein',
            count=12,
            age_months=18,
            status='healthy',
            created_by=self.user,
        )

        self.assertEqual(Livestock.objects.count(), 1)
        self.assertEqual(animal.farm, self.farm)
        self.assertEqual(str(animal), 'Holstein cow')

    def test_livestock_page_requires_login(self):
        response = self.client.get(reverse('livestock:list'))

        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_livestock_page_shows_records_for_logged_in_user(self):
        self.client.login(username='manager3', password='StrongPass123')
        Livestock.objects.create(
            farm=self.farm,
            animal_type='goat',
            breed='Boer',
            count=9,
            age_months=12,
            status='healthy',
            created_by=self.user,
        )

        response = self.client.get(reverse('livestock:list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Boer')
