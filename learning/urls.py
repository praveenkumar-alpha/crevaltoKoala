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
    path('course/detail/<int:pk>/activity/add', views.activity_create_on_course_view, name="course/detail/add_activity"),
    path('course/detail/<int:course_pk>/activity/unlink/<int:activity_pk>', views.activity_on_course_unlink_view, name="course/detail/unlink_activity"),
    path('course/detail/<int:course_pk>/activity/delete/<int:activity_pk>', views.activity_on_course_delete_view, name="course/detail/delete_activity"),
    path('course/delete/<pk>/', views.CourseDeleteView.as_view(), name='course/delete'),

    path('activity/my/', views.ActivityListView.as_view(), name="activity/my"),

    # Activity CRUD operations
    path('activity/add', views.ActivityCreateView.as_view(), name='activity/add'),
    path('activity/detail/<pk>/', views.ActivityDetailView.as_view(), name='activity/detail'),
    path('activity/delete/<pk>/', views.ActivityDeleteView.as_view(), name='activity/delete'),
    path('activity/update/<pk>/', views.ActivityUpdateView.as_view(), name='activity/update'),
]
