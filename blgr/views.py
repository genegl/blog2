from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from blgr.models import Post, Comment
from blgr.forms import PostForm, CommentForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView, ListView,
			DetailView, CreateView, UpdateView,
			DeleteView)
# Create your views here.

class AboutView(TemplateView):
	template_name = 'about.html'

class PostListView(ListView):
	model = Post

	def get_queryset(self):		# we getting from database only filtered data
		return Post.objects.filter(published_date__lte = timezone.now()).order_by('-published_date')	# __lte - less then
																# or equal to. "-" desh before for descending order

class PostDetailView(DetailView):
	model = Post

class CreatePostView(LoginRequiredMixin, CreateView):
	login_url = '/login/'
	redirect_field_name = 'blgr/post_detail.html'
	form_class = PostForm
	model = Post

class PostUpdateView(LoginRequiredMixin, UpdateView):
	login_url = '/login/'
	redirect_field_name = 'blgr/post_detail.html'
	form_class = PostForm
	model = Post

class PostDeleteView(LoginRequiredMixin, DeleteView):
	model = Post
	success_url = reverse_lazy('post_list')

class DraftListView(LoginRequiredMixin, ListView):
	login_url = '/login/'
	redirect_field_name = 'blgr/post_list.html'
	model = Post

	def get_queryset(self):
		return Post.objects.filter(published_date__isnull=True).order_by('created_date')		# __isnull, it is draft, so
														# there is no pub_date




###########################################		This is Comments related section
###########################################

@login_required
def post_publish(request, pk):
	post = get_object_or_404(Post, pk=pk)
	post.publish
	return redirect('post_detail', pk=pk)

@login_required		# this is a decorator from django, the view below is requiret login
def add_comment_to_post(request, pk):		# gettin the primary key for the post and request as parameters
	post = get_object_or_404(Post, pk = pk)
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit = False)		# we get data but not save to the DB, yet
			comment.post = post
			comment.save()							# now, we saved everything to the DB
			return redirect('post_detail', pk=post.pk)
	else:
		form = CommentForm()	# here we just showing the form
	return render(request, 'blgr/comment_form.html', {'form':form})

@login_required
def comment_approve(request, pk):
	comment = get_object_or_404(Comment, pk=pk)
	comment.approve()		# the Comment and approve() are located in the /models.py/
	return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
	comment = get_object_or_404(Comment, pk=pk)
	post_pk = comment.post.pk 		# temporary saving post's primary key
	comment.delete()
	return redirect('post_detail', pk = post_pk)	# here we used the saved primary key