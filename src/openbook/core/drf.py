# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.


from django.core.exceptions     import ValidationError as DjangoValidationError
from rest_framework.exceptions  import ValidationError as DRFValidationError
from rest_framework.permissions import BasePermission, DjangoObjectPermissions
from rest_framework.response    import Response
from rest_framework.serializers import ModelSerializer as DRFModelSerializer

class AllowNone(BasePermission):
    """
    Sentinel permission to rejects all access set as default permission in `settings.py`.
    This ensures that no view set is accidentally unprotected.
    """
    def has_permission(self, request, view):
        return False

class DjangoObjectPermissionsOnly(DjangoObjectPermissions):
    """
    Class `APIView`, which is a parent for `ModelViewSet` in Django REST Framework the method
    `check_permissions()` is called very early and later `check_object_permissions()`, too.
    Since `DjangoObjectPermissions` is a `DjangoModelPermissions` it implements both checks.
    But DRF raises an exception when either method returns `False`, thus inverting the logic
    in our own authentication backend. Also both classes don't check "view" permissions by default.

    This class replaces `DjangoObjectPermissions` with a version more in line with our own backend.
    """
    # Include "view" permission
    perms_map = {
        "GET":     ["%(app_label)s.view_%(model_name)s"],
        "OPTIONS": [],
        "HEAD":    [],
        "POST":    ["%(app_label)s.add_%(model_name)s"],
        "PUT":     ["%(app_label)s.change_%(model_name)s"],
        "PATCH":   ["%(app_label)s.change_%(model_name)s"],
        "DELETE":  ["%(app_label)s.delete_%(model_name)s"],
    }

    def has_permission(self, request, view):
        # Always True to avoid PermissionDenied.
        # Our authentication backend checks model-permissions as fallback, instead.
        True

class ModelSerializer(DRFModelSerializer):
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

class ModelViewSetMixin:
    """
    Make sure that object permissions are also checked when creating new model instances.
    By default, DRF applies object permissions on the unmodified object right after reading
    it from the database, before changes are applied. Here, when a new object is created,
    we check the object initialized with all values.

    NOTE: This is a mixin that must be used together with `ModelViewSet` to avoid a mysterious
    circular import in DRF. To overwrite the implementation of `post()` the mixin must come first.

    ```python
    class MyViewSet(ModelViewSetMixin, ModelViewSet):
        pass
    ```
    """
    permission_classes = [DjangoObjectPermissionsOnly]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if hasattr(serializer, "get_prefilled_instance"):
            instance = serializer.get_prefilled_instance()
            self.check_object_permissions(request, instance)

        serializer.save()
        return Response(serializer.data, status=201)