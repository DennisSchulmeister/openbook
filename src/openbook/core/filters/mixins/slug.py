# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django_filters.filterset import FilterSet
from django_filters.filters   import CharFilter

class SlugFilterMixin(FilterSet):
    """
    Mixin filter class for any model that implements any of the slug mixins and therefor
    has a `slug` field.
    """
    class Meta:
        fields = {"slug": ("exact",)}