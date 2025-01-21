# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.views.generic.base import TemplateView

class StartPage(TemplateView):
    template_name = "openbook/core/website/startpage.html"

class Error400(TemplateView):
    template_name = "openbook/core/website/400.html"

class Error403(TemplateView):
    template_name = "openbook/core/website/403.html"

class Error404(TemplateView):
    template_name = "openbook/core/website/404.html"

class Error500(TemplateView):
    template_name = "openbook/core/website/500.html"
