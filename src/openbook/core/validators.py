# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.core.exceptions   import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _
from PIL                      import Image

@deconstructible
class ValidateImage:
    """
    Validate image uploads so that only image files with an allowed maximum
    size are accepted.
    """
    def __init__(self, max_size=1024*1024):
        self.max_size = max_size

    def __call__(self, value):
        try:
            image = Image.open(value)
            image.verify()
            image.close()
        except IOError:
            raise ValidationError(_("Invalid image file"))

        if value.size > self.max_size:
            max_size_mb = self.max_size / (1024*1024)
            raise ValidationError(_("Image file too large (max %(max_size_mb).2fMB)"), params={"max_size_mb": max_size_mb})
