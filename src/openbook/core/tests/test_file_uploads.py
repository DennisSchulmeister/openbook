# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.auth                import get_user_model
from django.contrib.auth.models         import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile     import SimpleUploadedFile
from django.test                        import TestCase
from django.urls                        import reverse
from rest_framework.test                import APIClient
from uuid                               import uuid4

from ..models.file_uploads              import MediaFile

class MediaFile_Model_Tests(TestCase):
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

class MediaFile_ViewSet_Tests(TestCase):
    """
    Tests for the `MediaFileViewSet` REST API.
    """
    def setUp(self):
        User = get_user_model()

        content_type = ContentType.objects.get_for_model(MediaFile)
        permissions  = Permission.objects.filter(content_type=content_type)

        self.client_valid_user = APIClient()
        self.user_valid = User.objects.create_user(username="valid", password="password", email="valid@mail.com")
        self.user_valid.user_permissions.set(permissions)
        self.client_valid_user.force_authenticate(user=self.user_valid)

        self.user_invalid = User.objects.create_user(username="invalid", password="password", email="invalid@mail.com")
        self.client_invalid_user = APIClient()
        self.client_invalid_user.force_authenticate(user=self.user_invalid)

        self.dummy_model = ContentType.objects.get_for_model(ContentType)

        file_bytes1 = b"alpha content"
        file_bytes2 = b"beta content"
        file_bytes3 = b"gamma content"

        self.file1 = MediaFile.objects.create(
            content_type = self.dummy_model,
            object_id    = uuid4(),
            file_name    = "alpha.txt",
            file_size    = len(file_bytes1),
            mime_type    = "text/plain",
            file_data    = SimpleUploadedFile("alpha.txt", file_bytes1),
        )

        self.file2 = MediaFile.objects.create(
            content_type = self.dummy_model,
            object_id    = uuid4(),
            file_name    = "beta.txt",
            file_size    = len(file_bytes2),
            mime_type    = "text/plain",
            file_data    = SimpleUploadedFile("beta.txt", file_bytes2),
        )

        self.file3 = MediaFile.objects.create(
            content_type = self.dummy_model,
            object_id    = uuid4(),
            file_name    = "gamma.txt",
            file_size    = len(file_bytes3),
            mime_type    = "text/plain",
            file_data    = SimpleUploadedFile("gamma.txt", file_bytes3),
        )

    def test_list(self):
        """
        Should return all media files.
        """
        url = reverse("media_file-list")
        response = self.client_valid_user.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 3)
        self.assertEqual(len(response.data["results"]), 3)

    def test_search(self):
        """
        Should filter media files by file name using _search.
        """
        url = reverse("media_file-list")
        response = self.client_valid_user.get(url, {"_search": "beta"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["file_name"], "beta.txt")

    def test_sort(self):
        """
        Should sort media files by file name in ascending and descending order.
        """
        url = reverse("media_file-list")

        # Ascending order
        response = self.client_valid_user.get(url, {"_sort": "file_name"})
        self.assertEqual(response.status_code, 200)
        
        names = [item["file_name"] for item in response.data["results"]]
        self.assertEqual(names, sorted(names))

        # Descending order
        response = self.client_valid_user.get(url, {"_sort": "-file_name"})
        self.assertEqual(response.status_code, 200)
        
        names = [item["file_name"] for item in response.data["results"]]
        self.assertEqual(names, sorted(names, reverse=True))

    def test_pagination(self):
        """
        Should paginate media files using _page and _page_size.
        """
        url = reverse("media_file-list")

        response = self.client_valid_user.get(url, {"_page": 1, "_page_size": 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 2)
        
        response = self.client_valid_user.get(url, {"_page": 2, "_page_size": 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)

    def test_create(self):
        """
        Should create a new media file with valid permissions and file_data.
        """
        url = reverse("media_file-list")
        file_bytes = b"test content"
        file_data = SimpleUploadedFile("delta.txt", file_bytes)

        data = {
            "content_type": self.dummy_model.pk,
            "object_id":    str(uuid4()),
            "file_name":    "delta.txt",
            "file_size":    len(file_bytes),
            "mime_type":    "text/plain",
            "file_data":    file_data,
        }
        
        response = self.client_valid_user.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["file_name"], "delta.txt")

    def test_create_forbidden(self):
        """
        Should return 403 Forbidden when creating without permissions.
        """
        url = reverse("media_file-list")
        file_bytes = b"test content"
        file_data = SimpleUploadedFile("epsilon.txt", file_bytes)

        data = {
            "content_type": self.dummy_model.pk,
            "object_id":    str(uuid4()),
            "file_name":    "epsilon.txt",
            "file_size":    len(file_bytes),
            "mime_type":    "text/plain",
            "file_data":    file_data,
        }

        response = self.client_invalid_user.post(url, data)
        self.assertEqual(response.status_code, 404)

    def test_update(self):
        """
        Should update a media file with valid permissions and file_data.
        """
        url = reverse("media_file-detail", args=[self.file1.pk])
        file_bytes = b"test content"
        file_data = SimpleUploadedFile("alpha-renamed.txt", file_bytes)

        data = {
            "content_type": self.dummy_model.pk,
            "object_id":    str(self.file1.object_id),
            "file_name":    "alpha-renamed.txt",
            "file_size":    len(file_bytes),
            "mime_type":    "text/plain",
            "file_data":    file_data,
        }

        response = self.client_valid_user.put(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["file_name"], "alpha-renamed.txt")

    def test_update_forbidden(self):
        """
        Should return 403 Forbidden when updating without permissions.
        """
        url = reverse("media_file-detail", args=[self.file2.pk])
        file_bytes = b"test content"
        file_data = SimpleUploadedFile("beta-renamed.txt", file_bytes)

        data = {
            "content_type": self.dummy_model.pk,
            "object_id":    str(self.file2.object_id),
            "file_name":    "beta-renamed.txt",
            "file_size":    len(file_bytes),
            "mime_type":    "text/plain",
            "file_data":    file_data,
        }

        response = self.client_invalid_user.put(url, data)
        self.assertEqual(response.status_code, 404)

    def test_partial_update(self):
        """
        Should partially update a media file with valid permissions and file_data.
        """
        url = reverse("media_file-detail", args=[self.file3.pk])
        data = {"file_name": "gamma-renamed.txt"}
        response = self.client_valid_user.patch(url, data, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["file_name"], "gamma-renamed.txt")

    def test_partial_update_forbidden(self):
        """
        Should return 403 Forbidden when partially updating without permissions.
        """
        url = reverse("media_file-detail", args=[self.file3.pk])
        data = {"file_name": "gamma-renamed.txt"}
        response = self.client_invalid_user.patch(url, data)

        self.assertEqual(response.status_code, 404)

    def test_delete(self):
        """
        Should delete a media file with valid permissions.
        """
        url = reverse("media_file-detail", args=[self.file2.pk])
        response = self.client_valid_user.delete(url)

        self.assertEqual(response.status_code, 204)
        self.assertFalse(MediaFile.objects.filter(pk=self.file2.pk).exists())

    def test_delete_forbidden(self):
        """
        Should return 403 Forbidden when deleting without permissions.
        """
        url = reverse("media_file-detail", args=[self.file1.pk])
        response = self.client_invalid_user.delete(url)
        self.assertEqual(response.status_code, 404)

