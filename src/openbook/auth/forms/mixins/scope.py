# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from unfold.contrib.forms.widgets import UnfoldAdminSelectWidget
from django.forms                 import ModelForm
from django.utils.translation     import gettext_lazy as _
from ...models.mixins             import ScopedRolesMixin

class ScopeFormMixin(ModelForm):
    """
    Form mixin class that limits the list of scope types to valid choices and
    automatically updates the scope uuid list when the type is changed. Instead
    of the uuid the scope name will be shown in the select box.
    """
    class Meta:
        fields = ("scope_uuid",)

    class Media:
        js = ("openbook_auth/scope_uuid_autoload.js",)

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