from django.contrib import admin
from django.urls import path, include
from coreengine import views as core_views

urlpatterns = [
	path('', core_views.Home.as_view(), name='home_redirect'),
	path('home/', core_views.Home.as_view(), name='home'),
	path('curriculum/', core_views.Curriculum.as_view(), name='curriculum'),
	path('admission/', core_views.Admission.as_view(), name='admission'),
	path('faculties/', core_views.Faculties.as_view(), name='faculties'),
	path('founders/', core_views.Founders.as_view(), name='faculties'),
	path('principal/', core_views.Principal.as_view(), name='faculties'),
	path('infrastructure/', core_views.Infrastructure.as_view(), name='faculties'),
	path('contact/', core_views.Admission.as_view(), name='faculties'),
	path('about-us/', core_views.AboutUs.as_view(), name='faculties'),
	path('gallery/', core_views.Gallery.as_view(), name='faculties'),
	path('social/', core_views.Social.as_view(), name='faculties'),
	path('kbc/select_quiz/', core_views.KbcQuizList.as_view(), name='faculties'),
	path('kbc/start/', core_views.KbcQuizDetails.as_view(), name='faculties'),

	path('templates/banner/<str:banner_name>', core_views.Banner.as_view(), name='banner'),
	path('templates/photo/<str:banner_name>', core_views.Photo.as_view(), name='banner'),
	path('templates/kbc/<str:banner_name>', core_views.KbcImage.as_view(), name='banner'),
	path('templates/pdf/<str:pdf_name>', core_views.Pdfs.as_view(), name='pdf'),
	path('coreengine/timetables/<str:banner_name>', core_views.TimeTable.as_view(), name='banner'),

	path('templates/<str:site_name>.js', core_views.JSTemplates.as_view(), name='faculties'),
]
