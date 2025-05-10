# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from .audit import CreatedModifiedByMixin
from .auth  import RoleBasedObjectPermissionsMixin
from .auth  import ScopedRolesMixin
from .auth  import ScopeMixin