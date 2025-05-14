# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.auth.models         import Permission
from unfold.contrib.forms.widgets       import UnfoldAdminSelectWidget
from django.contrib.contenttypes.models import ContentType
from django.forms                       import ModelForm
from django.utils.translation           import gettext_lazy as _

from ...models.allowed_role_permission  import AllowedRolePermission
from ...models.mixins.auth              import ScopedRolesMixin
from ...validators                      import validate_permissions

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

        # Reduce scope type to allowed values
        scope_types = []

        for content_type in ScopedRolesMixin.get_scope_model_content_types():
            scope_types.append((content_type.pk, content_type.name))

        self.fields["scope_type"].choices = scope_types

        # Replace scope object widget
        self.fields["scope_uuid"].widget = UnfoldAdminSelectWidget()
        self.fields["scope_uuid"].label  = _("Scope Object")

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

class ScopedRolesFormMixin(ModelForm):
    """
    For mixin for model forms where the model implements the `ScopedRoles` mixin and
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