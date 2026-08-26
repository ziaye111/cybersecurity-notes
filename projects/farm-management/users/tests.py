from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from customers.models import Customer
from expenses.models import Expense
from inventory.models import StockMovement
from products.models import Product
from sales.models import Sale
from .models import UserProfile


class UserProfileTests(TestCase):
    def test_profile_is_created_for_new_user(self):
        user = get_user_model().objects.create_user(
            username='alice',
            email='alice@example.com',
            password='StrongPass123',
        )

        self.assertTrue(UserProfile.objects.filter(user=user).exists())
        self.assertEqual(user.profile.role, 'worker')

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('users:dashboard'))

        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_login_page_renders(self):
        response = self.client.get(reverse('login'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Farm Management')
        self.assertContains(response, 'Log in')

    def test_successful_login_redirects_to_dashboard(self):
        get_user_model().objects.create_user(
            username='david',
            password='StrongPass123',
        )

        response = self.client.post(
            reverse('login'),
            {'username': 'david', 'password': 'StrongPass123'},
        )

        self.assertRedirects(response, reverse('users:dashboard'))

    def test_dashboard_for_logged_in_user(self):
        user = get_user_model().objects.create_user(
            username='bob',
            email='bob@example.com',
            password='StrongPass123',
        )

        self.client.login(username='bob', password='StrongPass123')
        response = self.client.get(reverse('users:dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'bob')
        self.assertContains(response, 'worker')

    def test_dashboard_shows_financial_summary(self):
        user = get_user_model().objects.create_user(
            username='carol',
            email='carol@example.com',
            password='StrongPass123',
        )

        customer = Customer.objects.create(
            name='City Market',
            contact_person='Carol',
            phone='0700000007',
            email='city@example.com',
            created_by=user,
        )
        product = Product.objects.create(
            name='Corn',
            sku='CORN-001',
            category='Crop',
            unit='kg',
            unit_price='120.00',
            created_by=user,
        )

        sale = Sale.objects.create(
            customer=customer,
            invoice_number='SALE-9001',
            sale_date='2026-07-01',
            total_amount='1200.00',
            created_by=user,
        )
        sale.items.create(product=product, quantity='10.00', unit_price='120.00')

        Expense.objects.create(
            title='Feed',
            category='Livestock',
            amount='300.00',
            expense_date='2026-07-02',
            created_by=user,
        )

        StockMovement.objects.create(
            product=product,
            movement_type='purchase',
            quantity='25.00',
            created_by=user,
            notes='Stock received',
        )

        self.client.login(username='carol', password='StrongPass123')
        response = self.client.get(reverse('users:dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '1200.00')
        self.assertContains(response, '300.00')
        self.assertContains(response, '1')
        self.assertContains(response, '900.00')
