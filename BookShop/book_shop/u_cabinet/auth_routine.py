from django.http import HttpResponse , HttpResponseRedirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import (get_user_model, login as auth_login,)
from django.views.generic import UpdateView
from django.views.generic import CreateView
from .forms import NewUserRegisterForm, ReviewAuthorForm
from .models import ReviewAuthor
from django.urls import reverse, reverse_lazy
from django.core.exceptions import ImproperlyConfigured

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
#--------------------------


class RegisterUser(CreateView):
    form_class = NewUserRegisterForm
    model = ReviewAuthor
    template_name = 'u_cabinet/register.html'
    success_url = 'showcase:all_books'
    check_mail = False

    def form_valid(self, form):
        user = form.save(check_mail=self.check_mail)
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        self.check_mail = bool(request.POST.get('check_mail'))
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        if not self.success_url:
            raise ImproperlyConfigured("No URL to redirect to. Provide a success_url.")
        return str(reverse(self.success_url))  # success_url may be lazy


class BookShopLogin(LoginView):
    template_name = 'u_cabinet/auth.html'

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        return str(reverse('u_cabinet:profile', kwargs={'pk': self.request.session['reviewauthor_id']}))

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        self.request.session['reviewauthor_id'] = get_object_or_404(ReviewAuthor, user_id=form.get_user().id).id
        return HttpResponseRedirect(self.get_success_url())


@method_decorator(login_required, name='dispatch')
class UserProfile(UpdateView):
    template_name = 'u_cabinet/profile.html'
    form_class = ReviewAuthorForm
    model = ReviewAuthor
    extra_context = {'curr_tub': 'profile'}

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        return str(reverse('u_cabinet:profile', kwargs={'pk': self.request.session['reviewauthor_id']}))

