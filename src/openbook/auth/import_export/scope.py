# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.contenttypes.models import ContentType
from import_export.widgets              import ForeignKeyWidget
from import_export.widgets              import ManyToManyWidget

from openbook.core.utils.content_type   import content_type_for_model_string
from openbook.core.utils.content_type   import model_string_for_content_type

class ScopeTypeForeignKeyWidget(ForeignKeyWidget):
    """
    A customized foreign-key widget that exports and imports scope types with their
    Django-style model name (content type).
    """
    def __init__(self, *args, **kwargs):
        super().__init__(model=ContentType, *args, **kwargs)

    def render(self, value, row=None, **kwargs):
        return model_string_for_content_type(value) if value else ""
    
    def clean(self, value, obj=None, **kwargs):
        return content_type_for_model_string(value) if value else None

class ScopeTypeManyToManyWidget(ManyToManyWidget):
    """
    A customized many-to-many widget that exports and imports scope types with their
    Django-style model name (content type).
    """
    def __init__(self, *args, **kwargs):
        super().__init__(model=ContentType, *args, **kwargs)

    def render(self, value, row=None, **kwargs):
        if not value:
            return ""
        
        model_strings = [model_string_for_content_type(ct) for ct in value.all()]
        return self.separator.join(model_strings)
    
    def clean(self, value, obj=None, **kwargs):
        if not value:
            return []
        
        model_strings = value.split(self.separator)
        model_strings = filter(None, [ms.strip() for ms in model_strings])
        return [content_type_for_model_string(ms) for ms in model_strings]
