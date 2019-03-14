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

from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from guardian.shortcuts import assign_perm

from .models import Course


class CourseAdmin(GuardedModelAdmin):
    """
     Inheriting from GuardedModelAdmin just adds access to per-object
     permission management tools. This can be replaced by ModelAdmin at any
     time.
    """

    model = Course
    list_display = ('id', 'name', 'state', 'published', 'author')
    list_filter = ('published', 'state')

    def save_model(self, request, obj, form, change):
        super(CourseAdmin, self).save_model(request, obj, form, change)
        assign_perm('change_course', obj.author, obj)
        assign_perm('delete_course', obj.author, obj)


admin.site.register(Course, CourseAdmin)
