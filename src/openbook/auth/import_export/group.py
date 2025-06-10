# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from import_export.widgets import ForeignKeyWidget
from import_export.widgets import ManyToManyWidget
from ..models.group        import Group

class GroupForeignKeyWidget(ForeignKeyWidget):
    """
    A customized foreign-key widget that exports and imports groups with their slug.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(model=Group, field="slug", *args, **kwargs)

class GroupManyToManyWidget(ManyToManyWidget):
    """
    A customized many-to-many widget that exports and imports groups with their slug.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(model=Group, field="slug", *args, **kwargs)