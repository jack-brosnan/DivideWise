from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic
from django.views.generic import TemplateView
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import (
    ExpenseSpace,
    ExpenseLine,
    Contributor,
    Contribution,
)
from .forms import (
    ExpenseSpaceForm,
    ContributorForm,
    ExpenseLineForm,
    CustomAmountForm,
)


class ExpenseSpaceList(TemplateView):
    """
    Displays a welcome page for unauthenticated users
    and a list of expense spaces for authenticated users.
    """
    template_name = "expense_app/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            # Authenticated users see their expense spaces
            context["expense_spaces"] = ExpenseSpace.objects.filter(
                user=self.request.user
            ).order_by("-created_on")
        else:
            # Unauthenticated users see the welcome page
            context["expense_spaces"] = None
        return context


@login_required
def add_space(request):
    """
    Add a new expense space.
    """
    if request.method == "POST":
        expense_space_form = ExpenseSpaceForm(request.POST, request.FILES)
        if expense_space_form.is_valid():
            expense_space = expense_space_form.save(commit=False)
            expense_space.user = request.user
            expense_space.save()
            messages.success(request, "Expense Space added successfully!")
            return redirect("home")
    else:
        expense_space_form = ExpenseSpaceForm()

    return render(
        request,
        "expense_app/add_space.html",
        {"expense_space_form": expense_space_form},
    )


@login_required
def edit_space(request, edit_id):
    """
    Edit an existing expense space.
    """
    expense_space = get_object_or_404(
                    ExpenseSpace,
                    pk=edit_id,
                    user=request.user
                    )

    if request.method == "POST":
        expense_space_form = ExpenseSpaceForm(
            data=request.POST,
            files=request.FILES,
            instance=expense_space,
        )
        if expense_space_form.is_valid():
            expense_space_form.save()
            messages.success(request, "Space Updated!")
            return HttpResponseRedirect(reverse("home"))
        messages.error(request, "Error updating expense!")
    else:
        expense_space_form = ExpenseSpaceForm(instance=expense_space)

    return render(
        request,
        "expense_app/edit_space.html",
        {
            "expense_space_form": expense_space_form,
            "edit_id": edit_id,
        },
    )


@login_required
def delete_space(request, space_id):
    """
    Delete an existing expense space.
    """
    expense_space = get_object_or_404(ExpenseSpace,
                                      pk=space_id,
                                      user=request.user
                                      )
    if request.method == "POST":
        expense_space.delete()
        messages.success(request, "Space deleted successfully!")
    return redirect("home")


@login_required
def view_space(request, space_id):
    """
    Display the details of a specific ExpenseSpace along with
    its linked ExpenseLines.
    """
    expense_space = get_object_or_404(
        ExpenseSpace,
        pk=space_id,
        user=request.user
        )

    expense_line = ExpenseLine.objects.filter(
        expense_space=expense_space
        ).order_by('-created_on')

    contributor = Contributor.objects.filter(expense_space=expense_space)

    return render(
        request,
        'expense_app/view_space.html',
        {
            "expense_space": expense_space,
            "expense_line": expense_line,
            "contributor": contributor,
        }
    )


@login_required
def edit_contributor(request, space_id):
    """
    Add, edit, or delete contributors for an expense space.
    """
    expense_space = get_object_or_404(
        ExpenseSpace,
        pk=space_id,
        user=request.user
        )

    contributors = Contributor.objects.filter(expense_space=expense_space)

    form = ContributorForm()

    if request.method == 'POST':
        if 'edit' in request.POST:
            pk = request.POST.get('edit')
            contributor = get_object_or_404(
                Contributor,
                id=pk,
                expense_space=expense_space
                )
            form = ContributorForm(instance=contributor)

        elif 'save' in request.POST:
            pk = request.POST.get('save')
            if pk:
                contributor = get_object_or_404(
                    Contributor,
                    id=pk,
                    expense_space=expense_space
                    )
                form = ContributorForm(request.POST, instance=contributor)
                if form.is_valid():
                    form.save()
                    messages.add_message(
                        request,
                        messages.SUCCESS,
                        'Contributor edited!')

            else:
                form = ContributorForm(request.POST)
                if form.is_valid():
                    contributor = form.save(commit=False)
                    contributor.expense_space = expense_space
                    contributor.save()
                    messages.add_message(
                        request,
                        messages.SUCCESS,
                        'Contributor added!')

            form = ContributorForm()

        elif 'delete' in request.POST:
            pk = request.POST.get('delete')
            if pk:
                contributor = get_object_or_404(
                    Contributor,
                    id=pk,
                    expense_space=expense_space
                    )
                contributor.delete()
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    'Contributor deleted!')

        elif 'cancel' in request.POST:
            return redirect('edit_contributor', space_id=space_id)

    return render(request, 'expense_app/edit_contributor.html',
                  {
                    'expense_space': expense_space,
                    'contributor': contributors,
                    'form': form,
                  })


