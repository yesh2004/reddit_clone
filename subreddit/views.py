from django.shortcuts import render,redirect
from .models import Subreddit,Post,Comment
from .forms import CreateUserForm,CreatePostForm,CommentForm
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
# Create your views here.
def index(request):
	subreddits=Subreddit.objects.all()[:5]
	posts=Post.objects.all().order_by('-total_vote')[:5]
	followed_subreddits=Subreddit.objects.filter(followers__id=request.user.id)
	context={
	'subreddits':subreddits,
	'posts':posts,
	'followed_subreddits':followed_subreddits
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
	posts=Post.objects.filter(subreddit__title=pk).order_by('-total_vote')
	isfollowed=False
	if subreddit.followers.filter(id=request.user.id).exists():
		isfollowed=True
	context={
	'subreddit':subreddit,
	'posts':posts,
	'isfollowed':isfollowed
	}
	return render(request,'subreddit/subreddit.html',context)
@login_required(login_url='login_page')
def subreddit_follow(request,pk):
	subreddit=Subreddit.objects.get(pk=pk)

	if request.method=='POST':
		if subreddit.followers.filter(id=request.user.id).exists():
			subreddit.followers.remove(request.user)
		else:
			subreddit.followers.add(request.user)
	return HttpResponseRedirect(reverse('subreddit',args=(subreddit.title,)))

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

def post_content(request,pk):
	post=Post.objects.get(pk=pk)
	form=CommentForm()
	comments=Comment.objects.filter(post=post)
	if request.method=='POST':
		form=CommentForm(request.POST)
		if form.is_valid():
			commentform=form.save(commit=False)
			commentform.post=post 
			commentform.author=request.user
			commentform.save()
	context={
	'post':post,
	'form':form,
	'comments':comments
	}
	return render(request,'subreddit/post_content.html',context)

	
@login_required(login_url='login_page')
def up(request,pk):
	post = get_object_or_404(Post, id=pk)

	if request.method=='POST':
		
		if post.ups.filter(id=request.user.id).exists():
			data={
					'total_vote':post.total_vote
					
					}
			return JsonResponse(data) 
		else:
			if post.downs.filter(id=request.user.id).exists():

				post.downs.remove(request.user)
				post.ups.add(request.user)

				post.total_vote+=2

				post.save()
				data={
					'total_vote':post.total_vote

					}
				return JsonResponse(data)
			else:
				post.ups.add(request.user)
				post.total_vote+=1
				post.save()
				data={
					'total_vote':post.total_vote
					}
				return JsonResponse(data)
		
			
				
	return HttpResponseRedirect(reverse('index_page'))
@login_required(login_url='login_page')
def down(request,pk):
	post = get_object_or_404(Post, id=pk)
	if request.method=='POST':
		if post.downs.filter(id=request.user.id).exists():
			data={
				'total_vote':post.total_vote
				}
			return JsonResponse(data) 
		else:
			if post.ups.filter(id=request.user.id).exists():
				post.ups.remove(request.user)
				post.downs.add(request.user)
				post.total_vote-=2
				post.save()
				data={
				'total_vote':post.total_vote
				}
				return JsonResponse(data)
			else:
				post.downs.add(request.user)
				post.total_vote-=1
				post.save()
				data={
				'total_vote':post.total_vote
				}
				return JsonResponse(data)
	return HttpResponseRedirect(reverse('index_page'))