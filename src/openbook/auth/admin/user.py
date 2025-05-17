# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation  import gettext_lazy as _
from unfold.admin              import StackedInline
from unfold.forms              import AdminPasswordChangeForm
from unfold.forms              import UserChangeForm
from unfold.forms              import UserCreationForm

from openbook.admin            import CustomModelAdmin
from openbook.admin            import ImportExportModelResource
from ..models.user             import User
from ..models.user_profile     import UserProfile

# TODO: Import/Export
class UserResource(ImportExportModelResource):
    class Meta:
        model = User

class UserProfileInline(StackedInline):
    model               = UserProfile
    fk_name             = "user"
    can_delete          = False
    verbose_name        = _("User Profile")
    verbose_name_plural = _("User Profiles")
    tab                 = True
    hide_title          = True

class UserAdmin(CustomModelAdmin, DjangoUserAdmin):
    """
    Sub-class of Django's User Admin to integrate the additional fields of
    Application Users.
    """
    form                 = UserChangeForm
    add_form             = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    resource_classes     = (UserResource,)
    list_display         = DjangoUserAdmin.list_display + ("user_type",)
    list_filter          = DjangoUserAdmin.list_filter + ("user_type",)
    inlines              = (UserProfileInline,)

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "usable_password", "password1", "password2"),
        }),
        (_("Additional Information"), {
            "classes": ("wide",),
            "fields": ("user_type", "email",),
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        """
        Override e-mail to be obligatory.
        See: https://stackoverflow.com/a/66562177
        """
        form = super().get_form(request, obj, **kwargs)

        if "email" in form.base_fields:
            form.base_fields["email"].required = True

        return form

    def get_inline_instances(self, request, obj=None):
        """
        Handle case when no user profile exists.
        """
        if obj and not hasattr(obj, "profile"):
            UserProfile.objects.create(user=obj)

        return super().get_inline_instances(request, obj)
    
UserAdmin.fieldsets[0][1]["fields"] += ("user_type",)

UserAdmin.fieldsets[1][1]["classes"] = ("tab",)
UserAdmin.fieldsets[2][1]["classes"] = ("tab",)
UserAdmin.fieldsets[3][1]["classes"] = ("tab",)
