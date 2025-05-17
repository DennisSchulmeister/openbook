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
from .mixins.auth                      import scope_type_filter
from ..models.access_request           import AccessRequest

# TODO: Import/Export
class AccessRequestResource(ImportExportModelResource):
    class Meta:
        model = AccessRequest

class AccessRequestForm(ScopeFormMixin):
    class Meta:
        model  = AccessRequest
        fields = "__all__"
    
    class Media:
        js = ScopeFormMixin.Media.js

# TODO: Inline
class AccessRequestInline(GenericTabularInline, TabularInline):
    model               = AccessRequest
    form                = AccessRequestForm
    ct_field            = "scope_type"
    ct_fk_field         = "scope_uuid"
    # fields              = ("priority", "name", "slug", "is_active", *created_modified_by_fields)
    # ordering            = ("priority", "name")
    # readonly_fields     = (*created_modified_by_fields,)
    show_change_link    = True
    tab                 = True

# TODO:
class AccessRequestAdmin(CustomModelAdmin):
    model              = AccessRequest
    form               = AccessRequestForm
    resource_classes   = (AccessRequestResource,)
#     list_display       = ("id", "domain", "name", "short_name")
#     list_display_links = ("id", "domain")
#     list_filter        = (scope_type_filter, *created_modified_by_filter)
#     search_fields      = ("domain", "name", "short_name")
# 
#     fieldsets = (
#         (None, {
#             "fields": ("id", "domain", "name", "short_name", "about_url", "brand_color")
#         }),
#     )
