from django.conf.urls import url


from . import views


urlpatterns = [
    url(r'^$', views.ListPosts.as_view(), name='post_list'),
    # url(r'^page(?P<page>\d*)/$', Posts.as_view())
    url(r'^feed', views.Feed.as_view(), name='feed'),
    url(r'^new_post$', views.NewPost.as_view(), name='new_post'),
    url(r'^post/(?P<pk>[0-9]+)$', views.DetailPost.as_view(), name='post'),
    url(r'^users$', views.ListUsers.as_view(), name='users'),
    url(r'^user/(?P<pk>[0-9]+)$', views.DetailUser.as_view(), name='user')
]
