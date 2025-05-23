# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile     import SimpleUploadedFile
from django.test                        import TestCase
from uuid                               import uuid4

from ..models.file_uploads              import MediaFile

class TestMediaFileSaveMethod(TestCase):
    """
    Test cases for the `save` method of `MediaFile`.
    """

    def test_save_populates_meta_data_fields(self):
        """
        Should populate the meta-data fields correctly for valid file data.
        """
        # Create a test file
        file_bytes = b"Hello, world!"
        file_data  = SimpleUploadedFile("test.txt", file_bytes)

        # Create an instance of MediaFile
        dummy_model = ContentType.objects.get_for_model(ContentType)
        file_model  = MediaFile(content_type=dummy_model, object_id=uuid4(), file_data=file_data)

        # Call the save method
        file_model.save()

        # Assert that the meta-data fields are populated correctly
        self.assertEqual(file_model.file_name, "test.txt")
        self.assertEqual(file_model.file_size, len(file_bytes))
        self.assertEqual(file_model.mime_type, "text/plain")

        # Clean up
        file_model.delete()

    def test_save_with_none_file_data(self):
        """
        Should not populate the meta-data fields for None file data.
        """
        # Create an instance of MediaFile with None file_data
        dummy_model = ContentType.objects.get_for_model(ContentType)
        file_model  = MediaFile(content_type=dummy_model, object_id=uuid4(), file_data=None)

        # Call the save method
        file_model.save()

        # Assert that the meta-data fields are not populated
        self.assertFalse(file_model.file_name)
        self.assertFalse(file_model.file_size)
        self.assertFalse(file_model.mime_type)

    def test_save_with_empty_file_data(self):
        """
        Should populate the meta-data fields correctly for empty file data.
        """
        # Create an empty file
        file_data = SimpleUploadedFile("empty.txt", b"")

        # Create an instance of MediaFile with empty file_data
        dummy_model = ContentType.objects.get_for_model(ContentType)
        file_model  = MediaFile(content_type=dummy_model, object_id=uuid4(), file_data=file_data)

        # Call the save method
        file_model.save()

        # Assert that the meta-data fields are populated correctly
        self.assertEqual(file_model.file_name, "empty.txt")
        self.assertEqual(file_model.file_size, 0)
        self.assertEqual(file_model.mime_type, "text/plain")

        # Clean up
        file_model.delete()

    def test_save_with_invalid_file_data(self):
        """
        Should raise an error for invalid file data.
        """
        # Create an instance of MediaFile with invalid file_data
        dummy_model = ContentType.objects.get_for_model(ContentType)
        file_model  = MediaFile(content_type=dummy_model, object_id=uuid4(), file_data=" invalid file data ")

        # Call the save method
        with self.assertRaises(FileNotFoundError):
            file_model.save()