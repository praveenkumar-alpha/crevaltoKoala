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
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _, gettext
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView

from learning.forms import CourseCreateForm, CourseUpdateForm
from learning.models import Course


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


class CourseCreateView(LoginRequiredMixin, CreateView):
    model = Course
    form_class = CourseCreateForm
    template_name = "learning/course/add.html"
    success_url = reverse_lazy("learning:course/my")

    def form_valid(self, form):
        # Just in case somebody wants to play with the form…
        if not form.cleaned_data['author'].id == self.request.user.id:
            messages.error(self.request, _("The user given in your response does not match with you. Are you trying to test us? Consider joining instead."))
            return self.form_invalid(form)
        else:
            form.save()
            form.instance.apply_author_permissions(public_content=True)
            messages.success(self.request, _('Course “%(course_name)s” created.') % {'course_name': form.instance.name})
            return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)


class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = "learning/course/my.html"

    def get_queryset(self):
        return Course.objects.filter(author=self.request.user).all()


class CourseUpdateView(PermissionRequiredMixin, UpdateView):
    model = Course
    form_class = CourseUpdateForm
    template_name = "learning/course/change.html"

    def has_permission(self):
        course = Course.objects.get(pk=self.kwargs['pk'])
        return self.request.user.has_perm('learning.change_course', course)

    def form_invalid(self, form):
        form = update_valid_or_invalid_form_fields(form)
        return super().form_invalid(form)

    def form_valid(self, form):
        if form.has_changed():
            messages.success(self.request, _('The course “%(course_name)s” has been updated.') % {'course_name': self.object.name})
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('learning:course/detail', kwargs={'pk': self.object.id})


class CourseDetailView(PermissionRequiredMixin, DetailView):
    model = Course
    template_name = "learning/course/detail.html"

    def get_object(self, queryset=None):
        return super().get_object()

    def has_permission(self):
        course = Course.objects.get(pk=self.kwargs['pk'])
        return self.request.user.has_perm('learning.view_course', course)

    def handle_no_permission(self):
        messages.error(
            self.request,
            gettext("You do not have the required permissions to access this course.") + ' ' + gettext("Try to login, this may solve the issue.")
        )
        return redirect('learning:course/my')


class CourseDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Course
    success_url = reverse_lazy('learning:course/my')
    template_name = 'learning/course/delete.html'

    def has_permission(self):
        course = Course.objects.get(pk=self.kwargs['pk'])
        return self.request.user.has_perm('learning.delete_course', course)

    def handle_no_permission(self):
        messages.error(
            self.request,
            gettext("You do not have the required permissions to delete this course.") + ' ' + gettext("Try to login, this may solve the issue.")
        )
        return redirect('learning:course/detail', pk=self.kwargs['pk'])

    def get_success_url(self):
        messages.success(self.request, _('The course ”%(course_name)s” has been deleted') % {'course_name': self.object.name})
        return super().get_success_url()
