# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.core.exceptions     import ValidationError as DjangoValidationError
from rest_framework.exceptions  import ValidationError as DRFValidationError
from rest_framework.permissions import DjangoObjectPermissions, IsAuthenticatedOrReadOnly
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets    import ModelViewSet

class ImprovedModelSerializer(ModelSerializer):
    """
    Reuse full cleaning and validation logic on the model's in the REST API, including
    `full_clean()`, `clean()`, field validation and uniqueness checks. Also make sure,
    that the pre-filled model instance can be accessed in the DRF view.
    """
    def validate(self, attrs):
        # Create or update instance for validation and cache for access in view
        self._instance = self.instance or self.Meta.model()

        for attr, value in attrs.items():
            setattr(self._instance, attr, value)

        try:
            self._instance.full_clean()
        except DjangoValidationError as e:
            # Convert Django's ValidationError to DRF's ValidationError
            raise DRFValidationError(e.message_dict)

        return attrs

    def get_prefilled_instance(self):
        """
        Method to access the pre-filled model instance in `ImprovedModelViewSet`.
        """
        return getattr(self, '_instance', None)

class ImprovedModelViewSet(ModelViewSet):
    """
    Make sure that object permissions are also checked when creating new model instances.
    By default, DRF applies object permissions on the unmodified object right after reading
    it from the database, before changes are applied. Here, when a new object is created,
    we check the object initialized with all values.
    """
    permission_classes = [IsAuthenticatedOrReadOnly, DjangoObjectPermissions]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if hasattr(serializer, "get_prefilled_instance"):
            instance = serializer.get_prefilled_instance()
            self.check_object_permissions(request, instance)

        serializer.save()
        return Response(serializer.data, status=201)