# -*- coding: utf-8 -*-
import time
from django.db import models


class UserAccount(models.Model):
    id = models.IntegerField(primary_key=True, db_index=True)
    account = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=32)
    qq_account = models.CharField(max_length=32)
    wechat_account = models.CharField(max_length=32)
    sex = models.CharField(max_length=16)
    birthday = models.CharField(max_length=64)
    age = models.IntegerField()
    extra_info = models.TextField()

    class Meta:
        db_table = 'user_account'

