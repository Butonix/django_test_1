from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views


urlpatterns = [

    url(r'^$', login_required(views.ListPosts.as_view(), login_url='/'), name='post_list'),
    url(r'^feed$', views.ListFeed.as_view(), name='feed'),
    url(r'^feed/(?P<page>[0-9]+)$', views.ListFeed.as_view(), name='feed'),

    url(r'^new_post$', views.NewPost.as_view(), name='new_post'),
    url(r'^post/(?P<pk>[0-9]+)$', views.DetailPost.as_view(), name='post'),
    url(r'^delete_post/(?P<pk>[0-9]+)$', views.DeletePost.as_view(), name='delete_post'),

    url(r'^users$', views.ListUsers.as_view(), name='users'),
    url(r'^users/(?P<page>[0-9]*)$', views.ListUsers.as_view(), name='users'),

    url(r'^user/(?P<pk>[0-9]+)$', views.DetailUser.as_view(), name='user'),
    url(r'^subscribe$', views.CreateSubscribe.as_view(), name='subscribe'),
    url(r'^subscribes_list$', views.SubscribesList.as_view(), name='subscribes'),
    url(r'^delete_subscribe/(?P<pk>[0-9]+)$', views.DeleteSubscribe.as_view(), name='delete_subscribe'),
    url(r'^set_read', views.SetRead.as_view(), name='set_read'),
]
