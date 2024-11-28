from cloudinary.forms import CloudinaryFileField
from django import forms
from django.core.exceptions import ValidationError
from .models import ExpenseSpace


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
                'space_image': forms.ClearableFileInput(
                    attrs={'placeholder': 'Upload an image'}
                ),
                'currency': forms.Select(
                    attrs={'placeholder': 'Enter currency'}
                ),
            }

