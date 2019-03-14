from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from guardian.shortcuts import assign_perm

from .models import Course


class CourseAdmin(GuardedModelAdmin):
    """
     Inheriting from GuardedModelAdmin just adds access to per-object
     permission management tools. This can be replaced by ModelAdmin at any
     time.
    """

    model = Course
    list_display = ('id', 'name', 'state', 'published', 'author')
    list_filter = ('published', 'state')

    def save_model(self, request, obj, form, change):
        super(CourseAdmin, self).save_model(request, obj, form, change)
        assign_perm('change_course', obj.author, obj)
        assign_perm('delete_course', obj.author, obj)


admin.site.register(Course, CourseAdmin)
