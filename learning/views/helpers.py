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

def update_valid_or_invalid_form_fields(form):
    for field in form.fields:
        try:
            current_class = form.fields[field].widget.attrs['class']
        except KeyError:
            current_class = str()

        if field in form.errors:
            form.fields[field].widget.attrs.update({'class': current_class + ' ' + 'is-invalid'})
        elif field in form.changed_data:
            form.fields[field].widget.attrs.update({'class': current_class + ' ' + 'is-valid'})
    return form
