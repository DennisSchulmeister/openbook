# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

import threading
from rest_framework.authentication import SessionAuthentication

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

class CurrentUserTrackingAuthentication(SessionAuthentication):
    """
    The same as above but for Django REST Framework, which wraps the plain Django
    request object and resolves the user only when first accessed. Because of this
    the middleware above only sees the initial anonymous user.
    """
    def authenticate(self, request):
        result = super().authenticate(request)

        if result is not None:
            user, _ = result
            thread_local.current_user = user

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
