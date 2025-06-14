# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.auth.models                import Permission
from openbook.core.middleware.current_language import get_current_language

def perm_name_for_permission(permission: "Permission") -> str:
    """
    Get clear-text, translated permission name from permission object.
    """
    from .models.permission_text import PermissionText
    language = get_current_language()

    if not permission:
        return ""

    if language:
        try:
            translation = PermissionText.objects.get(parent = permission, language = language)

            if translation.name:
                return translation.name
        except PermissionText.DoesNotExist:
            pass
    
    return permission.name
    
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
    return permission.content_type.app_label if permission else ""

def app_name_for_permission(permission: "Permission") -> str:
    """
    Get translated app name from permission object
    """
    if not permission:
        return ""
    
    model = permission.content_type.model_class()
    return model._meta.app_config.verbose_name or permission.content_type.app_label

def model_for_permission(permission: "Permission") -> str:
    """
    Get model label from permission object.
    """
    if not permission:
        return ""
    
    return permission.content_type.model

def model_name_for_permission(permission: "Permission") -> str:
    """
    Get translated modal name from permission object.
    """
    if not permission:
        return ""
    
    model = permission.content_type.model_class()

    if not model:
        return ""

    return model._meta.verbose_name

def permission_for_perm_string(perm: str) -> "Permission":
    """
    Get permission object for a given permission string or raise `Permission.DoesNotExist`,
    when the permission cannot be found.
    """
    if not perm:
        return None
    
    app_label, codename = perm.split(".", 1)
    return Permission.objects.get(codename=codename, content_type__app_label=app_label)

