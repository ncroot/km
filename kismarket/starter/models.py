# -*- coding: utf-8 -*-

from django.db import models

class Default(models.Model):
    name = models.CharField(max_length=500, db_index=True, verbose_name=u'название')
    text = models.TextField(blank=True, null=True, verbose_name=u'какое-нибудь описание например')
    class Meta:
        abstract = True
    def __unicode__(self):
        return self.to_string()
    def to_string(self):
        return self.name
