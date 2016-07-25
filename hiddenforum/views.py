from urllib import quote_plus

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect

from django_messages.models import Message
from django.utils.translation import ugettext as _

from comments.forms import CommentForm
from comments.models import Comment
from openedprojects.models import Post
from .forms import HiddenPostForm
from .models import HiddenPost , HiddenForum
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import NameForm
from django.contrib.auth.models import User ,Group
# Create your views here.


@login_required
def kickstarter_integrate(request,slug):

	print ("entered into kickstarter_integrate def")

	instance = get_object_or_404(Post, slug=slug)
	slugtest = slug
	slugtest = slugtest.replace("-", " ")
	g = Group.objects.get(name=slugtest)
	users = g.user_set.all()
	print users

	context={
	'title': instance.title,
	'subcategory': instance.category,
	'description': instance.content,

    }

	return render(request,'integration_compile.html',context)

@login_required
def add_collaborators(request,slug,form_class=NameForm, recipient_filter=None):
	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = form_class(request.POST)
		# check whether it's valid:
		slugtest = slug
		slugtest = slugtest.replace("-", " ")
		
		# phrase = "pass the first if----------------------------"
		# print phrase
		print form.errors
		if form.is_valid():
			# g = Group.objects.get(name=slugtest) 
			# g.user_set.add()
			# phrase2 = "pass the second if----------------------------------"
			# print phrase2
			explicittest = (form.cleaned_data.get('recipient'))
			
			u = User.objects.get(username=explicittest[0])
			g = Group.objects.get(name=slugtest) 
			g.user_set.add(u)
			messages.info(request, _(u"Member added"))
			context2 = {
			"justname": slug,
			"slugtest": slugtest,
			}
			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

	# if a GET (or any other method) we'll create a blank form
		else:
			error = str(form.errors)
			form = NameForm()
			context = {
				"justname": slug,
				"slugtest": slugtest,
				"error": error,
			}
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
# @user_passes_test(is_in_group)

@login_required
def remove_collaborators(request,slug,form_class=NameForm, recipient_filter=None):
	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = form_class(request.POST)
		# check whether it's valid:
		slugtest = slug
		slugtest = slugtest.replace("-", " ")
		
		# phrase = "pass the first if----------------------------"
		# print phrase
		print form.errors
		if form.is_valid():
			# g = Group.objects.get(name=slugtest) 
			# g.user_set.add()
			# phrase2 = "pass the second if----------------------------------"
			# print phrase2
			explicittest = (form.cleaned_data.get('recipient'))
			
			u = User.objects.get(username=explicittest[0])
			g = Group.objects.get(name=slugtest) 
			g.user_set.remove(u)
			messages.info(request, _(u"Member removed"))
			context2 = {
			"justname": slug,
			"slugtest": slugtest,
			}
			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

	# if a GET (or any other method) we'll create a blank form
		else:
			error = str(form.errors)
			form = NameForm()
			context = {
				"justname": slug,
				"slugtest": slugtest,
				"error": error,
			}
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def hiddenpost_create(request, slug):
	if not request.user.is_authenticated():
		raise Http404
	
	global slug_data
	slug_data = slug

	form = HiddenPostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit = False)
		hiddenforum = Group.objects.get_or_create(name=instance.title)
		hiddenforum_category = HiddenForum.objects.get_or_create(name=instance.title)
		g = Group.objects.get(name=instance.title) 
		g.user_set.add(request.user)

		instance.user = request.user
		instance.save()
		#message success
		messages.success(request, "Successfully Created")
		return render(request, "hiddenpost_list.html")
	
	slugtest = slug
	slugtest = slugtest.replace("-", " ")

	context = {
		"form":form,
		"slugtest":slugtest,
	}
	return render(request, "hiddenpost_form.html", context)


@login_required
def hiddenpost_list(request,slug):
	context_dict = {}

	slugtest = slug
	slugtest = slugtest.replace("-", " ")
	is_in_group = False
	user = request.user

	print slugtest
	is_in_group = display_hidden(request,slug)

	try:
		hiddenforum = HiddenForum.objects.get(name=slugtest)
		posts = HiddenPost.objects.filter(hiddenforum=hiddenforum)
		query = request.GET.get("q")

		if query:
			posts = posts.filter(
				Q(title__icontains=query) |
				Q(content__icontains=query) |
				Q(user__username__icontains=query)
				).distinct()
		paginator = Paginator(posts, 10)
		page_request_var = "page"
		page = request.GET.get('page')
		try:
			queryset = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			queryset = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			queryset = paginator.page(paginator.num_pages)
		
		context_dict['posts'] = posts
		context_dict['hiddenforum'] = hiddenforum
		context_dict['page_request_var'] = page_request_var
		context_dict['object_list'] = queryset
	except HiddenForum.DoesNotExist:

		context_dict['category'] = None
		context_dict['pages'] = None
		
	context_dict['justname'] = slug	
	context_dict['slugtest'] = slugtest
	return render(request, 'hiddenpost_list.html', context_dict)


@login_required
# @user_passes_test(is_in_group, login_url=)
def display_hidden(request,slug):

	slugtest = slug
	slugtest = slugtest.replace("-", " ")
	is_in_group = False
	user = request.user

	# print ("in display_hidden function")
	# l = request.user.groups.values_list('name',flat=True)
	# print l

	if user.groups.filter(name=slugtest).exists():
		is_in_group = True
	else:
		print ("slugtest is false")
		context = {
		"justname": slug,
		"slugtest": slugtest,
		"username": request.user
		}
		return render(request,'hiddenforum_denied.html',context)	

	context = {
	"justname": slug,
	"slugtest": slugtest,
	}
	return render(request, 'hiddenpost_list.html', context)


@login_required
def hiddenpost_detail(request, slug):
	print ("now in hiddenpost_detail in views.py")
	instance = get_object_or_404(HiddenPost, slug=slug)
	
	if (instance==None):
		print ("HiddenPost is Nothing! ----------------------------")
	else:
		print ("HiddenPost is Something! ----------------------------")
	share_string = quote_plus(instance.content)

	initial_data = {
		"content_type": instance.get_content_type,
		"object_id": instance.id
	}
	form = CommentForm(request.POST or None, initial = initial_data)
	if form.is_valid():
		# print ("form is approved valid here ---------------------------------")
		# print (form.cleaned_data)
		c_type = form.cleaned_data.get("content_type")
		
		# print c_type

		content_type = ContentType.objects.get(model = "hiddenpost")
		obj_id = form.cleaned_data.get("object_id")
		content_data = form.cleaned_data.get("content")
		parent_obj = None
		try:
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None

		if parent_id:
			parent_qs = Comment.objects.filter(id = parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first()

		new_comment, created = Comment.objects.get_or_create(
			user = request.user,
			content_type = content_type,
			object_id = obj_id,
			content = content_data,
			parent = parent_obj,
			)
		# print ("-----------------------comment created")
		# print c_type
		# print type(new_comment.content_object)
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

	comments = instance.comments
	
	slugtest = slug
	context = {
	"slugtest": slugtest,
	"title": instance.title,
	"instance": instance,
	"share_string": share_string,
	"comments": comments,
	"comment_form": form
	}


	return render(request, "hiddenpost_detail.html",context)