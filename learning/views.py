from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, ListView, UpdateView
from guardian.shortcuts import assign_perm

from learning.forms import CourseForm
from learning.models import Course


class CreateCourse(LoginRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = "learning/course/add_new.html"
    success_url = reverse_lazy("learning:course/my")

    def form_valid(self, form):
        # Just in case somebody wants to play with the form..
        if not form.cleaned_data['author'].id == self.request.user.id:
            messages.error(self.request, _("The user given in your response does not match with you. Are you trying to test us ? Consider joining instead."))
            return self.form_invalid(form)
        else:
            form.save()
            assign_perm('change_course', form.instance.author, form.instance)
            assign_perm('delete_course', form.instance.author, form.instance)
            messages.success(self.request, "Course \"{course_name}\" created!".format(course_name=form.cleaned_data['name']))
            return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)


class CourseListView(ListView):
    model = Course
    template_name = "learning/course/my.html"

    def get_queryset(self):
        return Course.objects.filter(author=self.request.user).all()


class CourseUpdateView(PermissionRequiredMixin, UpdateView):
    model = Course
    template_name = "learning/course/detail.html"

    fields = ['name', 'description', 'state']

    def has_permission(self):
        course = Course.objects.get(pk=self.kwargs['pk'])
        return self.request.user.has_perm('learning.change_course', course)

    def get_success_url(self):
        messages.success(self.request, _("The course “{course_name}” has been updated.".format(course_name=self.object.name)))
        return reverse_lazy('learning:course/detail', kwargs={'pk': self.object.id})
