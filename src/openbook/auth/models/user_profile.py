# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.conf                import settings
from django.db                  import models
from django.db.models.signals   import post_save
from django.dispatch            import receiver
from django.utils.translation   import gettext_lazy as _

from openbook.core.models.utils import calc_file_path

class UserProfile(models.Model):
    """
    User profile with additional values for each user.
    """
    def _calc_file_path(self, filename):
        return calc_file_path(self._meta, self.id, filename)
    
    user        = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE, related_name="profile")
    description = models.TextField(verbose_name=_("Description"), blank=True, null=False)
    picture     = models.FileField(verbose_name=_("Profile Picture"), upload_to=_calc_file_path, null=True, blank=True)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, created, instance, **kwargs):
    """
    Automatically create a user profile for each new user. Since signals are not running
    for bulk operations, other code should not presume that a user profile always exists.
    """
    if not created:
        return
    
    UserProfile.objects.create(user=instance)