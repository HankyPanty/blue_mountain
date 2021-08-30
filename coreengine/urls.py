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
	path('contact/', core_views.Contact.as_view(), name='faculties'),
	path('about-us/', core_views.AboutUs.as_view(), name='faculties'),

	path('templates/banner/<str:banner_name>', core_views.Banner.as_view(), name='banner'),
	path('coreengine/timetables/<str:banner_name>', core_views.TimeTable.as_view(), name='banner'),

]
