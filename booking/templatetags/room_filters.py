from django import template

register = template.Library()


@register.filter(name='shorten_to')
def shorten_to(original_text: str, word_count: int):
    if original_text:
        return original_text[0:word_count] + '...'
    return 'No introduction recently.'
