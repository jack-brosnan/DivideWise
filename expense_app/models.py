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
    description = models.CharField(max_length=200, null=True, blank=True)
    space_image = CloudinaryField('image', default='placeholder')
    currency = models.IntegerField(choices=CURRENCY, default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def total_expense(self):
        total = 0
        expense_amount = ExpenseLine.objects.filter(expense_space=self)
        for line in expense_amount:
            total += line.amount
        return total

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["created_on"]

class ExpenseLine(models.Model):
    """
    Stores a single expense line entry related to :model:`expense_app.ExpenseSpace`.
    """
    expense_space = models.ForeignKey(ExpenseSpace, on_delete=models.CASCADE, related_name="expense_lines")
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_status = models.IntegerField(choices=PAID_STATUS, default=0)
    due_date = models.DateField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def total_custom_amount(self):
        total = 0
        contributions = Contribution.objects.filter(expense_line=self)
        for contribution in contributions:
            if contribution.custom_amount is not None:
                total += contribution.custom_amount
        return round(total, 2)

    class Meta:
        ordering = ["created_on"]

class Contributor(models.Model):
    """
    Stores a single contributor line entry related to :model:`expense_app.ExpenseSpace` and :model:`expense_app.Contribution`.
    """
    expense_space = models.ForeignKey(ExpenseSpace, on_delete=models.CASCADE, related_name="contributors")
    name = models.CharField(max_length=50)
    email = models.EmailField(null=True, blank=True)

    def total_contributions(self):
        total = 0
        contributions = Contribution.objects.filter(contributor=self)
        for share in contributions:
            if share.custom_amount is None:
                total += share.remaining_share
            else:
                total += share.custom_amount
        return round(total, 2)
        

    def __str__(self):
        return self.name

    
class Contribution(models.Model):
    """
    Stores a single contributor expense line entry related to :model:`expense_app.ExpenseLine`.
    """
    expense_line = models.ForeignKey(ExpenseLine, on_delete=models.CASCADE, related_name="expense_contributions")
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE, related_name="expense_contributors")
    custom_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    paid_status = models.IntegerField(choices=PAID_STATUS, default=0)

    # def __str__(self):
    #     return f"{self.contributer.name} - {self.expense_line.title}"

    def split_type(self):
        return "Equal Split" if self.custom_amount is None else "Custom"
        
    """
    Method to calculate the remaining balance of the expense if custom amounts are applied to some contributors.
    """
       
    @property
    def remaining_share(self):
        # Get all contributors that are assigned to the expense line 
        all_contributions = self.expense_line.expense_contributions.all()
        # Add the total sum of all custom amounts applied. If none is applied, defaults to 0
        total_custom_amount = sum(c.custom_amount or 0 for c in all_contributions)
        # calculate the remaining amount after deducting the total custom amounts
        remaining_amount = max(self.expense_line.amount - total_custom_amount, 0)
        # get all contributors with no custom amount applied
        contributors_non_custom = all_contributions.filter(custom_amount__isnull=True).count()
        # divide the remaining amount equally amongst all contributors with no custom amount applied
        if contributors_non_custom > 0:
            return round((remaining_amount / contributors_non_custom), 2)
        return 0
