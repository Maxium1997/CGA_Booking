from django import template

from registration.models import User
from registration.definition import Privilege, Identity

register = template.Library()


@register.filter(name='is_proprietor')
def is_proprietor(user: User):
    return True if user.identity == Identity.Proprietor.value[0] else False


@register.filter(name='readablePrivilege')
def readablePrivilege(privilege_value):
    for privilege in Privilege.__members__.values():
        if privilege_value == privilege.value[0]:
            return privilege.value[1]


@register.filter(name='readableIdentity')
def readablePrivilege(identity_value):
    for identity in Identity.__members__.values():
        if identity_value == identity.value[0]:
            return identity.value[1]
