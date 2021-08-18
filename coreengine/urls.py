from django.contrib import admin
from django.urls import path, include
from coreengine import views as core_views

urlpatterns = [
	path('', core_views.Home.as_view(), name='home_redirect'),
	path('home/', core_views.Home.as_view(), name='home'),
	path('curriculum/', core_views.Curriculum.as_view(), name='curriculum'),
	path('admission/', core_views.Admission.as_view(), name='admission'),
	path('banner/<str:banner_name>', core_views.Banner.as_view(), name='banner'),
	path('faculties/', core_views.Faculties.as_view(), name='faculties'),
]
