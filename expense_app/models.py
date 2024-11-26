from django.db import models

from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

PAID_STATUS = ((0, "Not Paid"), (1, "Paid"))
CURRENCY = ((0, "€"), (1, "£"), (2, "$"))

# Create your models here.

class ExpenseSpace(models.Model):
    """
    Stores a single expense space entry related to :model:`auth.User`.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expense_spaces")
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    space_image = CloudinaryField('image', default='placeholder')
    currency = models.IntegerField(choices=CURRENCY, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_on"]

class ExpenseLine(models.Model):
    """
    Stores a single expense line entry related to :model:`expense_app.ExpenseSpace`.
    """
    expense_space = models.ForeignKey(ExpenseSpace, on_delete=models.CASCADE, related_name="expense_lines")
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_status = models.IntegerField(choices=CURRENCY, default=0)
    due_date = models.DateTimeField
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_on"]

