#
# Copyright (C) 2019 Guillaume Bernard <guillaume.bernard@loria.fr>
#
# This file is part of Koala LMS (Learning Management system)

# Koala LMS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# We make an extensive use of the Django framework, https://www.djangoproject.com/
#

from django import template
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

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
def get_state_badge_title(value):
    if value == CourseState.DRAFT.name:
        badge_title = _("This course is a draft. It is not visible by others except collaborators and no one can register.")
    elif value == CourseState.PUBLISHED.name:
        badge_title = _("This course is published. Every change will be publicly available.")
    elif value == CourseState.ARCHIVED.name:
        badge_title = _("This course is archived. Therefore, it is read-only. No one can register to the course anymore.")
    else:
        badge_title = ""
    return badge_title


@register.filter
def render_markdown(value):
    try:
        import markdown
        return mark_safe(markdown.markdown(value))
    except ImportError:
        return value
