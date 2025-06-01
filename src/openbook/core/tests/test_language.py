# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.test          import TestCase
from django.urls          import reverse
from rest_framework.test  import APIClient

from openbook.auth.models import AnonymousPermission
from openbook.auth.utils  import permission_for_perm_string
from ..models.language    import Language

class Language_ViewSet_Tests(TestCase):
    """
    Tests for the `LanguageViewSet` REST API.
    """
    def setUp(self):
        Language.objects.create(language="en", name="English")
        Language.objects.create(language="de", name="Deutsch")
        Language.objects.create(language="fr", name="Français")

        AnonymousPermission.objects.create(permission=permission_for_perm_string("openbook_core.view_language"))

        self.client = APIClient()

    def test_list_languages(self):
        """
        Should return all available languages.
        """
        url = reverse("language-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 3)

    def test_filter_by_name(self):
        """
        Should filter languages by name (case-insensitive, partial match).
        """
        url = reverse("language-list")
        response = self.client.get(url, {"name": "deu"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["name"], "Deutsch")

    def test_search_by_language_code(self):
        """
        Should search languages by language code.
        """
        url = reverse("language-list")
        response = self.client.get(url, {"_search": "fr"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["language"], "fr")

    def test_sort_by_name(self):
        """
        Should sort languages by name in ascending and descending order.
        """
        url = reverse("language-list")

        # Ascending order
        response = self.client.get(url, {"_sort": "name"})
        self.assertEqual(response.status_code, 200)

        names = [item["name"] for item in response.data["results"]]
        self.assertEqual(names, sorted(names))

        # Descending order
        response = self.client.get(url, {"_sort": "-name"})
        self.assertEqual(response.status_code, 200)
        
        names = [item["name"] for item in response.data["results"]]
        self.assertEqual(names, sorted(names, reverse=True))

    def test_pagination(self):
        """
        Should paginate results using _page_size and _page query parameters.
        """
        url = reverse("language-list")

        # Page size 2, first page
        response = self.client.get(url, {"_page_size": 2, "_page": 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 2)

        # Page size 2, second page
        response = self.client.get(url, {"_page_size": 2, "_page": 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)