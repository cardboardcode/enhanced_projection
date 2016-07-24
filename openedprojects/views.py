from urllib import quote_plus

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User ,Group

from comments.forms import CommentForm
from comments.models import Comment
from .forms import PostForm
from .models import Post, Category
from django.contrib.auth.decorators import login_required
from hiddenforum.models import HiddenForum

# Create your views here.

@login_required
def post_create(request):
	if not request.user.is_authenticated():
		raise Http404

	form = PostForm(request.POST or None, request.FILES or None)
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
		return HttpResponseRedirect(instance.get_absolute_url())
	
	context = {
		"form":form,
	}
	return render(request, "post_form.html", context)


@login_required
def post_detail(request, slug=None):
	# instance = Post.objects.get(id=1)

	print ("now in post_detail in views.py")
	print slug


	instance = get_object_or_404(Post, slug=slug)
	share_string = quote_plus(instance.content)

	initial_data = {
		"content_type": instance.get_content_type,
		"object_id": instance.id
	}
	form = CommentForm(request.POST or None, initial = initial_data)
	if form.is_valid():
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model = c_type)
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
	return render(request, "post_detail.html", context)
	
@login_required
def post_list(request, category_name_slug):
	
	phrase = category_name_slug
	print phrase
	print type(category_name_slug)
	category = Category.objects.get(slug = category_name_slug)
	queryset_list = Post.objects.filter(category = category)#.order_by("-timestamp")
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
			Q(title__icontains=query) |
			Q(content__icontains=query) |
			Q(user__username__icontains=query)
			).distinct()
	paginator = Paginator(queryset_list, 10) # Show 25 contacts per page
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

	context ={
		"object_list": queryset,
		"title": category,
		"page_request_var": page_request_var
	}
	return render(request, "post_list.html", context)

@login_required
def post_update(request, slug=None):
	instance = get_object_or_404(Post, slug=slug)
	form = PostForm(request.POST or None, request.FILES or None, instance = instance)
	if form.is_valid():
		instance = form.save(commit = False)
		instance.save()
		#message success
		messages.success(request, "Item Saved")
		return HttpResponseRedirect(instance.get_absolute_url())


	context = {
		"title": instance.title,
		"instance": instance,
		"form": form,
	}
	return render(request, "post_form.html", context)

@login_required
def post_delete(request, slug=None):
	instance = get_object_or_404(Post, slug=slug)
	instance.delete()
	messages.success(request, "Successfully Deleted")
	return redirect("posts:list")
@login_required
def openedgenres (request):

	return render (request, 'genres2.html')
@login_required
def opened_subcategories (request):
	context={
	"queryset": "Test Message.."
	}
	return render (request, 'opened_subcategory.html', context)

	
@login_required
def show_category(request, category_name_slug):
	
	context_dict = {}

	try:
		category = Category.objects.get(slug=category_name_slug)
		posts = Post.objects.filter(category=category)
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
		context_dict['category'] = category
		context_dict['page_request_var'] = page_request_var
		context_dict['object_list'] = queryset
	except Category.DoesNotExist:

		context_dict['category'] = None
		context_dict['pages'] = None

	return render(request, 'testing.html', context_dict)


@login_required
def categories(request):
	category_list = Category.objects.all()
	context_dict = {'categories': category_list}
	
	return render(request, 'categories.html', context_dict)


