# -*- coding: utf-8 -*-

from django.db import models


class FileMapping(models.Model):
    id = models.AutoField(primary_key=True)
    identify = models.CharField(db_index=True, unique=True, max_length=64)    # maybe md5 of file_path ?
    file_path = models.TextField()

    class Meta:
        db_table = 'file_mapping'

    def __str__(self):
        return 'file_path: %s' % self.file_path


TREASURE_FILE_MUN = len(FileMapping.objects.all())
