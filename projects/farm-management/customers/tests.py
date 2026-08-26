from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Customer


class CustomerTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='manager4',
            email='manager4@example.com',
            password='StrongPass123',
        )
        self.user.profile.role = 'manager'
        self.user.profile.save()

    def test_customer_can_be_created(self):
        customer = Customer.objects.create(
            name='Aisha Market',
            contact_person='Aisha',
            phone='0700000001',
            email='aisha@example.com',
            created_by=self.user,
        )

        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(customer.name, 'Aisha Market')
        self.assertEqual(str(customer), 'Aisha Market')

    def test_customers_page_requires_login(self):
        response = self.client.get(reverse('customers:list'))

        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_customers_page_shows_customer_names_for_logged_in_user(self):
        self.client.login(username='manager4', password='StrongPass123')
        Customer.objects.create(
            name='Fresh Basket',
            contact_person='Ben',
            phone='0700000002',
            email='fresh@example.com',
            created_by=self.user,
        )

        response = self.client.get(reverse('customers:list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Fresh Basket')
