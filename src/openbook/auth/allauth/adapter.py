# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from allauth.account.adapter  import DefaultAccountAdapter as AllauthDefaultAccountAdapter
from django.core.exceptions   import ValidationError
from django.http              import HttpRequest
from django.utils.text        import format_lazy as _f

from ..models.auth_config     import AuthConfig

class DefaultAccountAdapter(AllauthDefaultAccountAdapter):
    """
    Adapted behavior for local account registration.
    """
    def is_open_for_signup(self, request: HttpRequest):
        """
        Check whether local account registration is allowed.
        """
        try:
            auth_config = AuthConfig.get_for_default_site()
            return auth_config.local_signup_allowed
        except AuthConfig.DoesNotExist:
            pass
        
        return True

    def clean_email(self, email: str) -> str:
        """
        Restrict local account e-mail to e-mails with a certain suffix.
        """
        try:
            auth_config  = AuthConfig.get_for_default_site()
            email_suffix = auth_config.signup_email_suffix.strip()

            if not email.endswith(email_suffix):
                raise ValidationError(_f("This e-mail is not allowed to sign-up. The e-mail must end with {suffix}", suffix=email_suffix))
        except AuthConfig.DoesNotExist:
            pass
        
        return email