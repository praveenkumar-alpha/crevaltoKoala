from django.urls import path
from django.views.generic import TemplateView

from learning.views import CreateCourse, CourseListView

app_name = 'learning'


urlpatterns = [
    path('', TemplateView.as_view(template_name="learning/index.html"), name='index'),

    path('course/add/', CreateCourse.as_view(), name='course/add'),
    path('course/my', CourseListView.as_view(), name='course/my')
]

