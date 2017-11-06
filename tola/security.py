from django.db import models
from tola.middleware import get_user
from guardian.shortcuts import get_perms
from rest_framework.exceptions import PermissionDenied
from tola.settings import local

class SecurityModel(models.Model):
    """
    Abstract Model to inherit security models from
    """
    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super(SecurityModel, self).__init__(*args, **kwargs)

        user = get_user()
        if not local.DEBUG and user is not None:
            print(type(self), user, get_perms(user, self))

            need_perm = "view_"+str(self.__class__.__name__).lower()  # The permission necessary to access the current model
            if need_perm not in get_perms(user, self):
                raise PermissionDenied("Not allowed")

    def save(self, *args, **kwargs):
        create_perm = "add_"+str(self.__class__.__name__).lower()
        edit_perm = "change_"+str(self.__class__.__name__).lower()

        user = get_user()
        if not local.DEBUG and user is not None:

            perms = get_perms(user, self)

            if self.pk is None and create_perm not in perms:
                raise PermissionDenied("Not allowed")
            elif edit_perm not in perms:
                raise PermissionDenied("Not allowed")

        super(SecurityModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        delete_perm = "delete_"+str(self.__class__.__name__).lower()

        user = get_user()
        if not local.DEBUG and user is not None:
            perms = get_perms(user, self)

            if delete_perm not in perms:
                raise PermissionDenied("Not allowed")

        super(SecurityModel, self).delete(*args, **kwargs)
