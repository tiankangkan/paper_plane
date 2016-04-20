# -*- coding: utf-8 -*-

from django.db import models
from account.models import UserAccount


class MailMsg(models.Model):
    t_id = models.AutoField(primary_key=True, db_index=True)
    t_type = models.CharField(max_length=64, null=True, blank=True)
    source = models.ForeignKey(UserAccount, null=True, blank=True, related_name='mail_from')
    target = models.ForeignKey(UserAccount, null=True, blank=True, related_name='mail_to')
    timestamp = models.DateTimeField(db_index=True, null=True, blank=True)
    theme = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    url = models.TextField(null=True, blank=True)
    is_read = models.BooleanField()

    class Meta:
        db_table = 'mail_msg'

    def __str__(self):
        return 'timestamp: %s, id:%s, source: %s, target: %s, is_read: %s' % (self.timestamp, self.t_id, self.source, self.target, self.is_read)


