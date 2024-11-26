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
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

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
    paid_status = models.IntegerField(choices=PAID_STATUS, default=0)
    due_date = models.DateTimeField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_on"]

class Contributor(models.Model):
    """
    Stores a single contributor line entry related to :model:`expense_app.ExpenseSpace` and :model:`expense_app.Contribution`.
    """
    expense_space = models.ForeignKey(ExpenseSpace, on_delete=models.CASCADE, related_name="contributors")
    name = models.CharField(max_length=50)
    email = models.EmailField()

class Contribution(models.Model):
    """
    Stores a single contributor expense line entry related to :model:`expense_app.ExpenseLine`.
    """
    expense_line = models.ForeignKey(ExpenseLine, on_delete=models.CASCADE, related_name="expense_contributions")
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE, related_name="expense_contributors")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    custom_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    paid_status = models.IntegerField(choices=PAID_STATUS, default=0)
    """
    Method to calculate the remaining balance of the expense if custom amounts are applied to some contributors.
    """
    @property
    def remaining_share(self):
        # Get all contributors that are assigned to the expense line 
        all_contributions = self.expense_line.expense_contributions.all()
        # Add the total sum of all custom amounts applied. If none is applied, defaults to 0
        total_custom_amount = sum(c.custom_amount or 0 for c in all_contributions)
        # calcualte the remaining amount after deducting the total custom amounts
        remaining_amount = max(self.expense_line.amount - total_custom_amounts, 0)
        # get all contributors with no custom amount applied
        contributors_non_custom = all_contributions.filter(custom_amount__isnull=True).count()
        # divide the remaining amount equally amongst all contributors with no custom amount applied
        if contributors_non_custom > 0:
            return remaining_amount / contributors_non_custom
        return 0
