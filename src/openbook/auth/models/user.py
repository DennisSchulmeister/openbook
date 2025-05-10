# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.auth.models import AbstractUser
from django.core.validators     import EmailValidator
from django.db                  import models
from django.utils.translation   import gettext_lazy as _

class User(AbstractUser):
    """
    Extension to Django's core user model to distinguish different user types. Not that other
    additional fields are stored in a separate `UserProfile` model with a 1:1 relationship.
    """
    class UserType(models.TextChoices):
        HUMAN = "human",  _("Human User")
        APP   = "app",    _("App User")
    
    user_type = models.CharField(verbose_name=_("User Type"), choices=UserType, default=UserType.HUMAN)
    email     = models.EmailField(_("E-Mail Address"), blank=False, null=False, validators=[EmailValidator])