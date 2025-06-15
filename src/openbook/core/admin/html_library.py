# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.utils.translation          import gettext_lazy as _
from import_export.fields              import Field
from unfold.admin                      import StackedInline
from unfold.admin                      import TabularInline
from unfold.sections                   import TableSection

from openbook.admin                    import CustomModelAdmin
from openbook.admin                    import ImportExportModelResource
from openbook.auth.admin.mixins.audit  import created_modified_by_fields
from openbook.auth.admin.mixins.audit  import created_modified_by_fieldset
from openbook.auth.admin.mixins.audit  import created_modified_by_filter
from ..import_export.boolean           import BooleanWidget
from ..models.html_library             import HTMLLibrary
from ..models.html_library             import HTMLLibraryText
from ..models.html_library             import HTMLLibraryVersion

class HTMLLibraryResource(ImportExportModelResource):
    published = Field(attribute="published", widget=BooleanWidget())

    class Meta:
        model = HTMLLibrary
        fields = [
            "id", "delete",
            "organization", "name",
            "author", "license",
            "website", "coderepo", "bugtracker",
            "published",
        ]

    @classmethod
    def get_display_name(cls):
        return _("HTML Libraries")

class HTMLLibraryVersionResource(ImportExportModelResource):
    class Meta:
        model = HTMLLibraryVersion
        fields = [
            "id", "delete",
            "parent", "version", "dependencies", "frontend_url",
            "file_data",    ### TEST
            "file_name", "file_size", "mime_type",
        ]

    @classmethod
    def get_display_name(cls):
        return _("HTML Library Versions")

    def filter_export(self, queryset, **kwargs):
        """
        Needed because by default it is not possible to export another model than the one
        from the admin view.
        """
        return self._meta.model.objects.all()

class _HTMLLibraryVersionSection(TableSection):
    verbose_name = _("Versions")
    related_name = "versions"
    fields       = ["version", "frontend_url", "file_name", "file_size", "mime_type",]

class _HTMLLibraryVersionInline(StackedInline):
    model               = HTMLLibraryVersion
    ordering            = ["-version"]
    readonly_fields     = ["frontend_url", "file_name", "file_size", "mime_type"]
    extra               = 0
    show_change_link    = True
    tab                 = True
    verbose_name        = _("Version")
    verbose_name_plural = _("Versions")

    fieldsets = [
        (None, {
                "fields": [
                    ("version", "frontend_url"),
                    ("file_data", "file_size"),
                    "dependencies",
                ],
        }),
    ]

class HTMLLibraryTextResource(ImportExportModelResource):
    class Meta:
        model = HTMLLibraryText
        fields = (
            "id", "delete",
            "parent", "language", "short_description"
        )

    @classmethod
    def get_display_name(cls):
        return _("HTML Library Translations")
    
    def filter_export(self, queryset, **kwargs):
        """
        Needed because by default it is not possible to export another model than the one
        from the admin view.
        """
        return self._meta.model.objects.all()

class _HTMLLibraryTextInline(TabularInline):
    model               = HTMLLibraryText
    fields              = ["language", "short_description"]
    ordering            = ["language"]
    extra               = 0
    show_change_link    = True
    tab                 = True
    verbose_name        = _("Translated Text")
    verbose_name_plural = _("Translated Texts")

class HTMLLibraryAdmin(CustomModelAdmin):
    model              = HTMLLibrary
    resource_classes   = [HTMLLibraryResource, HTMLLibraryVersionResource, HTMLLibraryTextResource]
    list_display       = ["fqn", "author", "license", "published", *created_modified_by_fields]
    list_display_links = ["fqn", "author", "license", "published"]
    list_filter        = ["organization", "author", "license", "published", *created_modified_by_filter]
    readonly_fields    = ["fqn", *created_modified_by_fields]
    search_fields      = ["organization", "name", "author"]
    ordering           = ["organization", "name"]
    list_sections      = [_HTMLLibraryVersionSection]
    inlines            = [_HTMLLibraryTextInline, _HTMLLibraryVersionInline]

    fieldsets = [
        (None, {
            "fields": ["organization", "name", "published"],
        }),
        (_("Meta Data"), {
            "classes": ["tab"],
            "fields": ["author", "license", "website", "coderepo", "bugtracker"],
        }),
        created_modified_by_fieldset,
    ]

    add_fieldsets = [
        (None, {
            "fields": ["organization", "name", "published"],
        }),
        (_("Meta Data"), {
            "classes": ["tab"],
            "fields": ["author", "license", "website", "coderepo", "bugtracker"],
        }),
    ]
