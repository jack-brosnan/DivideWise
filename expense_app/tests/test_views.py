from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from expense_app.models import ExpenseSpace


class HomePageViewTest(TestCase):
    """
    Tests for the home page view.
    """

    def setUp(self):
        """
        Setup test client, user, and expense space data.
        """
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpass"
        )
        self.home_url = reverse("home")
        self.expense_space = ExpenseSpace.objects.create(
            user=self.user, name="Test Space", description="Test Description"
        )

    def test_home_view_unauthenticated_user(self):
        """
        Test that the home view is accessible to unauthenticated users.
        """
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome")
        self.assertNotContains(response, "Your Expense Spaces")

    def test_home_view_authenticated_user(self):
        """
        Test that the home view displays expense spaces
        for authenticated users.
        """
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your Expense Spaces")
        self.assertContains(response, self.expense_space.name)

    def test_home_view_no_expense_spaces(self):
        """
        Test that the home view shows a message when the user has
        no expense spaces.
        """
        self.expense_space.delete()  # Remove all expense spaces
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your Expense Spaces")
