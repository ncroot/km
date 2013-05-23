# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Branch, Branch_Tech, Kis, Kis_Type, Kis_Sell, Person_Customer, Developer, Customer, Customer_Connection_Event, Developer_Customer_Relation_Status, Customer_Department, Person_Developer
from nested_inlines.admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline


class Branch_Technology_To_Branch_Inline(admin.TabularInline):
    model = Branch_Tech.branch.through
    extra = 0
class Branch_Admin(admin.ModelAdmin):
    inlines = [Branch_Technology_To_Branch_Inline]



class Kis_Type_Admin(admin.ModelAdmin):
    list_display = ('name', '_get_text', '_get_criteria')
    def _get_criteria(self, obj):
        return mark_safe('<br />'.join(obj.criteria.split('\n')))
    _get_criteria.short_description = u'критерии'
    def _get_text(self, obj):
        return mark_safe('<br />'.join(obj.text.split('\n')))
    _get_text.short_description = u'какое-нибудь описание например'



class Custumer_To_Branch_Inline(admin.TabularInline):
    model = Customer.branch.through
    extra = 0
class Custumer_Department_Inline(admin.TabularInline):
    model = Customer_Department
    extra = 0
class Customer_Admin(admin.ModelAdmin):
    list_display = ('name', 'name_lat', 'city', 'company_size', 'branch_description')
    inlines = [Custumer_Department_Inline, Custumer_To_Branch_Inline]



class Kis_Type_To_Kis_Inline(admin.TabularInline):
    model = Kis.kis_type.through
    extra = 0
class Branch_To_Kis_Inline(admin.TabularInline):
    model = Kis.branch.through
    extra = 0
class Kis_Admin(admin.ModelAdmin):
    inlines = [Branch_To_Kis_Inline, Kis_Type_To_Kis_Inline]



class Kis_Sell_To_Contact_Inline(admin.TabularInline):
    model = Kis_Sell.contact.through
    extra = 0
class Kis_Sell_Admin(admin.ModelAdmin):
    inlines = [Kis_Sell_To_Contact_Inline]



class Developer_Customer_Relation_Status_Inline(admin.TabularInline):
    def _get_last_contact_event(self, obj):
        return obj.last_contact_event
    _get_last_contact_event.short_description = u'последний контакт'
    model = Developer_Customer_Relation_Status
    fields = ['customer', 'status', 'next_contact_event_date', '_get_last_contact_event']
    readonly_fields = ['_get_last_contact_event']
    inlines = []
    extra = 0
#todo разобраться с вложенными инлайнами!
class Developer_Kis_To_Kis_Type_Inline(NestedTabularInline):
    model = Kis.kis_type.through
class Developer_Kis_To_Branch_Inline(NestedTabularInline):
    model = Kis.branch.through
class Developer_Kis_Inline(NestedTabularInline):
    model = Kis
    inlines = [Developer_Kis_To_Kis_Type_Inline, Developer_Kis_To_Branch_Inline]
    extra = 0

class Developer_Admin(NestedModelAdmin):
    inlines = [Developer_Customer_Relation_Status_Inline, Developer_Kis_Inline]
    list_display = ('name', 'city', 'revenue_2011', 'revenue_2010', 'revenue_incresure_from_2010_to_2012_in_percent', 'staff_2011', 'staff_2010', 'staff_incresure_from_2010_to_2012_in_percent')


admin.site.register(Branch, Branch_Admin)
admin.site.register(Branch_Tech)
admin.site.register(Kis, Kis_Admin)
admin.site.register(Kis_Type, Kis_Type_Admin)
admin.site.register(Kis_Sell, Kis_Sell_Admin)
admin.site.register(Customer, Customer_Admin)
admin.site.register(Person_Customer)
admin.site.register(Person_Developer)
admin.site.register(Developer, Developer_Admin)
admin.site.register(Customer_Connection_Event)
