from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.utils.safestring import mark_safe
from django.template import Library
import json


register = Library()


def jsonify(object):
    if isinstance(object, QuerySet):
        print(object)
        return mark_safe(serialize('json', object))

    if isinstance(object, list):
        object = list(map(lambda o: json.loads(json_serialize(o)), object))

    data = mark_safe(json.dumps(object))
    return data


def json_serialize(object):
    return json.dumps(object.__dict__)


register.filter('jsonify', jsonify)
jsonify.is_safe = True
