from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.decorators import login_required
from .models import ExpenseSpace, ExpenseLine, Contributor, Contribution
from .forms import ExpenseSpaceForm, ContributorForm

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

@login_required
def edit_space(request, edit_id):
    
    expense_space = get_object_or_404(ExpenseSpace, pk=edit_id, user=request.user)

    if request.method == "POST":
        expense_space_form = ExpenseSpaceForm(data=request.POST, files=request.FILES, instance=expense_space)
        if expense_space_form.is_valid():
            expense_space_form.save()
            messages.add_message(request, messages.SUCCESS, 'Space Updated!')
            return HttpResponseRedirect(reverse('home'))
        else:
            messages.add_message(request, messages.ERROR, 'Error updating expense!')

    else:
        expense_space_form = ExpenseSpaceForm(instance=expense_space)

    return render(
        request, 'expense_app/edit_space.html',
         {'expense_space_form': expense_space_form, 'edit_id': edit_id}
    )

@login_required
def delete_space(request, space_id):

    expense_space = get_object_or_404(ExpenseSpace, pk=space_id, user=request.user)
    if request.method == "POST":
        expense_space.delete()
        messages.add_message(request, messages.SUCCESS, 'Space deleted successfully!')
        return redirect('home')
    return redirect('home')

@login_required
def view_space(request, space_id):
    """
    Display the details of a specific ExpenseSpace along with its linked ExpenseLines.
    """
    expense_space = get_object_or_404(ExpenseSpace, pk=space_id, user=request.user)
    expense_line = ExpenseLine.objects.filter(expense_space=expense_space).order_by('-created_on')
    contributor = Contributor.objects.filter(expense_space=expense_space)
    
    
    return render(
        request,
        'expense_app/view_space.html',
        {'expense_space': expense_space, 'expense_line': expense_line, 'contributor': contributor,}
    )

@login_required
def edit_contributor(request, space_id):
    expense_space = get_object_or_404(ExpenseSpace, pk=space_id, user=request.user)
    contributors = Contributor.objects.filter(expense_space=expense_space)
    form = ContributorForm()

    if request.method == 'POST':
        if 'edit' in request.POST:
            pk = request.POST.get('edit')
            contributor = get_object_or_404(Contributor, id=pk, expense_space=expense_space)
            form = ContributorForm(instance=contributor)

        elif 'save' in request.POST:
            pk = request.POST.get('save')
            if pk:  
                contributor = get_object_or_404(Contributor, id=pk, expense_space=expense_space)
                form = ContributorForm(request.POST, instance=contributor)
                if form.is_valid():
                    form.save()
                    
            else:  
                form = ContributorForm(request.POST)
                if form.is_valid():
                    contributor = form.save(commit=False)
                    contributor.expense_space = expense_space
                    contributor.save()
                    
            form = ContributorForm()
            
        elif 'delete' in request.POST:
            pk = request.POST.get('delete')
            if pk:
                contributor = get_object_or_404(Contributor, id=pk, expense_space=expense_space)
                contributor.delete()
                
        elif 'cancel' in request.POST:
            return redirect('edit_contributor', space_id=space_id)

    return render(request, 'expense_app/edit_contributor.html', 
    {
        'expense_space': expense_space,
        'contributor': contributors,
        'form': form,
    })
