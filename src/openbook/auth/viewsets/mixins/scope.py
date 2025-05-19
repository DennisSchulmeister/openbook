# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

class ScopedRolesViewSetMixin:
    """
    DRF view set for classes whose model implements the `ScopedRolesMixin` and therefor
    acts as a permission scope for user roles. This maps the reduced write-fields for
    the `owner` and `public_permissions` when an entry is created or updated.
    """
    def create(self, validated_data):
        validated_data["owner"] = validated_data.pop("owner_username", None)

        instance = super().create(validated_data)
        instance.public_permissions.set(validated_data.pop("public_permission_strings", []))
        return instance

    def update(self, instance, validated_data):
        instance.owner = validated_data.pop("owner_username", instance.owner)

        instance = super().update(instance, validated_data)
        instance.public_permissions.set(validated_data.pop("public_permission_strings", []))
        return instance