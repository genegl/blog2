from django.conf.urls import url
from blgr import views

urlpatterns = [
	url(r'^$', views.PostListView.as_view(), name = 'post_list'),
	url(r'^about/$', views.AboutView.as_view(), name = 'about'),
	url(r'post/(?P<pk>\d+)$', views.PostDetailView.as_view(), name = 'post_detail'),
]