# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.


from django.contrib.auth   import get_user_model
from import_export.widgets import ForeignKeyWidget
from import_export.widgets import ManyToManyWidget

class UserForeignKeyWidget(ForeignKeyWidget):
    """
    A customized foreign-key widget that exports and imports users with their username.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(model=get_user_model(), field="username", *args, **kwargs)

class UserManyToManyWidget(ManyToManyWidget):
    """
    A customized many-to-many widget that exports and imports users with their username.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(model=get_user_model(), field="username", *args, **kwargs)