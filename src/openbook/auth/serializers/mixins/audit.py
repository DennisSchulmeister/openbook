# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from rest_framework.serializers import ModelSerializer
from ..user                     import UserReadField

class CreatedModifiedBySerializerMixin(ModelSerializer):
    """
    Mixin class for model serializers whose model implement the `CreatedModifiedByMixin` and
    therefor contain the audit fields `created_by`, `created_at`, `modified_by` and `modified_at`.
    """
    created_by  = UserReadField(read_only=True)
    modified_by = UserReadField(read_only=True)

    class Meta:
        fields = ("created_by", "created_at", "modified_by", "modified_at")
        read_only_fields = ("created_at", "modified_at")