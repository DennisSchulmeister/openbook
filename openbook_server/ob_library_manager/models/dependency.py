# OpenBook Studio: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.db                import models
from django.utils.translation import gettext_lazy as _
from openbook_server.utils    import models as db_utils
from .library                 import Library
from ..validators             import validate_library_name

class Dependency(db_utils.UUIDMixin):
    """
    Just like Node.js packages (which the OpenBook libraries usually are), libraries may depend
    on other libraries without which they cannot be used. Unfortunately we cannot use the declared
    dependencies of the `package.json` file for this as it mostly points to Node.js packages that
    will be included in the generated library bundle.

    Instead, dependencies between OpenBook libraries are declared in the `library.yml` file and
    uploaded into this database model. This allows the server to perform at least some basic
    dependency checks during installation to see that all required other libraries have also
    been installed. It also allows the server to warn the user in case a library that is needed
    by another library is de-installed.
    """
    library    = models.ForeignKey(Library, verbose_name=_("Library"), on_delete=models.CASCADE)
    dependency = models.CharField(verbose_name=_("Name"), max_length=100, validators=[validate_library_name])
    version    = models.CharField(verbose_name=_("Version"), max_length=50)

    class Meta:
        verbose_name        = _("Dependency")
        verbose_name_plural = _("Dependencies")

        constraints = [
            models.UniqueConstraint("library", "dependency", name="unique_library_dependency")
        ]

    def __str__(self):
        return "%s %s" % (self.dependency, self.version)
