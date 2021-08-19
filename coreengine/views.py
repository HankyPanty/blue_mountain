from django.shortcuts import render, redirect
import datetime
from django.http import HttpResponse,JsonResponse, HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

from datetime import time
import base64

import templates
from coreengine import models


class Home(APIView):
	def get(self, request):
		# return HttpResponse("This is Home Page.")
		return render(request, 'index.html')

class Banner(APIView):
	def get(self, request, banner_name):
		image_data = open("./templates/banner/"+str(banner_name), "rb").read()
		return HttpResponse(image_data, content_type="image/png")
		# return HttpResponse("This is Home Page.")
		return render(request, 'admission.html')


class Curriculum(APIView):
	def get(self, request):
		# return HttpResponse("This is Home Page.")
		return render(request, 'curriculum.html')

class Founders(APIView):
	def get(self, request):
		# return HttpResponse("This is Home Page.")
		return render(request, 'founders.html')

class Principal(APIView):
	def get(self, request):
		# return HttpResponse("This is Home Page.")
		return render(request, 'principal.html')

class Faculties(APIView):
	def get(self, request):
		# return HttpResponse("This is Home Page.")
		return render(request, 'faculties.html')


class Admission(APIView):
	def get(self, request):
		# return HttpResponse("This is Home Page.")
		return render(request, 'admission.html')


class Infrastructure(APIView):
	def get(self, request):
		# return HttpResponse("This is Home Page.")
		return render(request, 'infrastructure.html')


class Contact(APIView):
	def get(self, request):
		# return HttpResponse("This is Home Page.")
		return render(request, 'contact.html')

class AboutUs(APIView):
	def get(self, request):
		# return HttpResponse("This is Home Page.")
		return render(request, 'about-us.html')

