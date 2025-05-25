# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

import semver

from django.core.exceptions   import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_library_name(name: str) -> None:
    """
    Check that the name of a library roughly follows the same guidelines as for node.js
    packages in npmjs.org: `@organization/package` or just `package`, whereas each part
    must be at least three characters long and may only contain alpha-numerics, underline,
    minus or dot.
    """
    if name.startswith("@"):
        message = _("Expected format: @organization/package with each part alpha-numeric and at least three letters")

        try:
            org, lib = name.split("/", 1)
            org = org[1:]
        except ValueError:
            raise ValidationError(message)
        
        if len(org) < 3 or not all(c.isalnum() or c in ('.', '_', '-') for c in org) or not org.islower() \
        or len(lib) < 3 or not all(c.isalnum() or c in ('.', '_', '-') for c in lib) or not lib.islower():
            raise ValidationError(message)
    elif len(name) < 3 or not all(c.isalnum() or c in ('.', '_', '-') for c in name) or not name.islower():
        raise ValidationError(_("Expected alpha-numeric package name with at least three letters"))

def validate_version_number(version: str) -> None:
    """
    Check that version numbers use semver with numeric major, minor, patch
    and optional -prerelease and +build tags.
    """
    if not semver.Version.is_valid(version):
        raise ValidationError(_("The version must be in semver format with optional -prerelease and +build tags."))

