from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Supplier


class SupplierTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='manager5',
            email='manager5@example.com',
            password='StrongPass123',
        )
        self.user.profile.role = 'manager'
        self.user.profile.save()

    def test_supplier_can_be_created(self):
        supplier = Supplier.objects.create(
            name='Agro Supply Co.',
            contact_person='George',
            phone='0700000003',
            email='sales@agrosupply.com',
            created_by=self.user,
        )

        self.assertEqual(Supplier.objects.count(), 1)
        self.assertEqual(supplier.name, 'Agro Supply Co.')
        self.assertEqual(str(supplier), 'Agro Supply Co.')

    def test_suppliers_page_requires_login(self):
        response = self.client.get(reverse('suppliers:list'))

        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_suppliers_page_shows_supplier_names_for_logged_in_user(self):
        self.client.login(username='manager5', password='StrongPass123')
        Supplier.objects.create(
            name='Farm Inputs Ltd',
            contact_person='Maria',
            phone='0700000004',
            email='maria@farminputs.com',
            created_by=self.user,
        )

        response = self.client.get(reverse('suppliers:list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Farm Inputs Ltd')
