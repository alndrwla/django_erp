from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import model_to_dict

# Create your models here.
class User(AbstractUser):
    ci = models.CharField(max_length=13, unique=True, null=False, blank=False, verbose_name="Cédula")
    phone = models.CharField(max_length=15, null=True, blank=True, verbose_name="Teléfono/Celular")

    def toJSON(self):
        item = model_to_dict(self, exclude=['password', 'groups', 'user_permissions', 'last_login'])
        if self.is_superuser:
            item['is_superuser'] = "Administrador"
        else:
            item["is_superuser"] = "Trabajador"
        return item
