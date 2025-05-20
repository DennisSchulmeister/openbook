# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django_filters.filterset import FilterSet
from django_filters.filters   import CharFilter

class ValidityTimeSpanFilterMixin(FilterSet):
    """
    Mixin filter class for any model that implements the `ValidityTimeSpanMixin` and therefor
    has a `start_date` and `end_date`.
    """
    class Meta:
        fields = {
            "start_date": ("exact", "lte", "gte"),
            "end_date":   ("exact", "lte", "gte"),
        }

class DurationFilterMixin(FilterSet):
    """
    Mixin filter class for any model that implements the `DurationMixin` and therefor has a
    `duration_value` and `duration_period`.
    """
    class Meta:
        fields = {
            "duration_value": ("exact", "lte", "gte"),
            "duration_period": ("exact",),
        }