from django.contrib import admin
from django.contrib.auth.models import User

from coreengine import models
import datetime
import ast
import re
import json
# Register your models here.

admin.site.site_header = "Blue Mountain Admin"

@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    pass

@admin.register(models.StudentPersonalInfo)
class StudentPersonalInfoAdmin(admin.ModelAdmin):
    pass

@admin.register(models.StudentAttendance)
class StudentAttendanceAdmin(admin.ModelAdmin):
    pass

@admin.register(models.StudentComment)
class StudentCommentAdmin(admin.ModelAdmin):
    pass

@admin.register(models.FY)
class FYAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Teacher)
class TeacherAdmin(admin.ModelAdmin):
    pass

@admin.register(models.TeacherPersonalInfo)
class TeacherPersonalInfoAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ('fees_type', 'amountINR', 'created')

@admin.register(models.Amount)
class AmountAdmin(admin.ModelAdmin):
    readonly_fields = ['total_amount', 'amount_remaining']

