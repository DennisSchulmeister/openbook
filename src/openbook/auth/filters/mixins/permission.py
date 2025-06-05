# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django_filters.filters import CharFilter

class PermissionsFilterMixin:
    """
    Mixin filter class for any model that has a M2M relationship on the Django permission object.
    This allows to filter queries by the full permission string. Use it like this:

    ```python
    class RoleFilter(PermissionsFilterMixin, filters.FilterSet):
        class Meta:
            model  = Role
            fields = […] # Only fields from model allowed!
            permissions_field = "public_permissions" # If not called `permissions`
    ```

    This works hand in hand with the shared `PermissionSerializer` class.
    """
    permissions = CharFilter(method="permissions_filter")

    class Meta:
        fields = {
            "permissions": ("exact",),
        }

    def permissions_filter(self, queryset, name, value):
        try:
            app_label, codename = value.split(".", 1)
        except ValueError:
            return queryset.none()
        
        permissions_field = self.Meta.permissions_field or "permissions"

        filters = {
            f"{permissions_field}__content_type__app_label": app_label,
            f"{permissions_field}__codename": codename,
        }

        return queryset.filter(**filters)

class PermissionFilterMixin(PermissionsFilterMixin):
    """
    Like `PermissionsFilterMixin` but for FK relationships to Django permissions
    """
    permission  = CharFilter(method="permissions_filter")
    permissions = None

    class Meta:
        fields = {
            "permission": ("exact",),
        }
        permissions_field = "permission"