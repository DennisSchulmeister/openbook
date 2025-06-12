# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

import importlib, threading

from django.conf                   import settings
from drf_spectacular.extensions    import OpenApiAuthenticationExtension
from rest_framework.authentication import BaseAuthentication

thread_local = threading.local()

def CurrentUserMiddleware(get_response):
    """
    Save the current user in a thread-local variable so that it can be accessed
    within the model layer. This is done to auto-populate the `created_by` and
    `modified_by` fields of models that use the `CreatedModifiedByMixin` without
    needing to explicitly pass the user from the view layer to the model layer.
    """
    def middleware(request):
        thread_local.current_user = request.user
        return get_response(request)

    return middleware

class CurrentUserTrackingAuthentication(BaseAuthentication):
    """
    The same as above but for Django REST Framework, which wraps the plain Django
    request object and resolves the user only when first accessed. Because of this
    the middleware above only sees the initial anonymous user.
    """
    def __init__(self):
        """
        Dynamically import classes in the DRF setting _DEFAULT_AUTHENTICATION_CLASSES.
        We use this to re-implement the authentication logic in DRF, since we need to
        override DEFAULT_AUTHENTICATION_CLASSES to hook into it.
        """
        self.auth_classes = []

        for auth_class in settings.REST_FRAMEWORK["_DEFAULT_AUTHENTICATION_CLASSES"]:
            if isinstance(auth_class, str):
                auth_module, _, auth_class_name = auth_class.rpartition('.')
                auth_module = importlib.import_module(auth_module)
                auth_class = getattr(auth_module, auth_class_name)
            
            self.auth_classes.append(auth_class)

    def authenticate(self, request):
        result = False

        for auth_class in self.auth_classes:
            # Authenticate the same way DRF would do
            auth_obj = auth_class()
            result = auth_obj.authenticate(request)

            # Remember authenticated user
            if result is not None:
                user, _ = result
                thread_local.current_user = user
                break

        return result
    
def get_current_user():
    """
    Get the current request user, if any. Returns `None` otherwise.
    """
    return getattr(thread_local, "current_user", None)

def reset_current_user():
    """
    Needed for unit tests which all run in a single thread. Forget previous tests's
    user as it is probably not even existing anymore.
    """
    thread_local.current_user = None

class CurrentUserTrackingAuthExtension(OpenApiAuthenticationExtension):
    """
    To resolve the following warning: "could not resolve authenticator
    <class 'openbook.auth.middleware.current_user.CurrentUserTrackingAuthentication'>.
    There was no OpenApiAuthenticationExtension registered for that class.
    Try creating one by subclassing it. Ignoring for now."
    
    As it is defined, we are using session authentication despite our custom
    permission class (wich doesn't affect authentication at all)
    """
    target_class = CurrentUserTrackingAuthentication
    name         = "SessionAuthentication"  # name used in the schema"

    def get_security_definition(self, auto_schema):
        return {
            "type": "apiKey",
            "in":   "header",
            "name": "sessionId",
        }