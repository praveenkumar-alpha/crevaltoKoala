from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, ListView

import settings
from learning.forms import CourseForm
from learning.models import Course


class CreateCourse(LoginRequiredMixin, CreateView):
    login_url = settings.LOGIN_URL
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
