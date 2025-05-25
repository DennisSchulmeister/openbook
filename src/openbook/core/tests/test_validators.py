# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.core.exceptions         import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test                    import TestCase
from io                             import BytesIO
from PIL                            import Image
from ..                             import validators

class TestValidateImage(TestCase):
    """
    Test cases for the `ValidateImage` validator class.
    """
    def setUp(self):
        image_object = Image.new('RGB', (100, 100), (255, 255, 255))
        image_bytes  = BytesIO()
        image_object.save(image_bytes, format="JPEG")

        self.validator     = validators.ValidateImage()
        self.valid_image   = SimpleUploadedFile("test.jpg", image_bytes.getvalue())
        self.invalid_image = SimpleUploadedFile("test.txt", b"not an image")

    def test_validate_image_valid(self):
        """
        Valid image should pass validation.
        """
        self.validator(self.valid_image)

    def test_validate_image_invalid(self):
        """
        Invalid image should fail validation.
        """
        with self.assertRaises(ValidationError):
            self.validator(self.invalid_image)

    def test_validate_image_too_large(self):
        """
        Too large image should fail validation.
        """
        validator = validators.ValidateImage(max_size=10)

        with self.assertRaises(ValidationError):
            validator(self.valid_image)