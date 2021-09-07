from django.contrib import admin
from django.contrib.auth.models import User
from django.urls import resolve
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
    readonly_fields = ['user']
    def get_queryset(self, request):
        qs = super(StudentAdmin, self).get_queryset(request)
        if request.user.groups.filter(name='student-login'):
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

class activeFY(admin.SimpleListFilter):
    title = ('active_class')
    parameter_name = 'financial_year'

    def lookups(self, request, model_admin):
        return (
            # ('active', ('All')),
            (None, ('Active')),
            ('inactive', ('Inactive')),
            # ('all', ('All')),
        )
    def queryset(self, request, queryset):
        if self.value() == None:
            return queryset.filter(financial_year__status = 1)
        if self.value() == 'inactive':
            return queryset.filter(financial_year__status = 0)
        else:
            return queryset


@admin.register(models.Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    # form = ClassroomForm
    list_filter = ('financial_year','class_name')
    search_fields = ['students__first_name', 'students__last_name']
    filter_horizontal = ('students', )
    def get_readonly_fields(self, request, obj=None):
        print(obj.financial_year)
        if not obj or obj.financial_year.status == 1:
            return []
        else:
            return ['class_name', 'timetable', 'students', 'meet_link', 'section_name', 'financial_year']
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # print(db_field)
        # obj = kwargs.get("obj")
        # studs = []
        # other_classes = models.Classroom.objects.filter(financial_year__status = 1)
        # for clas in other_classes:
        #     studs += list(clas.students.all())
        # other_students = list(set(studs))
        kwargs["queryset"] = models.Student.objects.exclude(status=0)
        return super(ClassroomAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
    def get_queryset(self, request):
        qs = super(ClassroomAdmin, self).get_queryset(request)
        if request.user.groups.filter(name='student-login'):
            return qs.filter(students__user=request.user)
        return qs
    pass

# 

@admin.register(models.Teacher)
class TeacherAdmin(admin.ModelAdmin):
    readonly_fields = ['user']
    pass

# 

@admin.register(models.Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ('fees_type', 'description', 'financial_year', 'amountINR', 'created')

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

# 

class AmountDetailsinline(admin.TabularInline):
    model = models.AmountDetails
    def has_change_permission(self, request, obj=None):
        return False

@admin.register(models.Amount)
class AmountAdmin(admin.ModelAdmin):
    readonly_fields = ['student', 'fee', 'total_amount', 'amount_remaining', 'amount_paid']
    list_display = ('student', 'fee', 'amount_remaining', 'total_amount', 'completed', 'created', 'modified')
    list_filter = ('completed', RemainingGte)
    search_fields = ['student__first_name', 'student__last_name']
    inlines = [AmountDetailsinline]
    # actions = [filter_remaining_fees, filter_out_completed_fees]
    def get_queryset(self, request):
        qs = super(AmountAdmin, self).get_queryset(request)
        if request.user.groups.filter(name='student-login'):
            return qs.filter(student__user=request.user)
        return qs
    def has_add_permission(self, request, obj=None):
        return False

# 

@admin.register(file_models.Banner)
class BannerAdmin(admin.ModelAdmin):
    pass

# 

class PhotoOnline(admin.TabularInline):
    model = file_models.PhotoImage

@admin.register(file_models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    inlines = [PhotoOnline]

# 

class MarksTabularOnline(admin.TabularInline):
    model = models.ExamMark
    fields = ('student', 'marks', 'result', )
    def get_formset(self, request, obj=None, **kwargs):
        self.classroom = None
        if obj:
            self.classroom = obj.classroom
        return super(MarksTabularOnline, self).get_formset(request, obj, **kwargs)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'student' and self.classroom:
            kwargs["queryset"] = self.classroom.students.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(models.Exam)
class ExamAdmin(admin.ModelAdmin):
    inlines = [MarksTabularOnline]

