from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from decimal import Decimal

CURRENCY = ((0, "€"), (1, "£"), (2, "$"))


class ExpenseSpace(models.Model):
    """
    Represents an expense space related to a user, storing metadata
    like name, description, currency, and an optional image.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="expense_spaces"
    )
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, null=True, blank=True)
    space_image = CloudinaryField('image', default='placeholder')
    currency = models.IntegerField(choices=CURRENCY, default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def total_expense(self):
        """
        Calculates the total expense of all expense lines
        associated with this space.
        """
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
    Represents a single expense line under an expense space, tracking
    details like title, amount and description
    """
    expense_space = models.ForeignKey(
        ExpenseSpace,
        on_delete=models.CASCADE,
        related_name="expense_lines"
    )
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def total_custom_amount(self):
        """
        Calculates the total of all custom amounts assigned
        for this expense line.
        """
        total = 0
        contributions = Contribution.objects.filter(expense_line=self)
        for contribution in contributions:
            if contribution.custom_amount is not None:
                total += contribution.custom_amount
        return round(total, 2)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["created_on"]


class Contributor(models.Model):
    """
    Represents a contributor associated with the expense space,
    storing details like name and optional email.
    """
    expense_space = models.ForeignKey(
        ExpenseSpace,
        on_delete=models.CASCADE,
        related_name="contributors"
    )
    name = models.CharField(max_length=50)

    def total_contributions(self):
        """
        Calculates the total contributions made by this contributor
        across all associated expense lines.
        To display in expense space overview.
        """
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
    Represents a contributor's share in an expense line.
    """
    expense_line = models.ForeignKey(
        ExpenseLine,
        on_delete=models.CASCADE,
        related_name="expense_contributions"
    )
    contributor = models.ForeignKey(
        Contributor,
        on_delete=models.CASCADE,
        related_name="expense_contributors"
    )
    custom_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    def split_type(self):
        """
        Determines the type of contribution split (Equal or Custom).
        """
        return "Equal Split" if self.custom_amount is None else "Custom"

    @property
    def remaining_share(self):
        """
        Calculates remaining amount after custom amounts applied.
        Then divided into equal shares to the rest of the contributors.
        """
        all_contributions = self.expense_line.expense_contributions.all()
        total_custom_amount = Decimal(0)
        for contribution in all_contributions:
            custom_amount = contribution.custom_amount or Decimal(0)
            total_custom_amount += custom_amount

        remaining_amount = max(
            self.expense_line.amount - total_custom_amount,
            Decimal(0)
            )

        contributors_non_custom = all_contributions.filter(
                custom_amount__isnull=True).count()

        if contributors_non_custom > 0:
            return round(remaining_amount / contributors_non_custom, 2)
        return Decimal(0)
