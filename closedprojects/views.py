from django.conf import settings
from django.shortcuts import render

# Create your views here.
def closedgenres (request):
	context={
	"queryset": "Test Message.."
	}
	return render (request, 'genres1.html', context)

def closed_subcategories (request):
	context={
	"queryset": "Test Message.."
	}
	return render (request, 'closed_subcategory.html', context)