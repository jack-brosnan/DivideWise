from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from expense_app.models import (
    ExpenseSpace,
    ExpenseLine,
    Contributor,
    Contribution
    )
from decimal import Decimal


# Test class for the ExpenseSpace model
class ExpenseSpaceModelTest(TestCase):
    def setUp(self):
        # Create a test user and an ExpenseSpace instance
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
            )
        self.expense_space = ExpenseSpace.objects.create(
            user=self.user,
            name="Test Space",
            description="This is a test space",
        )

    def test_expense_space_str(self):
        """
        Test the string representation of the ExpenseSpace model.
        """
        self.assertEqual(str(self.expense_space), "Test Space")

    def test_total_expense_defaults_to_zero(self):
        """
        Test that the total expense method defaults to zero when
        there are no expense lines.
        """
        self.assertEqual(self.expense_space.total_expense(), 0)


# Test class for the ExpenseLine model
class ExpenseLineModelTest(TestCase):
    def setUp(self):
        """
        Create a test user and an ExpenseLine instance
        linked to an ExpenseSpace
        """
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
            )
        self.expense_space = ExpenseSpace.objects.create(
            user=self.user,
            name="Test Space"
        )
        self.expense_line = ExpenseLine.objects.create(
            expense_space=self.expense_space,
            title="Test Expense",
            amount=200.00
        )

    def test_expense_line_str(self):
        """
        Test the string representation of the ExpenseLine model.
        """
        self.assertEqual(str(self.expense_line), "Test Expense")

    def test_total_custom_amount(self):
        """
        Test the total_custom_amount method calculates the
        correct total for custom amounts.
        """
        Contributor.objects.create(
            expense_space=self.expense_space,
            name="Contributor 1"
            )
        Contribution.objects.create(
            expense_line=self.expense_line,
            contributor=Contributor.objects.first(),
            custom_amount=50.00
        )
        self.assertEqual(self.expense_line.total_custom_amount(), 50.00)


# Test class for the Contributor model
class ContributorModelTest(TestCase):
    def setUp(self):
        """
        Create a test user and a Contributor instance linked to an ExpenseSpace
        """
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
            )
        self.expense_space = ExpenseSpace.objects.create(
            user=self.user,
            name="Test Space"
        )
        self.contributor = Contributor.objects.create(
            expense_space=self.expense_space,
            name="Test Contributor"
        )

    def test_contributor_str(self):
        """
        Test the string representation of the Contributor model.
        """
        self.assertEqual(str(self.contributor), "Test Contributor")


# Test class for the Contribution model
class ContributionModelTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create_user(
            username='testuser', password='testpassword'
        )

        # Create an ExpenseSpace linked to the user
        self.expense_space = ExpenseSpace.objects.create(
            user=self.user,
            name="Test Space",
            description="Test Space Description",
            currency=0
        )

        # Create an ExpenseLine linked to the ExpenseSpace
        self.expense_line = ExpenseLine.objects.create(
            expense_space=self.expense_space,
            title="Test Expense",
            amount=Decimal('300.00')
        )

        # Create two Contributors linked to the ExpenseSpace
        self.contributor1 = Contributor.objects.create(
            expense_space=self.expense_space,
            name="Contributor 1"
        )
        self.contributor2 = Contributor.objects.create(
            expense_space=self.expense_space,
            name="Contributor 2"
        )

        # Create Contributions for each Contributor
        self.contribution1 = Contribution.objects.create(
            expense_line=self.expense_line,
            contributor=self.contributor1,
            custom_amount=Decimal('200.00')
        )
        self.contribution2 = Contribution.objects.create(
            expense_line=self.expense_line,
            contributor=self.contributor2,
            custom_amount=None  # No custom amount for this contributor
        )

    def test_remaining_share(self):
        """
        Test the remaining_share property for contributors
        without custom amounts.
        """
        self.assertEqual(self.contribution2.remaining_share, Decimal('100.00'))
