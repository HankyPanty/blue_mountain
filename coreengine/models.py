import datetime
import json
import urllib
import math
import requests
import hashlib
import base64
import pytz
import ast

from model_utils import Choices
from model_utils.models import TimeStampedModel

from django.db import transaction
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User, Group
from django.utils import timezone
# from django_fsm import transition, FSMIntegerField, get_available_FIELD_transitions, TransitionNotAllowed
from django.db.models import signals
from django.db.models import Q, F
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import RegexValidator
from django.conf import settings



class FY(models.Model):
	statusChoices = (
		(1, 'Active'),
		(0, 'Inactive'),
	)

	start_year = models.IntegerField()
	end_year = models.IntegerField()
	status = models.IntegerField(choices=statusChoices, default=0)

	def __str__(self):
		return str(self.start_year)+ ':' +str(self.end_year)

	def save(self, *args, **kwargs):
		if self.status == 1:
			if list(FY.objects.filter(status=1)):
				raise ValidationError("Cannot have more than one active Financial Year")
		super(FY, self).save(*args, **kwargs)


class Student(models.Model):
	statusChoices = (
		(1, 'Active'),
		(0, 'Inactive'),
	)

	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=20)
	user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
	status = models.IntegerField(choices=statusChoices, default=1)
	grn_number = models.IntegerField(null=True, blank=True)
	# call_time_end = models.DateTimeField()
	fathers_name = models.CharField(max_length=20, null=True, blank=True)
	mothers_name = models.CharField(max_length=20, null=True, blank=True)
	fathers_last_name = models.CharField(max_length=20, null=True, blank=True)
	address = models.CharField(max_length=200, null=True, blank=True)
	contact_no = models.CharField(max_length=10, null=True, blank=True)
	emergenct_contact = models.CharField(max_length=10, null=True, blank=True)
	dob = models.DateField()
	heightCM = models.FloatField(null=True, blank=True)
	weightKG = models.FloatField(null=True, blank=True)
	blood_group = models.CharField(max_length=10, null=True, blank=True)

	def __str__(self):
		return str(self.first_name)+" "+str(self.last_name)

	def save(self, *args, **kwargs):
		if not self.pk:
			username = self.last_name+'.'+self.first_name
			user = list(User.objects.filter(username=username))
			if user:
				username = self.last_name+'_'+self.first_name
			user = User.objects.create_user(username=username, password=str(self.dob), is_staff=1)
			try:
				user.groups.add(Group.objects.get(name='student-login'))
			except:
				print("ERROR in assigning Group to Sstudent-"+str(self.first_name))
			user.save()
			self.user = user
		super(Student, self).save(*args, **kwargs)

# def student_added(sender, instance, pk_set, **kwargs):


class Classroom(models.Model):
	class_name = models.CharField(max_length=20, null=True, blank=True)
	section_name = models.CharField(max_length=2, null=True, blank=True)
	timetable = models.FileField(upload_to='coreengine/timetables/', max_length=1000, null=True, blank=True)
	financial_year = models.ForeignKey(FY, on_delete=models.PROTECT)
	meet_link = models.CharField(max_length=200, null=True, blank=True)
	# students = models.ManyToManyField(Student, blank=True, help_text="Select all students to be present here")
	# exams = models.ManyToManyField(Exam, blank=True, help_text="Select/Create all tests taken for this class")

	@property
	def students(self):
		studs = ClassroomStudent.objects.filter(classroom_id=self.pk).values_list('student_id', flat=True)
		return Student.objects.filter(id__in = studs)

	def __str__(self):
		return str(self.class_name)+ ":" +str(self.section_name) + " " + str(self.financial_year.start_year)

	def save(self, *args, **kwargs):
		super(Classroom, self).save(*args, **kwargs)

class ClassroomStudent(models.Model):
	classroom = models.ForeignKey(Classroom, on_delete=models.PROTECT)
	student = models.ForeignKey(Student, on_delete=models.PROTECT)
	roll_no = models.IntegerField(null=True, blank=True)
	report_card = models.ImageField(upload_to='coreengine/report/', max_length=1000, null=True, blank=True)

	def __str__(self):
		return str(self.classroom)+ ": " +str(self.student)

	def save(self, *args, **kwargs):
		if ClassroomStudent.objects.filter(student=self.student, classroom__financial_year = self.classroom.financial_year):
			raise ValidationError(self.student.first_name + " is already in same or another class of this year.")
		super(ClassroomStudent, self).save(*args, **kwargs)

