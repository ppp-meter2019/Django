from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ReviewAuthor, Review, Comment


class NewUserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    def save(self, *args, **kwargs):
        django_user = User.objects.create_user(username=self.cleaned_data['username'],
                                               first_name=self.cleaned_data['first_name'],
                                               last_name=self.cleaned_data['last_name'],
                                               password=self.cleaned_data['password1'],
                                               email=self.cleaned_data['email'],
                                               is_staff=True,
                                               is_active=False if kwargs['check_mail'] else True
                                               )
        ReviewAuthor.objects.create(user=django_user)
        return django_user

    def get_cleaned_data(self, *args, **kwargs):
        return self.cleaned_data

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)


class ReviewAuthorForm(forms.ModelForm):

    class Meta:
        model = ReviewAuthor
        exclude = ('user',)
        widgets = {
            'date_birth': forms.DateInput(format='%m-%d-%Y',
                                          attrs={'class': 'form-control',
                                                 'placeholder': 'Select a date',
                                                 'type': 'date'}),
        }


class ReviewForm(forms.ModelForm):

    def save(self, *args, **kwargs):
        self.instance.author = kwargs['author']
        self.instance.book = kwargs['book']
        self.instance.save()

        return self.instance

    class Meta:
        model = Review
        exclude = ['author', 'create_at', 'book', 'comments']


class CommentForm(forms.ModelForm):

    def save(self, *args, **kwargs):
        self.instance.from_user = kwargs['from_user']
        self.instance.for_book = kwargs['for_book']
        self.instance.save()
        return self.instance

    class Meta:
        model = Comment
        exclude = ['from_user', 'for_book']
