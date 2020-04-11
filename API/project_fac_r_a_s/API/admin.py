from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Admin)
admin.site.register(Faculty)
admin.site.register(College)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(StudentAttendance)
admin.site.register(CollegeManagement)
admin.site.register(AzurePersonGroup)