class StudentAttendance(TimeStampedModel):
	student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
	date = models.DateField(null=True, blank=True)
	user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)



class StudentComment(models.Model):
	typeChoices = (
		(0, 'Note'),
		(1, 'Complaint'),
		(2, 'Remark'),
	)
	statusChoices = (
		(1, 'Resolved'),
		(0, 'Unresolved'),
	)

	student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
	comment = models.CharField(max_length=1000, null=True, blank=True)
	comment_type = models.IntegerField(choices=typeChoices, default=0)
	resolved = models.IntegerField(choices=statusChoices, default=0)

	def __str__(self):
		return str(self.student)


def exam_post_save(sender, instance, created, **kwargs):
	if created:
		students = instance.classroom.students
		for stud in students:
			ExamMark.objects.create(exam=instance, student=stud, marks=0)

class Exam(TimeStampedModel):
	subjectChoices = (
		(8, 'GeneralKnolowdge'),
		(7, 'Computer'),
		(6, 'Science'),
		(5, 'Maths'),
		(4, 'History'),
		(3, 'Geography'),
		(2, 'Marathi'),
		(1, 'Hindi'),
		(0, 'English'),
	)

	statusChoices = (
		(3, 'Closed'),
		(2, 'Completed'),
		(1, 'Started'),
		(0, 'Created'),
	)

	typeChoices= (
		(2, 'Endsem'),
		(1, 'Midsem'),
		(0, 'UnitTest'),
		)

	exam_name = models.CharField(max_length=100)
	exam_type = models.IntegerField(choices=typeChoices)
	classroom = models.ForeignKey(Classroom, on_delete=models.PROTECT)
	subject = models.IntegerField(choices=subjectChoices)
	status = models.IntegerField(choices=statusChoices, default=0)
	total_marks = models.IntegerField(default=20)
	weightage = models.IntegerField(default=0)

	def __str__(self):
		return str(self.classroom) + " " + str(dict(self.typeChoices).get(self.exam_type))+ "::" + str(dict(self.subjectChoices).get(self.subject))+ " -" +str(self.exam_name)

signals.post_save.connect(exam_post_save, sender=Exam)

class ExamMark(TimeStampedModel):
	typeChoices = (
		(2, 'Endsem'),
		(1, 'Midsem'),
		(0, 'UnitTest'),
		)

	resultChoices = (
		(2, 'Absent'),
		(1, 'Fail'),
		(0, 'Pass'),
		)

	exam = models.ForeignKey(Exam, on_delete=models.PROTECT)
	student = models.ForeignKey(Student, on_delete=models.PROTECT)
	marks = models.IntegerField(default=0)
	result = models.IntegerField(choices=resultChoices, null=True, blank=True)

	def __str__(self):
		return str(self.exam)+ ": " +str(self.student)

	def save(self, *args, **kwargs):
		if self.student not in self.exam.classroom.students.all():
			raise ValidationError("STUDENT NOT in this CLASS, his marks cannot be added in this exam.")
		super(ExamMark, self).save(*args, **kwargs)


class Teacher(TimeStampedModel):
	statusChoices = (
		(1, 'Active'),
		(0, 'Inactive'),
	)

	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=20)
	user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
	mobile_no = models.CharField(max_length=10, null=True, blank=True)
	status = models.IntegerField(choices=statusChoices, default=1)

	address = models.CharField(max_length=200, null=True, blank=True)
	contact_no = models.CharField(max_length=10, null=True, blank=True)
	emergenct_contact = models.CharField(max_length=10, null=True, blank=True)
	dob = models.DateField()
	blood_group = models.CharField(max_length=10, null=True, blank=True)
	aadhar_no = models.CharField(max_length=12, null=True, blank=True)

	def __str__(self):
		return str(self.first_name)+" "+str(self.last_name)

	def save(self, *args, **kwargs):
		if not self.pk:
			username = self.last_name+'.'+self.first_name
			user = list(User.objects.filter(username=username))
			if user:
				username = self.last_name+'_'+self.first_name
			user = User.objects.create_user(username=username, password=str(self.dob), is_staff=1)
			try:
				user.groups.add(Group.objects.get(name='teacher-login'))
				user.save()
				self.user = user
			except:
				print("ERROR in assigning Group to Teacher-"+str(self.first_name))
		super(Teacher, self).save(*args, **kwargs)


