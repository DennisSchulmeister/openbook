# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.core.management.base import BaseCommand
from ...models.html_library      import HTMLLibraryVersion

class Command(BaseCommand):
    help = "Install HTML libraries from archive files"

    def handle(self, *args, **options):
        # TODO: Command-line arguments: dir, --all, --extract-only
        pass
