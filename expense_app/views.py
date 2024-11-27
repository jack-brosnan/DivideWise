from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.models import AnonymousUser
from .models import ExpenseSpace, ExpenseLine, Contributor, Contribution

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