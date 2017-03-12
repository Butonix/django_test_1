from django.views import generic

from django.shortcuts import redirect, render
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate

from oauth.OAuth import OAuthVk


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


class Login(generic.FormView):

    form_class = LoginForm
    template_name = 'login_form.html'

    def form_valid(self, form):
        login_ = form.cleaned_data['login_']
        pass_ = form.cleaned_data['pass_']
        redirect_url = self.request.POST.get('redirect_url', default="/")

        user = authenticate(username=login_, password=pass_)
        if user:
            login(self.request, user)
            return redirect(redirect_url)
        return render(self.request,  # обработать неправильные данные
                      'error.html',
                      {'error': 'неправильные логин/пароль'})


class Logout(generic.View):

    def post(self, request, *args, **kwargs):
        logout(request)
        url_ = request.POST.get('redirect_url', default="/")
        print(url_)
        return redirect(url_)


class OAuth(generic.View):

    def get(self, request):
        code = request.GET.get('code', default=None)
        if code:
            result = OAuthVk.get_token(code)
            if result['error']:
                return render(request,
                              'error.html',
                              {'error': result['error'], 'description': result['description']}
                              )

            email = result['email']
            if User.objects.filter(email=email).exists():
                login(self.request, User.objects.get(email=email))
            else:
                new_user = User(username=email, email=email)
                new_user.save()
                login(self.request, new_user)
            return redirect('/')
        else:
            return redirect(OAuthVk.get_code_url())
