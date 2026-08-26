from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from products.models import Product
from .models import StockMovement


class StockMovementTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='manager7',
            email='manager7@example.com',
            password='StrongPass123',
        )
        self.user.profile.role = 'manager'
        self.user.profile.save()

        self.product = Product.objects.create(
            name='Rice Seed',
            sku='RICE-001',
            category='Seed',
            unit='kg',
            unit_price='300.00',
            created_by=self.user,
        )

    def test_stock_movement_can_be_created(self):
        stock = StockMovement.objects.create(
            product=self.product,
            movement_type='purchase',
            quantity='25.00',
            created_by=self.user,
            notes='Supplier delivery',
        )

        self.assertEqual(StockMovement.objects.count(), 1)
        self.assertEqual(stock.product, self.product)
        self.assertEqual(stock.movement_type, 'purchase')
        self.assertEqual(str(stock), 'purchase - Rice Seed')

    def test_stock_movements_page_requires_login(self):
        response = self.client.get(reverse('inventory:list'))

        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_stock_movements_page_shows_records_for_logged_in_user(self):
        self.client.login(username='manager7', password='StrongPass123')
        StockMovement.objects.create(
            product=self.product,
            movement_type='sale',
            quantity='5.00',
            created_by=self.user,
            notes='Customer order',
        )

        response = self.client.get(reverse('inventory:list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'sale')
