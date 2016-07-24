from django import forms
from pagedown.widgets import PagedownWidget
from .models import HiddenPost
from .fields import CommaSeparatedUserField

class HiddenPostForm(forms.ModelForm):
	content = forms.CharField(widget = PagedownWidget)
	class Meta:
		model = HiddenPost
		fields = [
			"title",
			"content",
			"image",
			"hiddenforum",
		]

class NameForm(forms.Form):
    recipient = CommaSeparatedUserField(label=(u"Recipient"))