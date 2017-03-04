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
            context['user_name'] = ''
            context['login_form'] = LoginForm()
        return context


class LoginForm(forms.Form):
    login_ = forms.CharField(label='Логин')
    pass_ = forms.CharField(label='Пароль', widget=forms.PasswordInput())


class Login2(generic.FormView):

    form_class = LoginForm
    template_name = 'login_form.html'

    def form_valid(self, form):
        login_ = form.cleaned_data['login_']
        pass_ = form.cleaned_data['pass_']
        redirect_url = self.request.POST.get('redirect_url', default="/")
        #form.cleaned_data['redirect_url']
        user = authenticate(username=login_, password=pass_)
        if user:
            login(self.request, user)
            return redirect(redirect_url)
        return redirect('/err')  # обработать неправильные данные


class Logout(generic.View):

    def post(self, request, *args, **kwargs):
        print('============== logout ')
        logout(request)
        url_ = request.POST.get('redirect_url', default="/")
        print(url_)
        return redirect(url_)

