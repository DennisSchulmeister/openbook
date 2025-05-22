# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.utils.translation                  import gettext_lazy as _
from drf_spectacular.utils                     import extend_schema_field
from rest_framework.serializers                import Field
from rest_framework.serializers                import ListField
from rest_framework.serializers                import ListSerializer
from rest_framework.serializers                import ValidationError

from openbook.core.serializers.mixins.active   import ActiveInactiveSerializerMixin
from openbook.core.serializers.mixins.text     import NameDescriptionListSerializerMixin
from openbook.core.serializers.mixins.uuid     import UUIDSerializerMixin
from ..models.enrollment_method                import EnrollmentMethod

class EnrollmentMethodReadSerializer(
    UUIDSerializerMixin,
    NameDescriptionListSerializerMixin,
    ActiveInactiveSerializerMixin,
):
    """
    Very short overview of only the very most important enrollment method fields to
    be embedded in parent models.
    """
    class Meta:
        model = EnrollmentMethod
        fields = (
            *UUIDSerializerMixin.Meta.fields,
            *NameDescriptionListSerializerMixin.Meta.fields,
            *ActiveInactiveSerializerMixin.Meta.fields,
        )
        read_only_fields = fields

@extend_schema_field(EnrollmentMethodReadSerializer)
class EnrollmentMethodReadField(Field):
    """
    Serializer field for reading an enrollment method.
    """
    def to_internal_value(self, data):
        raise RuntimeError("EnrollmentMethodReadField to write data. Use EnrollmentMethodWriteField, instead.")

    def to_representation(self, obj):
        return EnrollmentMethodReadSerializer(obj).data

@extend_schema_field(ListSerializer(child=EnrollmentMethodReadSerializer()))
class EnrollmentMethodListReadField(ListField):
    """
    Serializer field for reading multiple enrollment methods.
    """
    def __init__(self, **kwargs):
        self.child = EnrollmentMethodReadField()
        super().__init__(**kwargs)

    def to_representation(self, value):
        return [self.child.to_representation(item) for item in value.all()]
