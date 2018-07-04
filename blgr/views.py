from django.shortcuts import render
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