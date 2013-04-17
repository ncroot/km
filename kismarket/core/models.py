# -*- coding: utf-8 -*-
from ..starter.models import Default, City
from django.db import models


class Branch(Default):
    class Meta:
        unique_together = ('name',)
        ordering = ('name',)
        verbose_name = u'отрасль'
        verbose_name_plural = u'отрасли'


class Branch_Tech(Default):
    branch = models.ManyToManyField(Branch, through='Branch_Tech_To_Branch', verbose_name=u'отрасли')
    weight = models.IntegerField(max_length=3, default=1, db_index=True, verbose_name=u'вес')
    in_rf_percent = models.IntegerField(max_length=3, default=1, db_index=True, verbose_name=u'процент в РФ')
    in_world_percent = models.IntegerField(max_length=3, default=1, db_index=True, verbose_name=u'процент в мире')
    class Meta:
        unique_together = ('name',)
        ordering = ('name',)
        verbose_name = u'отраслевая концепция/технология'
        verbose_name_plural = u'отраслевые концепции/технологии'


class Branch_Tech_To_Branch(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='branch_to_tech', verbose_name=u'отрасль')
    branch_tech = models.ForeignKey(Branch_Tech, on_delete=models.CASCADE, related_name='tech_to_branch', verbose_name=u'концепции/технологии')
    class Meta:
        unique_together = ('branch', 'branch_tech')
        ordering = ('branch', 'branch_tech',)
        verbose_name = u'отраслевая концепция/технология'
        verbose_name_plural = u'отраслевые концепции/технологии'


class Developer(Default):
    city = models.ForeignKey(City, blank=True, null=True, related_name='developer_city', verbose_name=u'город')
    revenue_2011 = models.IntegerField(db_index=True, blank=True, null=True, verbose_name=u'выручка в 2011, тыс. руб.')
    revenue_2010 = models.IntegerField(db_index=True, blank=True, null=True, verbose_name=u'выручка в 2010, тыс. руб.')
    staff_2011 = models.IntegerField(db_index=True, blank=True, null=True, verbose_name=u'сотрудников на 31.12.2011')
    staff_2010 = models.IntegerField(db_index=True, blank=True, null=True, verbose_name=u'сотрудников на 31.12.2010')
    def revenue_incresure_from_2010_to_2012_in_percent(self):
        if not self.revenue_2011 or not self.revenue_2010:
            return None
        return '{0:.2f}'.format(float(self.revenue_2011) / float(self.revenue_2010) * 100 - 100)
    revenue_incresure_from_2010_to_2012_in_percent.short_description  = u'выручка 2010-2011, %'
    def staff_incresure_from_2010_to_2012_in_percent(self):
        if not self.staff_2011 or not self.staff_2010:
            return None
        return '{0:.2f}'.format(float(self.staff_2011) / float(self.staff_2010) * 100 - 100)
    staff_incresure_from_2010_to_2012_in_percent.short_description  = u'сотрудников 2010-2011, %'
    class Meta:
        unique_together = ('name',)
        ordering = ('name',)
        verbose_name = u'разработчик'
        verbose_name_plural = u'разработчики'


class Kis_Type(Default):
    criteria = models.TextField(blank=True, null=True, verbose_name=u'критерии')
    class Meta:
        unique_together = ('name',)
        ordering = ('name',)
        verbose_name = u'тип ИС'
        verbose_name_plural = u'типы ИС'


class Kis(Default):
    owner = models.ForeignKey(Developer, verbose_name=u'владелец')
    kis_type = models.ManyToManyField(Kis_Type, verbose_name=u'типы ИС')
    class Meta:
        unique_together = ('owner', 'name',)
        ordering = ('owner', 'name',)
        verbose_name = u'ИС'
        verbose_name_plural = u'ИС'


class Customer(Default):
    branch = models.ManyToManyField(Branch, through='Customer_To_Branch', verbose_name=u'отрасли')
    class Meta:
        unique_together = ('name',)
        ordering = ('name',)
        verbose_name = u'заказчик'
        verbose_name_plural = u'заказчики'


class Customer_To_Branch(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_to_branch', verbose_name=u'заказчик')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='branch_to_customer', verbose_name=u'отрасль')
    class Meta:
        unique_together = ('customer', 'branch')
        ordering = ('customer', 'branch')
        verbose_name = u'отрасль'
        verbose_name_plural = u'отрасли'


class Contact(Default):
    owner = models.ForeignKey(Developer, verbose_name=u'владелец')
    weight = models.IntegerField(max_length=3, default=1, db_index=True, verbose_name=u'вес')
    class Meta:
        unique_together = ('owner', 'name')
        ordering = ('owner', 'name')
        verbose_name = u'контакт'
        verbose_name_plural = u'контакты'