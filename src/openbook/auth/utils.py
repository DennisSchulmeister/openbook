# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.auth.models         import Permission
from django.contrib.contenttypes.models import ContentType

def perm_name_for_permission(permission: "Permission") -> str:
    """
    Get clear-text, untranslated permission name from permission object.
    """
    return permission.name if permission else ""

def perm_string_for_permission(permission: "Permission") -> str:
    """
    Serialize permission object into permission string as used by Django:
    `{app_label}.{codename}`
    """
    return f"{permission.content_type.app_label}.{permission.codename}" if permission else ""

def app_label_for_permission(permission: "Permission") -> str:
    """
    Get app label from permission object.
    """
    permission.content_type.app_label if permission else ""

def app_name_for_permission(permission: "Permission") -> str:
    """
    Get translated app name from permission object
    """
    if not permission:
        return ""
    
    model = permission.content_type.model_class()
    return model._meta.app_config.verbose_name or permission.content_type.app_label

def permission_for_perm_string(perm: str) -> "Permission":
    """
    Get permission object for a given permission string or raise `Permission.DoesNotExist`,
    when the permission cannot be found.
    """
    app_label, codename = perm.split(".", 1)
    return Permission.objects.get(codename=codename, content_type__app_label=app_label)

def model_string_for_content_type(content_type: "ContentType") -> str:
    """
    Serialize content type objet into model string as used by Django: `{app_label}.{model}`
    """
    return f"{content_type.app_label}.{content_type.name}".lower() if content_type else ""

def content_type_for_model_string(model_string: str) -> "ContentType":
    """
    Get content type object for a given model string or raise `ContentType.DoesNotExist`,
    when the content type cannot be found.
    """
    app_label, model = model_string.split(".", 1)
    return ContentType.objects.get(app_label=app_label, model=model)