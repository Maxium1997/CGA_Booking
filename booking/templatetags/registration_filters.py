from django import template

from registration.models import User
from registration.definition import Identity

register = template.Library()


@register.filter(name='is_proprietor')
def is_proprietor(user: User):
    return True if user.identity == Identity.Proprietor.value[0] else False
