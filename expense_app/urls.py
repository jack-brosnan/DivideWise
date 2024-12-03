from . import views
from django.urls import path

urlpatterns = [
    path('', views.ExpenseSpaceList.as_view(), name='home'),
    path("add_space/",views.add_space, name="add_space"),
    path("edit_space/<int:edit_id>/",views.edit_space, name="edit_space"),
    path("delete_space/<int:space_id>/",views.delete_space,name="delete_space"),
    path("view_space/<int:space_id>/", views.view_space, name="view_space"),
    path('edit_contributor/<int:space_id>/', views.edit_contributor, name='edit_contributor'),
    path('add_expense/<int:space_id>/', views.add_expense, name='add_expense'),
    path('edit_expense/<int:space_id>/<int:expense_id>/', views.edit_expense, name='edit_expense'),
    path('delete_expense/<int:space_id>/<int:expense_id>/', views.delete_expense, name='delete_expense'),
    
]