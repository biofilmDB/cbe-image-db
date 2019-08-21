from urllib.parse import urlencode
from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.copy()
    query.update(kwargs)
    return query.urlencode()

@register.simple_tag(takes_context=True)
def get_detail_image_name(context, **kwargs):
    # import ipdb; ipdb.set_trace()
    name = context['object'].document.name
    name = name.split('/')[-1]
    return name

@register.simple_tag(takes_context=True)
def get_list_image_name(context, **kwargs):
    name = context['image'].document.name.split('/')[-1]
    return name

@register.simple_tag(takes_context=True)
def get_lab_list(context, **kwargs):
    labs = [str(x) for x in context['experiment'].lab.all()]
    return ', '.join(labs)

@register.simple_tag(takes_context=True)
def get_organism_list(context, **kwargs):
    organ = [str(x) for x in context['experiment'].organism.all()]
    return ', '.join(organ)
