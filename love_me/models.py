# -*- coding: utf-8 -*-

from django.db import models
from account.models import UserAccount


class ConversationPage(models.Model):
    t_id = models.AutoField(primary_key=True, db_index=True)
    source = models.ForeignKey(UserAccount, null=True, blank=True, related_name='source_account')
    target = models.ForeignKey(UserAccount, null=True, blank=True, related_name='target_account')
    timestamp = models.DateTimeField(db_index=True, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    is_read = models.BooleanField(null=True, blank=True)

    class Meta:
        db_table = 'conversation_page'

    def __str__(self):
        return 'id:%s, source: %s, timestamp: %s, is_read: %s' % (self.t_id, self.source, self.timestamp, self.is_read)


