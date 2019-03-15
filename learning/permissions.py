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

from guardian.shortcuts import assign_perm, remove_perm

from learning import logger


def get_perm_suffix_from_obj(obj):
    return type(obj).__name__.lower()


def apply_author_permissions(obj, allow_anonymous=False):
    logger.debug("Applying author permissions for ”{author}” on “{obj}”.".format(author=obj.author, obj=obj))
    obj_type = get_perm_suffix_from_obj(obj)
    from guardian.utils import get_anonymous_user
    if not get_anonymous_user().has_perm('learning.view_{}'.format(obj_type), obj) and allow_anonymous:
        assign_perm('learning.view_{}'.format(obj_type), get_anonymous_user(), obj)
    for perm_type in ('add', 'view', 'change', 'delete'):
        assign_perm('learning.{perm_type}_{obj_type}'.format(perm_type=perm_type, obj_type=obj_type), obj.author, obj)


def remove_author_permissions(obj, old_author):
    logger.debug("Removing ”{old_author}” permissions on “{obj}”.".format(old_author=old_author, obj=obj))
    obj_type = get_perm_suffix_from_obj(obj)
    for perm_type in ('add', 'view', 'change', 'delete'):
        remove_perm('learning.{perm_type}_{obj_type}'.format(perm_type=perm_type, obj_type=obj_type), old_author, obj)
