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

        column = {
            "status": 0,
            "comment": 1,
            "customer_name_lat": 2,
            "customer_name": 3,
            "customer_url": 4,
            "position_category": 5,
            "position": 6,
            "customer_branch_description": 7,
            "customer_company_size": 8,
            "city_name": 10,
        }

        for s in book.sheets():
            for row in range(s.nrows):
                connection = Customer_Connection_Event()
                connection.status = s.cell(row, column['status']).value
                connection.comment = s.cell(row, column['comment']).value
                connection.position_category = s.cell(row, column['position_category']).value
                connection.position = s.cell(row, column['position']).value
                connection.developer = custis
                try:
                    customer = Customer.objects.get(name = s.cell(row, column['customer_name']).value)
                except ObjectDoesNotExist:
                    customer = Customer()
                    customer.name_lat = s.cell(row, column['customer_name_lat']).value
                    customer.name = s.cell(row, column['customer_name']).value
                    customer.url = s.cell(row, column['customer_url']).value
                    customer.branch_description = s.cell(row, column['customer_branch_description']).value
                    customer.company_size = s.cell(row, column['customer_company_size']).value
                    if s.cell(row, column['city_name']).value:
                        try:
                            city = City.objects.get(name = s.cell(row, column['city_name']).value)
                        except ObjectDoesNotExist:
                            city = City(name = s.cell(row, column['city_name']).value).save()
                            city_create_cnt += 1
                        customer.city = city
                    customer.save()
                    customer_create_cnt += 1
                connection.customer = customer
                connection.save()
                connection_create_cnt += 1

        self.stdout.write('%s connection created with %s customer & %s city' % (connection_create_cnt, customer_create_cnt, city_create_cnt))
