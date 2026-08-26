from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from products.models import Product
from suppliers.models import Supplier
from .models import Purchase, PurchaseItem


class PurchaseTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='manager8',
            email='manager8@example.com',
            password='StrongPass123',
        )
        self.user.profile.role = 'manager'
        self.user.profile.save()

        self.supplier = Supplier.objects.create(
            name='Seed Source Ltd',
            contact_person='John',
            phone='0700000005',
            email='john@seedsource.com',
            created_by=self.user,
        )
        self.product = Product.objects.create(
            name='Wheat Seed',
            sku='WHEAT-100',
            category='Seed',
            unit='kg',
            unit_price='220.00',
            created_by=self.user,
        )

    def test_purchase_and_item_can_be_created(self):
        purchase = Purchase.objects.create(
            supplier=self.supplier,
            invoice_number='INV-1001',
            purchase_date='2026-07-08',
            total_amount='2200.00',
            created_by=self.user,
        )
        item = PurchaseItem.objects.create(
            purchase=purchase,
            product=self.product,
            quantity='10.00',
            unit_cost='220.00',
        )

        self.assertEqual(Purchase.objects.count(), 1)
        self.assertEqual(PurchaseItem.objects.count(), 1)
        self.assertEqual(item.purchase, purchase)
        self.assertEqual(item.product, self.product)
        self.assertEqual(str(purchase), 'INV-1001')

    def test_purchases_page_requires_login(self):
        response = self.client.get(reverse('purchases:list'))

        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_purchases_page_shows_purchase_numbers_for_logged_in_user(self):
        self.client.login(username='manager8', password='StrongPass123')
        Purchase.objects.create(
            supplier=self.supplier,
            invoice_number='INV-2002',
            purchase_date='2026-07-10',
            total_amount='500.00',
            created_by=self.user,
        )

        response = self.client.get(reverse('purchases:list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'INV-2002')
