from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from customers.models import Customer
from products.models import Product
from .models import Sale, SaleItem


class SaleTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='manager9',
            email='manager9@example.com',
            password='StrongPass123',
        )
        self.user.profile.role = 'manager'
        self.user.profile.save()

        self.customer = Customer.objects.create(
            name='Town Market',
            contact_person='Alice',
            phone='0700000006',
            email='alice@townmarket.com',
            created_by=self.user,
        )
        self.product = Product.objects.create(
            name='Fresh Tomato',
            sku='TOMATO-200',
            category='Vegetable',
            unit='crate',
            unit_price='500.00',
            created_by=self.user,
        )

    def test_sale_and_item_can_be_created(self):
        sale = Sale.objects.create(
            customer=self.customer,
            invoice_number='S-1001',
            sale_date='2026-07-12',
            total_amount='5000.00',
            created_by=self.user,
        )
        item = SaleItem.objects.create(
            sale=sale,
            product=self.product,
            quantity='10.00',
            unit_price='500.00',
        )

        self.assertEqual(Sale.objects.count(), 1)
        self.assertEqual(SaleItem.objects.count(), 1)
        self.assertEqual(item.sale, sale)
        self.assertEqual(item.product, self.product)
        self.assertEqual(str(sale), 'S-1001')

    def test_sales_page_requires_login(self):
        response = self.client.get(reverse('sales:list'))

        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_sales_page_shows_sale_numbers_for_logged_in_user(self):
        self.client.login(username='manager9', password='StrongPass123')
        Sale.objects.create(
            customer=self.customer,
            invoice_number='S-2002',
            sale_date='2026-07-15',
            total_amount='2000.00',
            created_by=self.user,
        )

        response = self.client.get(reverse('sales:list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'S-2002')
