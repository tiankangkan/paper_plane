# -*- coding: utf-8 -*-

from django.db import models
from account.models import UserAccount


class Conversation(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    source = UserAccount
    target = UserAccount
    timestamp = models.DateTimeField(db_index=True)
    content = models.TextField()

    class Meta:
        db_table = 'user_account'

    def __str__(self):
        return 'wechat_openid: %s, qq_account: %s' % (self.wechat_openid, self.qq_account)


