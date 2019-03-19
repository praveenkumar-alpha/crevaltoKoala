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
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Max
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from learning.forms import ActivityCreateForm
from learning.forms.activity import CourseActivityForm
from learning.models import Activity, Course, CourseActivity
from learning.views.helpers import update_valid_or_invalid_form_fields


class ActivityCreateView(LoginRequiredMixin, CreateView):
    model = Activity
    form_class = ActivityCreateForm
    template_name = "learning/activity/add.html"
    success_url = reverse_lazy("learning:activity/my")


@login_required
def activity_create_on_course_view(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if not course.user_can_change(request.user):
        raise PermissionDenied

    if request.method == "POST":
        course_activity_form = CourseActivityForm(request.POST, prefix="course_activity")
        activity_form = ActivityCreateForm(request.POST, prefix="activity_create")

        if all([course_activity_form.is_valid(), activity_form.is_valid()]):

            # Manually set the activity author to the current user
            activity_form.instance.author = request.user
            activity_form.save()
            activity_form.instance.apply_author_permissions()

            # Linking activity and course to the course activity instance
            course_activity_form.instance.activity = activity_form.instance
            course_activity_form.instance.course = course
            course_activity_form.save()

            messages.success(
                request,
                _('The activity “%(activity_name)s” has been added to this course.') % {'activity_name': activity_form.instance.name}
            )
            return redirect("learning:course/detail", pk=course.id)
        else:
            course_activity_form = update_valid_or_invalid_form_fields(course_activity_form)
            activity_form = update_valid_or_invalid_form_fields(activity_form)
            for error in course_activity_form.errors:
                messages.error(request, course_activity_form.errors[error])
    else:
        rank = CourseActivity.objects.filter(course=course).aggregate(Max('rank'))['rank__max'] + 1
        course_activity_form = CourseActivityForm(prefix="course_activity", initial={'rank': rank, 'course': course})
        activity_form = ActivityCreateForm(prefix="activity_create", initial={'author': request.user})

    context = {
        'course_activity_form': course_activity_form,
        'activity_form': activity_form
    }
    return render(request, "learning/activity/add.html", context)


@login_required
def activity_on_course_unlink_view(request, course_pk, activity_pk):
    course = get_object_or_404(Course, pk=course_pk)
    activity = get_object_or_404(Activity, pk=activity_pk)
    course_activity = CourseActivity.objects.filter(course=course).filter(activity=activity).get()
    if course.user_can_change(request.user):
        course_activity.delete()
    else:
        messages.error(
            request,
            gettext("You do not have the required permissions to unlink this activity from this course.") + ' ' + gettext("Try to login, this may solve the issue.")
        )
    return redirect("learning:course/detail", pk=course.id)


@login_required
def activity_on_course_delete_view(request, course_pk, activity_pk):
    course = get_object_or_404(Course, pk=course_pk)
    activity = get_object_or_404(Activity, pk=activity_pk)

    if course.user_can_change(request.user):
        activity.delete()
    else:
        messages.error(
            request,
            gettext("You do not have the required permissions to delete this activity.") + ' ' + gettext("Try to login, this may solve the issue.")
        )

    return redirect("learning:course/detail", pk=course.id)


class ActivityListView(LoginRequiredMixin, ListView):
    model = Activity
    template_name = "learning/activity/my.html"

    def get_queryset(self):
        return Activity.objects.filter(author=self.request.user).all()


class ActivityDetailView(PermissionRequiredMixin, DetailView):
    model = Activity
    template_name = "learning/activity/detail.html"

    def has_permission(self):
        return self.get_object().user_can_view(self.request.user)

    def handle_no_permission(self):
        messages.error(
            self.request,
            gettext("You do not have the required permissions to access this activity.") + ' ' + gettext("Try to login, this may solve the issue.")
        )
        return redirect('learning:activity/my')


class ActivityDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Activity
    success_url = reverse_lazy('learning:activity/my')
    template_name = 'learning/activity/delete.html'

    def has_permission(self):
        return self.get_object().user_can_delete(self.request.user)

    def handle_no_permission(self):
        messages.error(
            self.request,
            gettext("You do not have the required permissions to delete this activity.") + ' ' + gettext("Try to login, this may solve the issue.")
        )
        return redirect('learning:activity/my')