@login_required
def add_expense(request, space_id):
    """
    Add a new expense line to an expense space.
    """
    expense_space = get_object_or_404(
        ExpenseSpace,
        pk=space_id,
        user=request.user)

    if request.method == 'POST':
        expense_line_form = ExpenseLineForm(request.POST)
        if expense_line_form.is_valid():
            expense_line = expense_line_form.save(commit=False)
            expense_line.expense_space = expense_space
            expense_line.save()
            messages.add_message(request, messages.SUCCESS, 'Expense added!')

            return redirect('view_space', space_id=space_id)
    else:
        expense_line_form = ExpenseLineForm()

    return render(
        request, 'expense_app/add_expense.html',
        {
            'expense_line_form': expense_line_form,
            'expense_space': expense_space

        }
        )


@login_required
def edit_expense(request, space_id, expense_id):
    """
    Edit an existing expense line.
    """
    expense_space = get_object_or_404(
        ExpenseSpace,
        pk=space_id,
        user=request.user
        )
    expense_line = get_object_or_404(ExpenseLine,
                                     pk=expense_id,
                                     expense_space=expense_space
                                     )

    if request.method == 'POST':
        expense_line_form = ExpenseLineForm(
                                        request.POST,
                                        instance=expense_line)
        if expense_line_form.is_valid():
            expense_line = expense_line_form.save(commit=False)
            expense_line.expense_space = expense_space
            expense_line.save()
            messages.add_message(request, messages.SUCCESS, 'Expense Updated!')

            return redirect('view_space', space_id=space_id)
    else:
        expense_line_form = ExpenseLineForm(instance=expense_line)

    return render(
        request, 'expense_app/edit_expense.html',
        {
         'expense_line_form': expense_line_form,
         'expense_space': expense_space,
         'expense_line': expense_line,
        }
        )


@login_required
def delete_expense(request, space_id, expense_id):
    """
    Delete an existing expense line.
    """
    expense_space = get_object_or_404(
        ExpenseSpace,
        pk=space_id,
        user=request.user)
    expense_line = get_object_or_404(
        ExpenseLine,
        pk=expense_id,
        expense_space=expense_space)

    if request.method == 'POST':
        expense_line.delete()
        messages.add_message(request, messages.SUCCESS, 'Expense Removed!')
        return redirect('view_space', space_id=space_id)

    return render(
        request, 'expense_app/edit_expense.html',
        {
            'expense_space': expense_space,
            'expense_line': expense_line,
        }
        )


@login_required
def edit_custom_amount(request, space_id, expense_id, contribution_id):
    """
    Edit a custom amount assigned to a contributor.
    """
    expense_space = get_object_or_404(
        ExpenseSpace,
        pk=space_id,
        user=request.user
        )

    expense_line = get_object_or_404(
        ExpenseLine,
        pk=expense_id,
        expense_space=expense_space
        )

    contribution = get_object_or_404(
        Contribution,
        pk=contribution_id,
        expense_line=expense_line
        )

    form = CustomAmountForm(
        request.POST or None,
        instance=contribution,
        expense_line=expense_line
        )

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Custom amount updated successfully.')
        return redirect('view_space', space_id=space_id)

    return render(request, 'expense_app/edit_custom_amount.html', {
        'expense_space': expense_space,
        'expense_line': expense_line,
        'contribution': contribution,
        'form': form,
    })


@login_required
def delete_contribution(request, space_id, expense_id, contribution_id):
    """
    Delete a contributor's contribution from an expense line.
    """
    expense_space = get_object_or_404(
        ExpenseSpace,
        pk=space_id,
        user=request.user
        )

    expense_line = get_object_or_404(
        ExpenseLine,
        pk=expense_id,
        expense_space=expense_space
        )

    contribution = get_object_or_404(
        Contribution,
        pk=contribution_id,
        expense_line=expense_line
        )

    if request.method == 'POST':
        contribution.delete()
        messages.add_message(request, messages.SUCCESS, 'Contribution Removed')
        return redirect('view_space', space_id=space_id)

    return render(
        request, 'expense_app/edit_expense.html',
        {
         'expense_space': expense_space,
         'expense_line': expense_line,
         'contribution': contribution,
        }
        )


@login_required
def add_contribution(request, space_id, expense_id):
    """
    Add a new contributor to an expense line.
    """

    expense_space = get_object_or_404(
        ExpenseSpace,
        pk=space_id,
        user=request.user
        )

    expense_line = get_object_or_404(
        ExpenseLine,
        pk=expense_id,
        expense_space=expense_space
        )

    added_contributors = expense_line.expense_contributions.all().values_list(
        'contributor_id',
        flat=True
        )

    unassigned_contributors = Contributor.objects.filter(
        expense_space=expense_space).exclude(id__in=added_contributors)

    if request.method == 'POST':
        selected_contributors = request.POST.getlist('contributors')
        if selected_contributors:
            for contributor_id in selected_contributors:
                contributor = get_object_or_404(
                    Contributor,
                    id=contributor_id,
                    expense_space=expense_space
                    )
                Contribution.objects.create(
                    expense_line=expense_line,
                    contributor=contributor
                    )
            messages.success(request, 'Contributors added to the expense')
            return redirect('view_space', space_id=space_id)

    return render(request, 'expense_app/add_contribution.html',
                  {
                   'expense_space': expense_space,
                   'expense_line': expense_line,
                   'unassigned_contributors': unassigned_contributors,
                  }
                  )
