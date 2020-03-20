from django.contrib import admin

# Register your models here.
from .models import Admin, Faculty

admin.site.register(Admin)
admin.site.register(Faculty)
