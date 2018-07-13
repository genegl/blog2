from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
# Create your models here.

class Post(models.Model):	# this is the Table Name
	author = models.ForeignKey('auth.User')		# this is one column imported from the User table
	title = models.CharField(max_length=200)	# this column is for Titles with maximum allowed length of 200 characters
	text = models.TextField()	# this column 'text' contains actual post text (no length limit described)
	create_date = models.DateTimeField(default=timezone.now())	# this column contains date of post creation
	published_date = models.DateTimeField(blank=True, null=True)	# this column contains the publish date, 
													# which can be Falls, if the post is not published

	def publish(self):		# we call this function when want to publish a post
		self.published_date = timezone.now()	# we check current time when the 'post' button is hitted
		self.save()			# we saving the published time

	def approve_comments(self):		# this function would separate approved and not approved comments
		return self.comments.filter(approved_comment=True)		# it returns only approved comments

	def get_absolute_url(self):		# this is where we are goiing sfter publishing a post
		return reverse("post_detail", kwargs = {'pk':self.pk})	# we are going to the 'post_detail' 
								# of this page (primary key (pk) same as pk of this new post)

	def __str__(self):		# string representation of our object - in this case the Ttitle of the post
		return self.title

class Comment(models.Model):
	post = models.ForeignKey('blgr.Post', related_name='comments')
	author = models.CharField(max_length=200)
	text = models.TextField()
	create_date = models.DateTimeField(default=timezone.now())
	approved_comment = models.BooleanField(default = False)

	def approve(self):
		self.approved_comment=True
		self.save()

	def get_absolute_url(self):
		return reverse('post_list')

	def __str__(self):
		return self.text


