# ValidityTimeSpanSerializerMixin# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from rest_framework.serializers import ModelSerializer

class ValidityTimeSpanSerializerMixin(ModelSerializer):
    """
    Mixin class for model serializers whose models implement the `ValidityTimeSpanMixin`
    and therefor have a `start_date` and `end_date`
    """
    class Meta:
        fields = ("start_date", "end_date")
        read_only_fields = ()

class DurationSerializerMixin(ModelSerializer):
    """
    Mixin class for model serializers whose models implement the `DurationMixin` and therefor
    have a `duration_value` and `duration_period`
    """
    class Meta:
        fields = ("duration_value", "duration_period")
        read_only_fields = ()