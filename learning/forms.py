from django import forms
from markdownx.fields import MarkdownxFormField

from learning.models import Course


class CourseForm(forms.ModelForm):

    description = MarkdownxFormField()

    class Meta:
        model = Course
        fields = ['name', 'description', 'author', 'state']
