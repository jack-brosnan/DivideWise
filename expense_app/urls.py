from . import views
from django.urls import path

urlpatterns = [
    path('', views.ExpenseSpaceList.as_view(), name='home'),
    path("add_space/",views.add_space, name="add_space"),
    path("edit_space/<int:edit_id>/",views.edit_space, name="edit_space"),
    path("delete_space/<int:space_id>/",views.delete_space,name="delete_space"),
    path("view_space/<int:space_id>/", views.view_space, name="view_space"),
]