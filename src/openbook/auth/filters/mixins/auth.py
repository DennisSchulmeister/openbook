# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django_filters.filterset import FilterSet
from django_filters.filters   import CharFilter

class ScopedRolesFilterMixin(FilterSet):
    """
    Mixin filter class for any model that implements the `ScopedRolesMixin` and as such has
    an `owner` field.
    """
    owner = CharFilter(method="owner_filter")

    class Meta:
        fields = {"owner": ("exact",)}

    def owner_filter(self, queryset, name, value):
        return queryset.filter(owner__username=value)

class ScopeFilterMixin(FilterSet):
    """
    Mixin filter class for any model that implements the `ScopedMixin` and therefor has
    a `scope_type` field.
    """
    scope_type = CharFilter(method="scope_type_filter")

    class Meta:
        fields = {
            "scope_type": ("exact",),
            "scope_uuid": ("exact",),
        }
    
    def scope_type_filter(self, queryset, name, value):
        app_label, model = value.split(".", 1)

        return queryset.filter(
            scope_type__app_label = app_label,
            scope_type__model     = model,
        )