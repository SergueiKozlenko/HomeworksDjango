from django.contrib import admin

from .models import Student, Teacher


class StudentInLine(admin.TabularInline):
    model = Student.teachers.through
    extra = 1


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    inlines = [StudentInLine]
    exclude = ('teachers',)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    inlines = [StudentInLine]
