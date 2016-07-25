from django.conf.urls import url, include, patterns
from django.contrib import admin


from .views import (
	hiddenpost_list,
	hiddenpost_create,
	hiddenpost_detail,
	add_collaborators,
	remove_collaborators,
	display_hidden,
	kickstarter_integrate,
	)

urlpatterns = [

	url(r'^$', hiddenpost_list, name = 'display_hidden'),
	url(r'^create/$', hiddenpost_create),
	url(r'^add-collaborators/$',add_collaborators, name='add-collaborators'),
	url(r'^remove-collaborators/$',remove_collaborators, name='remove-collaborators'),
	url(r'^(?P<slug>[\w-]+)/$', hiddenpost_detail, name='detail'),
	url(r'^integrate/$',kickstarter_integrate),
	
]