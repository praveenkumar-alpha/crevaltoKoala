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

from django.urls import path
from django.views.generic import TemplateView

import learning.views as views

app_name = 'learning'

urlpatterns = [
    path('', TemplateView.as_view(template_name="learning/index.html"), name='index'),

    path('course/my/', views.CourseListView.as_view(), name='course/my'),

    # Course CRUD operations
    path('course/add/', views.CourseCreateView.as_view(), name='course/add'),
    path('course/update/<pk>/', views.CourseUpdateView.as_view(), name='course/update'),
    path('course/detail/<pk>/', views.CourseDetailView.as_view(), name='course/detail'),
    path('course/delete/<pk>/', views.CourseDeleteView.as_view(), name='course/delete')
]
