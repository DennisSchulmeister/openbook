# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.admin               import RelatedOnlyFieldListFilter
from django.contrib.auth                import get_user_model
from django.contrib.auth.models         import Permission
from django.contrib.contenttypes.models import ContentType
from django.forms                       import ModelForm
from django.utils.translation           import gettext_lazy as _
from import_export.fields               import Field
from unfold.contrib.forms.widgets       import UnfoldAdminSelectWidget

from openbook.admin                     import ImportExportModelResource
from openbook.auth.utils                import perm_string_for_permission
from openbook.auth.utils                import permission_for_perm_string
from ...models.allowed_role_permission  import AllowedRolePermission
from ...models.mixins.auth              import ScopedRolesMixin
from ...validators                      import validate_permissions
from ...validators                      import validate_scope_type

scope_type_filter = ("scope_type", RelatedOnlyFieldListFilter)

permissions_fieldset = (_("Permissions"), {
    "classes": ("tab",),
    "fields": ("owner", "public_permissions"),
})

class ScopedRolesResourceMixin(ImportExportModelResource):
    """
    Mixin class for the import/export resource class of models that act as permissions
    scopes for user roles. Handles the import and export of the owner and public permissions.
    Note that the other scope fields (roles, enrollment methods, …) are not handled, because
    they are reverse relations for objects that support import/export themselves.
    """
    public_permissions = Field(column_name="")

    class Meta:
        fields = ("owner", "public_permissions")

    def dehydrate_owner(self, obj):
        """
        Export username instead of numeric PK for owner.
        """
        return obj.owner.username if obj.owner else ""

    def dehydrate_public_permissions(self, obj):
        """
        Export public permissions as white-space separated list of permission strings.
        """
        if not obj.public_permissions:
            return ""

        return " ".join([perm_string_for_permission(permission) for permission in obj.public_permissions.all()])

    def before_import_row(self, row, **kwargs):
        """
        Resolve owner and public permissions before import.
        """
        # Parse public permissions
        public_permissions = row.get("public_permissions") or ""
        row._parsed_permissions = []

        for public_permission in public_permissions.split():
            try:
                permission = permission_for_perm_string(public_permission)
                row._parsed_permissions.append(permission)
            except Permission.DoesNotExist:
                continue
        
        # Resolve owner
        owner = row.get("owner") or ""
        row["owner"] = None

        try:
            if owner:
                User = get_user_model()
                row["owner"] = User.objects.get(username=owner).pk
        except User.DoesNotExist:
            pass

    def after_save_instance(self, instance, row, **kwargs):
        """
        M2M relations can only be saved when the model instance already exists on the database.
        Therefor we cannot simply assign a list of objects to the M2M field in `before_import_row()`,
        as Django refuses direct assignments to M2M properties.
        """
        # Set public permissions M2M now that the row has been saved
        if hasattr(row, "_parsed_permissions"):
            instance.public_permissions.set(row._parsed_permissions)

class ScopeFormMixin(ModelForm):
    """
    Form mixin class for model forms where the model implements the `ScopeMixin`
    and therefor has two fields for scope type and scope uuid. The form mixin
    (this class) limits the list of scope types to valid choices and automatically
    updates the scope uuid list when the type is changed. Instead of the uuid the
    scope name will be shown in the select box.
    """
    class Meta:
        fields = ("scope_uuid",)

    class Media:
        css = {
            "all": ("openbook_auth/scope_uuid_autoload.css",)
        }
        js  = ("openbook_auth/scope_uuid_autoload.js",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "scope_type" in self.fields:
            # Reduce scope type to allowed values
            scope_types = []

            for content_type in ScopedRolesMixin.get_scope_model_content_types():
                scope_types.append((content_type.pk, content_type.name))

            self.fields["scope_type"].choices = scope_types

            if self.instance.pk:
                self.fields["scope_type"].disabled = True

        if "scope_uuid" in self.fields:
            # Replace scope object widget
            self.fields["scope_uuid"].widget = UnfoldAdminSelectWidget()
            self.fields["scope_uuid"].label  = _("Scope Object")

            if self.instance.pk:
                self.fields["scope_uuid"].disabled = True

            # Preserve scope uuid value when editing an existing instance
            instance = kwargs.get("instance")

            if instance and instance.scope_uuid:
                try:
                    model_class = instance.scope_type.model_class()
                    obj = model_class.objects.get(pk=instance.scope_uuid)
                    self.fields["scope_uuid"].widget.choices.append((str(obj.pk), str(obj)))
                except Exception as e:
                    # Object not found, JavaScript code will show an empty fallback option
                    pass

    def clean(self):
        """
        Check that only allowed scope types are assigned.
        """
        cleaned_data = super().clean()
        scope_type  = cleaned_data["scope_type"]

        validate_scope_type(scope_type)
        return cleaned_data

class ScopeRoleFieldMixin(ModelForm):
    """
    Form mixin for the enrollment models that combine a scope with a role, e.g. User role
    assignment, enrollment method etc. This mixin makes sure that only active roles of
    the selected scope can be chosen and updates the role selection list accordingly
    when the scope is changed.
    """
    class Media:
        css = {"all": ()}
        js  = ("openbook_auth/scope_roles_autoload.js",)

class ScopedRolesFormMixin(ModelForm):
    """
    Form mixin for model forms where the model implements the `ScopedRoles` mixin and
    therefor acts as a permission scope for user roles. This mixin makes sure that
    only allowed permissions are assigned as public permissions.
    """
    def __init__(self, *args, **kwargs):
        """
        Restrict visible choices in the HTML output to only allowed permissions.
        """
        super().__init__(*args, **kwargs)

        self._scope_type = ContentType.objects.get_for_model(self.Meta.model)
        allowed_permissions = AllowedRolePermission.get_for_scope_type(self._scope_type).values_list("permission", flat=True)

        self.fields["public_permissions"].queryset = Permission.objects.filter(id__in=allowed_permissions)

    def clean(self):
        """
        Check that only allowed permissions are assigned.
        """
        cleaned_data = super().clean()
        public_permissions = cleaned_data["public_permissions"]
        
        validate_permissions(self._scope_type, public_permissions)
        return cleaned_data