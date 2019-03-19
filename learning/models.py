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

from enum import Enum

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy

from accounts.models import Person
from learning.permissions import ObjectPermissionManagerMixin


class CourseState(Enum):
    DRAFT = _("Draft")
    PUBLISHED = _("Published")
    ARCHIVED = _("Archived")


class Course(ObjectPermissionManagerMixin, models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name=_("Name")
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Description"),
        help_text=mark_safe(_('You can use the <a href="https://www.markdownguide.org/basic-syntax/" target="_blank">Markdown</a> syntax here.'))
    )
    state = models.CharField(
        max_length=20,
        choices=[(state.name, state.value) for state in CourseState],
        default=CourseState.DRAFT.name,
        verbose_name=_("State")
    )
    published = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
        verbose_name=_("Published the")
    )
    updated = models.DateTimeField(
        auto_now_add=False,
        auto_now=True,
        verbose_name=_("Last updated the")
    )
    author = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="course",
        verbose_name=_("Author")
    )

    @property
    def activities(self):
        return [course_activity.activity for course_activity in self.course_activities.order_by('rank').all()]

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = pgettext_lazy("Course verbose name (singular form)", "course")
        verbose_name_plural = pgettext_lazy("Course verbose name (plural form)", "courses")


class Activity(ObjectPermissionManagerMixin, models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name=_("Name")
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Description"),
        help_text=mark_safe(_('You can use the <a href="https://www.markdownguide.org/basic-syntax/" target="_blank">Markdown</a> syntax here.'))
    )
    published = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
        verbose_name=_("Published the")
    )
    updated = models.DateTimeField(
        auto_now_add=False,
        auto_now=True,
        verbose_name=_("Last updated the")
    )
    author = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="activities",
        verbose_name=_("Author")
    )

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        pass

    class Meta:
        ordering = ["name"]
        verbose_name = pgettext_lazy("Activity verbose name (singular form)", "activity")
        verbose_name_plural = pgettext_lazy("Activity verbose name (plural form)", "activities")


class CourseActivity(models.Model):
    rank = models.PositiveIntegerField(
        verbose_name=_("Rank")
    )
    minimal_allowed_score = models.PositiveIntegerField(
        verbose_name=_("Minimal allowed score"),
        default=25,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ]
    )
    success_score = models.PositiveIntegerField(
        verbose_name=_("Success score"),
        default=50,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0),
        ]
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="course_activities",
        verbose_name=_("Course")
    )
    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
        related_name="course_activities",
        verbose_name=_("Activity")
    )

    def clean(self):
        if self.success_score <= self.minimal_allowed_score:
            raise ValidationError(
                _("Success score must be greater than minimal score.")
            )
        return super().clean()

    class Meta:
        unique_together = ("rank", "course")
        ordering = ["rank"]
        verbose_name = pgettext_lazy("Course activity verbose name (singular form)", "course activity")
        verbose_name_plural = pgettext_lazy("Course activity verbose name (plural form)", "course activities")
