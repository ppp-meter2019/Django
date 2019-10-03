from django.urls import path , include, re_path
from . import views
from .auth_routine import (CreateManager, ManagerLogin, ManagerMailConfirmation, ConfirmationError,
                           ConfirmationSuccessful, ManagersPasswordReset, ManagersPasswordResetDone,
                           ManagersPasswordResetConfirm, ManagersPasswordResetComplete)

from django.contrib.auth.views import LogoutView

app_name = 'manage'

urlpatterns = [
    path('', views.admin_home, name='home'),
    path('all_managers/', views.AllManagersList.as_view(), name='all_managers'),
    path('all-categoires/', views.CreateCategory.as_view(), name='all-categoires'),
    path('link-binding/', views.CategoryLink.as_view(), name='cat_link_binding'),
    path('link-edit/<slug:slug>', views.BindingLink.as_view(), name='cat_link_edit'),
    path('template-edit/<slug:slug>', views.BindingTemplate.as_view(), name='template_link_edit'),
    path('category-info/<slug:slug>', views.CategoryQuotes.as_view(), name='category-info'),

]

auth_urls = [
    path('register/', CreateManager.as_view(), name='register'),
    path('login/', ManagerLogin.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            ManagerMailConfirmation.as_view(), name='activate'),
    path('confirmation-success/', ConfirmationSuccessful.as_view(), name='c_success'),
    path('confirmation-error/', ConfirmationError.as_view(), name='c_error'),
]

password_reset_urls = [
    path('reset-password/', ManagersPasswordReset.as_view(), name='passwd_reset'),
    path('reset-password-done/', ManagersPasswordResetDone.as_view(),name='passwd_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', ManagersPasswordResetConfirm.as_view(),
         name='passwd_reset_confirm'),
    path('password-reset-complete/', ManagersPasswordResetComplete.as_view(), name='passwd_reset_complete')
]

urlpatterns += auth_urls

urlpatterns += password_reset_urls
