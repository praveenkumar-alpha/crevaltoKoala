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
from guardian.utils import get_anonymous_user

from learning import logger


class ObjectPermissionManagerMixin:

    author = None

    def __get_class_name(self):
        return type(self).__name__.lower()

    def __apply_perms_for(self, perms, user):
        for permission in self.__make_perms(perms):
            assign_perm(permission, user, self)

    def __remove_perms_for(self, perms, user):
        for permission in self.__make_perms(perms):
            remove_perm(permission, user, self)

    def __apply_perms_for_anonymous(self, perms):
        anon = get_anonymous_user()
        for permission in self.__make_perms(perms):
            if not anon.has_perm(permission):
                assign_perm(permission, anon, self)

    def __remove_perms_for_anonymous(self, perms):
        anon = get_anonymous_user()
        for permission in self.__make_perms(perms):
            if anon.has_perm(permission):
                remove_perm(permission, anon, self)

    def __make_perms(self, perms):
        obj_type = self.__get_class_name()
        well_perms = list()
        for perm_type in perms:
            well_perms.append('{perm_type}_{obj_type}'.format(perm_type=perm_type, obj_type=obj_type))
        return well_perms

    def apply_author_permissions(self, public_content=False):
        logger.debug("Applying author permissions for ”{author}” on “{obj}”.".format(author=self.author, obj=self))
        perms = ['add', 'view', 'change', 'delete']
        self.__apply_perms_for(perms, self.author)
        if public_content:
            self.__apply_perms_for_anonymous(['view'])

    def remove_author_permissions(self, old_author):
        logger.debug("Removing ”{old_author}” permissions on “{obj}”.".format(old_author=old_author, obj=self))
        self.__remove_perms_for(['add', 'view', 'change', 'delete'], old_author)

    def transfer_ownership(self, old_owner):
        self.remove_author_permissions(old_owner)
        self.apply_author_permissions()
