from django.views import generic
from django import forms
from blog import models
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User


class ErrorMixin:

    def error(self,  error):
        return render(self.request, 'blog/error.html', {'error': error})


def set_title(title):
    """
    Создает декоратор, заменющий obj.get_context_data
    на obj.get_context_data + context['title'] = title
    """
    def decorator(obj):
        tmp = obj.get_context_data

        def wrapper(self, **kwargs):
            context = tmp(self, **kwargs)
            context['title'] = title
            return context

        obj.get_context_data = wrapper
        return obj
    return decorator


@set_title('Мои посты')
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


class DeletePost(generic.DeleteView, ErrorMixin):
    model = models.Post

    def delete(self, request, *args, **kwargs):
        """class DeletionMixin(object).delete() добавил проверку post.author == request.user"""
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        obj = self.get_object()
        if obj.author == request.user:
            obj.delete()
            return redirect(request.POST.get('redirect_url', default='/'))
        else:
            return self.error('Вы не можете удалять чужие записи')


@set_title('Новый пост')
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


@set_title('Пост')
class DetailPost(generic.DetailView):
    model = models.Post

    def get_context_data(self, **kwargs):
        context = super(generic.DetailView, self).get_context_data( **kwargs)

        if models.Feed.objects.filter(subscriber=self.request.user, post=kwargs['object']).exists():
            context['subscribed'] = True
            context['is_read'] = models.Feed.objects.get(subscriber=self.request.user, post=kwargs['object']).is_read
        return context


class DetailUser(generic.DetailView):
    model = User
    template_name = "blog/user_detail.html"

    def get_context_data(self, **kwargs):
        context = super(generic.DetailView, self).get_context_data(**kwargs)
        user = context['object']
        context['title'] = user.username
        context['list_posts'] = models.Post.objects.filter(author=user)
        if models.Subscribers.objects.filter(blog=user, subscriber=self.request.user).exists():
            context['subscribe'] = models.Subscribers.objects.get(blog=user, subscriber=self.request.user)

        return context


@set_title('Список пользователей')
class ListUsers(generic.ListView):
    template_name = 'blog/user_list.html'
    paginate_by = 7

    def get_queryset(self):
        return User.objects.exclude(id=self.request.user.id)


class DeleteSubscribe(generic.DeleteView):
    model = models.Subscribers

    def get_success_url(self):
        return self.request.POST.get('redirect_url', default='/blog')


class CreateSubscribe(generic.View, ErrorMixin):    # лениво использовать form ради одного поля
                                                    # при том что второе всеравно заполнять из request
    def post(self, request):
        subscriber = request.user
        try:
            blog_id = int(request.POST['blog'])
        except (ValueError, KeyError):
            return self.error('Неверный id блога')

        blog = get_object_or_404(User, pk=blog_id)
        if models.Subscribers.objects.filter(blog=blog, subscriber=subscriber).exists():
            return self.error('Вы уже подписаны')
        models.Subscribers(blog=blog, subscriber=subscriber).save()
        return redirect(request.POST.get('redirect_url', default='/'))


@set_title('Мои подписки')
class SubscribesList(generic.ListView):

    def get_queryset(self):
        return models.Subscribers.objects.filter(subscriber=self.request.user)


@set_title('Лента')
class ListFeed(generic.ListView):
    paginate_by = 3

    def get_queryset(self):
        return models.Feed.objects.filter(subscriber=self.request.user)


class SetRead(generic.View, ErrorMixin):

    def post(self, request):
        try:
            post_id = int(request.POST['post_id'])
        except (ValueError, KeyError):
            return self.error('Неверный id поста')
        obj = get_object_or_404(models.Feed, subscriber=request.user, post__id=post_id)
        obj.is_read = not obj.is_read
        obj.save()
        return redirect(request.POST.get('redirect_url', default='/'))
