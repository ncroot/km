# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Branch, Branch_Tech, Kis, Kis_Type, Contact, Developer, Customer, Customer_Connection_Event


class Branch_Technology_To_Branch_Inline(admin.TabularInline):
    model = Branch_Tech.branch.through
    extra = 0
class Branch_Admin(admin.ModelAdmin):
    inlines = [Branch_Technology_To_Branch_Inline]


class Developer_Admin(admin.ModelAdmin):
    list_display = ('name', 'city', 'revenue_2011', 'revenue_2010', 'revenue_incresure_from_2010_to_2012_in_percent', 'staff_2011', 'staff_2010', 'staff_incresure_from_2010_to_2012_in_percent')


class Kis_Type_Admin(admin.ModelAdmin):
    list_display = ('name', '_get_text', '_get_criteria')
    def _get_criteria(self, obj):
        return mark_safe('<br />'.join(obj.criteria.split('\n')))
    _get_criteria.short_description = u'критерии'
    def _get_text(self, obj):
        return mark_safe('<br />'.join(obj.text.split('\n')))
    _get_text.short_description = u'какое-нибудь описание например'


class Branch_To_Custumer_Inline(admin.TabularInline):
    model = Customer.branch.through
    extra = 0
class Customer_Admin(admin.ModelAdmin):
    list_display = ('name', 'name_lat', 'city', 'company_size', 'branch_description')
    inlines = [Branch_To_Custumer_Inline]



class Kis_Type_To_Kis_Inline(admin.TabularInline):
    model = Kis.kis_type.through
    extra = 0
class Branch_To_Kis_Inline(admin.TabularInline):
    model = Kis.branch.through
    extra = 0
class Kis_Admin(admin.ModelAdmin):
    inlines = [Branch_To_Kis_Inline, Kis_Type_To_Kis_Inline]


admin.site.register(Branch, Branch_Admin)
admin.site.register(Branch_Tech)
admin.site.register(Kis, Kis_Admin)
admin.site.register(Kis_Type, Kis_Type_Admin)
admin.site.register(Customer, Customer_Admin)
admin.site.register(Contact)
admin.site.register(Developer, Developer_Admin)
admin.site.register(Customer_Connection_Event)