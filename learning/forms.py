from django import forms

from learning.models import Course


class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = ['name', 'description', 'author', 'state']
