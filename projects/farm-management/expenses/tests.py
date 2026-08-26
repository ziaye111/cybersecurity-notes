from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Expense


class ExpenseTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='manager10',
            email='manager10@example.com',
            password='StrongPass123',
        )
        self.user.profile.role = 'manager'
        self.user.profile.save()

    def test_expense_can_be_created(self):
        expense = Expense.objects.create(
            title='Fuel',
            category='Transport',
            amount='850.00',
            expense_date='2026-07-18',
            created_by=self.user,
        )

        self.assertEqual(Expense.objects.count(), 1)
        self.assertEqual(expense.title, 'Fuel')
        self.assertEqual(str(expense), 'Fuel')

    def test_expenses_page_requires_login(self):
        response = self.client.get(reverse('expenses:list'))

        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_expenses_page_shows_expense_titles_for_logged_in_user(self):
        self.client.login(username='manager10', password='StrongPass123')
        Expense.objects.create(
            title='Feed',
            category='Livestock',
            amount='1200.00',
            expense_date='2026-07-20',
            created_by=self.user,
        )

        response = self.client.get(reverse('expenses:list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Feed')
