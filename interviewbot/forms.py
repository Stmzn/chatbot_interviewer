from django import forms
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column,Submit
from .models import Interview

class SimpleForm(forms.ModelForm):
	class Meta:
		model = Interview
		fields = ['answers']

	def __init__(self,*args,**kwargs):
		super(SimpleForm, self).__init__(*args, **kwargs)