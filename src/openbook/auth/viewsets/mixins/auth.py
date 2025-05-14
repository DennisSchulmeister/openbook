# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

class ScopedRolesViewSetMixin:
    """
    DRF view set for classes that have a read-only `owner` and a write-only `owner_username`
    field, usually because the models implement the `ScopedRolesMixin`.
    """
    def create(self, validated_data):
        validated_data["owner"] = validated_data.pop("owner_username", None)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.owner = validated_data.pop("owner_username", instance.owner)
        return super().update(instance, validated_data)