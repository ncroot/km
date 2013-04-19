# -*- coding: utf-8 -*-

import os
from optparse import make_option
from django.core.management.base import BaseCommand
from django.utils.encoding import smart_str
from setuptools.command.develop import develop
from kismarket.core.models import Customer_Connection_Event, Customer, Developer
from kismarket.settings import PROJECT_DIR
from xlrd import open_workbook, XLRDError
from django.core.exceptions import ObjectDoesNotExist
from kismarket.starter.models import City


class Command(BaseCommand):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.option_list += (
            make_option('-f', '--file', action='store', dest='file', default='data/Customer_Connection_Event.xlsx', type='string', help='Path to customer connection event .xlsx file in %s' % PROJECT_DIR),
        )

    def handle(self, *args, **options):
        file_path = os.path.join(PROJECT_DIR, options.get('file'))

        try:
            book = open_workbook(file_path, encoding_override="cp1251")
        except IOError:
            return self.stdout.write('file not found "%s"' % file_path)
        except XLRDError:
            return self.stdout.write('file is not excel sheet "%s"' % file_path)

        custis = Developer.objects.get(name = 'CUSTIS')

        customer_create_cnt = 0
        connection_create_cnt = 0
        city_create_cnt = 0

        for s in book.sheets():
            for row in range(s.nrows):
                connection = Customer_Connection_Event()
                connection.status = s.cell(row, 0).value
                connection.comment = s.cell(row, 1).value
                connection.position_category = s.cell(row, 5).value
                connection.position = s.cell(row, 6).value
                connection.developer = custis
                try:
                    customer = Customer.objects.get(name = s.cell(row, 3).value)
                except ObjectDoesNotExist:
                    customer = Customer()
                    customer.name_lat = s.cell(row, 2).value
                    customer.name = s.cell(row, 3).value
                    customer.url = s.cell(row, 4).value
                    customer.branch_description = s.cell(row, 7).value
                    customer.company_size = s.cell(row, 8).value
                    try:
                        city = City.objects.get(name = s.cell(row, 10).value)
                    except ObjectDoesNotExist:
                        city = City(name = s.cell(row, 10).value).save()
                        city_create_cnt += 1
                    customer.city = city
                    customer.save()
                    customer_create_cnt += 1
                connection.customer = customer
                connection.save()
                connection_create_cnt += 1

        self.stdout.write('%s connection created with %s customer & %s city' % (connection_create_cnt, customer_create_cnt, city_create_cnt))
