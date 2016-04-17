# -*- coding: utf-8 -*-
import time
from django.db import models


class UserAccount(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    account = models.CharField(max_length=128, db_index=True, null=True, blank=True)
    password = models.CharField(max_length=128)
    email = models.CharField(max_length=128, db_index=True, null=True, blank=True)
    phone_number = models.CharField(max_length=32, db_index=True, null=True, blank=True)
    qq_account = models.CharField(max_length=32, db_index=True, null=True, blank=True)
    wechat_account = models.CharField(max_length=32, db_index=True, null=True, blank=True)
    wechat_openid = models.CharField(max_length=64, db_index=True, null=True, blank=True)
    sex = models.CharField(max_length=16, null=True, blank=True)
    birthday = models.DateField(max_length=64, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    extra_info = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'user_account'

    def __str__(self):
        return 'wechat_openid: %s, qq_account: %s' % (self.wechat_openid, self.qq_account)


