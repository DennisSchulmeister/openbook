# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from import_export.widgets import ForeignKeyWidget
from import_export.widgets import ManyToManyWidget
from ..models.site         import Site

class SiteForeignKeyWidget(ForeignKeyWidget):
    """
    A customized foreign-key widget that exports and imports sites as domain strings.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(model=Site, *args, **kwargs)

    def render(self, value, row=None, **kwargs):
        return value.domain
    
    def clean(self, value, obj=None, **kwargs):
        return Site.objects.get(domain=value)

class SiteManyToManyWidget(ManyToManyWidget):
    """
    A customized many-to-many widget that exports and imports sites as domain strings.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(model=Site, *args, **kwargs)

    def render(self, value, row=None, **kwargs):
        if not value:
            return ""
        
        domains = [site.domain for site in value.all()]
        return self.separator.join(domains)
    
    def clean(self, value, obj=None, **kwargs):
        domains = value.split(self.separator)
        domains = filter(None, [domain.strip() for domain in domains])
        return Site.objects.filter(domain__in=domains).all()