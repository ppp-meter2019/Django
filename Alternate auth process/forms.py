from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ManagersUser , Category
from pytils.translit import slugify

class NewManagerRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    #second_email = forms.EmailField(max_length=254, required=False, help_text='Secondary email. Can be blank.')

    def save(self, *args, **kwargs):
        django_user = User.objects.create_user(username=self.cleaned_data['username'],
                                               first_name=self.cleaned_data['first_name'],
                                               last_name=self.cleaned_data['last_name'],
                                               password=self.cleaned_data['password1'],
                                               email=self.cleaned_data['email'],
                                               is_staff=False,
                                               is_active=False
                                               )
        ManagersUser.objects.create(user=django_user)
        return django_user

    def get_cleaned_data(self, *args, **kwargs):
        return self.cleaned_data

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)







