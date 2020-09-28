from django import template

register = template.Library()


@register.filter(name='in_short')
def in_short(ori_str: str, shorten_value: int):
    return ori_str[:shorten_value]
