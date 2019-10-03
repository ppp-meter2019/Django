from django.views.generic import CreateView, RedirectView, TemplateView
from django.contrib.auth.models import User
from django.contrib.auth.views import (LoginView, PasswordResetView, PasswordResetCompleteView,
                                       PasswordResetConfirmView, PasswordResetDoneView)
from .forms import NewManagerRegisterForm
from .models import ManagersUser
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse , HttpResponseRedirect

#-------- Sending email confirmation mail -------------------

from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text

#-------------------------------------------------------------




class CreateManager(CreateView):

    form_class = NewManagerRegisterForm
    model = ManagersUser
    template_name = 'manage_site/pages/register.html'
    success_url = reverse_lazy('manage:login')

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        self.mail_confirmation(self.object, form.get_cleaned_data()['email'])
        return HttpResponseRedirect(self.get_success_url())

    def mail_confirmation(self, user_, to_email):
        current_site = get_current_site(self.request)
        message = render_to_string('mail/email_confirmation.html', {
            'user': user_,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user_.pk)),
            'token': account_activation_token.make_token(user_),
        })
        mail_subject = 'Mail confirmation message'
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
        return


class ManagerLogin(LoginView):

    template_name = 'manage_site/pages/login.html'
    success_url = 'manage:home'

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        return str(reverse(self.success_url))


class ManagerMailConfirmation(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        """
        Return the URL redirect to. Keyword arguments from the URL pattern
        match generating the redirect request are provided as kwargs to this
        method.
        """
        try:
            if self.activate(uidb64=self.kwargs['uidb64'], token=self.kwargs['token']):
                self.pattern_name = 'manage:c_success'
            else:
                self.pattern_name = 'manage:c_error'
        except Exception as e:
            self.pattern_name = 'manage:c_error'

        #url = reverse(self.pattern_name, args=args, kwargs=kwargs)
        url = reverse(self.pattern_name)
        return url

    def activate(self, *args, **kwargs):
        """
        Return the True or False. True - managers mail was confirmed and users 'is_active
        has' become True, False - in the other case, which means user activation failed.
        """
        confirmation = False
        try:
            uid = force_text(urlsafe_base64_decode(kwargs['uidb64']))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, kwargs['token']):
            user.is_active = True
            user.save()
            confirmation = True

        return confirmation


class ConfirmationSuccessful(TemplateView):

    template_name = 'mail/confirmation-success.html'


class ConfirmationError(TemplateView):

    template_name = 'mail/confirmation-error.html'


class ManagersPasswordReset(PasswordResetView):

    email_template_name = 'mail/password_reset_email.html'
    subject_template_name = 'mail/password_reset_subject.txt'
    success_url = reverse_lazy('manage:passwd_reset_done')
    template_name = 'mail/password_reset.html'


class ManagersPasswordResetDone(PasswordResetDoneView):

    template_name = 'mail/password_reset_done.html'


class ManagersPasswordResetConfirm(PasswordResetConfirmView):

    success_url = reverse_lazy('manage:passwd_reset_complete')
    template_name = 'mail/password_reset_confirm.html'


class ManagersPasswordResetComplete(PasswordResetCompleteView):

    template_name = 'mail/password_reset_complete.html'
