# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django_filters.filterset import FilterSet
from django_filters.filters   import CharFilter

class CreatedModifiedByFilterMixin(FilterSet):
    """
    Mixin filter class for any model that implements the `CreatedModifiedByMixin` and has the
    `created_by`, `created_at`, `modified_by` and `modified_at` fields.
    """
    created_by  = CharFilter(method="created_by_filter")
    modified_by = CharFilter(method="modified_by_filter")

    class Meta:
        fields = {
            "created_by":  ("exact",),
            "created_at":  ("exact", "lte", "gte"),
            "modified_by": ("exact",),
            "modified_at": ("exact", "lte", "gte"),
        }

    def created_by_filter(self, queryset, name, value):
        return queryset.filter(created_by__username=value)
    
    def modified_by_filter(self, queryset, name, value):
        return queryset.filter(modified_by__username=value)