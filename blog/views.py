from django.views import generic
from django import forms
from blog import models
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.core import exceptions

class ListPosts(generic.ListView):
    model = models.Post
    context_object_name = 'list_posts'
    paginate_by = 10

    def get_queryset(self):
        return models.Post.objects.filter(author=self.request.user.id)


class NewPost(generic.CreateView):
    model = models.Post
    fields = ['title', 'text']
    success_url = '/'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        instance.save()
        return redirect(self.success_url)


class DetailPost(generic.DetailView):
    model = models.Post
    context_object_name = 'post'


class ListFeed(generic.ListView):
   # model = models.Feed

    def get_queryset(self):
        return models.Feed.objects.filter(subscriber=self.request.user)


class DetailUser(generic.DetailView):
    model = User
    template_name = "blog/user_detail.html"

    def get_context_data(self, **kwargs):

        context = super(generic.DetailView, self).get_context_data(**kwargs)
        user = context['object']
        context['list_posts'] = models.Post.objects.filter(author=user)
        context['subscribe_form'] = SubscribeForm(initial={'blog': user.id})
        context['is_subscribed'] = models.Subscribers.objects.filter(
            blog=user, subscriber=self.request.user).exists()

        return context


class SubscribeForm(forms.Form):
    blog = forms.CharField(widget=forms.HiddenInput)
    #model = models.Subscribers


class Unsubscribe(generic.FormView):
    form_class = SubscribeForm

    def form_valid(self, form):
        redirect_url = self.request.POST.get('redirect_url', default='/')
        blog = User.objects.get(id=form.cleaned_data['blog'])
        subscriber = self.request.user

        # удаляем из списка подписчиков
        try:
            models.Subscribers.objects.get(blog=blog, subscriber=subscriber).delete()
        except exceptions.ObjectDoesNotExist as a:
            return render(self.request, 'blog/error.html', {'error': 'Подписки несуществует'})
        # очищаем ленту
        models.Feed.objects.filter(subscriber=subscriber, post__author=blog).delete()
        return redirect(redirect_url)


class Subscribe(generic.FormView):
    form_class = SubscribeForm

    def form_valid(self, form):
        redirect_url = self.request.POST.get('redirect_url', default='/')
        blog = User.objects.get(id=form.cleaned_data['blog'])
        subscriber = self.request.user

        if models.Subscribers.objects.filter(blog=blog, subscriber=subscriber).exists():
            return render(self.request, 'blog/error.html', { 'error': "Вы уже подписаны"})
        try:
            # добавили в список подписчиков
            s = models.Subscribers(blog=blog, subscriber=subscriber)
            s.save()

            # обновили ленту
            post_list = models.Post.objects.filter(author=blog)
            for post_ in post_list:
                models.Feed(subscriber=subscriber, post=post_, is_read=False).save()


        except Exception as e:
            print('===============')
            print(e)
            return render(self.request, 'error.html', {'error': e})

        return redirect(redirect_url)


class ListUsers(generic.ListView):
    template_name = 'blog\\user_list.html'

    def get_queryset(self):
        return User.objects.exclude(id=self.request.user.id)


class SubscribesList(generic.ListView):

    def get_queryset(self):
        return models.Subscribers.objects.filter(subscriber=self.request.user)





