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
    kis_type = models.ManyToManyField(Kis_Type, through='Kis_Type_To_Kis', verbose_name=u'типы ИС')
    branch = models.ManyToManyField(Branch, through='Branch_To_Kis', verbose_name=u'отрасли')
    class Meta:
        unique_together = ('owner', 'name',)
        ordering = ('owner', 'name',)
        verbose_name = u'ИС'
        verbose_name_plural = u'ИС'


class Kis_Type_To_Kis(models.Model):
    kis = models.ForeignKey(Kis, on_delete=models.CASCADE, related_name='kis_to_kis_type', verbose_name=u'ИС')
    kis_type = models.ForeignKey(Kis_Type, on_delete=models.CASCADE, related_name='kis_type_to_kis', verbose_name=u'тип ИС')
    class Meta:
        unique_together = ('kis', 'kis_type')
        ordering = ('kis', 'kis_type',)
        verbose_name = u'тип ИС'
        verbose_name_plural = u'типы ИС'


class Branch_To_Kis(models.Model):
    kis = models.ForeignKey(Kis, on_delete=models.CASCADE, related_name='kis_to_branch', verbose_name=u'ИС')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='branch_to_kis', verbose_name=u'отрасль')
    class Meta:
        unique_together = ('kis', 'branch')
        ordering = ('kis', 'branch',)
        verbose_name = u'отрасль'
        verbose_name_plural = u'отрасли'


class Customer(Default):
    name_lat = models.CharField(max_length=500, blank=True, null=True, db_index=True, verbose_name=u'название лат.')
    branch = models.ManyToManyField(Branch, blank=True, null=True, through='Customer_To_Branch', verbose_name=u'отрасли')
    branch_description = models.CharField(max_length=500, db_index=True, verbose_name=u'описание деятельности')
    city = models.ForeignKey(City, blank=True, null=True, related_name='customer_city', verbose_name=u'город')
    company_size = models.CharField(max_length=10, db_index=True, verbose_name=u'размер компании')
    url = models.CharField(max_length=500, verbose_name=u'URL')
    class Meta:
        unique_together = ('name',)
        ordering = ('name',)
        verbose_name = u'заказчик'
        verbose_name_plural = u'заказчики'
    def customer_connection_event_count(self):
        return self.customer_connection_event_set.count()
    def serialize_extra(self):
        return {'extras': ('customer_connection_event_count',)}


class Customer_To_Branch(models.Model):
    name_lat = models.CharField(max_length=500, blank=True, null=True, db_index=True, verbose_name=u'название лат.')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_to_branch', verbose_name=u'заказчик')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='branch_to_customer', verbose_name=u'отрасль')
    class Meta:
        unique_together = ('customer', 'branch')
        ordering = ('customer', 'branch')
        verbose_name = u'отрасль'
        verbose_name_plural = u'отрасли'


class Contact(models.Model):
    owner = models.ForeignKey(Developer, verbose_name=u'владелец')
    customer = models.ForeignKey(Customer, verbose_name=u'заказчик')
    name = models.CharField(max_length=500, blank=True, null=True, db_index=True, verbose_name=u'название')
    customer = models.ForeignKey(Customer, verbose_name=u'заказчик')
    name = models.CharField(max_length=500, blank=True, null=True, db_index=True, verbose_name=u'название')
    weight = models.IntegerField(max_length=3, default=1, db_index=True, verbose_name=u'вес')
    position_category = models.CharField(max_length=500, blank=True, null=True, db_index=True, verbose_name=u'категория должности')
    position = models.CharField(max_length=500, blank=True, null=True, db_index=True, verbose_name=u'должность')
    position_category = models.CharField(max_length=500, blank=True, null=True, db_index=True, verbose_name=u'категория должности')
    position = models.CharField(max_length=500, blank=True, null=True, db_index=True, verbose_name=u'должность')
    class Meta:
        unique_together = ('owner', 'customer', 'name')
        ordering = ('owner', 'customer', 'name')
        unique_together = ('owner', 'customer', 'name')
        ordering = ('owner', 'customer', 'name')
        verbose_name = u'контакт'
        verbose_name_plural = u'контакты'


class Customer_Connection_Event(models.Model):
    developer = models.ForeignKey(Developer, verbose_name=u'владелец')
    customer = models.ForeignKey(Customer, verbose_name=u'заказчик')
    status = models.CharField(max_length=500, blank=True, null=True, verbose_name=u'статус')
    comment = models.CharField(max_length=500, blank=True, null=True, verbose_name=u'комментарий')
    position_category = models.CharField(max_length=500, blank=True, null=True, db_index=True, verbose_name=u'категория должности')
    position = models.CharField(max_length=500, blank=True, null=True, db_index=True, verbose_name=u'должность')
    class Meta:
        verbose_name = u'контактное событие'
        verbose_name_plural = u'контактные события'
    def __unicode__(self):
        return self.to_string()
    def to_string(self):
        return u"%s" % (self.customer)