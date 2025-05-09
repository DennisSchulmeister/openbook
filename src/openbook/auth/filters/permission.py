# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django_filters.filters import CharFilter

class PermissionFilterMixin:
    """
    Mixin filter class for any model that has a many-to-many relationship on the Django
    permission object called `permissions`. This allows to filter queries by the full
    permission string. Use it like this:

    ```python
    class RoleFilter(PermissionFilterMixin, filters.FilterSet):
        class Meta:
            model  = Role
            fields = […] # Only fields from model allowed!
    ```

    This works hand in hand with the shared `PermissionSerializer` class.
    """
    perm = CharFilter(method="filter_by_perm")

    def filter_by_perm(self, queryset, name, value):
        try:
            app_label, rest = value.split(".", 1)
            model_name, codename = rest.split("_", 1)
        except ValueError:
            return queryset.none()

        return queryset.filter(
            permissions__content_type__app_label=app_label,
            permissions__content_type__model=model_name,
            permissions__codename=codename,
        )