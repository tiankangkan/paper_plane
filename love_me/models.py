# -*- coding: utf-8 -*-

from django.db import models
from account.models import UserAccount


class ConversationPage(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    source = models.ForeignKey(UserAccount, null=True, blank=True, related_name='source_account')
    target = models.ForeignKey(UserAccount, null=True, blank=True, related_name='target_account')
    timestamp = models.DateTimeField(db_index=True)
    content = models.TextField()
    is_read = models.BooleanField()

    class Meta:
        db_table = 'conversation_page'

    def __str__(self):
        return 'source: %s, timestamp: %s, is_read: %s' % (self.source, self.timestamp, self.is_read)


