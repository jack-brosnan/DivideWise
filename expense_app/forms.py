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
        
        """
        **Widgets**:

        1. ``name``: TextInput with a placeholder for entering the item name.
        2. ``description``: TextInput with a placeholder for entering the description.
        3. ``space_image``: FileInput for uploading an image.
        4. ``currency``: Select field for selecting the currency.
        """

        widgets = {
                'name': forms.TextInput(
                    attrs={'placeholder': 'Enter Title'}
                ),
                'description': forms.TextInput(
                    attrs={'placeholder': 'Enter Description'}
                ),                
            }

class ContributorForm(forms.ModelForm):
    class Meta:
        model = Contributor
        fields = ['name',]
        widgets = {
                'name': forms.TextInput(
                    attrs={'placeholder': 'Enter Name'}
                ),
        }

class ExpenseLineForm(forms.ModelForm):
    """
    Form for adding or editing an expense.
    """
    class Meta:
        """
        **Model**: :model:`ExpenseLine`

        **Fields**:

        1. ``title``: Text field for entering the item name.
        2. ``description``: TextInput for entering a description.
        3. ``due_date``: Date input.
        4. ``amount``: Float field to enter the expense amount.

        """
        model = ExpenseLine
        fields = ['title', 'description', 'amount', 'due_date']
        
        widgets = {
                'title': forms.TextInput(
                    attrs={'placeholder': 'Enter Title'}
                ),
                'description': forms.TextInput(
                    attrs={'placeholder': 'Enter Description'}
                ),
                'amount': forms.NumberInput(
                    attrs={'placeholder': 'Enter amount', 'min': '0', 'step': '0.01'}
                ),
                'due_date': forms.DateInput(
                    attrs={'placeholder': 'Optional'}
                ),
            }

class CustomAmountForm(forms.ModelForm):
    class Meta:
        model = Contribution
        fields = ['custom_amount',]

        widgets = {
                'custom_amount': forms.NumberInput(
                    attrs={'placeholder': 'Enter Custom Amount', 'min': '0', 'step': '0.01'}
                ),
        }
