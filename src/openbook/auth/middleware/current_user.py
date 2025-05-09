# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

import threading

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

def get_current_user():
    """
    Get the current request user, if any. Returns `None` otherwise.
    """
    return getattr(thread_local, "current_user", None)
