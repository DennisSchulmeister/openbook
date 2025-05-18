# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.auth.admin           import UserAdmin as DjangoUserAdmin
from django.utils.translation            import gettext_lazy as _
from import_export.fields                import Field
from import_export.widgets               import ManyToManyWidget
from unfold.admin                        import StackedInline
from unfold.forms                        import AdminPasswordChangeForm
from unfold.forms                        import UserChangeForm
from unfold.forms                        import UserCreationForm

from openbook.admin                      import CustomModelAdmin
from openbook.admin                      import ImportExportModelResource
from openbook.core.import_export.boolean import BooleanWidget
from ..models.group                      import Group
from ..models.user                       import User
from ..models.user_profile               import UserProfile
from ..import_export.permission          import PermissionManyToManyWidget

class UserResource(ImportExportModelResource):
    is_active        = Field(attribute="is_active",        widget=BooleanWidget())
    is_staff         = Field(attribute="is_staff",         widget=BooleanWidget())
    is_superuser     = Field(attribute="is_superuser",     widget=BooleanWidget())
    groups           = Field(attribute="groups",           widget=ManyToManyWidget(model=Group, field="slug"))
    user_permissions = Field(attribute="user_permissions", widget=PermissionManyToManyWidget())

    class Meta:
        model = User
        import_id_fields = ("username",)
        fields = (
            "username", "delete", "user_type", "email",
            "first_name", "last_name", "date_joined",
            "is_active", "is_staff", "is_superuser",
            "groups", "user_permissions",
            "profile__description", "profile__picture"
        )

    def after_save_instance(self, instance, row, **kwargs):
        """
        Save user profile after the user itself has been created/updated. Required because
        the user profile model has a foreign key on user, so that `user.profile` is just
        a backlink that can only be created once the user is there.
        """
        if instance.profile:
            instance.profile.description = row["profile__description"]
            instance.profile.picture     = row["profile__picture"]
            instance.profile.save()
        else:
            UserProfile.objects.create(
                user        = instance,
                description = row["profile__description"],
                picture     = row["profile__picture"],
            )

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
    list_display         = ("full_name", "username", "is_staff", "is_superuser", "user_type")
    list_display_links   = ("full_name", "username")
    list_filter          = DjangoUserAdmin.list_filter + ("is_superuser", "user_type")
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
