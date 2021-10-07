from django.shortcuts import render, redirect
import datetime
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, FileResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

from datetime import time
import base64
import os
import sys

import templates
from coreengine import models
from files import models as file_models

class Home(APIView):
	def get(self, request):
		# return HttpResponse("This is Home Page.")
		return render(request, 'index.html')

class Banner(APIView):
	def get(self, request, banner_name):
		image_data = open("./templates/banner/"+str(banner_name), "rb").read()
		return HttpResponse(image_data, content_type="image/png")

class Photo(APIView):
	def get(self, request, banner_name):
		image_data = open("./templates/photo/"+str(banner_name), "rb").read()
		return HttpResponse(image_data, content_type="image/png")

class Pdfs(APIView):
	def get(self, request, pdf_name):
		path = "./templates/pdf/"+str(pdf_name)
		if os.path.exists(path):
			with open(path, "r", encoding='ascii', errors='ignore') as excel:
				data = excel.readline()
			response = HttpResponse(data, content_type='application/pdf')
			response['Content-Disposition'] = 'attachment; filename='+str(pdf_name)
			return response 
		else:
			return HttpResponse(json.dumps({"no":"excel","no one": "cries"}))

class TimeTable(APIView):
	def get(self, request, banner_name):
		path = './coreengine/timetables/'+str(banner_name)
		if os.path.exists(path):
			with open(path, "r", encoding='ascii', errors='ignore') as excel:
				data = excel.readline()
			response = HttpResponse(data, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
			response['Content-Disposition'] = 'attachment; filename='+str(banner_name)
			return response 
		else:
			return HttpResponse(json.dumps({"no":"excel","no one": "cries"}))


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


class Gallery(APIView):
	def get(self, request):
		data = {}
		images_urls = list(file_models.PhotoImage.objects.filter(status=1, photo_type__status=1).order_by('-photo_type_id').values_list('photo_type__event_name', 'image'))
		for images_url in images_urls:
			if data.get(images_url[0], None):
				data[images_url[0]].append(images_url[1])
			else:
				data[images_url[0]] = [images_url[1]]

		# return HttpResponse("This is Home Page.")
		return render(request, 'gallery.html', {'event_images':data})


class Social(APIView):
	def get(self, request):
		# return HttpResponse("This is Home Page.")
		return render(request, 'social.html')


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

