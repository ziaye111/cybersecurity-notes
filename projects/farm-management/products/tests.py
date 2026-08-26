from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Product


class ProductTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='manager6',
            email='manager6@example.com',
            password='StrongPass123',
        )
        self.user.profile.role = 'manager'
        self.user.profile.save()

    def test_product_can_be_created(self):
        product = Product.objects.create(
            name='Maize Grain',
            sku='MAIZE-001',
            category='Crop',
            unit='kg',
            unit_price='250.00',
            created_by=self.user,
        )

        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(product.name, 'Maize Grain')
        self.assertEqual(str(product), 'Maize Grain')

    def test_products_page_requires_login(self):
        response = self.client.get(reverse('products:list'))

        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_products_page_shows_product_names_for_logged_in_user(self):
        self.client.login(username='manager6', password='StrongPass123')
        Product.objects.create(
            name='Tomato Basket',
            sku='TOMATO-001',
            category='Vegetable',
            unit='crate',
            unit_price='320.00',
            created_by=self.user,
        )

        response = self.client.get(reverse('products:list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Tomato Basket')
