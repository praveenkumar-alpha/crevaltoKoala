from django import template
from django.utils.safestring import mark_safe

from learning.models import CourseState

register = template.Library()


@register.filter
def get_state_badge_type(value):
    if value == CourseState.DRAFT.name:
        badge_type = 'info'
    elif value == CourseState.PUBLISHED.name:
        badge_type = 'success'
    elif value == CourseState.ARCHIVED.name:
        badge_type = 'warning'
    else:
        badge_type = 'light'
    return badge_type


@register.filter
def render_markdown(value):
    try:
        import markdown
        return mark_safe(markdown.markdown(value))
    except ImportError:
        return value
