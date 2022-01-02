from coreengine.models import *


def promote_students(old_year, new_year):
	classrooms = Classroom.objects.filter(financial_year = old_year)
	for classroom in classrooms:
		pass
