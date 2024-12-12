from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import ExpenseSpace, ExpenseLine, Contributor, Contribution

# Register your models here.


@admin.register(ExpenseSpace)
class ExpenseSpaceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'name',
        'currency',
        'created_on',
        'updated_on'
        )


@admin.register(ExpenseLine)
class ExpenseLineAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'expense_space',
                    'title',
                    'amount',
                    'created_on')


@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'expense_space',
        'name')


@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'expense_line',
                    'contributor',
                    'split_type',
                    'custom_amount',
                    'remaining_share',
                    )
    readonly_fields = ('remaining_share', 'split_type')

    def remaining_share(self, obj):
        """
        If custom amount applied. Display 0 under 'remaining_share' field.
        """
        if obj.custom_amount is None:
            return obj.remaining_share
        return 0
    remaining_share.short_description = 'Remaining Share'
