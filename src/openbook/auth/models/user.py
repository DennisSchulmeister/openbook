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
from unfold.decorators          import display

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

    groups = models.ManyToManyField(
        "openbook_auth.Group",
        verbose_name       = _("Groups"),
        blank              = True,
        help_text          = _("The groups this user belongs to. A user will get all permissions granted to each of their groups."),
        related_name       = "user_set",
        related_query_name = "user",
    )

    @display(header=True, description=_("Full Name"))
    def full_name(self, obj=None):
        """
        Name, e-mail and profile picture. Note that Django Unfold only supports this in the
        changelist not on the detail page.
        """
        if self.first_name and self.last_name:
            initials = f"{self.first_name[0]}{self.last_name[0]}"
        elif self.first_name:
            initials = self.first_name.zfill(2)[:2].strip()
        elif self.last_name:
            initials = self.last_name.zfill(2)[:2].strip()
        else:
            initials = self.username.zfill(2)[:2].strip()

        return (
            self.get_full_name(),
            self.email,
            initials.upper(),
            {
                "path":       self.profile.picture.url if self.profile and self.profile.picture else "",
                "borderless": True,
                "squared":    True,
            }
        )