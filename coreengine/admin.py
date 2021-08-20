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
    list_display = ('fees_type', 'financial_year', 'amountINR', 'created')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('fees_type', 'financial_year', 'amountINR', 'student', 'classroom')
        else:
            return []


class RemainingGte(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = ('Remaining Amount')
    parameter_name = 'amount_remaining'

    def lookups(self, request, model_admin):
        return (
            ('0', ('amount remaining')),
            ('1', ('fully paid')),
        )
    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.exclude(amount_remaining = 0)
        if self.value() == '1':
            return queryset.filter(amount_remaining = 0)

@admin.register(models.Amount)
class AmountAdmin(admin.ModelAdmin):
    readonly_fields = ['total_amount', 'amount_remaining']
    list_display = ('student', 'fee', 'amount_remaining', 'total_amount', 'completed')
    list_filter = ('completed', RemainingGte)
    search_fields = ['student__first_name', 'student__last_name']
    # actions = [filter_remaining_fees, filter_out_completed_fees]
    def get_queryset(self, request):
        qs = super(AmountAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(student__user=request.user)
        return qs

@admin.register(file_models.Banner)
class BannerAdmin(admin.ModelAdmin):
    pass
