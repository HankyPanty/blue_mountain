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



class Banner(models.Model):
	statusChoices = (
		(1, 'Active'),
		(0, 'Inactive'),
	)

	typeChoices = (
		(1, 'Active'),
		(0, 'Inactive'),
	)

	banner_type = models.IntegerField(choices=typeChoices, default=0)
	image = models.ImageField(upload_to='banner/', height_field=None, width_field=None, max_length=1000, null=True, blank=True)
	status = models.IntegerField(choices=statusChoices, default=0)

