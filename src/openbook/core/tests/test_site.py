# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.test                import TestCase
from django.urls                import reverse
from rest_framework.test        import APIClient

from ..models.site              import Site

class Site_ViewSet_Tests(TestCase):
    """
    Tests for the `SiteViewSet` REST API.
    """
    def setUp(self):
        self.client = APIClient()

        self.site1 = Site.objects.create(
            id          = 1,
            domain      = "example.com",
            name        = "Example Site",
            short_name  = "Example",
            about_url   = "https://test1.com/about",
            brand_color = "#123456",
        )

        self.site2 = Site.objects.create(
            id          = 2,
            domain      = "test.com",
            name        = "Test Site",
            short_name  = "Test",
            about_url   = "https://test.com/about",
            brand_color = "#471115",
        )

    def test_list_returns_all_sites(self):
        """
        List endpoint should return all sites.
        """
        url = reverse("site-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 2)
        self.assertEqual(len(response.data["results"]), 2)

    def test_filter_by_domain(self):
        """
        List endpoint should filter by domain.
        """
        url = reverse("site-list")
        response = self.client.get(url, {"domain": "example"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["domain"], "example.com")

    def test_filter_by_name(self):
        """
        List endpoint should filter by name.
        """
        url = reverse("site-list")
        response = self.client.get(url, {"name": "Test"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["name"], "Test Site")

    def test_filter_by_short_name(self):
        """
        List endpoint should filter by short_name.
        """
        url = reverse("site-list")
        response = self.client.get(url, {"short_name": "Ex"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["short_name"], "Example")

    def test_search_query_param(self):
        """
        List endpoint should support the _search query parameter.
        """
        url = reverse("site-list")
        response = self.client.get(url, {"_search": "Test"})

        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(response.data["count"], 1)

    def test_sort_query_param(self):
        """
        List endpoint should support the _sort query parameter.
        """
        url = reverse("site-list")
        response = self.client.get(url, {"_sort": "-name"})
        self.assertEqual(response.status_code, 200)

        names = [site["name"] for site in response.data["results"]]
        self.assertEqual(names, sorted(names, reverse=True))

    def test_pagination(self):
        """
        List endpoint should support pagination with _page and _page_size.
        """
        url = reverse("site-list")
        response = self.client.get(url, {"_page": 1, "_page_size": 1})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 2)
        self.assertEqual(len(response.data["results"]), 1)

    def test_health_endpoint(self):
        """
        Health endpoint should return status GOOD.
        """
        url = reverse("site-health")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "GOOD")

