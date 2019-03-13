from django.contrib import admin
from guardian.shortcuts import assign_perm

from .models import Course


class CourseAdmin(admin.ModelAdmin):
    model = Course
    list_display = ('id', 'name', 'state', 'published', 'author')
    list_filter = ('published', 'state')

    def save_model(self, request, obj, form, change):
        obj.save()
        assign_perm('change_course', obj.author, obj)
        assign_perm('delete_course', obj.author, obj)


admin.site.register(Course, CourseAdmin)
