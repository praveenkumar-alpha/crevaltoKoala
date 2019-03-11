from django.contrib import admin

from .models import Course


class CourseAdmin(admin.ModelAdmin):
    model = Course
    list_display = ('name', 'state', 'published', 'author')


admin.site.register(Course, CourseAdmin)
