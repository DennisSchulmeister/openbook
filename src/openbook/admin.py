# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.apps              import apps
from django.conf              import settings
from django.utils.translation import gettext_lazy as _
from djangoql.admin           import DjangoQLSearchMixin
from import_export.resources  import ModelResource
from import_export.admin      import ImportExportModelAdmin
from unfold.sites             import UnfoldAdminSite
from unfold.admin             import ModelAdmin as UnfoldModelAdmin

class ImportExportModelResource(ModelResource):
    """
    Custom `ModelResource` that allows to delete entries when importing model data
    in the Admin from CSV, YML, XLSX, … files. For this the files may include a row
    called `delete` with a boolean value to indicate the rows to be deleted.
    """
    def for_delete(self, row, instance):
        return "delete" in row and row["delete"].upper() in ["1", "X", "YES", "TRUE"]

class CustomModelAdmin(DjangoQLSearchMixin, UnfoldModelAdmin, ImportExportModelAdmin):
    """
    Custom `ModelAdmin` to combines several mixins from Django Unfold, Django QL and
    Django Import/Export into on common base-class.
    """
    save_as = True

class CustomAdminSite(UnfoldAdminSite):
    """
    Custom `AdminSite` class that allows us to override the default alphabetical
    order of apps and models on the dashboard. Instead apps will be sorted in the
    order they are liste in `settings.INSTALLED_APPS`. And models will be sorted
    in the order they are registered with the admin site.
    """
    # Not used by Unfold Admin, but set in settings.py
    # site_title  = _("OpenBook: Admin")
    # site_header = _("OpenBook: Admin")
    # index_title = _("Administration")

    def __init__(self):
        """
        Constructor. Defines `self._models_` which holdes the models in the order
        they were registered.
        """
        super().__init__()
        self._models_ = []

    def register(self, model_or_iterable, admin_class, **options):
        """
        Hook into Django Admin's `register()` method to remember the order in which
        the models were registered.
        """
        super().register(model_or_iterable, admin_class, **options)

        try:
            for model in iter(model_or_iterable):
                if model in self._models_:
                    self._models_.remove(model)

                self._models_.append(model)
        except TypeError:
            self._models_.append(model_or_iterable)

    def unregister(self, model_or_iterable):
        """
        Hook into Django Admin's `unregister()` method to remove a model from the
        internal list.
        """
        super().unregister(model_or_iterable)

        try:
            for model in iter(model_or_iterable):
                if model in self._models_:
                    self._models_.remove(model)
        except TypeError:
            if model_or_iterable in self._models_:
                self._models_.remove(model_or_iterable)

    def get_app_list(self, request, *args):
        """
        Hook into Django Admin's `get_app_list()` method to override the order in
        which the applications and models appear.
        """
        # Sort apps in the order they appear in the settings
        app_list = super().get_app_list(request, *args)

        for admin_app in app_list:
            app_config = apps.get_app_config(admin_app["app_label"])
            admin_app["_index_"] = settings.INSTALLED_APPS.index(app_config.name)

        app_list.sort(key = lambda admin_app: admin_app["_index_"])

        for admin_app in app_list:
            del admin_app["_index_"]

        # Sort models in the order they were registered
        for admin_app in app_list:
            for model in admin_app["models"]:
                model["_index_"] = self._models_.index(model["model"])

            admin_app["models"].sort(key = lambda model: model["_index_"])

            for model in admin_app["models"]:
                del model["_index_"]

        return app_list

admin_site = CustomAdminSite()