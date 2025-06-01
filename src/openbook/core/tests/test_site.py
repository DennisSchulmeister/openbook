# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.test                           import TestCase
from django.urls                           import reverse
from rest_framework.test                   import APIClient

from openbook.auth.models                  import AnonymousPermission
from openbook.auth.utils                   import permission_for_perm_string
from openbook.auth.middleware.current_user import reset_current_user
from ..models.site                         import Site

class Site_ViewSet_Tests(TestCase):
    """
    Tests for the `SiteViewSet` REST API.
    """
    def setUp(self):
        self.client = APIClient()
        reset_current_user()

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

        self.anonymous_permission = AnonymousPermission.objects.create(
            permission = permission_for_perm_string("openbook_core.view_site")
        )

        self.url_list   = reverse("site-list")
        self.url_site1  = reverse("site-detail", args=(self.site1.id,))
        self.url_health = reverse("site-health")

    def test_anonymous_permission(self):
        """
        Cannot access data without anonymous permission.
        """
        self.anonymous_permission.delete()

        response = self.client.get(self.url_list)
        self.assertEqual(response.data["count"], 0)

        response = self.client.get(self.url_site1)
        self.assertEqual(response.status_code, 403)

    def test_list_returns_all_sites(self):
        """
        List endpoint should return all sites.
        """
        response = self.client.get(self.url_list)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 2)
        self.assertEqual(len(response.data["results"]), 2)

    def test_filter_by_domain(self):
        """
        List endpoint should filter by domain.
        """
        response = self.client.get(self.url_list, {"domain": "example"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["domain"], "example.com")

    def test_filter_by_name(self):
        """
        List endpoint should filter by name.
        """
        response = self.client.get(self.url_list, {"name": "Test"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["name"], "Test Site")

    def test_filter_by_short_name(self):
        """
        List endpoint should filter by short_name.
        """
        response = self.client.get(self.url_list, {"short_name": "Ex"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["short_name"], "Example")

    def test_search_query_param(self):
        """
        List endpoint should support the _search query parameter.
        """
        response = self.client.get(self.url_list, {"_search": "Test"})

        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(response.data["count"], 1)

    def test_sort_query_param(self):
        """
        List endpoint should support the _sort query parameter.
        """
        response = self.client.get(self.url_list, {"_sort": "-name"})
        self.assertEqual(response.status_code, 200)

        names = [site["name"] for site in response.data["results"]]
        self.assertEqual(names, sorted(names, reverse=True))

    def test_pagination(self):
        """
        List endpoint should support pagination with _page and _page_size.
        """
        response = self.client.get(self.url_list, {"_page": 1, "_page_size": 1})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 2)
        self.assertEqual(len(response.data["results"]), 1)

    def test_health_endpoint(self):
        """
        Health endpoint should return status GOOD.
        """
        response = self.client.get(self.url_health)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "GOOD")

