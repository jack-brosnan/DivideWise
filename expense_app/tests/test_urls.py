from django.test import TestCase
from expense_app.forms import (
    ExpenseSpaceForm,
    ContributorForm,
    ExpenseLineForm,
    CustomAmountForm
)
from expense_app.models import ExpenseSpace, Contributor, ExpenseLine


class ExpenseSpaceFormTest(TestCase):
    """
    Test case for the ExpenseSpaceForm.
    """

    def test_valid_expense_space_form(self):
        """
        Test that the form is valid with proper data.
        """
        form = ExpenseSpaceForm(data={
            'name': 'Test Space',
            'description': 'This is a test expense space.',
            'currency': 0,
        })
        self.assertTrue(form.is_valid())

    def test_invalid_expense_space_form(self):
        """
        Test that the form is invalid when required fields are missing.
        """
        form = ExpenseSpaceForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)


class ContributorFormTest(TestCase):
    """
    Test case for the ContributorForm.
    """

    def test_valid_contributor_form(self):
        """
        Test that the form is valid with proper data.
        """
        form = ContributorForm(data={
            'name': 'Test Contributor',
        })
        self.assertTrue(form.is_valid())

    def test_invalid_contributor_form(self):
        """
        Test that the form is invalid when required fields are missing.
        """
        form = ContributorForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)


class ExpenseLineFormTest(TestCase):
    """
    Test case for the ExpenseLineForm.
    """

    def test_valid_expense_line_form(self):
        """
        Test that the form is valid with proper data.
        """
        form = ExpenseLineForm(data={
            'title': 'Test Expense',
            'description': 'This is a test expense line.',
            'amount': 100.00,
        })
        self.assertTrue(form.is_valid())

    def test_invalid_expense_line_form(self):
        """
        Test that the form is invalid when required fields are missing.
        """
        form = ExpenseLineForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        self.assertIn('amount', form.errors)
