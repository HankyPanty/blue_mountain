from django.contrib import admin
from django.contrib.auth.models import User
from django.urls import resolve
from django import forms
from django.urls import path, include
from django.http import HttpResponse
from django.db.models import Q, F, Sum, Value, ForeignKey, IntegerField, CharField, PROTECT
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
    list_display = ('student', 'comment_type', 'comment', 'resolved')

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

class ClassroomStudentInline(admin.TabularInline):
    model = models.ClassroomStudent
    def get_formset(self, request, obj=None, **kwargs):
        self.classroom = None
        if obj:
            self.classroom = obj
        return super(ClassroomStudentInline, self).get_formset(request, obj, **kwargs)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'student' and self.classroom:
            existing_studs = models.ClassroomStudent.objects.filter(classroom__financial_year = self.classroom.financial_year).exclude(classroom=self.classroom)
            existing_studs = list(existing_studs.values_list('student_id', flat = True))
            kwargs["queryset"] = models.Student.objects.filter(status=1).exclude(id__in = existing_studs)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class TimetableInline(admin.TabularInline):
    model = models.ClassroomTimeTable

class FeeInline(admin.TabularInline):
    model = models.Fee

@admin.register(models.Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    # form = ClassroomForm
    fields = ('class_name', 'section_name', 'financial_year', 'meet_link')
    list_filter = ('financial_year','class_name')
    search_fields = ['classroomstudent__student__first_name', 'classroomstudent__student__last_name']
    # filter_horizontal = ('students', )
    inlines = [ClassroomStudentInline, TimetableInline, FeeInline]
    def get_readonly_fields(self, request, obj=None):
        if not obj or obj.financial_year.status == 1:
            return []
        else:
            return ['class_name', 'timetable', 'meet_link', 'section_name', 'financial_year']
    # def get_search_results(self, request, queryset, search_term):
    #     queryset, use_distinct = super(ClassroomAdmin, self).get_search_results(request, queryset, search_term)
    #     try:
    #         queryset = model.Student.objects.get(id__in = )
    #     except:
    #         pass
    #     return queryset, use_distinct
    # def formfield_for_manytomany(self, db_field, request, **kwargs):
    #     # obj = kwargs.get("obj")
    #     # studs = []
    #     # other_classes = models.Classroom.objects.filter(financial_year__status = 1)
    #     # for clas in other_classes:
    #     #     studs += list(clas.students.all())
    #     # other_students = list(set(studs))
    #     kwargs["queryset"] = models.Student.objects.exclude(status=0)
    #     return super(ClassroomAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
    def get_queryset(self, request):
        qs = super(ClassroomAdmin, self).get_queryset(request)
        if request.user.groups.filter(name='student-login'):
            return qs.filter(classroomstudent__student__user=request.user)
        return qs
    pass

# 

@admin.register(models.Teacher)
class TeacherAdmin(admin.ModelAdmin):
    readonly_fields = ['user']
    pass

# 

# @admin.register(models.Fee)
# class FeeAdmin(admin.ModelAdmin):
#     list_display = ('fees_type', 'description', 'financial_year', 'amountINR', 'created')
#     fields = ('fees_type', 'description', 'amountINR', 'financial_year', ('student'), ('classroom'))

#     def get_readonly_fields(self, request, obj=None):
#         if obj:
#             return ('fees_type', 'financial_year', 'amountINR', 'student', 'classroom')
#         else:
#             return []

#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         if db_field.name == 'classroom':
#             kwargs["queryset"] = models.Classroom.objects.filter(financial_year__status = 1)
#         if db_field.name == 'financial_year':
#             kwargs["queryset"] = models.FY.objects.filter(status = 1)
#         return super().formfield_for_foreignkey(db_field, request, **kwargs)

# # 

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
    list_display = ('student', 'fee', 'amount_remaining', 'total_amount', 'completed', 'created', 'modified')
    list_filter = ('completed', RemainingGte)
    search_fields = ['student__first_name', 'student__last_name']
    inlines = [AmountDetailsinline]
    # actions = [filter_remaining_fees, filter_out_completed_fees]
    change_list_template = 'admin/total_amounts_template.html'
    def get_readonly_fields(self, request, obj=None):
        if not obj:
            return ['fee', 'amount_remaining', 'amount_paid']
        else:
            return ['student', 'fee', 'total_amount', 'amount_remaining', 'amount_paid']
    def get_queryset(self, request):
        qs = super(AmountAdmin, self).get_queryset(request)
        if request.user.groups.filter(name='student-login'):
            return qs.filter(student__user=request.user)
        return qs

    # def changelist_view(self, request, extra_context=None):
    #     response = super(AmountAdmin, self).changelist_view(request)
    #     try:
    #         qs = response.context_data['cl'].queryset
    #     except:
    #         return response
    #     total_amount = qs.aggregate(Sum('total_amount'))['total_amount__sum']
    #     total_amount_received = qs.aggregate(Sum('amount_paid'))['amount_paid__sum']
    #     total_amount_pending = qs.filter(completed=0).aggregate(Sum('amount_remaining'))['amount_remaining__sum']
    #     total_installments_pending = qs.filter(completed=0).count()

    #     response.context_data['cl'].queryset = list(qs)
    #     return response

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('total_amounts/', self.get_total_amounts)
        ]
        return custom_urls + urls

    def get_total_amounts(self, request):
        qs = self.get_queryset(request)
        total_amount = qs.aggregate(Sum('total_amount'))['total_amount__sum']
        total_amount_received = qs.aggregate(Sum('amount_paid'))['amount_paid__sum']
        total_amount_pending = qs.filter(completed=0).aggregate(Sum('amount_remaining'))['amount_remaining__sum']
        total_installments_pending = qs.filter(completed=0).count()
        return HttpResponse("Total expected amount: " + str(total_amount) + "<br/>Total received amount: " + str(total_amount_received) + "<br/>Pending amount: " + str(total_amount_pending) + "<br/>Total installments to track: " + str(total_installments_pending) + "<br/>")

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

class filterFY(admin.SimpleListFilter):
    title = ('year')
    parameter_name = 'financial_year'

    def lookups(self, request, model_admin):
        fy = tuple(models.FY.objects.all().values_list('id', 'start_year'))
        return fy
        return (
            # ('active', ('All')),
            (None, ('Active')),
            ('inactive', ('Inactive')),
            # ('all', ('All')),
        )
    def queryset(self, request, queryset):
        fy_id = self.value()
        if fy_id:
            return queryset.filter(classroom__financial_year_id = fy_id)
        return queryset

@admin.register(models.Exam)
class ExamAdmin(admin.ModelAdmin):
    inlines = [MarksTabularOnline]
    list_filter = ('subject', filterFY)
    search_fields = ['exammark__student__first_name', 'exammark__student__last_name']
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'classroom':
            kwargs["queryset"] = models.Classroom.objects.filter(financial_year__status = 1)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(models.Promote)
class PromoteAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'classroom':
            fy = models.FY.objects.filter(status=0).order_by('start_year').last()
            if not fy:
                return super().formfield_for_foreignkey(db_field, request, **kwargs)
            kwargs["queryset"] = models.Classroom.objects.filter(financial_year__id = fy.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
