from django.contrib import admin
from .models import HiddenPost, HiddenForum
# Register your models here.
class PostModelAdmin(admin.ModelAdmin):
	list_display = ["title", "updated", "timestamp"]
	list_display_links = ["updated"]
	list_editable = ["title"]
	list_filter = ["updated", "timestamp"]
	
	search_fields =["title", "content"]
	class Meta:
		model = HiddenPost

admin.site.register(HiddenPost)
admin.site.register(HiddenForum)