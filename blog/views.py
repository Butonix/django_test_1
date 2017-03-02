from django.views import generic
from django import forms
from blog import models
from django.shortcuts import redirect
from django.contrib.auth.models import User

class ListPosts(generic.ListView):
    model = models.Post
    context_object_name = 'list_posts'
    paginate_by = 10

    def get_queryset(self):
        return models.Post.objects.filter(owner=self.request.user.id)


class NewPost(generic.CreateView):
    model = models.Post
    fields = ['title', 'text']
    success_url = '/'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = self.request.user
        instance.save()
        return redirect(self.success_url)


class DetailPost(generic.DetailView):
    model = models.Post
    context_object_name = 'post'


class Feed(generic.ListView):
    model = 'Feed'
    template_name = 'feed.html'


class DetailUser(generic.DetailView):
    model = User
    template_name = "blog\\user_detail.html"

    def get_context_data(self, **kwargs):
        context = super(generic.DetailView, self).get_context_data(**kwargs)
        print(kwargs)

        context['list_posts'] = models.Post.objects.filter(owner=kwargs['object'])
        return context


class ListUsers(generic.ListView):
    template_name = 'blog\\user_list.html'
   # model = User
    def get_queryset(self):
        return User.objects.exclude(id=self.request.user.id)
