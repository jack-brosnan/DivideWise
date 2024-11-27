from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import ExpenseSpace, ExpenseLine, Contributor, Contribution

# Create your views here.

class HomePage(TemplateView):
    """
    Displays home page"
    """
    template_name = 'base.html'