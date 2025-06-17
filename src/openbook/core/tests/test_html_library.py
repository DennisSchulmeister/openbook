# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.test                           import TestCase

from openbook.auth.middleware.current_user import reset_current_user
from openbook.test                         import ModelViewSetTestMixin
from ..models.html_component               import HTMLComponent
from ..models.html_component               import HTMLComponentDefinition
from ..models.html_library                 import HTMLLibrary
from ..models.html_library                 import HTMLLibraryText
from ..models.html_library                 import HTMLLibraryVersion
from ..models.language                     import Language

class HTMLLibrary_Test_Mixin:
    def setUp(self):
        super().setUp()
        reset_current_user()

        # Languages
        self.language_de = Language.objects.create(language="de", name="Deutsch")
        self.language_fr = Language.objects.create(language="fr", name="Français")
        self.language_en = Language.objects.create(language="en", name="English")

        # Library 1
        self.lib1 = HTMLLibrary.objects.create(
            organization = "testorg1",
            name         = "lib1",
            author       = "John Q. Public",
            license      = "AGPL3",
            website      = "https://example1.com",
            coderepo     = "https://github.com/example1/lib1",
            bugtracker   = "https://github.com/example1/lib1/issues",
            readme       = "Read me 1",
            text_format  = "MD",
            published    = True,
        )

        self.lib1_text_en = HTMLLibraryText.objects.create(
            parent            = self.lib1,
            language          = self.language_en,
            short_description = "Test Library 1"
        )

        self.lib1_text_de = HTMLLibraryText.objects.create(
            parent            = self.lib1,
            language          = self.language_de,
            short_description = "Test-Bibliothek 1"
        )

        self.lib1_v1 = HTMLLibraryVersion.objects.create(
            parent       = self.lib1,
            version      = "1.0.0",
            dependencies = {"@test/other1": ">=1.0.0"}
        )

        self.lib1_v2 = HTMLLibraryVersion.objects.create(
            parent       = self.lib1,
            version      = "2.0.0",
            dependencies = {"@test/other1": ">=2.0.0"}
        )

        self.lib1_c1    = HTMLComponent.objects.create(library=self.lib1, tag_name="test-1")
        self.lib1_c1_d1 = HTMLComponentDefinition.objects.create(html_component=self.lib1_c1, library_version=self.lib1_v1, definition={})
        self.lib1_c1_d2 = HTMLComponentDefinition.objects.create(html_component=self.lib1_c1, library_version=self.lib1_v2, definition={})
        
        self.lib1_c2    = HTMLComponent.objects.create(library=self.lib1, tag_name="test-2")
        self.lib1_c2_d1 = HTMLComponentDefinition.objects.create(html_component=self.lib1_c2, library_version=self.lib1_v1, definition={})
        self.lib1_c2_d2 = HTMLComponentDefinition.objects.create(html_component=self.lib1_c2, library_version=self.lib1_v2, definition={})

        self.lib1_c3    = HTMLComponent.objects.create(library=self.lib1, tag_name="test-3")

        # Library 2
        self.lib2 = HTMLLibrary.objects.create(
            organization = "testorg2",
            name         = "lib2",
            author       = "Joe Doe",
            license      = "AGPL3",
            website      = "https://example2.com",
            coderepo     = "https://github.com/example2/lib2",
            bugtracker   = "https://github.com/example2/lib2/issues",
            readme       = "Read me 2",
            text_format  = "MD",
            published    = True,
        )

        self.lib2_text_en = HTMLLibraryText.objects.create(
            parent            = self.lib2,
            language          = self.language_en,
            short_description = "Test Library 2"
        )

        self.lib2_v1 = HTMLLibraryVersion.objects.create(
            parent       = self.lib2,
            version      = "1.0.0",
            dependencies = {"@test/other2": ">=1.0.0"}
        )

        self.lib_v2 = HTMLLibraryVersion.objects.create(
            parent       = self.lib2,
            version      = "2.0.0",
            dependencies = {"@test/other2": ">=2.0.0"}
        )
        
class HTMLLibrary_ViewSet_Tests(ModelViewSetTestMixin, HTMLLibrary_Test_Mixin, TestCase):
    """
    Tests for the `HTMLLibraryViewSet` REST API.
    """
    base_name         = "html_library"
    model             = HTMLLibrary
    search_string     = "testorg1"
    search_count      = 1
    sort_field        = "name"
    expandable_fields = ["translations[]", "versions[]", "created_by", "modified_by"]

    def pk_found(self):
        return self.lib1.pk
    
    operations = {
        "create": {
            "request_data": {
                "organization": "testorg3",
                "name":         "lib3",
                "author":       "Johnny Text",
                "license":      "AGPL3",
                "website":      "https://example3.com",
                "coderepo":     "https://github.com/example3/lib3",
                "bugtracker":   "https://github.com/example3/lib3/issues",
                "readme":       "Read me 3",
                "text_format":  "MD",
                "published":    True,
            },
        },
        "update": {
            "request_data": {
                "organization": "testorg3-changed",
                "name":         "lib3-changed",
                "author":       "Changed Author",
                "license":      "Changed License",
                "website":      "https://example3-changed.com",
                "coderepo":     "https://github.com/example3-changed/lib3",
                "bugtracker":   "https://github.com/example3/lib3-changed/issues",
                "readme":       "Changed Readme",
                "text_format":  "HTML",
                "published":    False,
            },
            "updates":      {
                "organization": "testorg3-changed",
                "name":         "lib3-changed",
                "author":       "Changed Author",
                "license":      "Changed License",
                "website":      "https://example3-changed.com",
                "coderepo":     "https://github.com/example3-changed/lib3",
                "bugtracker":   "https://github.com/example3/lib3-changed/issues",
                "readme":       "Changed Readme",
                "text_format":  "HTML",
                "published":    False,
            },
        },
        "partial_update": {
            "request_data": {"published": False},
            "updates":      {"published": False},
        },
    }

