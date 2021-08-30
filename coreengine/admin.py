from django.contrib import admin
from django.contrib.auth.models import User
from django import forms
from dal import autocomplete

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
    search_fields = ['first_name', 'last_name']
    def get_queryset(self, request):
        qs = super(StudentAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(user=request.user)
        return qs
    pass

# 

@admin.register(models.StudentAttendance)
class StudentAttendanceAdmin(admin.ModelAdmin):
    pass

# 

@admin.register(models.StudentComment)
class StudentCommentAdmin(admin.ModelAdmin):
    pass

# 

@admin.register(models.FY)
class FYAdmin(admin.ModelAdmin):
    pass

# 

class ClassroomForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ClassroomForm, self).__init__(*args, **kwargs)
        if not kwargs.get('instance'):
            pass
            # chain_choices = core_helper.get_all_chain_details_tuple()
            # self.fields['selected_chains'].choices = chain_choices

    exams = forms.ModelChoiceField(queryset=models.Exam.objects.all(),
                                    widget=autocomplete.ModelSelect2(), required=True)
    def get_current_fy(self):
        return self.cleaned_data.get("financial_year")

@admin.register(models.Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    # form = ClassroomForm
    list_filter = ('financial_year','class_name')
    search_fields = ['students__first_name', 'students__last_name']
    filter_horizontal = ('students', 'exams')
    def get_queryset(self, request):
        qs = super(ClassroomAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(students__user=request.user)
        return qs
    pass

# 

@admin.register(models.Teacher)
class TeacherAdmin(admin.ModelAdmin):
    pass

# 

@admin.register(models.Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ('fees_type', 'financial_year', 'amountINR', 'created')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('fees_type', 'financial_year', 'amountINR', 'student', 'classroom')
        else:
            return []

# 

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

# 

@admin.register(file_models.Banner)
class BannerAdmin(admin.ModelAdmin):
    pass

# 

class PhotoOnline(admin.TabularInline):
    model = file_models.PhotoImage

@admin.register(file_models.Photo)
class ExamAdmin(admin.ModelAdmin):
    inlines = [PhotoOnline]

# 

class MarksTabularOnline(admin.TabularInline):
    model = models.ExamMark

@admin.register(models.Exam)
class ExamAdmin(admin.ModelAdmin):
    inlines = [MarksTabularOnline]

# 

@admin.register(models.ExamMark)
class ExamMarkAdmin(admin.ModelAdmin):
    list_display = ('exam', 'student', 'subject', 'marks', 'total_marks', 'created')
    list_filter = ('exam', )
    search_fields = ['student__first_name', 'student__last_name']

    def get_exam(self):
        return self.exam.__str__
    def get_queryset(self, request):
        qs = super(ExamMarkAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(student__user=request.user)
        return qs


