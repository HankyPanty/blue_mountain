from django.contrib import admin
from django.contrib.auth.models import User

from coreengine import models
from files import models as file_models
import datetime
import ast
import re
import json
# Register your models here.

admin.site.site_header = "Blue Mountain Admin"

@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super(StudentAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(user=request.user)
        return qs
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
    def get_queryset(self, request):
        qs = super(ClassroomAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(students__user=request.user)
        return qs
    pass

@admin.register(models.Teacher)
class TeacherAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ('fees_type', 'amountINR', 'created')

@admin.register(models.Amount)
class AmountAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super(AmountAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(student__user=request.user)
        return qs
    readonly_fields = ['total_amount', 'amount_remaining']

@admin.register(file_models.Banner)
class BannerAdmin(admin.ModelAdmin):
    pass
