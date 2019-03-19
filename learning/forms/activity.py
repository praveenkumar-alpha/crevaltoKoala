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

from django import forms
from markdownx.fields import MarkdownxFormField

from learning.models import Activity, CourseActivity


class CourseActivityForm(forms.ModelForm):
    class Meta:
        model = CourseActivity
        fields = ['rank', 'minimal_allowed_score', 'success_score']


class ActivityForm(forms.ModelForm):
    description = MarkdownxFormField()


class ActivityCreateForm(ActivityForm):
    class Meta:
        model = Activity
        fields = ['name', 'description']


class ActivityUpdateForm(ActivityForm):
    class Meta:
        model = Activity
        fields = ['name', 'description', 'author']