class HTMLLibraryText_ViewSet_Tests(ModelViewSetTestMixin, HTMLLibrary_Test_Mixin, TestCase):
    """
    Tests for the `HTMLLibraryTextViewSet` REST API.
    """
    base_name         = "html_library_text"
    model             = HTMLLibraryText
    search_string     = "Library"
    search_count      = 2
    sort_field        = "language"
    expandable_fields = ["parent"]

    def pk_found(self):
        return self.lib1_text_en.pk

    def get_create_request_data(self):
        return {
            "parent":            self.lib1.pk,
            "language":          "fr",
            "short_description": "Bibliothèque de test 1"
        }

    def get_update_request_data(self):
        return {
            "parent":            self.lib1.pk,
            "language":          "fr",
            "short_description": "Bibliothèque de test 1 modifiée"
        }

    operations = {
        "create": {
            "request_data": get_create_request_data,
        },
        "update": {
            "request_data": get_update_request_data,
            "updates":      {"short_description": "Bibliothèque de test 1 modifiée"},
        },
        "partial_update": {
            "request_data": {"short_description": "Bibliothèque de test 1 modifiée à nouveau"},
            "updates":      {"short_description": "Bibliothèque de test 1 modifiée à nouveau"},
        },
    }

class HTMLLibraryVersion_ViewSet_Tests(ModelViewSetTestMixin, HTMLLibrary_Test_Mixin, TestCase):
    """
    Tests for the `HTMLLibraryVersionViewSet` REST API.
    """
    base_name         = "html_library_version"
    model             = HTMLLibraryVersion
    search_string     = "testorg1"
    search_count      = 2
    sort_field        = "version"
    expandable_fields = ["parent", "created_by", "modified_by"]

    def pk_found(self):
        return self.lib1_v1.pk

    def get_create_request_data(self):
        return {
            "parent":       self.lib1.pk,
            "version":      "3.0.0",
            "dependencies": {"@test/other1": ">=3.0.0"}
        }

    def get_update_request_data(self):
        return {
            "parent":       self.lib1.pk,
            "version":      "3.0.0-pre1",
            "dependencies": {"@test/other1": ">=3.0.0-pre1"}
        }
    
    operations = {
        "create": {
            "format":       "json",
            "content_type": None,
            "request_data": get_create_request_data,
        },
        "update": {
            "format":       "json",
            "content_type": None,
            "request_data": get_update_request_data,
            "updates":      {
                "version":      "3.0.0-pre1",
                "dependencies": {"@test/other1": ">=3.0.0-pre1"}
            },
        },
        "partial_update": {
            "format":       "json",
            "content_type": None,
            "request_data": {"version": "3.0.0-pre2"},
            "updates":      {"version": "3.0.0-pre2"},
        },
    }

class HTMLComponent_ViewSet_Tests(ModelViewSetTestMixin, HTMLLibrary_Test_Mixin, TestCase):
    """
    Tests for the `HTMLComponentViewSet` REST API.
    """
    base_name         = "html_component"
    model             = HTMLComponent
    search_string     = "test"
    search_count      = 3
    sort_field        = "tag_name"
    expandable_fields = ["library", "definitions[]"]

    def pk_found(self):
        return self.lib1_c1.pk

    def get_create_request_data(self):
        return {
            "library":   self.lib1.pk,
            "tag_name": "new-tag",
        }

    def get_update_request_data(self):
        return {
            "library":   self.lib1.pk,
            "tag_name": "changed-tag",
        }

    operations = {
        "create": {
            "request_data": get_create_request_data,
        },
        "update": {
            "request_data": get_update_request_data,
            "updates":      {"tag_name": "changed-tag"},
        },
        "partial_update": {
            "request_data": {"tag_name": "changed-tag"},
            "updates":      {"tag_name": "changed-tag"},
        },
    }

class HTMLComponentDefinition_ViewSet_Tests(ModelViewSetTestMixin, HTMLLibrary_Test_Mixin, TestCase):
    """
    Tests for the `HTMLComponentDefinitionViewSet` REST API.
    """
    base_name         = "html_component_definition"
    model             = HTMLComponentDefinition
    search_string     = "test"
    search_count      = 4
    sort_field        = ""
    expandable_fields = ["html_component", "library_version"]

    def pk_found(self):
        return self.lib1_c1_d1.pk

    def get_create_request_data(self):
        return {
            "html_component":  self.lib1_c3.pk,
            "library_version": self.lib1_v1.pk,
            "definition":      {},
        }

    def get_update_request_data(self):
        return {
            "html_component":  self.lib1_c3.pk,
            "library_version": self.lib1_v1.pk,
            "definition":      {"changed": True},
        }

    operations = {
        "create": {
            "format":       "json",
            "content_type": None,
            "request_data": get_create_request_data,
        },
        "update": {
            "format":       "json",
            "content_type": None,
            "request_data": get_update_request_data,
            "updates":      {"definition": {"changed": True}},
        },
        "partial_update": {
            "format":       "json",
            "content_type": None,
            "request_data": {"definition": {"changed": True}},
            "updates":      {"definition": {"changed": True}},
        },
    }