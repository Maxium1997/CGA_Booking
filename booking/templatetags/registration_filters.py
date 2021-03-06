from django import template
from datetime import datetime, timedelta

from registration.models import User
from registration.definition import Privilege, Identity, Gender

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
def readableIdentity(identity_value):
    for identity in Identity.__members__.values():
        if identity_value == identity.value[0]:
            return identity.value[1]


@register.filter(name='readableIdentity_shortening')
def readableIdentity_shortening(identity_value, shorten_value):
    for identity in Identity.__members__.values():
        if identity_value == identity.value[0]:
            return identity.value[1][:shorten_value]+"."


@register.filter(name='readableGender')
def readableGender(gender_value):
    gender_value = int(gender_value)
    for gender in Gender.__members__.values():
        if gender_value == gender.value[0]:
            return gender.value[1]


@register.filter(name='year_class')
def year_class(date: datetime):
    try:
        return date.year - 1911
    except AttributeError:
        pass
