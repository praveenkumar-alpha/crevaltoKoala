from enum import Enum

from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import pgettext_lazy
from django.utils.translation import ugettext_lazy as _

from accounts.models import Person


class CourseState(Enum):
    DRAFT = _("Draft")
    PUBLISHED = _("Published")
    ARCHIVED = _("Archived")


class Course(models.Model):
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
        related_name="writes",
        verbose_name=_("Author")
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = pgettext_lazy("Course verbose name (singular form)", "course")
        verbose_name_plural = pgettext_lazy("Course verbose name (plural form)", "courses")
