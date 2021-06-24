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
from django.contrib.auth.models import User
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


class Classroom(models.Model):
	class_name = models.CharField(max_length=20, null=True, blank=True)
	section_name = models.CharField(max_length=2, null=True, blank=True)
	timetable = models.CharField(max_length=1000, null=True, blank=True)
	financial_year = models.ForeignKey(FY, null=True, blank=True, on_delete=models.SET_NULL)
	meet_link = models.CharField(max_length=200, null=True, blank=True)

	def __str__(self):
		return str(self.class_name)+ ":" +str(self.section_name) + " - " + str(self.financial_year)



class Student(models.Model):
	statusChoices = (
		(1, 'Active'),
		(0, 'Inactive'),
	)

	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=20)
	user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
	classroom = models.ForeignKey(Classroom, null=True, blank=True, on_delete=models.SET_NULL)
	status = models.IntegerField(choices=statusChoices, default=0)
	# call_time_end = models.DateTimeField()

	def __str__(self):
		return str(self.first_name)+" "+str(self.last_name)+" - " +str(self.classroom)


class StudentPersonalInfo(models.Model):
	student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
	fathers_name = models.CharField(max_length=20, null=True, blank=True)
	mothers_name = models.CharField(max_length=20, null=True, blank=True)
	fathers_last_name = models.CharField(max_length=20, null=True, blank=True)
	address = models.CharField(max_length=200, null=True, blank=True)
	contact_no = models.CharField(max_length=10, null=True, blank=True)
	emergenct_contact = models.CharField(max_length=10, null=True, blank=True)
	dob = models.DateField(null=True, blank=True)
	heightCM = models.CharField(max_length=10, null=True, blank=True)
	weight = models.CharField(max_length=10, null=True, blank=True)
	blood_group = models.CharField(max_length=10, null=True, blank=True)


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




class Teacher(TimeStampedModel):
	statusChoices = (
		(1, 'Active'),
		(0, 'Inactive'),
	)

	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=20)
	user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
	mobile_no = models.CharField(max_length=10, null=True, blank=True)
	status = models.IntegerField(choices=statusChoices, default=0)



class TeacherPersonalInfo(models.Model):
	teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=True, blank=True)
	contact_no = models.CharField(max_length=10, null=True, blank=True)
	emergenct_contact = models.CharField(max_length=10, null=True, blank=True)
	dob = models.DateField(null=True, blank=True)
	blood_group = models.CharField(max_length=10, null=True, blank=True)
	aadhar_no = models.CharField(max_length=12, null=True, blank=True)



def fees_post_save(sender, instance, created, **kwargs):
	if not created:
		return
	with transaction.atomic():
		student = instance.student
		classroom = instance.classroom
		financial_year = instance.financial_year
		if financial_year:
			students=Student.objects.filter(classroom__financial_year=financial_year)
		if classroom:
			students=Student.objects.filter(classroom=classroom)
		if student:
			students=Student.objects.filter(student=student)

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
	financial_year = models.ForeignKey(FY, on_delete=models.SET_NULL, null=True, blank=True, help_text="Select Only ONE")

	def __str__(self):
		return str(self.id) + str(dict(self.fees_type_choices).get(self.fees_type))


signals.post_save.connect(fees_post_save, sender=Fee)



class Amount(TimeStampedModel):
	statusChoices = (
		(1, 'Completed'),
		(0, 'Pending'),
	)
	fee = models.ForeignKey(Fee, on_delete=models.SET_NULL, null=True)
	student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
	total_amount = models.IntegerField()
	amount_paid = models.IntegerField()
	amount_remaining = models.IntegerField()
	completed = models.IntegerField(choices=statusChoices, default=0)
	remark = models.CharField(max_length=200, null=True, blank=True)

	def __str__(self):
		return str(self.student) + " - " + str(self.fee)

	def save(self, *args, **kwargs):
		self.amount_remaining = self.total_amount - self.amount_paid if self.total_amount - self.amount_paid > 0 else 0
		super(Amount, self).save(*args, **kwargs)

