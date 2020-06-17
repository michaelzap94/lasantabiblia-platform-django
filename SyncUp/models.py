from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class SyncUp(models.Model):
    # The related_name attribute specifies the name of the reverse relation from the User model back to your model
    user = models.OneToOneField( settings.AUTH_USER_MODEL, related_name='sync_up', on_delete=models.CASCADE )
    version = models.IntegerField(default=0)
    last_device = models.CharField(blank=True, null=True,max_length=200, default=None)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email
