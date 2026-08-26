from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from farms.models import Farm, Field
from .models import Crop


class CropTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='manager2',
            email='manager2@example.com',
            password='StrongPass123',
        )
        self.user.profile.role = 'manager'
        self.user.profile.save()

        self.farm = Farm.objects.create(
            name='River Bend Farm',
            location='South Valley',
            created_by=self.user,
        )
        self.field = Field.objects.create(
            farm=self.farm,
            name='Lower Plot',
            area_hectares='20.00',
        )

    def test_crop_can_be_created(self):
        crop = Crop.objects.create(
            farm=self.farm,
            field=self.field,
            name='Maize',
            variety='Hybrid 12',
            planted_area_hectares='12.50',
            sowing_date='2026-01-15',
            expected_harvest_date='2026-05-20',
            status='active',
            created_by=self.user,
        )

        self.assertEqual(Crop.objects.count(), 1)
        self.assertEqual(crop.farm, self.farm)
        self.assertEqual(crop.field, self.field)
        self.assertEqual(str(crop), 'Maize on Lower Plot')

    def test_crops_page_requires_login(self):
        response = self.client.get(reverse('crops:list'))

        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_crops_page_shows_crop_names_for_logged_in_user(self):
        self.client.login(username='manager2', password='StrongPass123')
        Crop.objects.create(
            farm=self.farm,
            field=self.field,
            name='Tomato',
            variety='Roma',
            planted_area_hectares='5.00',
            sowing_date='2026-02-01',
            expected_harvest_date='2026-06-15',
            status='active',
            created_by=self.user,
        )

        response = self.client.get(reverse('crops:list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Tomato')
