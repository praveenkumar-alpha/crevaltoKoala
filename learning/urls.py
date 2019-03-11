from django.urls import path
from django.views.generic import TemplateView

from learning.views import CreateCourse

app_name = 'learning'

urlpatterns = [
    path('', TemplateView.as_view(template_name="learning/index.html"), name='index'),

    path('course/add/', CreateCourse.as_view(), name='create_course')
]

