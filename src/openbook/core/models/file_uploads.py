# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

import mimetypes

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db                          import models
from django.utils.translation           import gettext_lazy as _

from .mixins.uuid                       import UUIDMixin
from .utils.file                        import calc_file_path

class AbstractFileModel(UUIDMixin):
    """
    Abstract base class for the generic file upload models below. Contains the common
    fields and functionality like a generic relation to the owner model and fields for
    the file data and meta data.
    """
    # Link to related model
    def _calc_file_path(self, filename):
        return calc_file_path(self.content_type, self.id, filename)

    content_type   = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id      = models.UUIDField()
    content_object = GenericForeignKey("content_type", "object_id")

    # Uploaded file data
    file_data = models.FileField(verbose_name=_("File Data"), upload_to=_calc_file_path)
    file_name = models.CharField(verbose_name=_("File Name"), max_length=255, blank=True)
    file_size = models.PositiveIntegerField(verbose_name=_("File Size"), null=True)
    mime_type = models.CharField(verbose_name=_("MIME Type"), max_length=64)

    # Django meta information
    class Meta:
        abstract = True
        ordering = ["content_type", "object_id", "file_name"]
        indexes  = [models.Index(fields=["content_type", "object_id", "file_name"])]

    def __str__(self):
        return self.file_name

    def save(self, *args, **kwargs):
        """
        Populate meta-data fields when file is saved.
        """
        if self.file_data:
            if not self.file_name:
                self.file_name = self.file_data.name

            self.file_size = self.file_data.size
            self.mime_type, _ = mimetypes.guess_type(self.file_data.name)

            if not self.mime_type:
                self.mime_type = 'application/octet-stream'

        super().save(*args, **kwargs)

class MediaFile(AbstractFileModel):
    """
    Generic model for media files, when a model can have multiple media files like
    images or sounds that shall later be accessed by their file name. To use this
    model simply add a `GenericRelation` to the model that shall have media files.
    """
    class Meta(AbstractFileModel.Meta):
        verbose_name        = _("Media File")
        verbose_name_plural = _("Media Files")
