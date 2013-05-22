import json
from django.core import serializers
from django.http import HttpResponse


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

#todo go to wadofstuff.django.serializers.json
class JSONResponseMixinList(JSONResponseMixin):
    def convert_context_to_json(self, context):
        result = {}
        context_object_name = self.get_context_object_name(context['object_list'])

        for key in context.keys():
            if key in ('object_list', 'view', context_object_name):
                continue
            result[key] = context[key]

        result['object_list'] = json.loads(serializers.serialize('json', context['object_list']))

        return json.dumps(result, indent=4)



class JSONResponseMixinDetail(JSONResponseMixin):
    def convert_context_to_json(self, context):
        serializers.serialize('json', context['object'])