def fees_post_save(sender, instance, created, **kwargs):
	if not created:
		return
	with transaction.atomic():
		student = instance.student
		classroom = instance.classroom
		if classroom:
			students=classroom.students
		if student:
			students=Student.objects.filter(id=student.id)

		students=students.filter(status=1)

		for stud in list(students):
			Amount.objects.create(fee=instance, student=stud, total_amount=instance.amountINR,
								   amount_paid=0, amount_remaining=instance.amountINR,
								   completed=0, remark="Auto Created")

	return


class Fee(TimeStampedModel):
	fees_type_choices = (
		(0, 'Tution Fees'),
		(1, 'Kit Amount'),
		(2, 'Event Fees'),
		(3, 'Registration Fees'),
		(4, 'Damages'),
		(5, 'Others'),
	)

	fees_type = models.IntegerField(choices=fees_type_choices)
	description = models.CharField(max_length=200, null=True, blank=True)
	amountINR = models.IntegerField()
	classroom = models.ForeignKey(Classroom, on_delete=models.SET_NULL, null=True, blank=True, help_text="Select Only ONE")
	student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True, help_text="Select Only ONE")
	financial_year = models.ForeignKey(FY, on_delete=models.PROTECT)
	add_to_future_students = models.IntegerField(choices=((1,'yes'),(0,'no')), default=1, help_text="Applicable For Class level Fees")

	def __str__(self):
		return str(dict(self.fees_type_choices).get(self.fees_type)) +":" + self.description + ": "+ str(self.financial_year.start_year)

	def save(self, *args, **kwargs):
		if self.student and self.classroom:
			raise ValidationError("Only one can be selected")
		if self.classroom:
			self.financial_year = self.classroom.financial_year
		super(Fee, self).save(*args, **kwargs)


signals.post_save.connect(fees_post_save, sender=Fee)


class Amount(TimeStampedModel):
	statusChoices = (
		(1, 'Completed'),
		(0, 'Pending'),
	)
	fee = models.ForeignKey(Fee, on_delete=models.PROTECT)
	student = models.ForeignKey(Student, on_delete=models.PROTECT)
	total_amount = models.IntegerField()
	amount_paid = models.IntegerField()
	amount_remaining = models.IntegerField()
	completed = models.IntegerField(choices=statusChoices, default=0)
	remark = models.CharField(max_length=200, null=True, blank=True)

	def __str__(self):
		return str(self.student) + " - " + str(self.fee)

	def save(self, *args, **kwargs):
		self.amount_remaining = self.total_amount - self.amount_paid if self.total_amount - self.amount_paid > 0 else 0
		if not self.amount_remaining:
			self.completed = 1
		super(Amount, self).save(*args, **kwargs)


class AmountDetails(TimeStampedModel):
	typeChoices = (
		(2, 'Card'),
		(1, 'Gpay'),
		(0, 'Cash'),
		)

	amount = models.ForeignKey(Amount, on_delete=models.SET_NULL, null=True)
	amount_paid = models.IntegerField(default=0)
	payement_type = models.IntegerField(choices=typeChoices, default=0)

	def __str__(self):
		return str(self.amount)+ " - " + str(self.amount_paid)

	def save(self, *args, **kwargs):
		amount_paid_current = self.amount.amount_paid + self.amount_paid
		self.amount.amount_paid = amount_paid_current
		self.amount.save()
		super(AmountDetails, self).save(*args, **kwargs)


def classroomstudent_post_save(sender, instance, created, **kwargs):
	students = list(instance.classroom.students.values_list('id', flat=True))
	fee_applicable = Fee.objects.filter(classroom=instance.classroom, add_to_future_students=1)
	for fee in fee_applicable:
		already_studs = list(Amount.objects.filter(fee=fee).values_list('student_id', flat=True))
		rem_studs = list(set(students)-set(already_studs))
		for stud in rem_studs:
			Amount.objects.create(fee=fee, student_id=stud, total_amount=fee.amountINR,
								   amount_paid=0, amount_remaining=fee.amountINR,
								   completed=0, remark="Auto Created")

signals.post_save.connect(classroomstudent_post_save, sender=ClassroomStudent)
