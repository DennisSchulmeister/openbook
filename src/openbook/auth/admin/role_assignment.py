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
from ..models.role_assignment          import RoleAssignment

# TODO: Import/Export
class RoleAssignmentResource(ImportExportModelResource):
    class Meta:
        model = RoleAssignment

class RoleAssignmentForm(ScopeFormMixin, ScopeRoleFieldMixin):
    class Meta:
        model  = RoleAssignment
        fields = "__all__"
    
    class Media:
        css = {
            "all": (*ScopeFormMixin.Media.css["all"], *ScopeRoleFieldMixin.Media.css["all"]),
        }
        js = (*ScopeFormMixin.Media.js, *ScopeRoleFieldMixin.Media.js)

class RoleAssignmentInline(ScopeRoleFieldInlineMixin, GenericTabularInline, TabularInline):
    model            = RoleAssignment
    ct_field         = "scope_type"
    ct_fk_field      = "scope_uuid"
    fields           = ("role", "user", "is_active", "assignment_method", "enrollment_method", "access_request")
    ordering         = ("role", "user")
    readonly_fields  = ("assignment_method", "enrollment_method", "access_request")
    extra            = 0
    show_change_link = True
    tab              = True

class RoleAssignmentAdmin(CustomModelAdmin):
    model              = RoleAssignment
    form               = RoleAssignmentForm
    resource_classes   = (RoleAssignmentResource,)
    list_display       = ("scope_type", "scope_object", "role", "user", "assignment_method", "is_active", *created_modified_by_fields)
    list_display_links = ("scope_type", "scope_object", "role", "user", "assignment_method")
    ordering           = ("scope_type", "scope_uuid", "role", "user")
    search_fields      = ("role__name", "user__username", "user__first_name", "user__last_name")
    readonly_fields    = ("assignment_method", "enrollment_method", "access_request", *created_modified_by_fields,)

    list_filter = (
        scope_type_filter,
        ("role", RelatedOnlyFieldListFilter),
        ("user", RelatedOnlyFieldListFilter),
        "assignment_method",
        "is_active",
        *created_modified_by_filter
    )

    fieldsets = (
        (None, {
            "fields": (
                ("scope_type", "scope_uuid"),
                ("role", "user"),
                "is_active"
            ),
        }),
        (_("Validity"), {
            "classes": ("tab",),
            "description": _("Leave empty to make the assignment valid for an unlimited period."),
            "fields": ("start_date", "end_date"),
        }),
        (_("Source"), {
            "classes": ("tab",),
            "fields": ("assignment_method", "enrollment_method", "access_request"),
        }),
        created_modified_by_fieldset,
    )

    add_fieldsets = (
        (None, {
            "fields": (
                ("scope_type", "scope_uuid"),
                ("role", "user"),
                "is_active"
            ),
        }),
        (_("Validity"), {
            "classes": ("tab",),
            "description": _("Leave empty to make the assignment valid for an unlimited period."),
            "fields": ("start_date", "end_date"),
        }),
    )
