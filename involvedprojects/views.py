from django.shortcuts import render
from .models import InvolvedProject
# Create your views here.
def display_involved(request):
	l = []
	for g in request.user.groups.all():
			project = InvolvedProject()
			project.name = g.name
			# propername.append(g.name)
			g.name = g.name.replace(" ", "-")
			project.slug = g.name 
			l.append(project)
	# print ("group name printed here")
	# print l
	return render(request, 'involved_list.html', {"list": l})