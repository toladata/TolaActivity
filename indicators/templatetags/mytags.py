from datetime import datetime
from django.template import Variable, VariableDoesNotExist
from django import template
from django.utils.translation import ugettext_lazy as _
from indicators.models import Indicator

register = template.Library()

@register.filter('convert2dateobject')
def convert2dateobject(value):
    try:
        return datetime.strptime(value, '%Y-%m-%d')
    except AttributeError:
        return value
    except Exception:
        return value

@register.filter
def concat_string(value1, value2):
    """
    concatenates two strings together
    Usage: <a href="{{ SOME_LINK|concat_string:object.pk }}">LINK</a>
    """
    return "%s%s" % (value1, value2)

@register.filter('jsonify')
def jsonify(object):
    if isinstance(object, QuerySet):
        return serialize('json', object)
    return simplejson.dumps(object)


@register.filter('symbolize_change')
def symbolize_change(value):
    """
    Returns corresponding math symbol for Direction of change
    Usage:
    {{ indicator.direction_of_change|symbolize_change}}
    """
    if value == Indicator.DIRECTION_OF_CHANGE_NEGATIVE:
        return _("-")

    if value == Indicator.DIRECTION_OF_CHANGE_POSITIVE:
        return _("+")

    return _("NA")

@register.filter('symbolize_measuretype')
def symbolize_measuretype(value):
    """
    Returns corresponding math symbol for Direction of change
    Usage:
    {{ indicator.direction_of_change|symbolize_measuretype}}
    """
    if value == Indicator.NUMBER:
        return _("#")

    if value == Indicator.PERCENTAGE:
        return _("%")

    return ""

@register.filter('hash')
def hash(object, attr):
    """
    Loops a key in a dictionary
    Usage:
    {% for user in result.users %}
        {{user.name}}
        {% for item in result.items %}
            {{ user|hash:item }}
        {% endfor %}
    {% endfor %}
    """
    pseudo_context = {'object': object }
    try:
        value = Variable('object.{}'.format(attr)).resolve(pseudo_context)
    except VariableDoesNotExist:
        value = None
