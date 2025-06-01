# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.test   import TestCase
from django.urls   import reverse

from openbook.test import ModelViewSetTestMixin
from ..models.site import Site

class Site_ViewSet_Tests(ModelViewSetTestMixin, TestCase):
    """
    Tests for the `SiteViewSet` REST API.
    """
    base_name     = "site"
    model         = Site
    pk_found      = 1
    search_string = "test"
    search_count  = 1
    sort_field    = "brand_color"

    def setUp(self):
        super().setUp()

        self.site1 = Site.objects.create(
            id          = 1,
            domain      = "example.com",
            name        = "Example Site",
            short_name  = "Example",
            about_url   = "https://example.com/about",
            brand_color = "#FFFFFF",
        )

        self.site2 = Site.objects.create(
            id          = 2,
            domain      = "test.com",
            name        = "Test Site",
            short_name  = "Test",
            about_url   = "https://test.com/about",
            brand_color = "#777777",
        )

        self.url_list   = reverse("site-list")
        self.url_site1  = reverse("site-detail", args=(self.site1.id,))
        self.url_health = reverse("site-health")

    def assertHealthStatus(self, response):
        self.assertEqual(response.data["status"], "GOOD")

    operations = {
        "list":           {"requires_auth": False},
        "retrieve":       {"requires_auth": False},
        "create":         {"supported": False},
        "update":         {"supported": False},
        "partial_update": {"supported": False},
        "destroy":        {"supported": False},

        "health": {
            "supported":          True,
            "http_method":        ModelViewSetTestMixin.HttpMethod.GET,
            "status_code":        200,      # Okay
            "url_suffix":         "health",
            "requires_auth":      False,
            "model_permission":   (),
            "assertions":         (assertHealthStatus,),
        },
    }
