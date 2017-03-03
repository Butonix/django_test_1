from django.views import generic
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class Main(generic.TemplateView):
    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        context = super(generic.TemplateView, self).get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context['user_name'] = self.request.user.username
        else:
            context['login_form'] = LoginForm(initial={'redirect_url':self.request.path})
        return context


class LoginForm(forms.Form):
    login_ = forms.CharField(label='Логин')
    pass_ = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    redirect_url = forms.CharField() #widget=forms.HiddenInput()



class Login2(generic.FormView):
    form_class = LoginForm
    template_name = 'login_form.html'


    def form_valid(self, form):
        login_ = form.cleaned_data['login_']
        pass_ = form.cleaned_data['pass_']
        redirect_url = form.cleaned_data['redirect_url']
        user = authenticate(username=login_, password=pass_)
        if user:
            login(self.request, user)
            return redirect(redirect_url)
        return redirect('/err')  # обработать неправильные данные

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        return {'redirect_url': '/'}


class Login1(generic.View):

    def post(self, request, *args, **kwargs):
        login_ = request.POST['login_']
        pass_ = request.POST['pass_']
        url_ = request.POST['redirect_url']
        print(self.request.path)
        user = authenticate(username=login_, password=pass_)
        if user:
            login(request, user)
        return redirect(url_)

    def get(self, request, *args, **kvargs):
        return redirect('/login')


class Logout(generic.View):

    def post(self, request):
        logout(request)
        url_ = request.POST['url']
        return redirect(url_)

