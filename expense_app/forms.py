from cloudinary.forms import CloudinaryFileField
from django import forms
from django.core.exceptions import ValidationError
from .models import ExpenseSpace, Contributor, ExpenseLine, Contribution


class ExpenseSpaceForm(forms.ModelForm):
    """
    Form for adding or editing an expense.
    """
    class Meta:
        """
        **Model**: :model:`ExpenseSpace`

        **Fields**:

        1. ``name``: Text field for entering the item name.
        2. ``description``: TextInput for entering a description.
        3. ``space_image``: File input for uploading an image.
        4. ``currency``: Dropdown field to select the currency.

        """
        model = ExpenseSpace
        fields = ['name', 'description', 'space_image', 'currency']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter Title'}),
            'description': forms.TextInput(
                attrs={'placeholder': 'Enter Description'}
            ),
        }


class ContributorForm(forms.ModelForm):
    """
    Form for adding or editing a contributor.
    """
    class Meta:
        """
        **Model**: :model:`Contributor`

        **Fields**:

        1. ``name``: TextInput for entering the item name.

        """
        model = Contributor
        fields = ['name', ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter Name'}),
        }


class ExpenseLineForm(forms.ModelForm):
    """
    Form for adding or editing an expense line.
    """
    class Meta:
        """
        **Model**: :model:`ExpenseLine`

        **Fields**:

        1. ``title``: TextInput for entering the item name.
        2. ``description``: TextInput for entering a description.
        3. ``amount``: Decimal Field to enter the expense amount.

        **Widgets**

        3. ``amount``: min and step attributes to avoid negative
        and null inputs

        """
        model = ExpenseLine
        fields = ['title', 'description', 'amount', ]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter Title'}),
            'description': forms.TextInput(
                attrs={'placeholder': 'Enter Description'}
            ),
            'amount': forms.NumberInput(
                attrs={'placeholder': 'Enter amount',
                       'min': '0',
                       'step': '0.01'}
            ),
        }


class CustomAmountForm(forms.ModelForm):
    """
    Form for adding or editing a custom amount for a contribution.
    """
    class Meta:
        """
        **Model**: :model:`Contribution`

        **Fields**:

        1. ``custom_amount``: Decimal Field for inputting custom amounts.

        """

        model = Contribution
        fields = ['custom_amount', ]
        widgets = {
            'custom_amount': forms.NumberInput(
                attrs={'placeholder': 'Enter Custom Amount',
                       'min': '0',
                       'step': '0.01'}
            ),
        }

    def __init__(self, *args, expense_line=None, **kwargs):
        """
        Initialize the form with `expense_line` parameter(optional).
        """
        super().__init__(*args, **kwargs)
        self.expense_line = expense_line
        self.update_amount_text()

    def update_amount_text(self):
        """
        Update the text to show the remaining amount allowed.
        """
        if self.expense_line:
            remaining_amount = self.get_remaining_amount()
            self.fields['custom_amount'].help_text = f"{remaining_amount}"

    def get_remaining_amount(self):
        """
        Calculate the remaining amount for custom amount input.
        """
        total_custom_amount = self.get_total_custom_amount()
        return max(self.expense_line.amount - total_custom_amount, 0)

    def get_total_custom_amount(self):
        """
        Calculate the total custom amount for other contributions.
        """
        contributions = self.expense_line.expense_contributions
        filtered_contributions = contributions.exclude(pk=self.instance.pk)
        return sum(c.custom_amount or 0 for c in filtered_contributions)

    def clean_custom_amount(self):
        """
        Validate custom amount to ensure it doesn't exceed the limit.
        """
        custom_amount = self.cleaned_data.get('custom_amount', 0)
        if custom_amount is None:
            return custom_amount

        total_custom_amount = self.get_total_custom_amount() + custom_amount
        if (
            self.expense_line
            and total_custom_amount > self.expense_line.amount
        ):
            currency = self.expense_line.expense_space.get_currency_display()
            raise forms.ValidationError(
                f"Custom amount exceeds the remaining allowable amount. "
                f"Maximum allowed: {currency} {self.get_remaining_amount()}"
            )
        return custom_amount
