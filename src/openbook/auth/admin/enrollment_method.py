# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.admin              import RelatedOnlyFieldListFilter
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.translation          import gettext_lazy as _
from unfold.admin                      import TabularInline

from openbook.admin                    import CustomModelAdmin
from openbook.admin                    import ImportExportModelResource
from .mixins.audit                     import created_modified_by_fields
from .mixins.audit                     import created_modified_by_fieldset
from .mixins.audit                     import created_modified_by_filter
from .mixins.auth                      import ScopeFormMixin
from .mixins.auth                      import ScopeRoleFieldMixin
from .mixins.auth                      import ScopeRoleFieldInlineMixin
from .mixins.auth                      import scope_type_filter
from ..models.enrollment_method        import EnrollmentMethod

# TODO: Import/Export
class EnrollmentMethodResource(ImportExportModelResource):
    class Meta:
        model = EnrollmentMethod

class EnrollmentMethodForm(ScopeFormMixin, ScopeRoleFieldMixin):
    class Meta:
        model  = EnrollmentMethod
        fields = "__all__"
    
    class Media:
        css = {
            "all": (*ScopeFormMixin.Media.css["all"], *ScopeRoleFieldMixin.Media.css["all"]),
        }
        js = (*ScopeFormMixin.Media.js, *ScopeRoleFieldMixin.Media.js)

class EnrollmentMethodInline(ScopeRoleFieldInlineMixin, GenericTabularInline, TabularInline):
    model               = EnrollmentMethod
    ct_field            = "scope_type"
    ct_fk_field         = "scope_uuid"
    fields              = ("name", "role", "is_active", "passphrase")
    ordering            = ("name", "role")
    extra               = 0
    show_change_link    = True
    tab                 = True

class EnrollmentMethodAdmin(CustomModelAdmin):
    model              = EnrollmentMethod
    form               = EnrollmentMethodForm
    resource_classes   = (EnrollmentMethodResource,)
    list_display       = ("scope_type", "scope_object", "name", "role", "passphrase", "is_active", *created_modified_by_fields)
    list_display_links = ("scope_type", "scope_object", "name", "role")
    ordering           = ("scope_type", "scope_uuid", "name", "role")
    search_fields      = ("name", "role__name", "user__username")
    readonly_fields    = (*created_modified_by_fields,)

    list_filter = (
        scope_type_filter,
        ("role", RelatedOnlyFieldListFilter),
        "end_date",
        "is_active",
        *created_modified_by_filter
    )

    fieldsets = (
        (None, {
            "fields": (
                ("scope_type", "scope_uuid"),
                ("role", "passphrase",),
                "is_active"
            ),
        }),
        (_("Description"), {
            "classes": ("tab",),
            "fields": ("description", "text_format"),
        }),
        (_("Validity"), {
            "classes": ("tab",),
            "description": _("Leave empty to make the enrollment valid for an unlimited period. Otherwise either set a duration or an end date."),
            "fields": (
                ("duration_value", "duration_period"),
                "end_date"
            ),
        }),
        created_modified_by_fieldset,
    )

    add_fieldsets = (
        (None, {
            "fields": (
                ("scope_type", "scope_uuid"),
                ("role", "passphrase"),
                "is_active"
            ),
        }),
        (_("Description"), {
            "classes": ("tab",),
            "fields": ("description", "text_format"),
        }),
        (_("Validity"), {
            "classes": ("tab",),
            "description": _("Leave empty to make the enrollment valid for an unlimited period. Otherwise either set a duration or an end date."),
            "fields": (
                ("duration_value", "duration_period"),
                "end_date"
            ),
        }),
    )
