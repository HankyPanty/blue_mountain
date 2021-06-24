from django.contrib import admin
from django.urls import path, include
from coreengine import views as core_views

urlpatterns = [
	path('', core_views.Home.as_view(), name='home_redirect'),
	path('home/', core_views.Home.as_view(), name='home'),
	path('curriculum/', core_views.Curriculum.as_view(), name='home'),
	path('admission/', core_views.Admission.as_view(), name='home'),
	path('faculties/', core_views.Faculties.as_view(), name='home'),]
