from . import views
from django.urls import path

urlpatterns = [
    path('', views.ExpenseSpaceList.as_view(), name='home'),
    path("add_space/",views.add_space, name="add_space"),
]