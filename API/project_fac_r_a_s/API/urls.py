from django.urls import path
from . import views
from .Admin.AdminLoginView import AdminLoginView
from .Admin.CreateNewCollegeView import CreateNewCollegeView
from .Admin.DeleteCollegeView import DeleteCollegeView

from . import get_csrf_token

urlpatterns = [
    path('admin/login',  AdminLoginView.as_view(), name='admin-login'),
    path('admin/add_college',  CreateNewCollegeView.as_view(), name='admin-add-college'),
    path('admin/delete_college',  DeleteCollegeView.as_view(), name='admin-delete-college'),
    path('get_csrf_token', get_csrf_token.getTokenFunction , name='get-csrf-token')
]

