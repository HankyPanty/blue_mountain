import datetime
from datetime import time
import base64
import os
import sys

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, FileResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.urls import reverse

import templates
from coreengine import models
from files import models as file_models


class JSTemplates(APIView):
	def get(self, request, site_name):
		data = open("./templates/"+str(site_name)+".js").read()
		return HttpResponse(data, content_type="application/javascript")

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

		return render(request, 'gallery.html', {'event_images':data})


class Social(APIView):
	def get(self, request):
		return render(request, 'social.html')


class Infrastructure(APIView):
	def get(self, request):
		return render(request, 'infrastructure.html')


class Contact(APIView):
	def get(self, request):
		return render(request, 'contact.html')

class AboutUs(APIView):
	def get(self, request):
		return render(request, 'about-us.html')


class KbcImage(APIView):
	def get(self, request, banner_name):
		image_data = open("./templates/kbc/"+str(banner_name), "rb").read()
		return HttpResponse(image_data, content_type="image/png")

@method_decorator(login_required, name='dispatch')
class KbcQuizList(APIView):
	def get(self, request):
		data = {}
		quizes = list(models.Quiz.objects.filter(status = 1))
		for quiz in quizes:
			data[str(quiz.id)] = str(quiz)
		return render(request, 'kbc_select.html', {'data': data})

@method_decorator(login_required, name='dispatch')
class KbcQuizDetails(APIView):
	def get(self, request):
		# if not request.user.is_authenticated:
		# 	return HttpResponseRedirect(reverse('admin:index'))
		try:
			quiz_questions = []
			tournament_id = int(request.GET.get("quiz_id"))
			quiz = models.Quiz.objects.get(id=tournament_id, status=1)
			# teams = models.QuizTeam.objects.filter(tournament_id=quiz.id)
		except:
			return Response("Could Not Find Quiz Id.", status=status.HTTP_400_BAD_REQUEST)

		quiz_questions = get_questions_from_sheet("./" + str(quiz.upload_questions))

		# for team in teams:
		# 	questions=[]
		# 	team_questions = list(models.Question.objects.filter(team_id = team.id).order_by('no').values_list('question', 'opt_a', 'opt_b', 'opt_c', 'opt_d', 'correct', 'image'))
		# 	for team_question in team_questions:
		# 		questions.append(list(team_question))
		# 	quiz_questions.append([team.team_name, questions])
		# quiz_questions.append(["end"])
		prize_list = ["Fail", "1", "2", "3", "4", "5", "10", "20", "30", "40", "50", "60", "70", "80", "90", "100"]
		prize_list = prize_list[0:len(quiz_questions[0][1])+1]
		return render(request, 'kbc.html', {'data': quiz_questions, 'prize_list':prize_list})
