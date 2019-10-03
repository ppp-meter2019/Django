from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.generic import ListView
from .models import ManagersUser, Category, Link
from django.shortcuts import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from .permission_decorators import specific_manager_permission_required


# Create your views here.


class CustomUserListUpdateMixin:
    def post(self, request, *args, **kwargs):

        try:
            path = request.get_full_path()
            page_num = path[path.index('?page='):]
        except Exception as e:
            page_num = ''
        try:

            all_items = list(map(int, request.POST.get('managers_items_onpage').split(',')))

            list_to_grant_access_is_manager = list(map(int, request.POST.getlist('for_action_manager')))
            self.change_status(all_items, list_to_grant_access_is_manager, 'is_manager')

            list_to_grant_access_is_super_manager = list(map(int, request.POST.getlist('for_action_super_manager')))
            self.change_status(all_items, list_to_grant_access_is_super_manager, 'is_super_manager')

        except Exception as e:
            pass

        return HttpResponseRedirect(str(reverse("manage:all_managers")) + page_num)

    def change_status(self, all_items, list_to_grant_access, field_name):
        list_to_revoke_access = set(all_items) - set(list_to_grant_access)
        if list_to_revoke_access:
            revoke_objects_list = ManagersUser.objects.filter(id__in=list_to_revoke_access)
            revoke_objects_list.update(**{field_name: False})

        if list_to_grant_access:
            grant_objects_list = ManagersUser.objects.filter(id__in=list_to_grant_access)
            grant_objects_list.update(**{field_name: True})


@login_required(login_url=settings.MANAGER_LOGIN_URL)
@specific_manager_permission_required('is_manager', raise_exception=True)
def admin_home(request):
    return render(request, 'manage_site/pages/home.html', {})


@method_decorator(login_required, name='dispatch')
@method_decorator(specific_manager_permission_required('is_super_manager', raise_exception=True), name='dispatch')
class AllManagersList(CustomUserListUpdateMixin, ListView):
    model = ManagersUser
    context_object_name = 'all_managers'
    template_name = "manage_site/pages/all_managers.html"
    paginate_by = 3
    success_url = "manage:all_managers"






