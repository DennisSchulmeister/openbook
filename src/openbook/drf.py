# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.


from collections                import defaultdict

from django.conf                import settings
from django.core.exceptions     import ValidationError as DjangoValidationError
from rest_framework             import status
from rest_framework.exceptions  import ValidationError as DRFValidationError
from rest_framework.filters     import BaseFilterBackend
from rest_framework.pagination  import PageNumberPagination as DRFPageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.permissions import BasePermission
from rest_framework.permissions import DjangoObjectPermissions
from rest_framework.response    import Response
from rest_framework.serializers import ModelSerializer as DRFModelSerializer

class AllowNone(BasePermission):
    """
    Sentinel permission to rejects all access set as default permission in `settings.py`.
    This ensures that no view set is accidentally unprotected.
    """
    def has_permission(self, request, view):
        return False

class PageNumberPagination(DRFPageNumberPagination):
    """
    Custom pagination class that allows changing the query parameters used for pagination
    in the Django config, following the same style the DRF uses for the filter backends.
    """
    page_query_param      = settings.REST_FRAMEWORK.get("PAGE_PARAM", "_page")
    page_size_query_param = settings.REST_FRAMEWORK.get("PAGE_SIZE_PARAM", "_page_size")

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
        "OPTIONS": ["%(app_label)s.view_%(model_name)s"],
        "HEAD":    ["%(app_label)s.view_%(model_name)s"],
        "POST":    ["%(app_label)s.add_%(model_name)s"],
        "PUT":     ["%(app_label)s.change_%(model_name)s"],
        "PATCH":   ["%(app_label)s.change_%(model_name)s"],
        "DELETE":  ["%(app_label)s.delete_%(model_name)s"],
    }

    def has_permission(self, request, view):
        # Always True to avoid PermissionDenied.
        # Our authentication backend checks model-permissions as fallback, instead.
        return True

class DjangoObjectPermissionsFilter(BaseFilterBackend):
    """
    Filter implementation inspired by `django-rest-framework-guardian2` `ObjectPermissionsFilter`.
    Filters out all objects from a queryset for which the user has no object-level view permission.
    """
    def filter_queryset(self, request, queryset, view):
        app_label   = queryset.model._meta.app_label
        model_name  = queryset.model._meta.model_name
        perm_string = f"{app_label}.view_{model_name}"
        allowed_pks = []

        for obj in queryset:
            if request.user.has_perm(perm_string, obj):
                allowed_pks.append(obj.pk)

        return queryset.model.objects.filter(pk__in=allowed_pks)

class ModelSerializer(DRFModelSerializer):
    """
    Reuse full cleaning and validation logic of the models in the REST API, including
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
    Ensure that object permissions are also checked when creating new model instances.
    DRF checks object permissions on database-loaded objects, but during creation,
    the object doesn't exist yet. Here we validate the input and construct the instance
    before saving to allow permission checks.

    NOTE: This is a mixin that must be used together with `ModelViewSet` to avoid a mysterious
    circular import in DRF. To overwrite the implementation of `post()` the mixin must come first.

    ```python
    class MyViewSet(ModelViewSetMixin, ModelViewSet):
        pass
    ```
    """
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if hasattr(serializer, "get_prefilled_instance"):
            # Use custom method to construct the instance
            instance = serializer.get_prefilled_instance()
        else:
            # Default behavior: construct the instance manually
            instance = serializer.Meta.model(**serializer.validated_data)

        self.check_object_permissions(request, instance)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class AllowAnonymousListViewSetMixin:
    """
    Small view set mixin class that allows unrestricted access to the `list` action while
    deferring permission checks for all other actions to the permission classes of the
    view set (usually defined in `settings.py`).
    """
    def get_permissions(self):
        if self.action == "list":
            return (AllowAny(),)
        else:
            return super().get_permissions()

OPERATION_ID_SUMMARY = {
    "list":           "List",
    "retrieve":       "Retrieve",
    "create":         "Create",
    "update":         "Update",
    "partial_update": "Partial Update",
    "destroy":        "Delete",
}

def add_tag_groups(result, **kwargs):
    """
    Builds x-tagGroups for drf-spectacular based on OpenAPI extensions:

    - `x-app-name`:   used for tag group
    - `x-model-name`: used as the tag for the endpoint
    """
    tag_groups = defaultdict(set)

    for path_item in result.get("paths", {}).values():
        for method, operation in path_item.items():
            if not isinstance(operation, dict):
                continue

            # Get tag info
            extensions = operation.get("extensions", operation)
            app_name   = extensions.get("x-app-name")
            model_name = extensions.get("x-model-name")

            if app_name and model_name:
                tag_groups[app_name].add(model_name)
                operation["tags"] = [model_name]

            # Parse operationId to assign friendly label
            operation_id = operation.get("operationId")

            if operation_id and not "summary" in operation:
                for action, summary in OPERATION_ID_SUMMARY.items():
                    if operation_id.endswith(f"_{action}"):
                        operation["summary"] = summary

    result["x-tagGroups"] = [
        {"name": app_name, "tags": sorted(tags)}
        for app_name, tags in sorted(tag_groups.items())
    ]

    return result