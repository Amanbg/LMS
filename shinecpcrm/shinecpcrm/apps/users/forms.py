from django import forms
from leadsource.models import LeadSource
from users.models import MyUser


class AddLeadForm(forms.Form):
    username = forms.CharField(max_length=20)
    email_id = forms.CharField(max_length=50)
    name = forms.CharField(max_length=30)
    contact = forms.CharField(max_length=10)
    city = forms.CharField(max_length=20)
    experience_years = forms.IntegerField()
    experience_level = forms.IntegerField()
    industry = forms.CharField(max_length=40)
    salary = forms.IntegerField()
    source = forms.ModelChoiceField(queryset=LeadSource.objects.all())
    product_name = forms.CharField(max_length=40)


class TeamAddLeadForm(AddLeadForm):
    assign_to = forms.ModelChoiceField(queryset=MyUser.objects.filter(role='Caller'))


class CommentForm(forms.Form):
    category = forms.CharField(max_length=30)
    sub_category = forms.CharField(max_length=30)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 40}))
    package_offered = forms.CharField(max_length=30)


class PasswordResetForm(forms.Form):
    username = forms.CharField(max_length=20)
    password1 = forms.CharField(widget=forms.PasswordInput,)
    password2 = forms.CharField(widget=forms.PasswordInput,)
