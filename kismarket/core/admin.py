from django.contrib import admin
from .models import Branch, Branch_Tech, Kis, Kis_Type, Contact, Developer, Customer


class Branch_Technology_Inline(admin.TabularInline):
    model = Branch_Tech.branch.through
    extra = 0

class Branch_Admin(admin.ModelAdmin):
    inlines = [Branch_Technology_Inline]

class Branch_Inline(admin.TabularInline):
    model = Customer.branch.through
    extra = 0

class Customer_Admin(admin.ModelAdmin):
    inlines = [Branch_Inline]


admin.site.register(Branch, Branch_Admin)
admin.site.register(Branch_Tech)
admin.site.register(Kis)
admin.site.register(Kis_Type)
admin.site.register(Customer, Customer_Admin)
admin.site.register(Contact)
admin.site.register(Developer)