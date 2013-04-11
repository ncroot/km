# -*- coding: utf-8 -*-

import os, json
from django.db import connection, transaction
from django.conf import settings
from django.db.models import get_app
from django.core import serializers
from django.http import HttpResponse
from random import randrange
from datetime import timedelta



def instance_dict(instance, key_format=None):
   "Returns a dictionary containing field names and values for the given instance"
   from django.db.models.fields.related import ForeignKey
   if key_format:
       assert '%s' in key_format, 'key_format must contain a %s'
   key = lambda key: key_format and key_format % key or key

   d = {}
   for field in instance._meta.fields:
       attr = field.name
       value = getattr(instance, attr)
       if value is not None and isinstance(field, ForeignKey):
           value = value._get_pk_val()
       d[key(attr)] = value
   for field in instance._meta.many_to_many:
       d[key(field.name)] = [obj._get_pk_val() for obj in getattr(instance, field.attname).all()]
   return d


def pluralize(value, arg=u"один,два,ноль/много"):
    args = arg.split(",")
    if not value:
       return args[2]
    number = abs(int(value))
    a = number % 10
    b = number % 100
    if (a == 1) and (b != 11):
        return args[0]
    elif (a > 1) and (a < 5) and ((b < 10) or (b > 20)):
        return args[1]
    else:
        return args[2]


def load_customized_sql(**kwargs_parent):
    def run_sql_from_file(**kwargs):
        app = get_app(kwargs.get('app'))
        app_dir = os.path.normpath(os.path.join(os.path.dirname(app.__file__), 'sql'))
        name = kwargs_parent.get('name', 'custom')
        custom_files = [
            os.path.join(app_dir, "%s.%s.sql" % (name, settings.DATABASE_ENGINE)),
            os.path.join(app_dir, "%s.sql" % name)
        ]
        for custom_file in custom_files:
            if os.path.exists(custom_file):
                print "Loading SQL for %s from '%s'" % (app.__name__, os.path.basename(custom_file))
                fp = open(custom_file, 'U')
                cursor = connection.cursor()
                try:
                    cursor.execute(fp.read())
                except Exception, e:
                    print "Couldn't execute SQL for %s from %s" % (app.__name__, os.path.basename(custom_file))
                    import traceback
                    traceback.print_exc()
                    transaction.rollback_unless_managed()
                else:
                    transaction.commit_unless_managed()
    return run_sql_from_file


class JSONResponseMixin(object):
    """
    A mixin that can be used to render a JSON response.
    """
    response_class = HttpResponse

    def render_to_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        response_kwargs['content_type'] = 'application/json'
        return self.response_class(
            self.convert_context_to_json(context),
            **response_kwargs
        )

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return json.dumps(context)

class JSONResponseMixinList(JSONResponseMixin):
    def convert_context_to_json(self, context):
        try:
            extra = context['object_list'][0].serialize_extra()
            return serializers.serialize('json', context['object_list'], **extra)
        except:
            try:
                return json.dumps(context)
            except:
                return json.dumps({})

class JSONResponseMixinDetail(JSONResponseMixin):
    def convert_context_to_json(self, context):
        serializers.serialize('json', context['object_list'])


def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return (start + timedelta(seconds=random_second))
