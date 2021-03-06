from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save

from django.utils.text import slugify
from comments.models import Comment


# Create your models here.
# MVC MODEL VIEW CONTROLLER
class UserData():
	name = "default"
	email = "default" 

def upload_location(instance, filename):
	return "%s/%s" %(instance.id, filename)



class HiddenForum(models.Model):
	name = models.CharField(max_length = 120, unique = True)
	slug = models.SlugField()

	class Meta:
		verbose_name_plural = 'hidden Forums'
		
	def __unicode__(self):
		return self.name

	def __str__(self):
		return self.name




class HiddenPost(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default = 1)
	title = models.CharField(max_length=120)
	slug = models.SlugField(unique =True)
	image = models.ImageField(upload_to = upload_location,
		null = True, 
		blank=True, 
		width_field="width_field", 
		height_field="height_field")
	height_field = models.IntegerField(default = 0)
	width_field = models.IntegerField(default = 0)
	content = models.TextField()
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	hiddenforum = models.CharField(max_length=120)

	# def save(self):
	#   hiddenforum = slugData()
	#   super(HiddenPost,self).save()

	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		# path = reverse("hiddenposts:detail", kwargs={"slug": self.slug})
		# print path 
		return '/contact/'
		
	def __str__(self):
		return self.title

	class Meta:
		ordering = ["-timestamp", "-updated"]

	@property
	def comments(self):
		instance = self
		qs = Comment.objects.filter_by_instance(self)
		return qs
	 
	@property
	def get_content_type(self):
		instance = self
		content_type = ContentType.objects.get_for_model(instance.__class__)
		return content_type 


def create_slug(instance, new_slug = None):
	slug = slugify(instance.title)
	if new_slug is not None:
		slug = new_slug
	qs = HiddenPost.objects.filter(slug=slug).order_by("-id")
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug, qs.first().id)
		return create_slug(instance, new_slug=new_slug)
	return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender = HiddenPost)


