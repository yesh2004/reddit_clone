from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Post
class CreateUserForm(UserCreationForm):
	class Meta:
		model=User
		fields= ['username', 'email', 'password1', 'password2']
	def __init__(self, *args, **kwargs):
		super(CreateUserForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control register-form'
			visible.field.widget.attrs['placeholder']=visible.field.label

class CreatePostForm(forms.ModelForm):
	class Meta:
		model=Post 
		fields=['title','body']

	def __init__(self, *args, **kwargs):
		super(CreatePostForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control post-form'
			