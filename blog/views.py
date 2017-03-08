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


class PostForm(forms.Form):
    model = models.Post

    title = forms.CharField(label='',
                            widget=forms.TextInput(attrs={'id': 'ti'}))
    text = forms.CharField(label='',
                           widget=forms.Textarea(attrs={'id': 'ta'}))


class DeletePost(generic.DeleteView):
    model = models.Post

    def get_success_url(self):
        return self.request.POST.get('redirect_url', default='/')


class NewPost(generic.FormView):
    model = models.Post
    template_name = 'blog/post_form.html'
    form_class = PostForm

    def form_valid(self, form):
        title = form.cleaned_data['title']
        text = form.cleaned_data['text']
        author = self.request.user
        redirect_url = self.request.POST.get('redirect_url', default='/')
        models.Post(text=text, title=title, author=author).save()
        return redirect(redirect_url)

    def form_invalid(self, form):
        return render(self.request, 'error.html', {'error': 'ошибки в заполнении формы'})





class DetailPost(generic.DetailView):
    model = models.Post


class ListFeed(generic.ListView):

    def get_queryset(self):
        return models.Feed.objects.filter(subscriber=self.request.user)


class DetailUser(generic.DetailView):
    model = User
    template_name = "blog/user_detail.html"

    def get_context_data(self, **kwargs):
        context = super(generic.DetailView, self).get_context_data(**kwargs)
        user = context['object']
        context['list_posts'] = models.Post.objects.filter(author=user)
        context['subscribe_form'] = SubscribeForm(initial={'blog': user.id,
                                                           'subscriber': self.request.user.id})
        context['is_subscribed'] = models.Subscribers.objects.filter(
            blog=user, subscriber=self.request.user).exists()
        return context


class SubscribeForm(forms.Form):
    blog = forms.CharField(widget=forms.HiddenInput)
    subscriber = forms.CharField(widget=forms.HiddenInput)


class DeleteSubscribe(generic.DeleteView):
    model = models.Subscribers

    def get_success_url(self):
        return self.request.POST.get('redirect_url', default='/')


class CreateSubscribe(generic.CreateView):
    model = models.Subscribers
    fields = ['subscriber', 'blog']

    def get_success_url(self):
        return self.request.POST.get('redirect_url', default='/')


class ListUsers(generic.ListView):
    template_name = 'blog/user_list.html'

    def get_queryset(self):
        return User.objects.exclude(id=self.request.user.id)


class SubscribesList(generic.ListView):

    def get_queryset(self):
        return models.Subscribers.objects.filter(subscriber=self.request.user)





