# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.contenttypes.admin import GenericTabularInline
from ..                                import models

class MediaFileInline(GenericTabularInline):
    model           = models.MediaFile
    extra           = 1
    fields          = ["file_data", "file_name", "file_size", "mime_type"]
    readonly_fields = ["file_size", "mime_type"]
    classes         = ["collapse"]
