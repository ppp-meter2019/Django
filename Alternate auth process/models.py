from django.db import models
from django.contrib.auth.models import User

# from django.template.defaultfilters import slugify

# from django.utils.text import slugify


# Create your models here.








class ManagersUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_manager = models.BooleanField(default=False)
    is_super_manager = models.BooleanField(default=False)
    second_email = models.EmailField(blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
