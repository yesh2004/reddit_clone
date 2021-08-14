from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class Subreddit(models.Model):
	author=models.ForeignKey(User,on_delete=models.CASCADE)
	date_created=models.DateTimeField(default=timezone.now)
	title=models.CharField(max_length=500)
	class Meta:
		ordering=['-date_created']
	def __str__(self):
		return self.title

class Post(models.Model):
	subreddit=models.ForeignKey(Subreddit,on_delete=models.CASCADE)
	title=models.CharField(max_length=500)
	body=models.TextField(max_length=5000)
	total_vote=models.IntegerField(default=0)
	ups=models.ManyToManyField(User, related_name='post_ups',blank=True)
	downs=models.ManyToManyField(User, related_name='post_downs',blank=True)
	author=models.ForeignKey(User,on_delete=models.CASCADE)
	date_created=models.DateTimeField(default=timezone.now)
	
class Comment(models.Model):
	post=models.ForeignKey(Post,on_delete=models.CASCADE)
	author=models.ForeignKey(User,on_delete=models.CASCADE)
	content=models.TextField(max_length=1000)
	date_created=models.DateTimeField(default=timezone.now)
