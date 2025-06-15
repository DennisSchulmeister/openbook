# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.admin               import RelatedOnlyFieldListFilter
from django.contrib.auth.models         import Permission
from django.contrib.contenttypes.models import ContentType
from django.forms                       import ModelForm
from django.utils.translation           import gettext_lazy as _
from import_export.fields               import Field
from unfold.admin                       import TabularInline
from unfold.contrib.forms.widgets       import UnfoldAdminSelectWidget

from openbook.admin                     import ImportExportModelResource
from ...import_export.permission        import PermissionManyToManyWidget
from ...import_export.scope             import ScopeTypeForeignKeyWidget
from ...import_export.user              import UserForeignKeyWidget
from ...models.allowed_role_permission  import AllowedRolePermission
from ...models.mixins.scope             import ScopedRolesMixin
from ...models.role                     import Role
from ...validators                      import validate_permissions
from ...validators                      import validate_scope_type

scope_type_filter = ["scope_type", RelatedOnlyFieldListFilter]

permissions_fieldset = (_("Permissions"), {
    "classes": ["tab"],
    "fields": ["owner", "public_permissions"],
})

class ScopedRolesResourceMixin(ImportExportModelResource):
    """
    Mixin class for the import/export resource class of models that act as permissions
    scopes for user roles. Handles the import and export of the owner and public permissions.
    Note that the other scope fields (roles, enrollment methods, …) are not handled, because
    they are reverse relations for objects that support import/export themselves.
    """
    owner = Field(attribute="owner", widget=UserForeignKeyWidget())
    public_permissions = Field(attribute="public_permissions", widget=PermissionManyToManyWidget())

    class Meta:
        fields = ["owner", "public_permissions"]

class ScopeResourceMixin(ImportExportModelResource):
    """
    Mixin class for the import/export resource class of models that reference an authorization
    scope with the fields `scope_type` and `scope_uuid`.
    """
    scope_type = Field(attribute="scope_type", widget=ScopeTypeForeignKeyWidget())
    scope_id   = Field(attribute="scope_uuid", column_name="scope_id")

    class Meta:
        fields = ["scope_type", "scope_id"]
    
    def dehydrate_scope_id(self, instance) -> str:
        """
        Export scope id using either slug (if existing as it should) or id of the scope model.
        """
        if not instance \
        or not hasattr(instance, "scope_type") or not instance.scope_type \
        or not hasattr(instance, "scope_uuid") or not instance.scope_uuid:
            return ""

        content_type: ContentType = instance.scope_type
        scope = content_type.model_class().objects.get(pk=instance.scope_uuid)
        return scope.slug if hasattr(scope, "slug") else scope.id

    def before_save_instance(self, instance, row, **kwargs):
        """
        Resolve slug from scope model back to UUID.
        """
        if not instance or not instance.scope_type:
            return None
        
        content_type: ContentType = instance.scope_type
        model_class = content_type.model_class()

        if hasattr(model_class, "slug"):
            try:
                instance.scope_uuid = model_class.objects.get(slug=row["scope_id"]).id
                return
            except model_class.DoesNotExist:
                return
        
        instance.scope_uuid = row["scope_id"]

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
            "all": ["openbook_auth/scope_uuid_autoload.css"]
        }
        js  = ["openbook_auth/scope_uuid_autoload.js"]

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

class ScopeRoleFieldFormMixin(ModelForm):
    """
    Form mixin for the enrollment models that combine a scope with a role, e.g. User role
    assignment, enrollment method etc. This mixin makes sure that only active roles of
    the selected scope can be chosen and updates the role selection list accordingly
    when the scope is changed.
    """
    class Media:
        css = {"all": ()}
        js  = ["openbook_auth/scope_roles_autoload.js"]

class ScopeRoleFieldInlineMixin(TabularInline):
    """
    Tabular inline mixin that restricts the choice of roles to the current scope.
    """
    def get_formset(self, request, obj=None, **kwargs):
        self.parent_obj = obj
        return super().get_formset(request, obj, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if self.parent_obj and db_field.name == "role":
            scope_type = ContentType.objects.get_for_model(self.parent_obj)
            kwargs["queryset"] = Role.objects.filter(scope_type=scope_type, scope_uuid=self.parent_obj.id)
            pass
    
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

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