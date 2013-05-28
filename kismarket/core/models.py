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


class Organization(Default):
    name_full = models.CharField(max_length=500, blank=True, null=True, db_index=True, verbose_name=u'название полное')
    name_lat = models.CharField(max_length=500, blank=True, null=True, db_index=True, verbose_name=u'название лат.')
    city = models.ForeignKey(City, blank=True, null=True, verbose_name=u'город')
    company_size = models.CharField(max_length=10, blank=True, null=True, db_index=True, verbose_name=u'размер компании')
    class Meta:
        abstract = True
        unique_together = ('name',)
        ordering = ('name',)
        verbose_name = u'организация'
        verbose_name_plural = u'организация'


class Customer(Organization):
    branch = models.ManyToManyField(Branch, blank=True, null=True, through='Customer_To_Branch', verbose_name=u'отрасли')
    branch_description = models.CharField(max_length=500, blank=True, null=True, db_index=True, verbose_name=u'описание деятельности')
    url = models.CharField(max_length=500, blank=True, null=True, verbose_name=u'URL')
    relationship = models.ManyToManyField('self', blank=True, null=True, through='Customer_To_Customer', symmetrical=False, verbose_name=u'отношения')
    class Meta:
        unique_together = ('name',)
        ordering = ('name',)
        verbose_name = u'заказчик'
        verbose_name_plural = u'заказчики'
    def customer_connection_event_count(self):
        return self.customer_connection_event_set.count()
    def serialize_extra(self):
        return {'extras': ('customer_connection_event_count',)}


class Customer_To_Customer(models.Model):
    WHAT_CHOICES = [
        ('1', 'Материнская компания'),
        ('2', 'Дочерняя'),
        ('3', 'Аффилированная'),
    ]
    who = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_to_customer_who', verbose_name=u'кто')
    whom = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_to_customer_whom', verbose_name=u'с кем')
    what = models.IntegerField(max_length=1, blank=True, null=True, db_index=True, choices=WHAT_CHOICES, verbose_name=u'тип')
    when = models.DateTimeField(auto_now_add=True, blank=True, db_index=True, verbose_name=u'когда появилась запись')
    class Meta:
        unique_together = ('who', 'whom')
        ordering = ('who', 'whom')
        verbose_name = u'отношение'
        verbose_name_plural = u'отношения'


class Customer_Department(Default):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name=u'заказчик')
    class Meta:
        verbose_name = u'поразделение заказчика'
        verbose_name_plural = u'поразделения заказчика'
    def to_string(self):
        return '%s - %s' % (self.customer, self.name)



class Customer_To_Branch(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_to_branch', verbose_name=u'заказчик')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='branch_to_customer', verbose_name=u'отрасль')
    class Meta:
        unique_together = ('customer', 'branch')
        ordering = ('customer', 'branch')
        verbose_name = u'отрасль'
        verbose_name_plural = u'отрасли'


class Developer(Organization):
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
        verbose_name = u'исполнитель'
        verbose_name_plural = u'исполнители'


class Developer_Customer_Relation_Status(models.Model):
    STATUS_CHOICES = [
        ('1', 'Заморожен'),
        ('2', 'Холодный'),
        ('3', 'Теплый'),
        ('4', 'Горячий'),
        ('5', 'Горит'),
    ]
    developer = models.ForeignKey(Developer, verbose_name=u'исполнитель')
    customer = models.ForeignKey(Customer, verbose_name=u'заказчик')
    status = models.IntegerField(max_length=1, blank=True, null=True, db_index=True, choices=STATUS_CHOICES, verbose_name=u'статус')
    when = models.DateTimeField(auto_now_add=True, blank=True, db_index=True, verbose_name=u'когда появилась запись')
    next_contact_event_date = models.DateTimeField(blank=True, null=True, db_index=True, verbose_name=u'дата следующего контакта')
    class Meta:
        index_together = [['developer', 'customer', 'when']]
        ordering = ('developer', 'customer', '-when')
        verbose_name = u'статус отношений'
        verbose_name_plural = u'статусы отношений'
    @property
    def last_contact_event(self):
        try:
            return Customer_Connection_Event.objects.filter(developer=self.developer, customer=self.customer).latest('when').when
        except:
            return


class Kis_Type(Default):
    criteria = models.TextField(blank=True, null=True, verbose_name=u'критерии')
    class Meta:
        unique_together = ('name',)
        ordering = ('name',)
        verbose_name = u'тип ИС'
        verbose_name_plural = u'типы ИС'


class Kis(Default):
    developer = models.ForeignKey(Developer, verbose_name=u'владелец')
    kis_type = models.ManyToManyField(Kis_Type, through='Kis_Type_To_Kis', verbose_name=u'типы ИС')
    branch = models.ManyToManyField(Branch, through='Branch_To_Kis', verbose_name=u'отрасли')
    class Meta:
        unique_together = ('developer', 'name',)
        ordering = ('developer', 'name',)
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


class Person(Default):
    birthdate = models.DateField(blank=True, null=True, db_index=True, verbose_name=u'дата рождения')
    city = models.ForeignKey(City, blank=True, null=True, verbose_name=u'город')
    position_category = models.CharField(max_length=500, blank=True, null=True, db_index=True, verbose_name=u'категория должности')
    position = models.CharField(max_length=500, blank=True, null=True, db_index=True, verbose_name=u'должность')
    class Meta:
        abstract = True


class Person_Customer(Person):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name=u'заказчик')
    customer_department = models.ForeignKey(Customer_Department, on_delete=models.CASCADE, blank=True, null=True, verbose_name=u'департамент')
    class Meta:
        ordering = ('customer', 'name')
        verbose_name = u'персона заказчик'
        verbose_name_plural = u'персоны заказчики'


