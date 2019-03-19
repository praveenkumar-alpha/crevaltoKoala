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
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.utils.translation import gettext
from django.views.generic import ListView, DetailView

from learning.models import Activity


class ActivityListView(LoginRequiredMixin, ListView):
    model = Activity
    template_name = "learning/activity/my.html"

    def get_queryset(self):
        return Activity.objects.filter(author=self.request.user).all()


class ActivityDetailView(PermissionRequiredMixin, DetailView):
    model = Activity
    template_name = "learning/activity/detail.html"

    def get_object(self, queryset=None):
        return super().get_object()

    def has_permission(self):
        activity = Activity.objects.get(pk=self.kwargs['pk'])
        return self.request.user.has_perm('view_activity', activity)

    def handle_no_permission(self):
        messages.error(
            self.request,
            gettext("You do not have the required permissions to access this activity.") + ' ' + gettext("Try to login, this may solve the issue.")
        )
        return redirect('learning:activity/my')
