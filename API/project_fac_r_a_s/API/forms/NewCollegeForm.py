from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from API.models import College

class NewCollegeForm(forms.Form):
    
    college_name = forms.CharField(max_length=100, required=True)
    college_code = forms.IntegerField(required=True)
    gtu_afflicated = forms.BooleanField(required=False)
    domain = forms.CharField(max_length=50, required=True)

    def clean_college_code(self):
        c_c = self.cleaned_data['college_code']
        if College.objects.filter(college_code=c_c):
            self.add_error('college_code','college code is already exists')
    
    def clean_domain(self):

        domain = self.cleaned_data['domain']

        if College.objects.filter(domain=domain):
            self.add_error('domain', 'domain is already exists')