class Person_Developer(Person):
    developer = models.ForeignKey(Developer, verbose_name=u'исполнитель')
    class Meta:
        ordering = ('developer', 'name')
        verbose_name = u'персона исполнитель'
        verbose_name_plural = u'персоны исполнитель'


class Customer_Connection_Event(models.Model):
    developer = models.ForeignKey(Developer, verbose_name=u'владелец')
    customer = models.ForeignKey(Customer, verbose_name=u'заказчик')
    when = models.DateField(auto_now_add=True, blank=True, db_index=True, verbose_name=u'когда')
    status = models.CharField(max_length=500, blank=True, null=True, verbose_name=u'статус')
    comment = models.CharField(max_length=500, blank=True, null=True, verbose_name=u'комментарий')
    position_category = models.CharField(max_length=500, blank=True, null=True, db_index=True, verbose_name=u'категория должности')
    position = models.CharField(max_length=500, blank=True, null=True, db_index=True, verbose_name=u'должность')
    class Meta:
        index_together = [['developer', 'customer', 'when']]
        ordering = ('developer', 'customer', 'when')
        verbose_name = u'контактное событие'
        verbose_name_plural = u'контактные события'
    def __unicode__(self):
        return self.to_string()
    def to_string(self):
        return u"%s — %s & %s" % (self.when, self.developer, self.customer)


class Kis_Sell(Default):
    STATUS_CHOICES = [
        ('start', 'Начало'),
        ('routine', 'Текучка'),
        ('rejected', 'Отклонен'),
        ('sold', 'Продано'),
    ]
    status = models.CharField(max_length=500, blank=True, null=True, db_index=True, choices=STATUS_CHOICES, verbose_name=u'статус')
    when = models.DateField(auto_now_add=True, db_index=True, verbose_name=u'когда')
    customer = models.ForeignKey(Customer, verbose_name=u'заказчик')
    kis = models.ForeignKey(Kis, verbose_name=u'ИС')
    contact = models.ManyToManyField(Person_Customer, through='Contact_To_Kis_Sell', verbose_name=u'контакты')
    class Meta:
        unique_together = ('customer', 'kis')
        ordering = ('kis', 'customer')
        verbose_name = u'проект-проджа'
        verbose_name_plural = u'проекты-продажи'


class Contact_To_Kis_Sell(models.Model):
    kis_sell = models.ForeignKey(Kis_Sell, on_delete=models.CASCADE, related_name='kis_sell_to_contact', verbose_name=u'проект-продажа')
    contact = models.ForeignKey(Person_Customer, on_delete=models.CASCADE, related_name='contact_to_kis_sell', verbose_name=u'контакт')
    class Meta:
        unique_together = ('kis_sell', 'contact')
        ordering = ('kis_sell', 'contact')
        verbose_name = u'продажа через контакт'
        verbose_name_plural = u'продажи через контакты'
