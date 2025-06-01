# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.contenttypes.models import ContentType

from django.test                        import TestCase
from openbook.course.models.course      import Course
from openbook.test                      import ModelViewSetTestMixin
from ..models.allowed_role_permission   import AllowedRolePermission
from ..models.role                      import Role
from ..utils                            import content_type_for_model_string
from ..utils                            import model_string_for_content_type
from ..utils                            import permission_for_perm_string

class Role_ViewSet_Tests(ModelViewSetTestMixin, TestCase):
    """
    Tests for the `RoleViewSet` REST API.
    """
    base_name = "scope_type"
    model     = ContentType
    count     = -1
    pk_found  = "openbook_course.course"

    operations = {
        "list":           {"model_permission": ()},
        "retrieve":       {"model_permission": ()},
        "create":         {"supported": False},
        "update":         {"supported": False},
        "partial_update": {"supported": False},
        "destroy":        {"supported": False},
    }