from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.decorators import login_required
from .models import ExpenseSpace, ExpenseLine, Contributor, Contribution
from .forms import ExpenseSpaceForm

# Create your views here.

# class HomePage(TemplateView):
#     """
#     Displays home page"
#     """
#     template_name = 'base.html'

class ExpenseSpaceList(generic.ListView):
    model = ExpenseSpace
    template_name = 'expense_app/index.html'
    context_object_name = 'expense_spaces'
    
    def get_queryset(self):
        if isinstance(self.request.user, AnonymousUser):
            return ExpenseSpace.objects.none()
        
        return ExpenseSpace.objects.filter(user=self.request.user).order_by('-created_on')

@login_required
def add_space(request):
   
    if request.method == 'POST':
        expense_space_form = ExpenseSpaceForm(request.POST, request.FILES)
        if expense_space_form.is_valid():
            expense_space = expense_space_form.save(commit=False)
            expense_space.user = request.user
            expense_space.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Expense Space added successfully!'
            )
            return redirect('home')
    else:
        expense_space_form = ExpenseSpaceForm()

    return render(
        request, 'expense_app/add_space.html', {'expense_space_form': expense_space_form})