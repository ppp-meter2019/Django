from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from . import models


def specific_manager_permission_required(perm_field, login_url=None, raise_exception=False):
    """
    Decorator for views that checks whether a manager has a particular status which stored in 'perm_field'
    in the model.
    If the raise_exception parameter is given the PermissionDenied exception
    is raised.
    """
    def check_manager_perm_field(user_obj):
        try:
            permission_status = models.ManagersUser.objects.filter(user=user_obj).values(perm_field)[0][perm_field]
        except Exception as e:
            permission_status = False

        if permission_status == True:
            return permission_status
        if raise_exception:
            raise PermissionDenied
        return False
    return user_passes_test(check_manager_perm_field, login_url=login_url)




