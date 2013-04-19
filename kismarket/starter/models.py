# -*- coding: utf-8 -*-

from django.db import models
from django.core.exceptions import ValidationError

class Default(models.Model):
    name = models.CharField(max_length=500, blank=False, null=False, db_index=True, verbose_name=u'название')
    text = models.TextField(blank=True, null=True, verbose_name=u'какое-нибудь описание например')
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.name:
            raise ValidationError('Empty error message')
        return super(Default, self).save(force_insert, force_update, using, update_fields)
    class Meta:
        abstract = True
    def __unicode__(self):
        return self.to_string()
    def to_string(self):
        return self.name


class City(Default):
    class Meta:
        unique_together = ('name',)
        ordering = ('name',)
        verbose_name = u'страна'
        verbose_name_plural = u'страны'
