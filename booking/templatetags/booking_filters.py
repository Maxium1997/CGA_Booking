from django import template

from booking.definition import Use, State

register = template.Library()


@register.filter(name='readableUse')
def readableUse(use_value: int):
    for use in Use.__members__.values():
        if use_value == use.value[0]:
            return use.value[1]


@register.filter(name='readableState')
def readableState(state_value: int):
    for state in State.__members__.values():
        if state_value == state.value[0]:
            return state.value[1]
