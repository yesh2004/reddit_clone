from django.shortcuts import render,redirect
from .models import Subreddit,Post
from .forms import CreateUserForm,CreatePostForm
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
	subreddits=Subreddit.objects.all()[:5]
	context={
	'subreddits':subreddits
	}
	return render(request,'subreddit/homepage.html',context)

def signup(request):
	if request.user.is_authenticated:
		return redirect('index_page')
	else:
		form =CreateUserForm()
		if request.method=='POST':
			form=CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				return redirect('login_page')
		context={
		'form':form
		}
		return render(request,'subreddit/signup.html',context)

def login(request):
	if request.user.is_authenticated:
		return redirect('index_page')
	else:
		if request.method=='POST':
			username=request.POST.get('username')
			password=request.POST.get('password')
			user=authenticate(username=username,password=password)
			if user is not None:
				django_login(request,user)
				return redirect('index_page')
			else:
				messages.info(request, 'Username OR password is incorrect')
		context={}
		return render(request,'subreddit/login.html',context)

@login_required(login_url='login_page')
def logout(request):
	django_logout(request)
	return redirect('login_page')

@login_required(login_url='login_page')
def subreddit_create(request):
	if request.method=='POST':
		title=request.POST.get('title')
		author=request.user 
		if Subreddit.objects.filter(title=title).exists():
			messages.info(request,'subreddit with name exists')
		else:
			subreddit=Subreddit(title=title,author=author)
			
			subreddit.save()
			messages.info(request,'subreddit created')
		
	context={}
	return render(request,'subreddit/subreddit_create.html',context)

def subreddit(request,pk):
	subreddit=Subreddit.objects.get(title=pk)
	posts=Post.objects.filter(subreddit__title=pk)
	context={
	'subreddit':subreddit,
	'posts':posts
	}
	return render(request,'subreddit/subreddit.html',context)

@login_required(login_url='login_page')
def post(request,pk):
	subreddit=Subreddit.objects.get(title=pk)
	
	form=CreatePostForm()
	if request.method=='POST':
		form=CreatePostForm(request.POST)
		if form.is_valid():
			postform=form.save(commit=False)
			
			postform.author=request.user 
			postform.subreddit=subreddit
			postform.save()
			return redirect('subreddit',pk=subreddit.title)
	context={
	'form':form
	}
	return render(request,'subreddit/post.html',context)